#!/usr/bin/env bash
# Lezione 38 · lato Kali · ripasso e preparazione al CTF. Mini sfide da tutto il
# corso, con verificatore. Offline. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-38"

echo "== Lezione 38 · Ripasso e preparazione al CTF =="
mkdir -p "$DIR"

# Sfida A (pipe/grep): flag nascosta tra tante righe
{ for i in $(seq 1 200); do echo "riga di rumore numero $i"; done
  echo "nota-importante: FLAG{ripasso_pipe}"
  for i in $(seq 201 400); do echo "riga di rumore numero $i"; done; } > "$DIR/rumore.txt"

# Sfida B (base64): flag offuscata
printf 'FLAG{ripasso_base64}' | base64 > "$DIR/segreto.b64"

# Sfida C (cracking): un hash MD5 da rompere con la wordlist
cat > "$DIR/wordlist.txt" <<'EOF'
estate
inverno
montagna
girasole2012
password
qwerty
EOF
printf '%s\n' "$(printf '%s' girasole2012 | md5sum | awk '{print $1}')" > "$DIR/hash.txt"

# Sfida D (log): trova l'IP attaccante
{ for i in $(seq 1 80); do echo "ok login da 10.10.10.$((30+RANDOM%5))"; done
  for i in $(seq 1 150); do echo "FALLITO login da 10.10.10.77"; done; } > "$DIR/accessi.log"

chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab38-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  cracking)
    [ "$(low "${2:-}")" = "girasole2012" ] \
      && { echo "[OK] Hash rotto!"; echo "FLAG{ripasso_cracking}"; } \
      || echo "[--] No. Rompi l'MD5 in hash.txt con la wordlist." ;;
  log)
    [ "${2:-}" = "10.10.10.77" ] \
      && { echo "[OK] Attaccante individuato!"; echo "FLAG{ripasso_log}"; } \
      || echo "[--] No. Conta i FALLITI per IP in accessi.log." ;;
  *)
    echo "Uso: lab38-verifica {cracking <password> | log <ip>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab38-verifica

cat <<'MSG'

------------------------------------------------------------
 ALLENAMENTO · Ripasso a sfide (preparati al CTF finale)
------------------------------------------------------------
 Quattro mini sfide, una per abilita'. Cartella:  ~/lab/lezione-38

 [ ] A  Pipe/grep: trova la flag nel rumore                    (+15)
        grep FLAG rumore.txt

 [ ] B  Base64: decodifica il segreto                          (+15)
        cat segreto.b64 | base64 -d

 [ ] C  Cracking: rompi l'hash MD5                             (+20)
        cat hash.txt
        for w in $(cat wordlist.txt); do echo "$(printf %s "$w" | md5sum | cut -d" " -f1) $w"; done | grep -f hash.txt
        lab38-verifica cracking <password>

 [ ] D  Log: trova l'IP dell'attaccante                        (+20)
        grep FALLITO accessi.log | grep -oE "10[0-9.]+" | sort | uniq -c | sort -rn | head
        lab38-verifica log <ip>

 Ripasso sul BERSAGLIO (per il CTF web): rigioca lab 12-18 (SQLi, XSS, cookie,
 brute force, LFI). Rivedi anche recon (lab 8-10) e rete (lab 23-27).
------------------------------------------------------------
MSG
