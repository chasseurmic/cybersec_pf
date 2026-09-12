#!/usr/bin/env bash
# Lezione 40 · lato Kali · debrief, valutazione e difese apprese. Offline.
set -uo pipefail

echo "== Lezione 40 · Debrief e difese apprese =="

cat > /usr/local/bin/lab40-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  difese)
    shift
    if [ "$(low "$*")" = "parametrizzate escape ratelimiting cifratura dominio" ]; then
      echo "[OK] Hai abbinato ogni attacco alla sua difesa. Sei un difensore consapevole!"
      echo "FLAG{difensore_consapevole}"
    else
      echo "[--] Non tutti giusti. Ordine attacchi: SQLi, XSS, brute force, sniffing, phishing."
      echo "     Uso: lab40-verifica difese <d1> <d2> <d3> <d4> <d5>"
    fi ;;
  fine)
    echo "[OK] Corso completato. Grazie e buona sicurezza!"
    echo "FLAG{corso_completato}"
    ;;
  *)
    echo "Uso: lab40-verifica {difese <d1..d5> | fine}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab40-verifica

cat <<'MSG'

------------------------------------------------------------
 CHIUSURA · Dall'attacco alla difesa
------------------------------------------------------------
 Tutto il corso ha un senso solo: capire l'attacco per saper difendere.
 Ripassa la mappa e completa il quiz finale.

 [ ] 1  Abbina ogni ATTACCO alla sua DIFESA principale         (+50)
        Attacchi (in ordine):  SQLi · XSS · brute force · sniffing · phishing
        Difese possibili:  parametrizzate · escape · ratelimiting · cifratura · dominio
        lab40-verifica difese <d1> <d2> <d3> <d4> <d5>

 [ ] 2  Chiudi il corso                                        (+20)
        lab40-verifica fine

 Riflessione (in classe): qual e' stata la lezione piu' utile? Cosa cambierai
 nelle TUE abitudini digitali (password, aggiornamenti, link, backup)?
------------------------------------------------------------
MSG
