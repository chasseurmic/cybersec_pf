#!/usr/bin/env bash
# Lezione 09 · lato bersaglio · apre un servizio "segreto" su una porta insolita
# (7777) da scoprire con il port scanning, oltre ai servizi web abituali.
# Idempotente. Eseguire sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 9"
  exit 1
fi
echo "== Lezione 09 (bersaglio) · servizio segreto su porta 7777 =="

# 1) Assicura SSH attivo (porta 22, un classico da trovare)
export DEBIAN_FRONTEND=noninteractive
if [ ! -x /usr/sbin/sshd ]; then apt-get update && apt-get -y install openssh-server; fi
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true

# 2) Servizio segreto su 7777 con la flag
mkdir -p /opt/lab/segreto
cat > /opt/lab/segreto/index.html <<'EOF'
<!doctype html><meta charset="utf-8"><title>servizio nascosto</title>
<h1>Servizio interno non documentato</h1>
<p>Complimenti: hai trovato una porta che nessuno pensava fosse aperta.</p>
<p>FLAG{porta_segreta_scoperta}</p>
EOF
cat > /etc/systemd/system/lab09-porta.service <<'EOF'
[Unit]
Description=Lab09 servizio segreto su porta 7777
[Service]
ExecStart=/usr/bin/python3 -m http.server 7777 --directory /opt/lab/segreto --bind 0.0.0.0
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab09-porta.service >/dev/null 2>&1 || true
systemctl restart lab09-porta.service >/dev/null 2>&1 || true

# 3) Il sito banca su :8080 deve essere su (altra porta da trovare)
if command -v docker >/dev/null 2>&1; then
  if ! docker ps --format '{{.Names}}' | grep -q '^banca$'; then
    if [ -d /opt/lab/banca ] && docker image inspect nginx:alpine >/dev/null 2>&1; then
      docker run -d --name banca --restart unless-stopped -p 8080:80 \
        -v /opt/lab/banca:/usr/share/nginx/html:ro nginx:alpine >/dev/null 2>&1 || true
    fi
  fi
fi

sleep 1
echo
if curl -s http://localhost:7777 | grep -q FLAG; then
  echo "[OK] Servizio segreto attivo su :7777."
else
  echo "[!] Il servizio 7777 non risponde. Controlla:  systemctl status lab09-porta"
fi
echo "     Dalla Kali:  python3 portscan.py 10.10.10.20 1 10000"
