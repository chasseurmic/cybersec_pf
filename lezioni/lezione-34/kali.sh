#!/usr/bin/env bash
# Lezione 34 · lato Kali · analisi dinamica e indicatori di compromissione (IOC).
# Installa un "campione" INNOCUO che si comporta in modo sospetto (lascia un file,
# tenta un C2) da osservare mentre gira. Sandbox, offline. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-34"

echo "== Lezione 34 · Analisi dinamica e IOC =="
mkdir -p "$DIR"

cat > "$DIR/sample-sim.py" <<'PY'
#!/usr/bin/env python3
# sample-sim.py - simulazione INNOCUA di malware per l'analisi dinamica.
# NON fa danni: lascia un file "esca" in una sandbox e tenta (invano) di
# contattare un finto server C2. Serve solo per essere osservato mentre gira.
import socket, os, time
SANDBOX = "/tmp/lab34-sandbox"
C2 = ("10.66.66.66", 4444)          # finto server di comando e controllo
os.makedirs(SANDBOX, exist_ok=True)
with open(os.path.join(SANDBOX, ".persistenza"), "w") as f:
    f.write("finto marcatore di persistenza (innocuo)\n")
print("[sim] avviato: lascio /tmp/lab34-sandbox/.persistenza e chiamo il C2 %s:%s" % C2)
for i in range(15):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect(C2)          # nel lab isolato fallisce: conta il TENTATIVO
    except OSError:
        pass
    s.close()
    print("[sim] tentativo di connessione al C2 numero %d" % (i + 1))
    time.sleep(2)
print("[sim] finito. (nessun danno reale)")
PY
chmod +x "$DIR/sample-sim.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab34-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "$*" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  c2)
    [ "$(low "${2:-}")" = "10.66.66.66:4444" ] \
      && { echo "[OK] Hai individuato il server di comando e controllo (C2)."; echo "FLAG{ho_trovato_il_c2}"; } \
      || echo "[--] No. Osserva le connessioni del campione (strace/ss): a chi si collega?" ;;
  file)
    [ "$(low "${2:-}")" = ".persistenza" ] \
      && { echo "[OK] Hai trovato l'artefatto lasciato su disco."; echo "FLAG{indicatore_su_disco}"; } \
      || echo "[--] No. Guarda cosa compare in /tmp/lab34-sandbox mentre il campione gira." ;;
  *)
    echo "Uso: lab34-verifica {c2 <ip:porta> | file <nomefile>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab34-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Osservare il malware mentre agisce (analisi dinamica)
------------------------------------------------------------
 L'analisi dinamica guarda il COMPORTAMENTO del programma mentre gira, in una
 sandbox isolata. Il campione di oggi e' innocuo: lascia un file e chiama un
 (finto) server C2 che nel lab non risponde.

 Cartella:  ~/lab/lezione-34

 [ ] 1  Scopri con chi cerca di parlare (il C2)                (+35)
        # Terminale A: osserva le connessioni di sistema
        strace -f -e trace=connect python3 sample-sim.py
        # (in alternativa, mentre gira in un altro terminale:)
        #   ss -tnp | grep 4444
        lab34-verifica c2 <ip:porta>

 [ ] 2  Trova l'artefatto lasciato su disco                    (+35)
        ls -la /tmp/lab34-sandbox        # compare un file nascosto
        lab34-verifica file <nomefile>

 Concetti:  analisi dinamica  sandbox  C2  artefatti  IOC  strace  ss
------------------------------------------------------------
MSG
