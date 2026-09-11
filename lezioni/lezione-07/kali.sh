#!/usr/bin/env bash
# Lezione 07 · lato Kali · footprinting e OSINT (simulati nel lab).
# Prepara una piccola wordlist per il dir busting e mostra la missione.
# Di sola lettura sul bersaglio. Idempotente. Lanciato con sudo da 'lab'.
set -uo pipefail

TARGET_IP="10.10.10.20"
UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-07"

echo "== Lezione 07 · Footprinting e OSINT (simulati) =="
mkdir -p "$DIR"

# Wordlist piccola e deterministica per gobuster/dirb
cat > "$DIR/parole.txt" <<'EOF'
admin
login
backup
riservato
config
images
css
js
uploads
old
test
private
EOF
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

echo
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080"; then
  echo "[OK] Il sito della Banca risponde su :8080."
else
  echo "[--] Il sito non risponde. Il docente ha lanciato  lab 7  sul bersaglio?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Profila il bersaglio senza toccarlo (troppo)
------------------------------------------------------------
 Obiettivo: raccogliere informazioni dal "footprint pubblico" della Banca.

 [ ] 1  Fingerprint del server e intestazioni HTTP               (+15)
        whatweb http://10.10.10.20:8080
        curl -I http://10.10.10.20:8080        # guarda le intestazioni

 [ ] 2  Leggi il codice della pagina: cerca commenti nascosti    (+15)
        curl -s http://10.10.10.20:8080/chi-siamo.html
        curl -s http://10.10.10.20:8080/chi-siamo.html | grep FLAG

 [ ] 3  Cosa nasconde robots.txt?                                (+20)
        curl -s http://10.10.10.20:8080/robots.txt
        curl -s http://10.10.10.20:8080/riservato/promemoria.txt

 [ ] 4  Trova una cartella NON citata da robots (dir busting)    (+20)
        cd ~/lab/lezione-07
        gobuster dir -u http://10.10.10.20:8080 -w parole.txt
        curl -s http://10.10.10.20:8080/backup/credenziali.old

 Bonus (profilazione): dai nomi in "chi siamo" ricava il formato delle email.
 Attrezzi:  whatweb  curl  gobuster  dirb  grep
------------------------------------------------------------
MSG
