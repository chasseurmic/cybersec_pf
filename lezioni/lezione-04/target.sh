#!/usr/bin/env bash
# Lezione 04 · lato bersaglio · semina il "setaccio nei log".
# Crea un dataset realistico (log, CSV, tanti file) su cui esercitarsi con
# redirezioni e pipe via SSH come utente ospite 'studente'. Idempotente:
# a ogni esecuzione ripulisce e ricrea il dataset (cosi' si rigioca/resetta).
# Va eseguito sul BERSAGLIO tramite:  lab 4   (che lo lancia con sudo).
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 4"
  exit 1
fi
echo "== Lezione 04 (bersaglio) · semina del setaccio nei log =="

# 1) Utente ospite 'studente' (porta d'ingresso, come nella Lezione 3)
if ! id studente >/dev/null 2>&1; then
  useradd -m -s /bin/bash studente
fi
echo 'studente:studente' | chpasswd

# 2) SSH con password abilitato (di solito gia' presente su Ubuntu Server)
export DEBIAN_FRONTEND=noninteractive
if [ ! -x /usr/sbin/sshd ]; then
  apt-get update && apt-get -y install openssh-server
fi
mkdir -p /etc/ssh/sshd_config.d
printf 'PasswordAuthentication yes\n' > /etc/ssh/sshd_config.d/99-lab.conf
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true
systemctl restart ssh >/dev/null 2>&1 || systemctl restart sshd >/dev/null 2>&1 || true

# 3) Dataset dell'azienda (ripulito e ricreato a ogni run).
#    Lo generiamo con python3 (sempre presente su Ubuntu): e' robusto e non
#    dipende da array bash, RANDOM o shuf, che su alcuni target lasciavano il
#    log vuoto.
BASE=/srv/azienda
rm -rf "$BASE"
mkdir -p "$BASE/logs" "$BASE/documenti"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3 non trovato: e' richiesto per generare il dataset."; exit 1
fi

python3 - "$BASE" <<'PY'
import os, random, sys
base = sys.argv[1]
random.seed(42)                         # dataset stabile e riproducibile
SCANNER_IP = "10.10.10.66"
FLAG_LOG = "FLAG{le_pipe_scavano_nei_log}"
FLAG_DOC = "FLAG{un_file_su_mille}"
FLAG_IP  = "FLAG{ho_trovato_lo_scanner}"

pagine = ["/", "/home", "/login", "/style.css", "/logo.png",
          "/chi-siamo", "/contatti", "/prodotti", "/faq"]
ip_normali = ["10.10.10.31", "10.10.10.42", "10.10.10.55", "10.10.10.7", "10.10.10.88"]
scanpath = ["/admin", "/wp-login.php", "/.env", "/backup.zip", "/config.php",
            "/phpmyadmin", "/.git/config", "/server-status", "/shell.php", "/old"]

righe = []
# ~600 richieste normali (una parte come 404 sparsi)
for _ in range(600):
    ip = random.choice(ip_normali)
    pg = random.choice(pagine)
    code = 404 if random.randint(0, 7) == 0 else 200
    righe.append('%s - - [12/Sep/2026:10:%02d:%02d +0200] "GET %s HTTP/1.1" %d %d'
                 % (ip, random.randint(0, 59), random.randint(0, 59), pg, code,
                    random.randint(0, 2999)))
# ~450 richieste dello SCANNER: quasi tutte 404 su percorsi da attaccante
for _ in range(450):
    pg = random.choice(scanpath)
    righe.append('%s - - [12/Sep/2026:11:%02d:%02d +0200] "GET %s HTTP/1.1" 404 0'
                 % (SCANNER_IP, random.randint(0, 59), random.randint(0, 59), pg))
# la riga col SEGRETO (flag da trovare con grep nel log)
righe.append('10.10.10.42 - - [12/Sep/2026:11:59:59 +0200] '
             '"GET /note?SEGRETO=%s HTTP/1.1" 200 42' % FLAG_LOG)
random.shuffle(righe)

with open(os.path.join(base, "logs", "access.log"), "w") as f:
    f.write("\n".join(righe) + "\n")

