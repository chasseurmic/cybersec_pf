#!/usr/bin/env bash
# Lezione 19 · lato Kali · come sono conservate le password (hash e salt).
# Prepara un finto dump di password e un verificatore. Tutto offline. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-19"

echo "== Lezione 19 · Hash e salt =="
mkdir -p "$DIR"

# Finto dump di un database: utente:md5(password) senza sale
{
  printf 'alice:%s\n' "$(printf '%s' password | md5sum | awk '{print $1}')"
  printf 'bob:%s\n'   "$(printf '%s' qwerty   | md5sum | awk '{print $1}')"
  printf 'carla:%s\n' "$(printf '%s' letmein  | md5sum | awk '{print $1}')"
  printf 'dave:%s\n'  "$(printf '%s' password | md5sum | awk '{print $1}')"
  printf 'erik:%s\n'  "$(printf '%s' sole     | md5sum | awk '{print $1}')"
} > "$DIR/dump.txt"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

# Verificatore (offline)
cat > /usr/local/bin/lab19-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
cmd="${1:-}"
case "$cmd" in
  coppia)
    a="${2:-}"; b="${3:-}"
    pair="$(printf '%s\n%s\n' "$a" "$b" | tr 'A-Z' 'a-z' | sort | tr '\n' ',' )"
    if [ "$pair" = "alice,dave," ]; then
      echo "[OK] Esatto: alice e dave hanno lo STESSO hash, quindi la stessa password."
      echo "FLAG{stesso_hash_stessa_password}"
    else
      echo "[--] No. Cerca nel dump i due utenti con l'hash identico (sort aiuta)."
    fi ;;
  sha256)
    h="${2:-}"
    vero="$(printf '%s' 'hash a senso unico' | sha256sum | awk '{print $1}')"
    if [ "$(echo "$h" | tr 'A-Z' 'a-z')" = "$vero" ]; then
      echo "[OK] sha256 corretto."
      echo "FLAG{hash_a_senso_unico}"
    else
      echo "[--] Non coincide. Calcola:  printf '%s' 'hash a senso unico' | sha256sum"
    fi ;;
  sale)
    h="${2:-}"
    vero="$(printf '%s' 's4leprimavera' | sha256sum | awk '{print $1}')"
    if [ "$(echo "$h" | tr 'A-Z' 'a-z')" = "$vero" ]; then
      echo "[OK] Hash salato corretto: il sale va PRIMA della password (s4le+primavera)."
      echo "FLAG{il_sale_cambia_tutto}"
    else
      echo "[--] Non coincide. Calcola:  printf '%s' 's4leprimavera' | sha256sum"
    fi ;;
  *)
    echo "Uso: lab19-verifica {coppia <u1> <u2> | sha256 <hash> | sale <hash>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab19-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Come si conservano (bene e male) le password
------------------------------------------------------------
 Cartella:  ~/lab/lezione-19

 Riscaldamento: un hash e' a senso unico. Stesso testo, stesso hash.
   printf '%s' password | md5sum
   printf '%s' password | sha256sum
   printf '%s' Password | sha256sum      # cambia una lettera: cambia tutto

 [ ] 1  Nel dump, trova i due utenti con la stessa password    (+25)
        cat ~/lab/lezione-19/dump.txt
        sort -t: -k2 ~/lab/lezione-19/dump.txt    # gli hash uguali finiscono vicini
        lab19-verifica coppia <utente1> <utente2>

 [ ] 2  Calcola l'hash sha256 di:  hash a senso unico          (+20)
        printf '%s' 'hash a senso unico' | sha256sum
        lab19-verifica sha256 <hash>

 [ ] 3  Il sale: calcola sha256 di sale+password = s4le+primavera (+25)
        printf '%s' 's4leprimavera' | sha256sum
        lab19-verifica sale <hash>

 Concetti:  hash  a senso unico  MD5/SHA  collisione di password  salt
------------------------------------------------------------
MSG
