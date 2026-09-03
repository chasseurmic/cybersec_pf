#!/usr/bin/env bash
# Lezione 03 · lato Kali · briefing della caccia al tesoro (di sola lettura).
# Controlla che il bersaglio accetti SSH e mostra la missione. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 03 · CACCIA AL TESORO su filesystem e permessi =="
echo

# La porta SSH del bersaglio e' aperta?
if command -v nc >/dev/null 2>&1 && nc -z -w 3 "$TARGET_IP" 22 2>/dev/null; then
  echo "[OK] Il bersaglio accetta connessioni SSH: puoi entrare."
else
  echo "[--] Non raggiungo la porta SSH del bersaglio ($TARGET_IP:22)."
  echo "     Controlla: la VM bersaglio e' accesa? Ci hai lanciato prima  lab 3 ?"
fi

cat <<'MSG'

La tua missione: entra nel bersaglio ed esplora il suo filesystem.
Porta d'ingresso (per oggi il bersaglio ti lascia entrare come ospite):

   ssh studente@10.10.10.20        (password: studente)

Da trovare (riporta flag e punteggio al docente):
   [ ] Punto 1  il file di BENVENUTO nella tua home          (10)
   [ ] Punto 2  un file NASCOSTO nella tua home              (10)
   [ ] Punto 3  un file dimenticato in PROFONDITA' in /srv   (15)
   [ ] Punto 4  un segreto lasciato LEGGIBILE a tutti        (15)
   [ ] Punto 5  IL MURO: un file che NON riesci a leggere    (10)
   [ ] Bonus    metti in SICUREZZA la tua password           (10)

I tuoi attrezzi:  pwd   ls -la   cd   cat   find   grep   stat   chmod
MSG
