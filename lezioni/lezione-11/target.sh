#!/usr/bin/env bash
# Lezione 11 · lato bersaglio · "portale" HTTP didattico su :8090.
# App Python (solo stdlib) per capire HTTP: query GET, POST, header, cookie,
# codici di stato e redirect. Idempotente. Eseguire sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 11"
  exit 1
fi
echo "== Lezione 11 (bersaglio) · portale HTTP didattico su :8090 =="

mkdir -p /opt/lab/portale
cat > /opt/lab/portale/portale.py <<'PY'
#!/usr/bin/env python3
# Portale della Banca della Scuola - didattico. Solo libreria standard.
# Mostra come funziona HTTP: metodi, query, header, cookie, stati, redirect.
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

HOME = """<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Portale Banca della Scuola</title></head><body>
<h1>Portale Banca della Scuola</h1>
<ul>
  <li>GET con parametro:  /saluta?nome=tuonome</li>
  <li>POST login:  /login  (campi utente, password)</li>
  <li>Area staff (serve un header):  /staff</li>
  <li>Area clienti (serve un cookie):  /area-clienti</li>
  <li>Pagina spostata:  /vecchio</li>
</ul></body></html>"""


class H(BaseHTTPRequestHandler):
    def _send(self, code, body, headers=None):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            self._send(200, HOME)
        elif u.path == "/saluta":
            nome = (q.get("nome", [""])[0])
            extra = ""
            if nome == "admin":
                extra = "<p>FLAG{parametri_nella_url}</p>"
            self._send(200, "<h1>Ciao, %s!</h1>%s" % (nome, extra))
        elif u.path == "/staff":
            if self.headers.get("X-Ruolo", "") == "dipendente":
                self._send(200, "<h1>Area staff</h1><p>FLAG{gli_header_contano}</p>")
            else:
                self._send(403, "<h1>403</h1><p>Serve l'header giusto (X-Ruolo).</p>")
        elif u.path == "/area-clienti":
            cookie = self.headers.get("Cookie", "")
            if "sessione=valida" in cookie:
                self._send(200, "<h1>Ciao cliente</h1><p>FLAG{i_cookie_ti_seguono}</p>")
            else:
                self._send(302, "Vai al login", {"Location": "/login"})
        elif u.path == "/login":
            self._send(200, "<h1>Login</h1><form method=post action=/login>"
                            "<input name=utente><input name=password type=password>"
                            "<button>Entra</button></form>")
        elif u.path == "/vecchio":
            self._send(301, "Spostato", {"Location": "/"})
        else:
            self._send(404, "<h1>404</h1><p>Pagina non trovata.</p>")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace")
        form = parse_qs(raw)
        if self.path == "/login":
            u = form.get("utente", [""])[0]
            p = form.get("password", [""])[0]
            if u == "admin" and p == "banca123":
                self._send(200, "<h1>Benvenuto admin</h1><p>FLAG{ho_inviato_una_post}</p>")
            else:
                self._send(200, "<h1>Credenziali errate</h1>")
        else:
            self._send(404, "<h1>404</h1>")

    def log_message(self, *a):
        pass  # silenzioso


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8090), H).serve_forever()
PY
chmod 755 /opt/lab/portale/portale.py

cat > /etc/systemd/system/lab11-portale.service <<'EOF'
[Unit]
Description=Lab11 portale HTTP didattico (:8090)
[Service]
ExecStart=/usr/bin/python3 /opt/lab/portale/portale.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab11-portale.service >/dev/null 2>&1 || true
systemctl restart lab11-portale.service >/dev/null 2>&1 || true

sleep 1
echo
if curl -s http://localhost:8090/ | grep -q "Portale"; then
  echo "[OK] Portale attivo su http://10.10.10.20:8090"
else
  echo "[!] Portale non risponde. Controlla:  systemctl status lab11-portale"
fi
