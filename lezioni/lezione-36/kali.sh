#!/usr/bin/env bash
# Lezione 36 · lato Kali · log, monitoraggio e rilevamento (blue team).
# Semina un log di autenticazione con dentro un attacco brute force e la
# successiva compromissione. Il verificatore controlla le risposte. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-36"

echo "== Lezione 36 · Log, monitoraggio e rilevamento =="
mkdir -p "$DIR"

LOG="$DIR/auth.log"
: > "$LOG"
UTENTI=(anna luca sara marco giulia)
IPOK=(10.10.10.31 10.10.10.42 10.10.10.55)
# traffico normale: accessi riusciti sparsi
for i in $(seq 1 120); do
  u="${UTENTI[$((RANDOM % ${#UTENTI[@]}))]}"; ip="${IPOK[$((RANDOM % ${#IPOK[@]}))]}"
  printf 'Sep 12 09:%02d:%02d server sshd[%d]: Accepted password for %s from %s port %d ssh2\n' \
    "$((RANDOM%60))" "$((RANDOM%60))" "$((1000+RANDOM%9000))" "$u" "$ip" "$((30000+RANDOM%20000))" >> "$LOG"
done
# ATTACCO: raffica di Failed da un solo IP (10.10.10.66) su tanti utenti
for i in $(seq 1 300); do
  u="${UTENTI[$((RANDOM % ${#UTENTI[@]}))]}"; [ $((RANDOM%3)) -eq 0 ] && u="backup"
  printf 'Sep 12 11:%02d:%02d server sshd[%d]: Failed password for %s from 10.10.10.66 port %d ssh2\n' \
    "$((RANDOM%60))" "$((RANDOM%60))" "$((1000+RANDOM%9000))" "$u" "$((40000+RANDOM%20000))" >> "$LOG"
done
# LA COMPROMISSIONE: dopo tante prove, un accesso RIUSCITO dall'IP attaccante
printf 'Sep 12 11:59:58 server sshd[4242]: Accepted password for backup from 10.10.10.66 port 51888 ssh2\n' >> "$LOG"
sort -k1,3 "$LOG" -o "$LOG" 2>/dev/null || true
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab36-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  ip)
    [ "${2:-}" = "10.10.10.66" ] \
      && { echo "[OK] Esatto: l'IP con centinaia di tentativi falliti e' l'attaccante."; echo "FLAG{attaccante_smascherato}"; } \
      || echo "[--] No. Conta i Failed per IP: chi esagera e' lui." ;;
  account)
    [ "$(low "${2:-}")" = "backup" ] \
      && { echo "[OK] Esatto: e' l'account su cui l'attaccante e' infine entrato."; echo "FLAG{account_compromesso}"; } \
      || echo "[--] No. Cerca l'Accepted dall'IP attaccante: quale utente ha ceduto?" ;;
  *)
    echo "Uso: lab36-verifica {ip <indirizzo> | account <utente>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab36-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Leggere i log per scoprire l'attacco (blue team)
------------------------------------------------------------
 Un log che nessuno guarda non protegge. Qui c'e' un attacco nascosto tra
 centinaia di righe: trovalo con le pipe (ricordi la Lezione 4?).

 File:  ~/lab/lezione-36/auth.log

 [ ] 1  Trova l'IP dell'attaccante (tanti accessi falliti)     (+35)
        cd ~/lab/lezione-36
        grep "Failed password" auth.log | grep -oE "from [0-9.]+" \
          | sort | uniq -c | sort -rn | head
        lab36-verifica ip <indirizzo>

 [ ] 2  Trova l'account compromesso (accesso riuscito da lui)  (+35)
        grep "Accepted password" auth.log | grep "10.10.10.66"
        lab36-verifica account <utente>

 Concetti:  log  auth.log  brute force nei log  correlazione  timeline
------------------------------------------------------------
MSG
