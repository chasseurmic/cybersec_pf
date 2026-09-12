#!/usr/bin/env bash
# Lezione 11 · lato Kali · come funziona il web (HTTP, DevTools, curl).
# Di sola lettura: mostra la missione e verifica il portale. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 11 · Come funziona il web =="
echo

if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8090"; then
  echo "[OK] Il portale risponde su http://${TARGET_IP}:8090"
else
  echo "[--] Portale non raggiungibile: il docente ha lanciato  lab 11  sul bersaglio?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Parla la lingua del web con curl
------------------------------------------------------------
 Il web e' fatto di richieste e risposte HTTP. curl te le fa vedere.

 Guarda una richiesta completa (verbose):
        curl -v http://10.10.10.20:8090/

 [ ] 1  Passa un parametro nella URL (GET)                     (+15)
        curl "http://10.10.10.20:8090/saluta?nome=admin"

 [ ] 2  Invia dati con una POST (come un form)                 (+20)
        curl -d "utente=admin&password=banca123" http://10.10.10.20:8090/login

 [ ] 3  Aggiungi un header alla richiesta                      (+15)
        curl -H "X-Ruolo: dipendente" http://10.10.10.20:8090/staff

 [ ] 4  Manda un cookie                                        (+20)
        curl -b "sessione=valida" http://10.10.10.20:8090/area-clienti

 Extra: guarda i codici di stato e i redirect
        curl -i http://10.10.10.20:8090/staff        # 403 senza header
        curl -i http://10.10.10.20:8090/vecchio      # 301 (spostato)
        curl -L http://10.10.10.20:8090/vecchio      # -L segue il redirect

 In aula: apri lo stesso portale in Firefox e usa gli Strumenti per
 sviluppatori (F12), scheda Rete, per vedere le stesse richieste.
------------------------------------------------------------
MSG
