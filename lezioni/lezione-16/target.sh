#!/usr/bin/env bash
# Lezione 16 · lato bersaglio · brute force del login e la sua difesa.
# Avvia un servizio di login su :8095 con due porte d'ingresso: /debole (nessuna
# protezione, forzabile) e /forte (blocca dopo pochi tentativi). Idempotente.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 16"; exit 1
fi
echo "== Lezione 16 (bersaglio) · login da forzare su :8095 =="

APPDIR=/opt/lab/banca-app
mkdir -p "$APPDIR" /opt/lab/lab16
[ -f "$APPDIR/flags.env" ] || { touch "$APPDIR/flags.env"; chmod 600 "$APPDIR/flags.env"; }
r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
grep -q '^FLAG_BRUTE='  "$APPDIR/flags.env" || echo "FLAG_BRUTE=FLAG{password_forzata_$(r)}"  >> "$APPDIR/flags.env"
grep -q '^FLAG_DIFESA=' "$APPDIR/flags.env" || echo "FLAG_DIFESA=FLAG{rate_limit_regge_$(r)}" >> "$APPDIR/flags.env"

cat > /opt/lab/lab16/login.py <<'PY'
#!/usr/bin/env python3
# Servizio di login didattico per il brute force. Solo stdlib.
#   POST /debole  -> nessuna protezione: si puo' forzare a dizionario
#   POST /forte   -> dopo 5 tentativi sbagliati blocca (rate limiting)
import os, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

UTENTI = {"sara.verdi": "primavera", "cassa": "estate2019"}
FLAG_BRUTE = os.environ.get("FLAG_BRUTE", "FLAG{password_forzata_demo}")
FLAG_DIFESA = os.environ.get("FLAG_DIFESA", "FLAG{rate_limit_regge_demo}")
falliti = {}   # ip -> [timestamp, ...]


class H(BaseHTTPRequestHandler):
    def reply(self, code, testo):
        b = testo.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        form = parse_qs(self.rfile.read(n).decode("utf-8", "replace"))
        u = form.get("utente", [""])[0]
        p = form.get("password", [""])[0]
        ip = self.client_address[0]
        if self.path == "/debole":
            if UTENTI.get(u) == p:
                self.reply(200, "OK accesso riuscito. " + FLAG_BRUTE)
            else:
                self.reply(401, "Credenziali errate")
        elif self.path == "/forte":
            ora = time.time()
            recenti = [t for t in falliti.get(ip, []) if ora - t < 60]
            if len(recenti) >= 5:
                self.reply(429, "Troppi tentativi, riprova piu' tardi. " + FLAG_DIFESA)
                return
            if UTENTI.get(u) == p:
                falliti[ip] = []
                self.reply(200, "OK accesso riuscito.")
            else:
                recenti.append(ora)
                falliti[ip] = recenti
                self.reply(401, "Credenziali errate")
        else:
            self.reply(404, "non trovato")

    def do_GET(self):
        self.reply(200, "Login lab16. Usa POST su /debole o /forte "
                        "(campi: utente, password).")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8095), H).serve_forever()
PY
chmod 755 /opt/lab/lab16/login.py

cat > /etc/systemd/system/lab16-login.service <<'EOF'
[Unit]
Description=Lab16 login da forzare (:8095)
After=network.target
[Service]
EnvironmentFile=/opt/lab/banca-app/flags.env
ExecStart=/usr/bin/python3 /opt/lab/lab16/login.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab16-login.service >/dev/null 2>&1 || true
systemctl restart lab16-login.service >/dev/null 2>&1 || true

sleep 1
if curl -s -o /dev/null "http://localhost:8095/"; then
  echo "[OK] Servizio login attivo su :8095 (endpoint /debole e /forte)."
  echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
else
  echo "[!] Servizio non attivo. Controlla:  systemctl status lab16-login"
fi
