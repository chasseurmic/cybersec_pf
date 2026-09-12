#!/usr/bin/env bash
# Lezione 12 · lato bersaglio · installa la "Banca della Scuola" vulnerabile.
# App web in Python (solo stdlib + sqlite3): funziona OFFLINE, senza Docker ne'
# pip. E' la piattaforma del Blocco 4 (Lezioni 12-18). Sostituisce la pagina
# statica su :8080. Idempotente: rilanciare 'lab 12' resetta il database e
# ricrea l'app. I VALORI delle flag sono generati a runtime (non nel repo).
# Eseguire sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 12"
  exit 1
fi
echo "== Lezione 12 (bersaglio) · Banca della Scuola vulnerabile su :8080 =="

APPDIR=/opt/lab/banca-app
mkdir -p "$APPDIR"

# 1) Flag generate a runtime (restano fuori dal repo pubblico). Create una sola
#    volta e poi riusate, cosi' i valori sono stabili per tutto il blocco.
if [ ! -f "$APPDIR/flags.env" ]; then
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  cat > "$APPDIR/flags.env" <<EOF
FLAG_SQLI_LOGIN=FLAG{login_bypassato_$(r)}
FLAG_SQLI_DUMP=FLAG{tutti_i_conti_$(r)}
FLAG_SQLI_UNION=FLAG{union_select_$(r)}
FLAG_XSS_REFLECTED=FLAG{xss_riflesso_$(r)}
FLAG_XSS_STORED=FLAG{xss_memorizzato_$(r)}
FLAG_COOKIE_ADMIN=FLAG{cookie_manomesso_$(r)}
FLAG_LFI=FLAG{path_traversal_$(r)}
BANCA_ADMIN_PW=adm_$(r)$(r)
BANCA_CASSA_PW=primavera
EOF
  chmod 600 "$APPDIR/flags.env"
  echo "[*] Flag generate in $APPDIR/flags.env (solo il docente puo' leggerle)."
fi

# 2) Scrivi l'applicazione (sorgente unica, leggibile anche in questo target.sh)
cat > "$APPDIR/banca.py" <<'BANCA_PY'
#!/usr/bin/env python3
# Banca della Scuola - applicazione web VOLUTAMENTE VULNERABILE (didattica).
# Solo libreria standard di Python (http.server + sqlite3): funziona offline,
# senza pip ne' Docker. E' la piattaforma del Blocco 4 (Lezioni 12-18).
#
# Vulnerabilita' presenti di proposito (uso SOLO nel laboratorio isolato):
#   - SQL injection nel login e nella ricerca (Lezioni 12-13)
#   - XSS riflesso (ricerca) e memorizzato (bacheca) (Lezione 14)
#   - cookie di sessione prevedibile / controllo accessi rotto (Lezione 15)
#   - login forzabile a dizionario (Lezione 16)
#   - path traversal / LFI e upload non validato (Lezione 17)
#
# I VALORI delle flag arrivano dall'ambiente (file flags.env), generati a
# runtime dal target.sh: non stanno nel repo pubblico.
import os
import sqlite3
import html as _html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HOME = os.environ.get("BANCA_HOME", "/opt/lab/banca-app")
DB = os.path.join(HOME, "banca.db")
DOCS = os.path.join(HOME, "documenti")
UPLOADS = os.path.join(HOME, "uploads")
SEGRETI = os.path.join(HOME, "segreti")


def flag(nome, default):
    return os.environ.get(nome, default)


