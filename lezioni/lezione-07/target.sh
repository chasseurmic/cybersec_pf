#!/usr/bin/env bash
# Lezione 07 · lato bersaglio · semina il "footprint pubblico" della Banca.
# Arricchisce il sito su :8080 con briciole di informazione tipiche dell'OSINT:
# commenti nel codice, robots.txt, directory listing attivo, intestazioni HTTP
# parlanti e file dimenticati. Tutto offline. Idempotente. Eseguire sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 7"
  exit 1
fi
if ! command -v docker >/dev/null 2>&1; then
  echo "[!] Docker non e' presente: questo script va sul BERSAGLIO."; exit 1
fi
echo "== Lezione 07 (bersaglio) · footprint pubblico della Banca =="

BANCA=/opt/lab/banca
mkdir -p "$BANCA/riservato" "$BANCA/backup"

# 1) Home con login e un commento da sviluppatore (distrattore)
cat > "$BANCA/index.html" <<'EOF'
<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Banca della Scuola</title></head><body>
<h1>Banca della Scuola</h1>
<h2>Accesso clienti</h2>
<form><input placeholder="utente"><input type="password" placeholder="password">
<button>Entra</button></form>
<p><a href="chi-siamo.html">Chi siamo</a></p>
<!-- TODO: rimuovere la pagina chi-siamo prima del lancio, elenca troppi dettagli -->
</body></html>
EOF

# 2) Pagina "chi siamo": nomi, email (formato prevedibile) e FLAG nel commento
cat > "$BANCA/chi-siamo.html" <<'EOF'
<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>Chi siamo · Banca della Scuola</title></head><body>
<h1>Il nostro team</h1>
<ul>
  <li>Anna Rossi, Direttrice - anna.rossi@bancadellascuola.local</li>
  <li>Luca Bianchi, IT Manager - luca.bianchi@bancadellascuola.local</li>
  <li>Sara Verdi, Cassiera - sara.verdi@bancadellascuola.local</li>
</ul>
<p>Formato email aziendale: nome.cognome@bancadellascuola.local</p>
<!-- nota interna dello sviluppatore: FLAG{commenti_nel_codice} -->
</body></html>
EOF

# 3) robots.txt: rivela una cartella "riservata" (ma non tutte!)
cat > "$BANCA/robots.txt" <<'EOF'
User-agent: *
Disallow: /riservato/
Disallow: /admin/
EOF

# 4) /riservato/ (citata da robots): un promemoria con la FLAG
cat > "$BANCA/riservato/promemoria.txt" <<'EOF'
Promemoria interno: cambiare le password entro fine mese.
robots.txt non protegge niente, dice solo ai motori di non indicizzare.
FLAG{robots_non_nasconde}
EOF

# 5) /backup/ (NON in robots: la si trova solo con un dir buster) con credenziali vecchie
cat > "$BANCA/backup/credenziali.old" <<'EOF'
# Backup credenziali vecchio pannello (dimenticato online)
admin:Estate2021!
La direttrice riusa spesso questa password.
FLAG{directory_dimenticata}
EOF

# 6) Config nginx: directory listing attivo + intestazioni HTTP "parlanti"
cat > /opt/lab/banca-nginx.conf <<'EOF'
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    autoindex on;
    add_header X-Powered-By "BancaScuola/1.0";
    add_header X-Debug-Flag "FLAG{intestazioni_parlano}";
    location / { try_files $uri $uri/ =404; }
}
EOF

# 7) (Ri)avvio del container banca con html + conf montati (offline: nginx in cache)
if ! docker image inspect nginx:alpine >/dev/null 2>&1; then
  echo "[!] Manca nginx:alpine in cache. Una volta con internet:  docker pull nginx:alpine"; exit 1
fi
docker rm -f banca >/dev/null 2>&1 || true
docker run -d --name banca --restart unless-stopped -p 8080:80 \
  -v "$BANCA":/usr/share/nginx/html:ro \
  -v /opt/lab/banca-nginx.conf:/etc/nginx/conf.d/default.conf:ro \
  nginx:alpine >/dev/null

sleep 1
echo
if curl -s -I http://localhost:8080 | grep -qi 'X-Debug-Flag'; then
  echo "[OK] Sito arricchito e intestazioni attive su :8080."
else
  echo "[!] Il sito risponde ma l'intestazione non compare. Controlla: docker logs banca"
fi
cat <<'MSG'
------------------------------------------------------------
 LEZIONE 7 (bersaglio) · footprint seminato su http://10.10.10.20:8080
   commenti HTML · robots.txt · /riservato/ · /backup/ · header X-Debug-Flag
------------------------------------------------------------
MSG
