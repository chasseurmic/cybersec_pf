#!/usr/bin/env bash
# Lezione 05 · lato Kali · briefing "utenti, gruppi, processi e servizi".
# Di sola lettura: mostra la missione e controlla che il bersaglio risponda.
# Idempotente. Lanciato con sudo dal launcher 'lab'.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 05 · Utenti, gruppi, processi e servizi =="
echo

echo "Prima, conosci te stesso sulla Kali:"
echo "   whoami ; id ; groups"
echo "   ps aux | head ; sudo -l"
echo

if command -v nc >/dev/null 2>&1 && nc -z -w 3 "$TARGET_IP" 22 2>/dev/null; then
  echo "[OK] Il bersaglio accetta SSH: puoi entrare per l'enumerazione."
else
  echo "[--] Non raggiungo SSH del bersaglio ($TARGET_IP:22)."
  echo "     Il docente ha lanciato prima  lab 5  sul bersaglio? La VM e' accesa?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Chi comanda su questa macchina?
------------------------------------------------------------
 Entra:  ssh studente@10.10.10.20    (password: studente)

 [ ] 1  Enumera gli utenti e trova quello di troppo            (+15)
        cat /etc/passwd | column -t -s:        # elenco leggibile
        grep bash /etc/passwd                  # chi ha una shell di login
        # leggi il campo commento dell'utente sospetto

 [ ] 2  Trova la password lasciata in un processo              (+20)
        ps aux | grep -i pass
        systemctl status lab05-daemon          # da dove arriva

 [ ] 3  Scopri il servizio su una porta insolita               (+15)
        ss -tlnp                               # porte in ascolto
        curl http://localhost:31337

 [ ] 4  Scopri cosa puoi fare come root senza password         (+20)
        sudo -l
        sudo /usr/local/bin/lab05-flag

 Attrezzi:  id  whoami  ps  top  ss  systemctl  sudo  grep  cut  column
------------------------------------------------------------
MSG
