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

# 3) Dataset dell'azienda (ripulito e ricreato a ogni run)
BASE=/srv/azienda
rm -rf "$BASE"
mkdir -p "$BASE/logs" "$BASE/documenti"

SCANNER_IP="10.10.10.66"      # l'IP che "martella" il server (lo scanner)
FLAG_LOG="FLAG{le_pipe_scavano_nei_log}"
FLAG_DOC="FLAG{un_file_su_mille}"
FLAG_IP="FLAG{ho_trovato_lo_scanner}"

# 3a) access.log in stile web: molte righe "normali" e un IP che scansiona
LOG="$BASE/logs/access.log"
: > "$LOG"
PAGINE=(/ /home /login /style.css /logo.png /chi-siamo /contatti /prodotti /faq)
IP_NORMALI=(10.10.10.31 10.10.10.42 10.10.10.55 10.10.10.7 10.10.10.88)
# ~600 richieste normali (200 come 404 sparsi)
for i in $(seq 1 600); do
  ip="${IP_NORMALI[$((RANDOM % ${#IP_NORMALI[@]}))]}"
  pg="${PAGINE[$((RANDOM % ${#PAGINE[@]}))]}"
  code=200; [ $((RANDOM % 8)) -eq 0 ] && code=404
  echo "$ip - - [12/Sep/2026:10:$((RANDOM%60)):$((RANDOM%60)) +0200] \"GET $pg HTTP/1.1\" $code $((RANDOM%3000))" >> "$LOG"
done
# ~450 richieste dello SCANNER: quasi tutte 404 su percorsi da attaccante
SCANPATH=(/admin /wp-login.php /.env /backup.zip /config.php /phpmyadmin /.git/config /server-status /shell.php /old)
for i in $(seq 1 450); do
  pg="${SCANPATH[$((RANDOM % ${#SCANPATH[@]}))]}"
  echo "$SCANNER_IP - - [12/Sep/2026:11:$((RANDOM%60)):$((RANDOM%60)) +0200] \"GET $pg HTTP/1.1\" 404 0" >> "$LOG"
done
# 3b) la riga con il SEGRETO (flag da trovare con grep nel log)
echo "10.10.10.42 - - [12/Sep/2026:11:59:59 +0200] \"GET /note?SEGRETO=$FLAG_LOG HTTP/1.1\" 200 42" >> "$LOG"
# mescola le righe
shuf "$LOG" -o "$LOG"

# 3c) file dell'IP scanner: lo si legge SOLO dopo averlo scoperto con le pipe
cat > "$BASE/ip-$SCANNER_IP.txt" <<EOF
Questo IP ha fatto piu' richieste di tutti, quasi tutte errori 404:
e' uno scanner automatico che cerca pagine di amministrazione.
$FLAG_IP
EOF

# 4) 200 documenti: quasi tutti innocui, UNO contiene una password
for n in $(seq -w 1 200); do
  cat > "$BASE/documenti/nota-$n.txt" <<EOF
Nota interna numero $n
Promemoria riunione, nessun dato sensibile qui.
Riga di riempimento $((RANDOM)).
EOF
done
cat > "$BASE/documenti/nota-137.txt" <<EOF
Nota interna numero 137
Appunto del tecnico: credenziali del vecchio pannello.
password=Autunno2021!
$FLAG_DOC
EOF

# 5) CSV utenti (materiale per cut/sort/uniq)
cat > "$BASE/utenti.csv" <<'EOF'
nome,email,reparto
Anna Rossi,anna.rossi@scuola.local,IT
Luca Bianchi,luca.bianchi@scuola.local,Amministrazione
Sara Verdi,sara.verdi@scuola.local,IT
Marco Neri,marco.neri@scuola.local,Direzione
Giulia Gialli,giulia.gialli@scuola.local,IT
Paolo Blu,paolo.blu@scuola.local,Amministrazione
EOF

# 6) permessi: tutto leggibile dall'ospite, cartelle attraversabili
chown -R studente:studente "$BASE"
chmod -R a+rX "$BASE"

# 7) Verificatore del passo con la redirezione su file (flag bonus)
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
