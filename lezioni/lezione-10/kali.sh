#!/usr/bin/env bash
# Lezione 10 · lato Kali · enumerazione servizi e banner grabbing.
# Di sola lettura: mostra la missione e controlla il bersaglio. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 10 · Enumerazione servizi e banner grabbing =="
echo

if command -v nmap >/dev/null 2>&1; then echo "[OK] nmap presente."; else echo "[--] nmap mancante."; fi
if command -v nc >/dev/null 2>&1; then echo "[OK] netcat (nc) presente."; else echo "[--] nc mancante."; fi
if ping -c1 -W2 "$TARGET_IP" >/dev/null 2>&1; then
  echo "[OK] Bersaglio raggiungibile."
else
  echo "[--] Bersaglio non raggiungibile: lanciato  lab 10  sul bersaglio?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Non basta sapere QUALE porta, serve sapere COSA c'e'
------------------------------------------------------------
 Il banner e' il messaggio di saluto che molti servizi mandano appena ti
 colleghi: spesso rivela nome e versione. E' il "banner grabbing".

 [ ] 1  Cattura a mano il banner del servizio su 2121          (+35)
        nc 10.10.10.20 2121
        # (se resta in attesa, premi Invio; poi Ctrl+C per uscire)

 [ ] 2  Fai identificare i servizi a nmap (versione)           (+35)
        nmap -sV -p 2121,2525 10.10.10.20
        # leggi il banner del servizio SMTP-like sulla 2525

 Altri banner da provare (senza punti):
        nc 10.10.10.20 22                 # il banner di OpenSSH (versione!)
        curl -I http://10.10.10.20:8080   # l'header Server del web

 Perche' conta: nome + versione => si cercano le vulnerabilita' note (CVE).
 Attrezzi:  nc   nmap -sV   curl -I   whatweb
------------------------------------------------------------
MSG
