#!/usr/bin/env bash
# Lezione 22 · lato bersaglio · HTTPS con certificato self-signed su :8443.
# Genera un certificato con una flag nel campo OU e serve una pagina HTTPS con
# un'altra flag. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 22"; exit 1
fi
echo "== Lezione 22 (bersaglio) · HTTPS self-signed su :8443 =="

DIR=/opt/lab/lab22
mkdir -p "$DIR"

# Certificato self-signed con una flag nel campo OU (Organizational Unit)
if [ ! -f "$DIR/cert.pem" ]; then
  openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
    -keyout "$DIR/key.pem" -out "$DIR/cert.pem" \
    -subj "/C=IT/ST=AO/O=Banca della Scuola/OU=FLAG{certificato_letto}/CN=banca.local" \
    2>/dev/null
fi

cat > "$DIR/https.py" <<'PY'
#!/usr/bin/env python3
# Piccolo server HTTPS con certificato self-signed. Solo stdlib.
import http.server, ssl
PAG = (b"<!doctype html><meta charset='utf-8'><title>Banca HTTPS</title>"
       b"<h1>Banca della Scuola (HTTPS)</h1>"
       b"<p>Questa pagina viaggia cifrata con TLS.</p>"
       b"<p>FLAG{https_ignora_il_lucchetto}</p>")


class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAG)

    def log_message(self, *a):
        pass


httpd = http.server.HTTPServer(("0.0.0.0", 8443), H)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("/opt/lab/lab22/cert.pem", "/opt/lab/lab22/key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
PY
chmod 755 "$DIR/https.py"

cat > /etc/systemd/system/lab22-https.service <<'EOF'
[Unit]
Description=Lab22 HTTPS self-signed (:8443)
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/lab/lab22/https.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab22-https.service >/dev/null 2>&1 || true
systemctl restart lab22-https.service >/dev/null 2>&1 || true

sleep 1
if curl -sk https://localhost:8443/ | grep -q FLAG; then
  echo "[OK] HTTPS attivo su https://10.10.10.20:8443 (certificato self-signed)."
else
  echo "[!] HTTPS non risponde. Controlla:  systemctl status lab22-https"
fi
