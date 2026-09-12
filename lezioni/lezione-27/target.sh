#!/usr/bin/env bash
# Lezione 27 · lato bersaglio · difese di rete (firewall + IDS honeypot).
# Avvia un servizio "insicuro" su :9099 (da chiudere col firewall) e un IDS a
# porte esca che rileva le scansioni. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 27"; exit 1
fi
echo "== Lezione 27 (bersaglio) · firewall e IDS =="

DIR=/opt/lab/lab27
mkdir -p "$DIR"
[ -f "$DIR/flags.env" ] || {
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  { echo "FLAG_FW=FLAG{firewall_chiuso_$(r)}"
    echo "FLAG_IDS=FLAG{ids_ha_visto_lo_scan_$(r)}"; } > "$DIR/flags.env"
  chmod 600 "$DIR/flags.env"
}

# 1) Servizio "insicuro" da chiudere col firewall (porta 9099)
cat > /etc/systemd/system/lab27-insicuro.service <<'EOF'
[Unit]
Description=Lab27 servizio insicuro (:9099)
After=network.target
[Service]
ExecStart=/usr/bin/python3 -m http.server 9099 --bind 0.0.0.0
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# 2) IDS a porte esca: rileva chi tocca piu' porte "trappola"
cat > "$DIR/ids.py" <<'PY'
#!/usr/bin/env python3
# IDS didattico a porte esca (honeypot). Se un IP tocca piu' porte trappola,
# e' quasi certo uno scanner: scatta l'allarme. Solo stdlib.
import socket, threading, os, time
PORTS = [2323, 33060, 44445]        # finto telnet, finto mysql, finto smb
FLAG = os.environ.get("FLAG_IDS", "FLAG{ids_demo}")
LOG = "/opt/lab/lab27/allarmi.log"
hits, allarmati = {}, set()
lock = threading.Lock()


def servi(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port)); s.listen(16)
    while True:
        try:
            c, addr = s.accept(); ip = addr[0]
            with lock:
                hits.setdefault(ip, set()).add(port)
                if len(hits[ip]) >= 2 and ip not in allarmati:
                    allarmati.add(ip)
                    with open(LOG, "a") as f:
                        f.write("ALLARME %s: scansione da %s (porte esca %s) -> %s\n"
                                % (time.ctime(), ip, sorted(hits[ip]), FLAG))
            c.close()
        except Exception:
            pass


for p in PORTS:
    threading.Thread(target=servi, args=(p,), daemon=True).start()
open(LOG, "a").close()
while True:
    time.sleep(60)
PY
chmod 755 "$DIR/ids.py"
cat > /etc/systemd/system/lab27-ids.service <<'EOF'
[Unit]
Description=Lab27 IDS a porte esca
After=network.target
[Service]
EnvironmentFile=/opt/lab/lab27/flags.env
ExecStart=/usr/bin/python3 /opt/lab/lab27/ids.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# 3) Verificatore del firewall (controlla la regola iptables su 9099)
cat > /usr/local/bin/lab27-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
. /opt/lab/lab27/flags.env 2>/dev/null || true
if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo:  sudo lab27-verifica firewall"; exit 1; fi
case "${1:-}" in
  firewall)
    if iptables -C INPUT -p tcp --dport 9099 -j DROP 2>/dev/null; then
      echo "[OK] La porta 9099 e' bloccata dal firewall."
      echo "${FLAG_FW:-FLAG{firewall_chiuso_demo}}"
    else
      echo "[--] Nessuna regola trovata. Blocca la porta con:"
      echo "     sudo iptables -A INPUT -p tcp --dport 9099 -j DROP"
    fi ;;
  *) echo "Uso: sudo lab27-verifica firewall" ;;
esac
EOF
chmod 755 /usr/local/bin/lab27-verifica

systemctl daemon-reload
for u in lab27-insicuro lab27-ids; do
  systemctl enable --now "$u.service" >/dev/null 2>&1 || true
  systemctl restart "$u.service" >/dev/null 2>&1 || true
done

sleep 1
echo "[OK] Servizio insicuro su :9099 e IDS a porte esca (2323/33060/44445) attivi."
echo "     Allarmi IDS in:  /opt/lab/lab27/allarmi.log"
echo "     Flag (docente):  sudo cat $DIR/flags.env"
