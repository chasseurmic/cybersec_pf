#!/usr/bin/env bash
# Lezione 09 · lato Kali · port scanning con nmap + scanner in Python.
# Installa lo strumento portscan.py in ~/lab/lezione-09/ e mostra la missione.
# Idempotente. Lanciato con sudo dal launcher 'lab'.
set -uo pipefail

TARGET_IP="10.10.10.20"
UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-09"

echo "== Lezione 09 · Port scanning =="
mkdir -p "$DIR"

# Lo strumento della lezione: un port scanner TCP in Python (solo stdlib)
cat > "$DIR/portscan.py" <<'PY'
#!/usr/bin/env python3
# portscan.py - semplice scanner di porte TCP (didattico, solo stdlib).
# Uso:  python3 portscan.py <host> [porta_inizio] [porta_fine]
#   esempio:  python3 portscan.py 10.10.10.20 1 10000
# Prova a connettersi a ogni porta: se la connessione riesce, la porta e' aperta.
import socket
import sys
import threading
from queue import Queue

host = sys.argv[1] if len(sys.argv) > 1 else "10.10.10.20"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10000

aperte = []
coda = Queue()
lock = threading.Lock()


def lavora():
    while True:
        porta = coda.get()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        # connect_ex torna 0 se la porta e' aperta
        if s.connect_ex((host, porta)) == 0:
            with lock:
                aperte.append(porta)
        s.close()
        coda.task_done()


print("[*] Scansione di %s porte %d-%d ..." % (host, start, end))
for _ in range(200):                      # 200 thread di lavoro
    t = threading.Thread(target=lavora, daemon=True)
    t.start()
for p in range(start, end + 1):
    coda.put(p)
coda.join()

aperte.sort()
print("\nPORTE APERTE su %s:" % host)
for p in aperte:
    print("  %d/tcp aperta" % p)

# premio: hai trovato il servizio segreto?
if 7777 in aperte:
    print("\n[OK] Il tuo scanner ha trovato il servizio nascosto sulla porta 7777.")
    print("FLAG{scanner_python_funziona}")
PY
chmod +x "$DIR/portscan.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

echo
if command -v nmap >/dev/null 2>&1; then echo "[OK] nmap presente."; else echo "[--] nmap mancante."; fi
if curl -s -o /dev/null -m 4 "http://${TARGET_IP}:8080"; then
  echo "[OK] Il bersaglio risponde."
else
  echo "[--] Bersaglio non raggiungibile: il docente ha lanciato  lab 9  sul bersaglio?"
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Quali porte sono aperte sul bersaglio?
------------------------------------------------------------
 [ ] 1  Scansiona con il TUO scanner Python                    (+35)
        cd ~/lab/lezione-09
        cat portscan.py            # leggi come funziona
        python3 portscan.py 10.10.10.20 1 10000

 [ ] 2  Collegati al servizio segreto che hai scoperto         (+35)
        curl http://10.10.10.20:7777

 Cross-check con lo strumento professionale (nmap):
        sudo nmap -sS -p- -T4 10.10.10.20     # tutte le porte (SYN scan)
        nmap --top-ports 20 10.10.10.20       # le 20 piu' comuni
        nmap -Pn 10.10.10.20                  # anche se ignora il ping

 Concetti:  porta  TCP  handshake  open/closed/filtered  socket  connect_ex
------------------------------------------------------------
MSG
