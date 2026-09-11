#!/usr/bin/env bash
# Lezione 06 · lato bersaglio · questa lezione si svolge sulla Kali.
# Qui garantiamo solo che il bersaglio risponda al ping e tenga aperta la
# porta 8080, cosi' lo scanner della Kali lo trova. Idempotente.
set -uo pipefail

echo "== Lezione 06 (bersaglio) =="
echo "Questa lezione si svolge quasi tutta sulla Kali (scripting bash)."
echo "Qui mi assicuro solo che il bersaglio sia visibile allo scanner."

# 1) Il ping deve funzionare: assicuriamoci che non sia bloccato da regole locali
#    (di default Ubuntu risponde all'echo ICMP; non tocchiamo il firewall).
if command -v sysctl >/dev/null 2>&1; then
  sysctl -w net.ipv4.icmp_echo_ignore_all=0 >/dev/null 2>&1 || true
fi

# 2) La porta 8080 (Banca della Scuola) deve essere su, per la prova con la porta
if command -v docker >/dev/null 2>&1; then
  if ! docker ps --format '{{.Names}}' | grep -q '^banca$'; then
    if [ -d /opt/lab/banca ] && docker image inspect nginx:alpine >/dev/null 2>&1; then
      docker run -d --name banca --restart unless-stopped -p 8080:80 \
        -v /opt/lab/banca:/usr/share/nginx/html:ro nginx:alpine >/dev/null 2>&1 || true
    fi
  fi
fi

IP="$(hostname -I | awk '{print $1}')"
echo
echo "[OK] Bersaglio pronto. Dalla Kali:  ./scanner-host.sh 10.10.10 8080"
echo "     Il bersaglio dovrebbe comparire come ${IP:-10.10.10.20} con porta 8080 aperta."
