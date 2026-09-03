#!/usr/bin/env bash
# Lezione 01 · configurazione lato bersaglio (target)
# Serve la pagina "Banca della Scuola" su :8080 con la flag nel commento HTML.
# Idempotente. Va eseguito sul BERSAGLIO (ruolo target), che ha Docker.
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
  echo "[!] Docker non e' installato qui."
  echo "    Questo script va eseguito sul BERSAGLIO, non sulla Kali."
  exit 1
fi

echo "== Lezione 01 (target): Banca della Scuola su :8080 =="

# 1) Pagina con la terza flag nel commento HTML
mkdir -p /opt/lab/banca
cat > /opt/lab/banca/index.html <<'EOF'
<!doctype html>
<html lang="it">
<head><meta charset="utf-8"><title>Banca della Scuola</title></head>
<body>
  <h1>Banca della Scuola</h1>
  <h2>Accesso clienti</h2>
  <form>
    <input placeholder="utente">
    <input type="password" placeholder="password">
    <button>Entra</button>
  </form>
  <!-- FLAG{ho_parlato_col_server} -->
</body>
</html>
EOF

# 2) Il target e' isolato: l'immagine nginx deve essere gia' in cache
if ! docker image inspect nginx:alpine >/dev/null 2>&1; then
  echo "[!] Immagine nginx:alpine non presente in cache."
  echo "    Sull'immagine base, una volta con internet: docker pull nginx:alpine"
  exit 1
fi

# 3) (Ri)avvia il container in modo idempotente
docker rm -f banca >/dev/null 2>&1 || true
docker run -d --name banca --restart unless-stopped -p 8080:80 \
  -v /opt/lab/banca:/usr/share/nginx/html:ro nginx:alpine >/dev/null

# 4) Verifica locale
sleep 1
if curl -s http://localhost:8080 | grep -q FLAG; then
  echo "[OK] Pagina attiva, flag servita su :8080."
else
  echo "[!] Container avviato ma la flag non compare. Controlla: docker logs banca"
fi

IP="$(hostname -I | awk '{print $1}')"
cat <<MSG

------------------------------------------------------------
 LEZIONE 1 (target) · pronto
------------------------------------------------------------
 Dalla Kali gli studenti potranno fare:
   ping -c 3 ${IP:-10.10.10.20}
   curl -s http://${IP:-10.10.10.20}:8080 | grep FLAG
 Terza flag: FLAG{ho_parlato_col_server}
------------------------------------------------------------
MSG