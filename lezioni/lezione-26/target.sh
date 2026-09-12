#!/usr/bin/env bash
# Lezione 26 · lato bersaglio · la vittima usa la Kali come DNS e "aggiorna".
# Ogni pochi secondi risolve aggiornamenti.banca.local col DNS 10.10.10.5 e invia
# le credenziali all'IP che riceve. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 26"; exit 1
fi
echo "== Lezione 26 (bersaglio) · vittima che si fida del DNS 10.10.10.5 =="

mkdir -p /opt/lab/lab26
cat > /opt/lab/lab26/client26.py <<'PY'
#!/usr/bin/env python3
# La vittima: risolve un nome usando il DNS 10.10.10.5 (la Kali) e invia le
# credenziali all'IP ottenuto. Se il DNS e' canaglia, finisce sul sito civetta.
import socket, struct, random, time, urllib.request

DNS = "10.10.10.5"
NOME = "aggiornamenti.banca.local"
CRED = b"utente=cliente&password=HomeBanking#9 FLAG{dns_spoofing_riuscito}"


def risolvi(nome, server):
    tid = random.randint(0, 65535)
    header = struct.pack(">HHHHHH", tid, 0x0100, 1, 0, 0, 0)
    q = b"".join(bytes([len(p)]) + p.encode() for p in nome.split(".")) + b"\x00"
    q += struct.pack(">HH", 1, 1)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(3)
    try:
        s.sendto(header + q, (server, 53))
        data, _ = s.recvfrom(512)
    except OSError:
        return None
    finally:
        s.close()
    if struct.unpack(">H", data[6:8])[0] < 1:
        return None
    return socket.inet_ntoa(data[-4:])   # IP nell'ultima risposta (server semplice)


while True:
    ip = risolvi(NOME, DNS)
    if ip:
        try:
            urllib.request.urlopen("http://%s/login" % ip, data=CRED, timeout=3)
        except Exception:
            pass
    time.sleep(5)
PY
chmod 755 /opt/lab/lab26/client26.py

cat > /etc/systemd/system/lab26-client.service <<'EOF'
[Unit]
Description=Lab26 vittima che si fida del DNS 10.10.10.5
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab26/client26.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab26-client.service >/dev/null 2>&1 || true
systemctl restart lab26-client.service >/dev/null 2>&1 || true

sleep 1
systemctl is-active --quiet lab26-client.service \
  && echo "[OK] La vittima interroga il DNS 10.10.10.5 ogni 5s e invia le credenziali." \
  || echo "[!] Client non attivo. Controlla: systemctl status lab26-client"
