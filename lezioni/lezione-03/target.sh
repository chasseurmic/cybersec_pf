#!/usr/bin/env bash
# Lezione 03 · lato bersaglio · semina la "caccia al tesoro" su filesystem e permessi.
# Crea l'utente ospite 'studente', abilita l'accesso SSH e semina i file esca con
# permessi didattici (alcuni leggibili, uno no). Idempotente: si puo' rilanciare.
# Va eseguito sul BERSAGLIO tramite:  lab 3   (che lo lancia con sudo).
set -uo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 3"
  exit 1
fi
echo "== Lezione 03 (bersaglio) · semina della caccia al tesoro =="

# 1) Utente ospite 'studente' (la porta d'ingresso di oggi)
if ! id studente >/dev/null 2>&1; then
  useradd -m -s /bin/bash studente
fi
echo 'studente:studente' | chpasswd

# 2) Accesso SSH con password (openssh di solito e' gia' presente su Ubuntu Server)
export DEBIAN_FRONTEND=noninteractive
if [ ! -x /usr/sbin/sshd ]; then
  apt-get update && apt-get -y install openssh-server
fi
# forza l'autenticazione a password anche se un drop-in la disattiva
mkdir -p /etc/ssh/sshd_config.d
printf 'PasswordAuthentication yes\n' > /etc/ssh/sshd_config.d/99-lab.conf
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true
systemctl restart ssh >/dev/null 2>&1 || systemctl restart sshd >/dev/null 2>&1 || true

H=/home/studente

# 3) FLAG 1 · benvenuto (file leggibile nella home)
cat > "$H/README-caccia.txt" <<'EOF'
CACCIA AL TESORO · filesystem e permessi
Regola d'oro: esplori SOLO questo bersaglio del laboratorio.
Ci sono 4 flag da leggere e 1 "muro" da capire. Buona caccia!
Prima flag (sei gia' partito bene):
FLAG{la_caccia_ha_inizio}
EOF

# 4) FLAG 2 · file nascosto (dotfile: si vede con  ls -a)
printf 'Hai mostrato i file nascosti. I punti davanti al nome li rendono invisibili a ls.\nFLAG{anche_i_nascosti_si_vedono}\n' > "$H/.diario_nascosto"

# 5) File esca del punto DIFENSIVO (parte leggibile a tutti = sbagliato, da sistemare)
printf 'Password del mio diario personale: tramonto2011\n' > "$H/mia_password.txt"
chmod 644 "$H/mia_password.txt"
chown studente:studente "$H/README-caccia.txt" "$H/.diario_nascosto" "$H/mia_password.txt"

# 6) FLAG 3 · sepolta in profondita' (si trova con  find  o  grep -r)
mkdir -p /srv/dati/reparto-IT/archivio/2021 /srv/dati/direzione
cat > /srv/dati/reparto-IT/archivio/2021/config.old <<'EOF'
# vecchia configurazione dimenticata qui nel 2021
db_host=10.10.10.20
nota=chi scava a fondo trova le cose dimenticate
FLAG{con_find_scavi_a_fondo}
EOF
chmod 644 /srv/dati/reparto-IT/archivio/2021/config.old

# 7) FLAG 4 · "permesso di troppo": segreto di root ma leggibile da chiunque
cat > /srv/dati/reparto-IT/password_backup.txt <<'EOF'
Backup credenziali reparto IT (NON dovrebbe essere leggibile da tutti!)
admin:EstateCalda2020
FLAG{permesso_di_troppo}
EOF
chown root:root /srv/dati/reparto-IT/password_backup.txt
chmod 644 /srv/dati/reparto-IT/password_backup.txt

# 8) IL MURO · segreto di root protetto bene: studente NON puo' leggerlo (Permission denied)
cat > /srv/dati/direzione/stipendi.csv <<'EOF'
nome,ruolo,stipendio
qui i permessi fanno il loro dovere: 600, solo root puo' leggere
EOF
chown root:root /srv/dati/direzione/stipendi.csv
chmod 600 /srv/dati/direzione/stipendi.csv

# cartelle attraversabili (per navigarci dentro)
chmod 755 /srv /srv/dati /srv/dati/reparto-IT /srv/dati/reparto-IT/archivio \
          /srv/dati/reparto-IT/archivio/2021 /srv/dati/direzione

# 9) Verificatore del punto difensivo: premia chi mette in sicurezza la propria password
cat > /usr/local/bin/caccia-verifica <<'EOF'
#!/usr/bin/env bash
f="$HOME/mia_password.txt"
[ -f "$f" ] || { echo "Non trovo $f (sei entrato come studente?)."; exit 1; }
modo="$(stat -c '%a' "$f")"
if [ "$modo" = "600" ] || [ "$modo" = "400" ]; then
  echo "[OK] Ora il file e' protetto (permessi $modo): solo tu puoi leggerlo."
  echo "FLAG{ora_e_al_sicuro}"
else
  echo "[--] Il file e' ancora leggibile da altri (permessi $modo)."
  echo "     Mettilo in sicurezza con:  chmod 600 $f"
fi
EOF
chmod 755 /usr/local/bin/caccia-verifica

cat <<'MSG'

------------------------------------------------------------
 LEZIONE 3 (bersaglio) · caccia al tesoro seminata
------------------------------------------------------------
 Dalla Kali gli studenti entrano con:
   ssh studente@10.10.10.20        (password: studente)
 Poi esplorano filesystem e permessi per trovare le flag.
------------------------------------------------------------
MSG
