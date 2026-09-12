#!/usr/bin/env bash
# Lezione 31 · lato Kali · cos'e' il malware: tipi e ciclo di vita.
# Solo descrizioni (nessun malware vero). Semina l'esercizio e il verificatore.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-31"

echo "== Lezione 31 · Malware: tipi e ciclo di vita =="
mkdir -p "$DIR"

cat > "$DIR/campioni.txt" <<'EOF'
=== 5 comportamenti descritti: che tipo di malware e'? (nessun file vero!) ===

1) Si nasconde dentro un gioco gratis; quando lo apri, apre di nascosto una
   porta di servizio (backdoor) per l'attaccante.

2) Si copia da solo attraverso la rete e infetta altri computer senza che
   nessuno debba aprire nulla.

3) Cifra tutti i tuoi file e chiede un riscatto in cambio della chiave per
   riaverli.

4) Si attacca ad altri programmi o file e si diffonde quando li esegui o li
   condividi.

5) Registra di nascosto quello che scrivi (tasti, password) e lo invia
   all'attaccante.

Tipi possibili (uno per riga):  trojan · worm · ransomware · virus · spyware
EOF

cat > "$DIR/ciclo.txt" <<'EOF'
=== Il ciclo di vita di un attacco malware: rimetti in ORDINE le 5 fasi ===

 - azione        (fa il danno: cifra, ruba, distrugge)
 - persistenza   (si assicura di ripartire a ogni riavvio)
 - consegna      (arriva sul PC: email, chiavetta, download)
 - comando       (si collega all'attaccante per ricevere ordini, C2)
 - esecuzione    (viene avviato e prende piede)

Qual e' l'ordine giusto, dalla prima all'ultima fase?
EOF
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab31-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  tipi)
    shift
    [ "$(low "$*")" = "trojan worm ransomware virus spyware" ] \
      && { echo "[OK] Classificazione corretta!"; echo "FLAG{classifico_i_malware}"; } \
      || echo "[--] Non tutti giusti. Uso: lab31-verifica tipi <t1> <t2> <t3> <t4> <t5>" ;;
  ciclo)
    shift
    [ "$(low "$*")" = "consegna esecuzione persistenza comando azione" ] \
      && { echo "[OK] Ordine del ciclo di vita corretto!"; echo "FLAG{ciclo_di_vita}"; } \
      || echo "[--] Ordine sbagliato. Uso: lab31-verifica ciclo <f1> <f2> <f3> <f4> <f5>" ;;
  *)
    echo "Uso: lab31-verifica {tipi <t1..t5> | ciclo <f1..f5>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab31-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Conoscere il nemico (senza toccarlo)
------------------------------------------------------------
 In questo blocco NON si eseguono mai malware veri: si analizzano
 descrizioni e simulazioni innocue, in una sandbox isolata senza internet.

 Cartella:  ~/lab/lezione-31

 [ ] 1  Classifica i 5 campioni per tipo                       (+40)
        cat campioni.txt
        lab31-verifica tipi <t1> <t2> <t3> <t4> <t5>

 [ ] 2  Rimetti in ordine il ciclo di vita                     (+30)
        cat ciclo.txt
        lab31-verifica ciclo <f1> <f2> <f3> <f4> <f5>

 Concetti:  virus  worm  trojan  ransomware  spyware  ciclo di vita  sandbox
------------------------------------------------------------
MSG
