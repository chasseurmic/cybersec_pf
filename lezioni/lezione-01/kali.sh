#!/usr/bin/env bash
# Lezione 01 · configurazione lato Kali
# Triade CIA e primo accesso. Idempotente: eseguibile piu' volte senza danni.
#
# Nota didattica: le flag di benvenuto qui sotto sono volutamente banali.
# Per le lezioni successive tieni i VALORI delle flag fuori dagli script
# pubblici (usa un repo privato o generale le a runtime), altrimenti si
# leggono direttamente su GitHub.
set -euo pipefail

# Lo script gira tramite "sudo bash", quindi l'utente reale non e' root:
# lo recuperiamo da SUDO_USER. Cosi' funziona sia con l'utente "kali"
# sia con "parallels" o qualunque altro.
UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"

echo "== Lezione 01: Triade CIA e primo accesso =="

# 1) Cartella di lavoro dello studente
mkdir -p "$HOME_UTENTE/lab/lezione-01"

# 2) Flag 1 · file di benvenuto (si trova con: cat README-corso.txt)
cat > "$HOME_UTENTE/README-corso.txt" <<'EOF'
Benvenuto nel corso di Sicurezza Informatica.
Regola d'oro: si attacca SOLO dentro questo laboratorio isolato.
Fuori da qui gli stessi comandi su altri computer sono un reato.

La tua prima flag e' qui sotto. Comunica il punteggio al docente.

FLAG{benvenuto_nel_gioco}
EOF

# 3) Flag 2 · file nascosto (si trova con: ls -a  e poi  cat .segreto)
printf 'FLAG{i_file_nascosti_non_bastano}\n' > "$HOME_UTENTE/.segreto"

# 4) I file appartengono allo studente, non a root
chown "$UTENTE:$UTENTE" "$HOME_UTENTE/README-corso.txt" "$HOME_UTENTE/.segreto"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab/lezione-01"

# 5) Briefing mostrato allo studente
cat <<'MSG'

------------------------------------------------------------
 LEZIONE 1 · Pronti!
------------------------------------------------------------
 Obiettivo: capire cosa protegge la sicurezza (triade CIA)
 e muovere i primi passi da attaccante nel terminale.

 Comandi da provare:
   whoami                 chi sei sulla macchina
   id                     il tuo numero e i tuoi gruppi
   ip a                   il tuo indirizzo in questa rete
   ls                     cosa c'e' nella cartella
   cat README-corso.txt   <-- prima flag
   ls -a                  mostra anche i file nascosti
   cat .segreto           <-- seconda flag

 Bonus (se il bersaglio e' acceso):
   ping -c 3 10.10.10.20
   curl -s http://10.10.10.20:8080 | grep FLAG   <-- terza flag

 Trova le flag e comunica il punteggio al docente.
------------------------------------------------------------
MSG

echo "[OK] Ambiente Lezione 01 pronto per l'utente $UTENTE."