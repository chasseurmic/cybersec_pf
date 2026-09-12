#!/usr/bin/env bash
# Lezione 24 · lato bersaglio · traffico con credenziali in chiaro da raccogliere.
# Un beacon manda in broadcast (UDP :9998) finte login: alcune frequenti, una
# rara (premia chi lascia girare il sniffer). Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 24"; exit 1
fi
echo "== Lezione 24 (bersaglio) · beacon credenziali (UDP :9998) =="

mkdir -p /opt/lab/lab24
cat > /opt/lab/lab24/beacon24.py <<'PY'
#!/usr/bin/env python3
# Manda in broadcast finte richieste di login in chiaro. Solo stdlib.
# La login "admin" e' rara: compare circa 1 volta su 4.
import socket, time
COMUNI = [
    b"POST /login utente=cassiere password=Estate2022",
    b"POST /login utente=sportello password=Banca!01",
]
RARA = b"POST /login utente=admin password=Ammiragli0!2024"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
i = 0
while True:
    msg = RARA if (i % 4 == 3) else COMUNI[i % len(COMUNI)]
    for dest in ("10.10.10.255", "255.255.255.255"):
        try:
            s.sendto(msg, (dest, 9998))
        except OSError:
            pass
    i += 1
    time.sleep(3)
PY
chmod 755 /opt/lab/lab24/beacon24.py

cat > /etc/systemd/system/lab24-beacon.service <<'EOF'
[Unit]
Description=Lab24 beacon credenziali (UDP :9998)
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab24/beacon24.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab24-beacon.service >/dev/null 2>&1 || true
systemctl restart lab24-beacon.service >/dev/null 2>&1 || true

sleep 1
systemctl is-active --quiet lab24-beacon.service \
  && echo "[OK] Beacon credenziali attivo su UDP :9998 (la login admin e' rara)." \
  || echo "[!] Beacon non attivo. Controlla: systemctl status lab24-beacon"
