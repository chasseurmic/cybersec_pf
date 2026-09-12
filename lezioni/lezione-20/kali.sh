#!/usr/bin/env bash
# Lezione 20 · lato Kali · cracking a dizionario di hash MD5 (tool + john/hashcat).
# Installa un cracker Python, una wordlist e un file di hash da rompere. Offline.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-20"

echo "== Lezione 20 · Cracking a dizionario =="
mkdir -p "$DIR"

# Wordlist piccola e deterministica (contiene le password giuste tra i distrattori)
cat > "$DIR/wordlist.txt" <<'EOF'
password
123456
qwerty
estate
inverno
giardino
montagna
tramonto2011
calcio
gattonero
letmein
draghi
EOF

# File di hash da rompere (MD5), calcolati al volo
{
  printf '%s\n' "$(printf '%s' password     | md5sum | awk '{print $1}')"
  printf '%s\n' "$(printf '%s' tramonto2011 | md5sum | awk '{print $1}')"
  printf '%s\n' "$(printf '%s' giardino     | md5sum | awk '{print $1}')"
  printf '%s\n' "$(printf '%s' qwerty       | md5sum | awk '{print $1}')"
} > "$DIR/hashes.txt"

# Lo strumento della lezione: cracker MD5 a dizionario (solo stdlib)
cat > "$DIR/cracker.py" <<'PY'
#!/usr/bin/env python3
# cracker.py - rompe hash MD5 provando ogni parola di una wordlist.
# Uso:  python3 cracker.py <file_hash> <wordlist>
import sys, hashlib

hashfile = sys.argv[1] if len(sys.argv) > 1 else "hashes.txt"
wordlist = sys.argv[2] if len(sys.argv) > 2 else "wordlist.txt"

hashes = set(h.strip().lower() for h in open(hashfile) if h.strip())
parole = [w.strip() for w in open(wordlist) if w.strip()]

trovate = {}
for w in parole:
    h = hashlib.md5(w.encode()).hexdigest()
    if h in hashes:
        trovate[h] = w

print("[*] Rotti %d hash su %d:" % (len(trovate), len(hashes)))
for h in hashes:
    print("  %s : %s" % (h, trovate.get(h, "(non trovato)")))
PY
chmod +x "$DIR/cracker.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

# Verificatore
cat > /usr/local/bin/lab20-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
md5() { printf '%s' "$1" | md5sum | awk '{print $1}'; }
if [ "${1:-}" = "pro" ]; then
  [ "$(md5 "${2:-}")" = "$(md5 giardino)" ] && { echo "[OK] Giusto!"; echo "FLAG{john_e_hashcat}"; } || echo "[--] No. Rompi il secondo hash con john o hashcat."
else
  [ "$(md5 "${1:-}")" = "$(md5 tramonto2011)" ] && { echo "[OK] Password recuperata!"; echo "FLAG{cracker_a_dizionario}"; } || echo "[--] No. Usa cracker.py per trovare la password segreta."
fi
EOF
chmod 755 /usr/local/bin/lab20-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Ritrovare le password dagli hash
------------------------------------------------------------
 Cartella:  ~/lab/lezione-20   (hashes.txt, wordlist.txt, cracker.py)

 [ ] 1  Rompi gli hash col TUO cracker                         (+40)
        cd ~/lab/lezione-20
        cat cracker.py
        python3 cracker.py hashes.txt wordlist.txt
        # una password recuperata e' quella "segreta": consegnala
        lab20-verifica <password_segreta>

 [ ] 2  Fai lo stesso con gli strumenti professionali          (+30)
        john --format=raw-md5 --wordlist=wordlist.txt hashes.txt
        john --show --format=raw-md5 hashes.txt
        # oppure hashcat:
        # hashcat -m 0 -a 0 hashes.txt wordlist.txt --force
        # hashcat -m 0 hashes.txt --show
        lab20-verifica pro <una_password_recuperata>

 Nota: su Kali c'e' anche rockyou:  /usr/share/wordlists/rockyou.txt.gz
       (scompattala con  gunzip -k  per una wordlist enorme).
------------------------------------------------------------
MSG
