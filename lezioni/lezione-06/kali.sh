#!/usr/bin/env bash
# Lezione 06 · lato Kali · bash scripting offensivo + host alive scanner.
# Prepara la palestra di scripting e installa lo strumento della lezione
# (scanner-host) in ~/lab/lezione-06/. Idempotente. Lanciato con sudo da 'lab'.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-06"

echo "== Lezione 06 · Bash scripting offensivo =="
mkdir -p "$DIR"

# 1) Palestra: file di partenza per il primo script
cat > "$DIR/esempio.sh" <<'EOF'
#!/usr/bin/env bash
# Esempio commentato: variabili, ciclo for, condizione if.
nome="mondo"
echo "Ciao, $nome!"
for n in 1 2 3; do
  echo "giro numero $n"
done
if [ -f /etc/hostname ]; then
  echo "questo file esiste: $(cat /etc/hostname)"
fi
EOF
chmod +x "$DIR/esempio.sh"

# 2) Lo strumento della lezione: scanner-host (ping sweep parallelo + porta)
cat > "$DIR/scanner-host.sh" <<'EOF'
#!/usr/bin/env bash
# scanner-host · trova gli host vivi su una /24 e controlla una porta.
# Uso:  ./scanner-host.sh [prefisso /24] [porta]
#   esempio:  ./scanner-host.sh 10.10.10 8080
# Rileva da solo il prefisso interno se non lo passi.
set -uo pipefail

# prefisso di rete: argomento 1, oppure ricavato dal proprio IP 10.x interno
PREFISSO="${1:-}"
if [ -z "$PREFISSO" ]; then
  MIO="$(hostname -I | tr ' ' '\n' | grep -E '^10\.10\.10\.' | head -n1)"
  PREFISSO="${MIO%.*}"; [ -z "$PREFISSO" ] && PREFISSO="10.10.10"
fi
PORTA="${2:-}"

echo "[*] Scansione host vivi su ${PREFISSO}.1-254 ..."
tmp="$(mktemp)"
# ping in parallelo: 254 processi che scrivono l'IP se rispondono
for i in $(seq 1 254); do
  ip="${PREFISSO}.${i}"
  ( ping -c1 -W1 "$ip" >/dev/null 2>&1 && echo "$ip" >> "$tmp" ) &
done
wait

echo
echo "HOST VIVI:"
sort -t. -k4 -n "$tmp" | while read -r ip; do
  riga="  $ip"
  if [ -n "$PORTA" ]; then
    if timeout 1 bash -c "echo > /dev/tcp/${ip}/${PORTA}" 2>/dev/null; then
      riga="$riga   [porta ${PORTA} APERTA]"
    else
      riga="$riga   [porta ${PORTA} chiusa]"
    fi
  fi
  echo "$riga"
done

# premi: hai trovato il bersaglio del laboratorio?
if grep -q '^10\.10\.10\.20$' "$tmp"; then
  echo
  echo "[OK] Bersaglio 10.10.10.20 individuato dallo scanner."
  echo "FLAG{ho_trovato_il_bersaglio}"
  if [ "${PORTA:-}" = "8080" ] && timeout 1 bash -c 'echo > /dev/tcp/10.10.10.20/8080' 2>/dev/null; then
    echo "[OK] E la porta 8080 del bersaglio e' aperta."
    echo "FLAG{porta_aperta_trovata}"
  fi
fi
rm -f "$tmp"
EOF
chmod +x "$DIR/scanner-host.sh"

# 3) Verificatore del primo script (flag di riscaldamento)
cat > /usr/local/bin/lab06-verifica <<'EOF'
#!/usr/bin/env bash
# Premia chi scrive saluta.sh: un ciclo che stampa 5 righe "riga N".
set -uo pipefail
S="$HOME/lab/lezione-06/saluta.sh"
[ -f "$S" ] || { echo "[--] Non trovo $S. Scrivilo con un ciclo for che stampa 'riga 1'..'riga 5'."; exit 1; }
out="$(bash "$S" 2>/dev/null)"
atteso="$(printf 'riga 1\nriga 2\nriga 3\nriga 4\nriga 5\n')"
if [ "$out" = "$atteso" ]; then
  echo "[OK] Il tuo primo script funziona!"
  echo "FLAG{primo_script_bash}"
else
  echo "[--] L'output non e' quello atteso. Deve stampare esattamente: riga 1 ... riga 5"
  echo "     Suggerimento:  for n in 1 2 3 4 5; do echo \"riga \$n\"; done"
fi
EOF
chmod 755 /usr/local/bin/lab06-verifica

chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Diventa uno che scrive i suoi strumenti
------------------------------------------------------------
 Cartella di lavoro:  ~/lab/lezione-06

 [ ] 1  Scrivi il tuo primo script saluta.sh (ciclo for)      (+10)
        nano saluta.sh    # stampa: riga 1 ... riga 5
        bash saluta.sh
        lab06-verifica

 [ ] 2  Usa lo scanner per trovare il bersaglio               (+40)
        cat scanner-host.sh        # leggi il codice, commentato
        ./scanner-host.sh 10.10.10

 [ ] 3  Ripeti controllando anche la porta 8080               (+20)
        ./scanner-host.sh 10.10.10 8080

 Concetti:  variabili  $()  for  if  [ ... ]  exit code  &  wait  /dev/tcp
------------------------------------------------------------
MSG
