#!/usr/bin/env bash
# Lezione 30 · lato Kali · riconoscere e difendersi dal phishing. Offline.
# Semina una lista di URL da classificare e un ispettore di URL. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-30"

echo "== Lezione 30 · Riconoscere e difendersi dal phishing =="
mkdir -p "$DIR"

cat > "$DIR/urls.txt" <<'EOF'
=== Quali di questi link portano DAVVERO alla Banca? (dominio vero: bancadellascuola.local)

1) http://bancadellascuola.local/login
2) http://bancadellascuola-sicurezza.xyz/login
3) https://login.bancadellascuola.local/area-clienti
4) http://bancadellascuola.local.verifica-conto.ru/login
5) http://bancadellascuola.secure-login.com/accedi

Suggerimento: conta le etichette del dominio da DESTRA. Le ultime due (es.
esempio.com) sono il dominio vero; tutto quello prima puo' essere una trappola.
EOF

cat > "$DIR/url-inspector.py" <<'PY'
#!/usr/bin/env python3
# url-inspector.py - mostra il vero host di un URL e il dominio registrabile.
# Uso:  python3 url-inspector.py <url>
import sys
from urllib.parse import urlparse

url = sys.argv[1] if len(sys.argv) > 1 else ""
host = urlparse(url).hostname or "(nessun host)"
parti = host.split(".")
dominio = ".".join(parti[-2:]) if len(parti) >= 2 else host
print("URL:      ", url)
print("HOST vero:", host)
print("DOMINIO:  ", dominio, "  <-- e' qui che finisci davvero")
PY
chmod +x "$DIR/url-inspector.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab30-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  phishing)
    shift
    sel="$(printf '%s\n' "$@" | sort -u | tr '\n' ' ' | sed 's/ *$//')"
    if [ "$sel" = "2 4 5" ]; then
      echo "[OK] Hai riconosciuto tutti i link falsi!"
      echo "FLAG{occhio_al_dominio}"
    else
      echo "[--] Non e' l'insieme giusto. I falsi hanno un dominio diverso da bancadellascuola.local"
      echo "     Uso: lab30-verifica phishing <numeri dei link falsi>"
    fi ;;
  dominio)
    [ "$(low "${2:-}")" = "verifica-conto.ru" ] && { echo "[OK] Esatto: il link 4 porta a verifica-conto.ru, non alla Banca."; echo "FLAG{link_smascherato}"; } \
      || echo "[--] No. Usa url-inspector.py sul link 4 e guarda il DOMINIO (ultime due etichette)." ;;
  *)
    echo "Uso: lab30-verifica {phishing <numeri> | dominio <dominio>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab30-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Non farsi pescare
------------------------------------------------------------
 Hai costruito una pagina di phishing: ora impara a smascherarla.
 Il dominio vero della Banca e':  bancadellascuola.local

 Cartella:  ~/lab/lezione-30

 [ ] 1  Riconosci i link falsi                                 (+40)
        cat urls.txt
        lab30-verifica phishing <numeri dei link falsi>

 [ ] 2  Smaschera dove porta DAVVERO il link 4                 (+30)
        python3 url-inspector.py "http://bancadellascuola.local.verifica-conto.ru/login"
        lab30-verifica dominio <dominio-vero>

 Concetti:  dominio  sottodominio  lookalike  leggere la barra degli indirizzi
------------------------------------------------------------
MSG