def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    os.makedirs(DOCS, exist_ok=True)
    os.makedirs(UPLOADS, exist_ok=True)
    c = db()
    cur = c.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS utenti(
        id INTEGER PRIMARY KEY, username TEXT, password TEXT, ruolo TEXT,
        conto TEXT, saldo INTEGER, nota TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS segreti(
        id INTEGER PRIMARY KEY, chiave TEXT, valore TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS messaggi(
        id INTEGER PRIMARY KEY, autore TEXT, testo TEXT)""")
    cur.execute("SELECT COUNT(*) AS n FROM utenti")
    if cur.fetchone()["n"] == 0:
        admin_pw = flag("BANCA_ADMIN_PW", "S3gr3t0Adm!")
        cassa_pw = flag("BANCA_CASSA_PW", "estate")   # debole, per il brute force (L16)
        utenti = [
            ("admin", admin_pw, "admin", "IT00BANCA0001", 999999,
             "Conto amministratore riservato"),
            ("anna.rossi", "Prima!vera_2019", "direttrice", "IT00BANCA0002", 50000, "Direzione"),
            ("luca.bianchi", "L4voro#IT", "it", "IT00BANCA0003", 1500, "Reparto IT"),
            ("sara.verdi", cassa_pw, "cassiera", "IT00BANCA0004", 800, "Cassa"),
            ("cliente", "cliente", "cliente", "IT00BANCA0100", 250, "Cliente di prova"),
            ("tesoreria", "n0n_tr0v4rmi", "nascosto", "IT00BANCA9999", 0,
             flag("FLAG_SQLI_DUMP", "FLAG{tutti_i_conti_demo}")),
        ]
        cur.executemany(
            "INSERT INTO utenti(username,password,ruolo,conto,saldo,nota) "
            "VALUES(?,?,?,?,?,?)", utenti)
        cur.execute("INSERT INTO segreti(chiave,valore) VALUES(?,?)",
                    ("flag_union", flag("FLAG_SQLI_UNION", "FLAG{union_select_demo}")))
        cur.execute("INSERT INTO segreti(chiave,valore) VALUES(?,?)",
                    ("promemoria", "i segreti non vanno nel db in chiaro"))
        c.commit()
    c.close()
    # file per la LFI (fuori dalla cartella documenti pubblica)
    os.makedirs(SEGRETI, exist_ok=True)
    with open(os.path.join(SEGRETI, "lfi.txt"), "w") as f:
        f.write("Documento riservato raggiunto con path traversal.\n"
                + flag("FLAG_LFI", "FLAG{path_traversal_demo}") + "\n")
    with open(os.path.join(DOCS, "informazioni.txt"), "w") as f:
        f.write("Orari sportelli: 8:30-13:30. Documento pubblico.\n")


PAG = """<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Banca della Scuola</title></head><body>
<h1>Banca della Scuola</h1>
<nav><a href="/">Home</a> | <a href="/cerca">Cerca conto</a> |
<a href="/bacheca">Bacheca</a> | <a href="/documenti">Documenti</a> |
<a href="/pannello">Pannello admin</a></nav><hr>%s</body></html>"""

LOGIN_FORM = """<h2>Accesso clienti</h2>
<form method="post" action="/login">
<p>Utente: <input name="utente"></p>
<p>Password: <input name="password" type="password"></p>
<button>Entra</button></form>"""


class H(BaseHTTPRequestHandler):
    server_version = "BancaScuola/1.0"

    def page(self, code, inner, headers=None):
        body = (PAG % inner).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def cookie_val(self, nome):
        raw = self.headers.get("Cookie", "")
        for part in raw.split(";"):
            if "=" in part:
                k, v = part.strip().split("=", 1)
                if k == nome:
                    return v
        return ""

    # ---------------------- GET ----------------------
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            self.page(200, LOGIN_FORM)
        elif u.path == "/cerca":
            self.cerca(q)
        elif u.path == "/bacheca":
            self.bacheca_get()
        elif u.path == "/dashboard":
            self.dashboard()
        elif u.path == "/pannello":
            self.pannello()
        elif u.path == "/documenti":
            self.documenti(q)
        else:
            self.page(404, "<p>Pagina non trovata.</p>")

    # ---------------------- POST ---------------------
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length).decode("utf-8", "replace")
        form = parse_qs(raw)
        if self.path == "/login":
            self.login(form)
        elif self.path == "/bacheca":
            self.bacheca_post(form)
        else:
            self.page(404, "<p>Pagina non trovata.</p>")

    # ---------------------- logica -------------------
    def login(self, form):
        utente = form.get("utente", [""])[0]
        pw = form.get("password", [""])[0]
        # VULNERABILE: query costruita per concatenazione (SQL injection)
        query = ("SELECT * FROM utenti WHERE username='%s' AND password='%s'"
                 % (utente, pw))
        c = db()
        try:
            row = c.execute(query).fetchone()
        except sqlite3.Error as e:
            c.close()
            self.page(200, "<p>Errore SQL: %s</p><pre>%s</pre>"
                      % (_html.escape(str(e)), _html.escape(query)))
            return
        c.close()
        if row:
            ruolo = row["ruolo"]
            extra = ""
            if ruolo == "admin":
                extra = ("<p><b>Sei entrato come amministratore!</b></p><p>%s</p>"
                         % flag("FLAG_SQLI_LOGIN", "FLAG{login_bypassato_demo}"))
            self.page(200, "<h2>Benvenuto %s (%s)</h2>%s<p><a href='/dashboard'>"
                      "Vai al conto</a></p>" % (_html.escape(row["username"]),
                                                _html.escape(ruolo), extra),
                      headers={"Set-Cookie": "sessione=%s; Path=/" % row["username"]})
        else:
            self.page(200, "<p>Credenziali errate.</p>" + LOGIN_FORM)

    def dashboard(self):
        user = self.cookie_val("sessione")
        if not user:
            self.page(200, "<p>Non sei autenticato.</p>" + LOGIN_FORM)
            return
        # cookie usato direttamente in query (di nuovo vulnerabile, ma qui basta)
        c = db()
        row = c.execute("SELECT * FROM utenti WHERE username=?", (user,)).fetchone()
        c.close()
        if not row:
            self.page(200, "<p>Sessione non valida.</p>")
            return
        self.page(200, "<h2>Conto di %s</h2><p>IBAN: %s</p><p>Saldo: %s euro</p>"
                  "<p>Nota: %s</p>" % (_html.escape(row["username"]), row["conto"],
                                       row["saldo"], _html.escape(row["nota"])))

    def pannello(self):
        # controllo accessi ROTTO: si fida del cookie 'sessione'
        user = self.cookie_val("sessione")
        c = db()
        row = c.execute("SELECT ruolo FROM utenti WHERE username=?", (user,)).fetchone()
        c.close()
        if row and row["ruolo"] == "admin":
            self.page(200, "<h2>Pannello amministratore</h2><p>Accesso riservato.</p>"
                      "<p>%s</p>" % flag("FLAG_COOKIE_ADMIN", "FLAG{cookie_manomesso_demo}"))
        else:
            self.page(403, "<p>403 - Solo gli amministratori possono entrare qui.</p>"
                      "<p>(sei: %s)</p>" % (_html.escape(user) or "anonimo"))

    def cerca(self, q):
        termine = q.get("conto", [""])[0]
        blocco = "<h2>Cerca un conto</h2><form method='get' action='/cerca'>" \
                 "<input name='conto' value='%s'><button>Cerca</button></form>" \
                 % _html.escape(termine)
        if not termine:
            self.page(200, blocco)
            return
        # riflessione NON filtrata (XSS riflesso) + ricompensa didattica
        premio = ""
        low = termine.lower()
        if "<script" in low or "onerror=" in low or "<img" in low:
            premio = "<!-- payload iniettato: %s -->" % flag(
                "FLAG_XSS_REFLECTED", "FLAG{xss_riflesso_demo}")
        riflesso = "<p>Risultati per: %s</p>" % termine  # NON escappato: XSS
        # VULNERABILE: SQL injection nella ricerca (3 colonne: username, conto, nota)
        query = ("SELECT username, conto, nota FROM utenti "
                 "WHERE username LIKE '%%%s%%'" % termine)
        c = db()
        try:
            rows = c.execute(query).fetchall()
            tab = "<table border=1><tr><th>utente</th><th>conto</th><th>nota</th></tr>"
            for r in rows:
                tab += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    _html.escape(str(r[0])), _html.escape(str(r[1])),
                    _html.escape(str(r[2])))
            tab += "</table>"
        except sqlite3.Error as e:
            tab = "<p>Errore SQL: %s</p><pre>%s</pre>" % (
                _html.escape(str(e)), _html.escape(query))
        c.close()
        self.page(200, blocco + riflesso + tab + premio)

    def bacheca_get(self):
        c = db()
        msgs = c.execute("SELECT autore, testo FROM messaggi ORDER BY id DESC").fetchall()
        c.close()
        premio = ""
        lista = ""
        for m in msgs:
            # testo NON escappato: XSS memorizzato
            lista += "<li><b>%s</b>: %s</li>" % (_html.escape(m["autore"]), m["testo"])
            if "<script" in m["testo"].lower() or "onerror=" in m["testo"].lower():
                premio = "<!-- script memorizzato: %s -->" % flag(
                    "FLAG_XSS_STORED", "FLAG{xss_memorizzato_demo}")
        form = ("<h2>Bacheca messaggi</h2><form method='post' action='/bacheca'>"
                "<input name='autore' placeholder='nome'>"
                "<input name='testo' placeholder='messaggio'>"
                "<button>Pubblica</button></form><ul>%s</ul>" % lista)
        self.page(200, form + premio)

    def bacheca_post(self, form):
        autore = form.get("autore", ["anonimo"])[0] or "anonimo"
        testo = form.get("testo", [""])[0]
        c = db()
        c.execute("INSERT INTO messaggi(autore,testo) VALUES(?,?)", (autore, testo))
        c.commit()
        c.close()
        self.send_response(302)
        self.send_header("Location", "/bacheca")
        self.end_headers()

    def documenti(self, q):
        nome = q.get("file", [""])[0]
        if not nome:
            try:
                elenco = os.listdir(DOCS)
            except OSError:
                elenco = []
            links = "".join("<li><a href='/documenti?file=%s'>%s</a></li>" % (n, n)
                            for n in elenco)
            self.page(200, "<h2>Documenti</h2><ul>%s</ul>"
                      "<p>Apri con: /documenti?file=nomefile</p>" % links)
            return
        # VULNERABILE: nessuna sanitizzazione, path traversal / LFI
        percorso = os.path.join(DOCS, nome)
        try:
            with open(percorso, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
        except OSError as e:
            self.page(404, "<p>Impossibile leggere: %s</p>" % _html.escape(str(e)))

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    init_db()
    porta = int(os.environ.get("BANCA_PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", porta), H).serve_forever()
BANCA_PY
chmod 755 "$APPDIR/banca.py"

# 3) Reset del database (rigioca da capo la piattaforma)
rm -f "$APPDIR/banca.db"

# 4) Libera la porta 8080 dalla vecchia pagina statica (container nginx)
if command -v docker >/dev/null 2>&1; then
  docker rm -f banca >/dev/null 2>&1 || true
fi

# 5) Helper di comodo: banca-ctl {start|stop|reset|stato}
cat > /usr/local/bin/banca-ctl <<'EOF'
#!/usr/bin/env bash
case "${1:-stato}" in
  start) systemctl start banca ;;
  stop)  systemctl stop banca ;;
  reset) systemctl stop banca; rm -f /opt/lab/banca-app/banca.db; systemctl start banca; echo "database azzerato";;
  stato) systemctl status banca --no-pager ;;
  *) echo "Uso: banca-ctl {start|stop|reset|stato}" ;;
esac
EOF
chmod 755 /usr/local/bin/banca-ctl

# 6) Servizio systemd
cat > /etc/systemd/system/banca.service <<'EOF'
[Unit]
Description=Banca della Scuola (app web vulnerabile del laboratorio)
After=network.target
[Service]
EnvironmentFile=/opt/lab/banca-app/flags.env
ExecStart=/usr/bin/python3 /opt/lab/banca-app/banca.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now banca.service >/dev/null 2>&1 || true
systemctl restart banca.service >/dev/null 2>&1 || true

sleep 1
echo
if curl -s http://localhost:8080/ | grep -q "Banca della Scuola"; then
  echo "[OK] Banca della Scuola attiva su http://10.10.10.20:8080"
  echo "     Utente di prova (login regolare):  cliente / cliente"
  echo "     Flag e password (solo docente):    sudo cat $APPDIR/flags.env"
else
  echo "[!] La Banca non risponde. Controlla:  systemctl status banca"
fi
