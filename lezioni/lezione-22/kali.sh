#!/usr/bin/env bash
# Lezione 22 · lato Kali · HTTPS e TLS, certificati. Sola lettura.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 22 · HTTPS e TLS, certificati =="
echo
if curl -sk -o /dev/null -m 4 "https://${TARGET_IP}:8443/"; then
  echo "[OK] Il servizio HTTPS risponde su :8443."
else
  echo "[--] Non risponde: sul bersaglio lancia  lab 22 ."
fi
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Cosa c'e' dietro il lucchetto
------------------------------------------------------------
 HTTPS = HTTP dentro un tunnel cifrato (TLS). Il sito presenta un
 CERTIFICATO che dovrebbe garantire "sono davvero io".

 [ ] 1  Leggi il certificato del server                        (+35)
        echo | openssl s_client -connect 10.10.10.20:8443 2>/dev/null \
          | openssl x509 -noout -subject -issuer -dates
        # nel campo OU del subject c'e' una flag

 [ ] 2  Scarica la pagina HTTPS                                (+35)
        curl https://10.10.10.20:8443/            # ERRORE: certificato non fidato
        curl -k https://10.10.10.20:8443/         # -k ignora il controllo: ecco la flag

 Rifletti: perche' il primo curl fallisce? Il certificato e' "self-signed",
 nessuna autorita' (CA) lo garantisce. In un browser vedresti l'avviso rosso.
 Il -k salta il controllo: comodo nel lab, PERICOLOSO nella vita reale.
------------------------------------------------------------
MSG
