#!/usr/bin/env bash
# Lezione 21 · lato Kali · cifratura simmetrica e asimmetrica (openssl). Offline.
# Prepara un messaggio cifrato AES e una coppia di chiavi RSA con un messaggio
# cifrato per la chiave pubblica. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-21"

echo "== Lezione 21 · Cifratura simmetrica e asimmetrica =="
mkdir -p "$DIR"; cd "$DIR" || exit 1

# 1) SIMMETRICO: messaggio cifrato con AES-256 e una passphrase
printf 'Messaggio riservato della Banca.\nFLAG{decifrato_simmetrico}\n' > /tmp/lab21_plain.txt
openssl enc -aes-256-cbc -pbkdf2 -salt -in /tmp/lab21_plain.txt \
  -out "$DIR/segreto.enc" -pass pass:chiavesegreta 2>/dev/null
rm -f /tmp/lab21_plain.txt

# 2) ASIMMETRICO: coppia di chiavi RSA + messaggio cifrato con la pubblica
openssl genrsa -out "$DIR/priv.pem" 2048 2>/dev/null
openssl rsa -in "$DIR/priv.pem" -pubout -out "$DIR/pub.pem" 2>/dev/null
printf 'Solo chi ha la chiave privata mi legge.\nFLAG{la_chiave_privata_apre}\n' > /tmp/lab21_msg.txt
openssl pkeyutl -encrypt -pubin -inkey "$DIR/pub.pem" \
  -in /tmp/lab21_msg.txt -out "$DIR/messaggio.enc" 2>/dev/null
rm -f /tmp/lab21_msg.txt

chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Aprire cio' che e' cifrato
------------------------------------------------------------
 Cartella:  ~/lab/lezione-21

 Ripasso: HASH = a senso unico (non si torna indietro).
          CIFRATURA = reversibile, se hai la chiave giusta.

 [ ] 1  Cifratura SIMMETRICA (una sola chiave/passphrase)      (+30)
        # ti hanno dato la passphrase:  chiavesegreta
        openssl enc -d -aes-256-cbc -pbkdf2 -in segreto.enc -pass pass:chiavesegreta
        # dentro c'e' la flag

 [ ] 2  Cifratura ASIMMETRICA (chiave pubblica/privata)        (+40)
        # il messaggio e' stato cifrato con la chiave PUBBLICA:
        # solo la chiave PRIVATA (priv.pem) puo' aprirlo
        openssl pkeyutl -decrypt -inkey priv.pem -in messaggio.enc

 Approfondimento (senza punti): la firma digitale
        # si firma con la chiave privata e si verifica con la pubblica
        echo "io sono io" > f.txt
        openssl dgst -sha256 -sign priv.pem -out f.sig f.txt
        openssl dgst -sha256 -verify pub.pem -signature f.sig f.txt   # Verified OK

 Concetti:  simmetrico (AES)  asimmetrico (RSA)  chiave pubblica/privata  firma
------------------------------------------------------------
MSG
