#!/usr/bin/env bash
# Lezione 23 · lato bersaglio · genera traffico in chiaro da catturare.
# Un "beacon" invia in broadcast, ogni pochi secondi, un messaggio in chiaro con
# credenziali e una flag: materiale per Wireshark/tcpdump. Idempotente.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 23"; exit 1
fi
echo "== Lezione 23 (bersaglio) · beacon in chiaro (UDP :9999) =="

mkdir -p /opt/lab/lab23
cat > /opt/lab/lab23/beacon.py <<'PY'
#!/usr/bin/env python3
# Invia in broadcast un messaggio in chiaro (credenziali + flag) ogni 3 secondi.
# Serve a far vedere quanto e' esposto il traffico non cifrato. Solo stdlib.
import socket, time
MSG = (b"BANCA-SYNC utente=cassiere password=Autunno2021 "
       b"FLAG{ho_annusato_la_rete}")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
while True:
    for dest in ("10.10.10.255", "255.255.255.255"):
        try:
            s.sendto(MSG, (dest, 9999))
        except OSError:
            pass
    time.sleep(3)
PY
chmod 755 /opt/lab/lab23/beacon.py

cat > /etc/systemd/system/lab23-beacon.service <<'EOF'
[Unit]
Description=Lab23 beacon in chiaro (UDP :9999)
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab23/beacon.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab23-beacon.service >/dev/null 2>&1 || true
systemctl restart lab23-beacon.service >/dev/null 2>&1 || true

sleep 1
if systemctl is-active --quiet lab23-beacon.service; then
  echo "[OK] Beacon attivo: manda in broadcast su UDP :9999 ogni 3 secondi."
  echo "     Dalla Kali:  sudo tcpdump -i any -A udp port 9999"
else
  echo "[!] Beacon non attivo. Controlla:  systemctl status lab23-beacon"
fi
