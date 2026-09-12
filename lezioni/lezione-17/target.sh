#!/usr/bin/env bash
# Lezione 17 · lato bersaglio · file upload, path traversal e LFI.
# LFI: riusa /documenti della Banca (Lezione 12). Upload: avvia un piccolo
# servizio non validato su :8096. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 17"; exit 1
fi
APPDIR=/opt/lab/banca-app
if [ ! -f "$APPDIR/banca.py" ]; then
  echo "[!] La Banca non e' installata (serve per la parte LFI). Esegui prima:  lab 12"; exit 1
fi
echo "== Lezione 17 (bersaglio) · upload, path traversal e LFI =="

systemctl restart banca.service >/dev/null 2>&1 || true   # ricrea documenti e segreti/lfi.txt

grep -q '^FLAG_UPLOAD=' "$APPDIR/flags.env" 2>/dev/null || {
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  echo "FLAG_UPLOAD=FLAG{upload_non_validato_$(r)}" >> "$APPDIR/flags.env"
}

mkdir -p /opt/lab/lab17/uploads
cat > /opt/lab/lab17/upload.py <<'PY'
#!/usr/bin/env python3
# Servizio di upload NON validato (didattico). Solo stdlib.
#   POST /upload?nome=<file>  con il contenuto nel corpo -> salva senza controlli
#   GET  /                    -> istruzioni ed elenco file caricati
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

UP = "/opt/lab/lab17/uploads"
FLAG_UPLOAD = os.environ.get("FLAG_UPLOAD", "FLAG{upload_non_validato_demo}")
PERICOLOSE = (".php", ".sh", ".py", ".jsp", ".asp", ".aspx", ".cgi", ".pl")


class H(BaseHTTPRequestHandler):
    def reply(self, code, testo):
        b = testo.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        try:
            files = os.listdir(UP)
        except OSError:
            files = []
        self.reply(200, "Upload lab17. Carica con:\n"
                        "  curl --data-binary @file 'http://IP:8096/upload?nome=file'\n"
                        "File presenti: " + ", ".join(files))

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/upload":
            self.reply(404, "non trovato"); return
        nome = parse_qs(u.query).get("nome", ["senza-nome"])[0]
        n = int(self.headers.get("Content-Length", 0) or 0)
        dati = self.rfile.read(n)
        # NESSUNA validazione di nome ne' di tipo: vulnerabile
        dest = os.path.join(UP, nome)
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as f:
                f.write(dati)
        except OSError as e:
            self.reply(500, "errore: %s" % e); return
        msg = "File '%s' caricato (%d byte)." % (nome, len(dati))
        if nome.lower().endswith(PERICOLOSE):
            msg += ("\nATTENZIONE: tipo eseguibile accettato senza controlli! "
                    "Un server reale avrebbe potuto eseguirlo.\n" + FLAG_UPLOAD)
        self.reply(200, msg)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8096), H).serve_forever()
PY
chmod 755 /opt/lab/lab17/upload.py

cat > /etc/systemd/system/lab17-upload.service <<'EOF'
[Unit]
Description=Lab17 upload non validato (:8096)
After=network.target
[Service]
EnvironmentFile=/opt/lab/banca-app/flags.env
ExecStart=/usr/bin/python3 /opt/lab/lab17/upload.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab17-upload.service >/dev/null 2>&1 || true
systemctl restart lab17-upload.service >/dev/null 2>&1 || true

sleep 1
echo
if curl -s "http://localhost:8080/documenti?file=../segreti/lfi.txt" | grep -q FLAG; then
  echo "[OK] LFI pronta sulla Banca (:8080/documenti)."
else
  echo "[!] LFI non pronta: controlla il servizio banca."
fi
curl -s -o /dev/null "http://localhost:8096/" && echo "[OK] Servizio upload attivo su :8096." || echo "[!] upload :8096 non attivo."
echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
