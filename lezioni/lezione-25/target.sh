#!/usr/bin/env bash
# Lezione 25 · lato bersaglio · il bersaglio "parla" con un server centrale
# (10.10.10.30) che non esiste: manda credenziali in chiaro a quell'IP. Con
# l'ARP spoofing, la Kali si fingera' quel server e intercettera' il traffico.
# Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 25"; exit 1
fi
echo "== Lezione 25 (bersaglio) · client verso il server 10.10.10.30 =="

mkdir -p /opt/lab/lab25
cat > /opt/lab/lab25/client25.py <<'PY'
#!/usr/bin/env python3
# Ogni 3s manda credenziali in chiaro al "server centrale" 10.10.10.30:9997.
# Se nessuno risponde all'ARP, i pacchetti non partono; quando la Kali si
# finge 10.10.10.30 (ARP spoofing), li ricevera' lei. Solo stdlib.
import socket, time
SERVER = ("10.10.10.30", 9997)
MSG = (b"SYNC verso server centrale | utente=direttore "
       b"password=CasseforT3! FLAG{traffico_dirottato}")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    try:
        s.sendto(MSG, SERVER)
    except OSError:
        pass
    time.sleep(3)
PY
chmod 755 /opt/lab/lab25/client25.py

cat > /etc/systemd/system/lab25-client.service <<'EOF'
[Unit]
Description=Lab25 client verso il server centrale (10.10.10.30:9997)
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab25/client25.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab25-client.service >/dev/null 2>&1 || true
systemctl restart lab25-client.service >/dev/null 2>&1 || true

sleep 1
systemctl is-active --quiet lab25-client.service \
  && echo "[OK] Il bersaglio manda credenziali a 10.10.10.30:9997 (server inesistente)." \
  || echo "[!] Client non attivo. Controlla: systemctl status lab25-client"
echo "     Finche' nessuno e' 10.10.10.30, quel traffico non raggiunge nessuno."