# file dell'IP scanner: lo si legge SOLO dopo averlo scoperto con le pipe
with open(os.path.join(base, "ip-%s.txt" % SCANNER_IP), "w") as f:
    f.write("Questo IP ha fatto piu' richieste di tutti, quasi tutte errori 404:\n"
            "e' uno scanner automatico che cerca pagine di amministrazione.\n"
            + FLAG_IP + "\n")

# 200 documenti: quasi tutti innocui, UNO contiene una password
docs = os.path.join(base, "documenti")
for n in range(1, 201):
    with open(os.path.join(docs, "nota-%03d.txt" % n), "w") as f:
        f.write("Nota interna numero %03d\n"
                "Promemoria riunione, nessun dato sensibile qui.\n"
                "Riga di riempimento %d.\n" % (n, random.randint(0, 99999)))
with open(os.path.join(docs, "nota-137.txt"), "w") as f:
    f.write("Nota interna numero 137\n"
            "Appunto del tecnico: credenziali del vecchio pannello.\n"
            "password=Autunno2021!\n" + FLAG_DOC + "\n")

# CSV utenti (materiale per cut/sort/uniq)
with open(os.path.join(base, "utenti.csv"), "w") as f:
    f.write("nome,email,reparto\n"
            "Anna Rossi,anna.rossi@scuola.local,IT\n"
            "Luca Bianchi,luca.bianchi@scuola.local,Amministrazione\n"
            "Sara Verdi,sara.verdi@scuola.local,IT\n"
            "Marco Neri,marco.neri@scuola.local,Direzione\n"
            "Giulia Gialli,giulia.gialli@scuola.local,IT\n"
            "Paolo Blu,paolo.blu@scuola.local,Amministrazione\n")

print("[*] Dataset generato: %d righe di log, 200 documenti, utenti.csv"
      % len(righe))
PY

# 4) permessi: tutto leggibile dall'ospite, cartelle attraversabili
chown -R studente:studente "$BASE"
chmod -R a+rX "$BASE"

# 5) Verifica: il log deve avere contenuto
RIGHE="$(wc -l < "$BASE/logs/access.log" 2>/dev/null || echo 0)"
if [ "$RIGHE" -lt 100 ]; then
  echo "[!] Attenzione: access.log ha solo $RIGHE righe. Controlla python3 sul target."
else
  echo "[OK] access.log generato con $RIGHE righe."
fi

# 6) Verificatore del passo con la redirezione su file (flag bonus)
cat > /usr/local/bin/lab04-verifica <<'EOF'
#!/usr/bin/env bash
# Premia chi salva su ~/report.txt l'elenco ORDINATO e SENZA DOPPIONI degli IP
# del log, usando cut | sort -u  e la redirezione  > report.txt
set -uo pipefail
LOG=/srv/azienda/logs/access.log
R="$HOME/report.txt"
[ -f "$LOG" ] || { echo "Non trovo il log. Il docente ha lanciato 'lab 4' sul bersaglio?"; exit 1; }
[ -f "$R" ] || { echo "[--] Non trovo $R. Salva l'elenco IP con:  cut -d' ' -f1 $LOG | sort -u > report.txt"; exit 1; }
atteso="$(cut -d' ' -f1 "$LOG" | sort -u)"
ottenuto="$(sort -u "$R")"
if [ "$atteso" = "$ottenuto" ]; then
  echo "[OK] report.txt contiene tutti gli IP unici, ordinati. Redirezione riuscita!"
  echo "FLAG{redirezione_su_file}"
else
  echo "[--] Il contenuto di report.txt non coincide con l'elenco atteso."
  echo "     Suggerimento:  cut -d' ' -f1 $LOG | sort -u > report.txt"
fi
EOF
chmod 755 /usr/local/bin/lab04-verifica

cat <<MSG

------------------------------------------------------------
 LEZIONE 4 (bersaglio) · dataset seminato in /srv/azienda
------------------------------------------------------------
 Dalla Kali gli studenti entrano con:
   ssh studente@10.10.10.20        (password: studente)
 Poi lavorano con pipe e redirezioni su:
   /srv/azienda/logs/access.log
   /srv/azienda/documenti/  (200 file)
   /srv/azienda/utenti.csv
 Verificatore del passo bonus:  lab04-verifica
------------------------------------------------------------
MSG
