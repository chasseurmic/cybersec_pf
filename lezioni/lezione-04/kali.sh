#!/usr/bin/env bash
# Lezione 04 · lato Kali · briefing "redirezioni e pipe" + palestra locale.
# Prepara una piccola palestra offline sulla Kali (per esercitarsi senza il
# bersaglio) e controlla che il bersaglio sia raggiungibile via SSH.
# Idempotente. Lanciato con sudo dal launcher 'lab'.
set -uo pipefail

TARGET_IP="10.10.10.20"
UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
PAL="$HOME_UTENTE/lab/lezione-04"

echo "== Lezione 04 · Redirezioni e pipe =="
echo

# 1) Palestra locale (offline): un file di frasi su cui allenarsi
mkdir -p "$PAL"
cat > "$PAL/frasi.txt" <<'EOF'
la pipe unisce due comandi
grep filtra le righe che ci interessano
sort mette in ordine e uniq toglie i doppioni
la pipe passa il testo da un comando al comando dopo
grep filtra sort ordina uniq conta
EOF
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

# 2) Verificatore della palestra (flag di riscaldamento)
cat > /usr/local/bin/lab04-warmup <<'EOF'
#!/usr/bin/env bash
# Premia chi estrae le PAROLE UNICHE in ordine dal file frasi.txt.
set -uo pipefail
D="$HOME/lab/lezione-04"
F="$D/frasi.txt"; R="$D/parole.txt"
[ -f "$F" ] || { echo "Manca $F. Rilancia:  lab 4  sulla Kali."; exit 1; }
[ -f "$R" ] || { echo "[--] Non trovo $R. Crea l'elenco parole con le pipe, poi salvalo:"; \
                 echo "     tr ' ' '\\n' < frasi.txt | sort -u > parole.txt"; exit 1; }
atteso="$(tr ' ' '\n' < "$F" | sort -u | sed '/^$/d')"
ottenuto="$(sort -u "$R" | sed '/^$/d')"
if [ "$atteso" = "$ottenuto" ]; then
  echo "[OK] parole.txt contiene tutte le parole uniche in ordine. Sei pronto!"
  echo "FLAG{sono_pronto_per_le_pipe}"
else
  echo "[--] Non ci siamo ancora. Riprova con:  tr ' ' '\\n' < frasi.txt | sort -u > parole.txt"
fi
EOF
chmod 755 /usr/local/bin/lab04-warmup

# 3) Il bersaglio e' pronto?
if command -v nc >/dev/null 2>&1 && nc -z -w 3 "$TARGET_IP" 22 2>/dev/null; then
  echo "[OK] Il bersaglio accetta SSH: puoi entrare per il setaccio nei log."
else
  echo "[--] Non raggiungo SSH del bersaglio ($TARGET_IP:22)."
  echo "     Il docente ha lanciato prima  lab 4  sul bersaglio? La VM e' accesa?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Redirezioni e pipe
------------------------------------------------------------
 A) Palestra sulla Kali (offline):
    cd ~/lab/lezione-04
    cat frasi.txt
    tr ' ' '\n' < frasi.txt | sort -u > parole.txt
    lab04-warmup                         <-- flag di riscaldamento (+10)

 B) Setaccio sul bersaglio (via SSH):
    ssh studente@10.10.10.20             (password: studente)
    cd /srv/azienda

    [ ] 1  Trova nel log la riga con la parola SEGRETO           (+15)
           grep SEGRETO logs/access.log
    [ ] 2  Tra 200 file, trova l'unico con una password          (+15)
           grep -rl password documenti/ 2>/dev/null
    [ ] 3  Scopri l'IP che ha martellato il server e leggi il    (+20)
           suo file:  cut -d' ' -f1 logs/access.log | sort | uniq -c | sort -rn | head
    [ ] 4  Salva gli IP unici in report.txt e verifica           (+10)
           cut -d' ' -f1 logs/access.log | sort -u > report.txt
           lab04-verifica

 Attrezzi:  |   >   >>   2>/dev/null   grep   cut   sort   uniq   wc   head
------------------------------------------------------------
MSG
