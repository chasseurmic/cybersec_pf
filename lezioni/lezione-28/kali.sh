#!/usr/bin/env bash
# Lezione 28 · lato Kali · social engineering: analisi di messaggi e pretexting.
# Semina messaggi-esca e un dossier, installa un verificatore. Offline. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-28"

echo "== Lezione 28 · Social engineering =="
mkdir -p "$DIR"

cat > "$DIR/messaggi.txt" <<'EOF'
=== 5 messaggi intercettati: che trucco usa ciascuno? ===

1) "ATTENZIONE: la tua password scade tra 1 ORA. Cambiala subito a questo link
    o perderai l'accesso per sempre."

2) "Sono il Dirigente Scolastico. Mi serve SUBITO il file con gli stipendi.
    Non farmi perdere tempo, mandalo a questa email."

3) "Solo per oggi! I primi 10 che compilano il modulo ricevono un buono da
    50 euro. Affrettati, i posti finiscono."

4) "Ciao, ti ho appena sistemato il PC io del supporto. Ora fammi un favore
    veloce: dimmi la tua password cosi' completo l'aggiornamento."

5) "Tutti i tuoi colleghi hanno gia' aggiornato i loro dati sul nuovo portale.
    Sei rimasto solo tu, non fare la figura di quello indietro."

Tecniche possibili (una per messaggio):
  urgenza · autorita · scarsita · reciprocita · riprovasociale
EOF

cat > "$DIR/dossier.txt" <<'EOF'
=== Dossier OSINT sul bersaglio (Mario, tecnico della Banca) ===
- Pubblica spesso foto del suo cane, che si chiama Fido.
- Tifa una squadra di calcio, festeggia ogni vittoria online.
- Ha scritto che "odia cambiare le password".
- Il suo responsabile e' in ferie fino a venerdi.

Domanda: qual e' il nome del cane? Un attaccante lo userebbe per indovinare
password o risposte alle domande di sicurezza.
EOF
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab28-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  abbina)
    shift
    if [ "$(low "$*")" = "urgenza autorita scarsita reciprocita riprovasociale" ]; then
      echo "[OK] Hai smascherato tutti i trucchi!"
      echo "FLAG{smaschero_i_trucchi}"
    else
      echo "[--] Non tutti giusti. Ordine: messaggio 1..5, una tecnica ciascuno."
      echo "     Uso: lab28-verifica abbina <t1> <t2> <t3> <t4> <t5>"
    fi ;;
  indizio)
    [ "$(low "${2:-}")" = "fido" ] && { echo "[OK] Giusto: il nome del cane e' un indizio d'oro."; echo "FLAG{pretesto_costruito}"; } \
      || echo "[--] No. Leggi il dossier: qual e' il dato che un attaccante sfrutterebbe?" ;;
  *)
    echo "Uso: lab28-verifica {abbina <t1..t5> | indizio <parola>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab28-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Smascherare la manipolazione
------------------------------------------------------------
 L'anello debole non e' il software, sono le persone. Il social engineering
 sfrutta emozioni e automatismi. Impara a riconoscere i trucchi.

 Cartella:  ~/lab/lezione-28

 [ ] 1  Abbina ogni messaggio alla sua tecnica                 (+40)
        cat messaggi.txt
        # tecniche: urgenza autorita scarsita reciprocita riprovasociale
        lab28-verifica abbina <t1> <t2> <t3> <t4> <t5>

 [ ] 2  Trova l'indizio per il pretesto                        (+30)
        cat dossier.txt
        lab28-verifica indizio <parola>

 Concetti:  pretexting  urgenza  autorita  scarsita  reciprocita  riprova sociale
------------------------------------------------------------
MSG
