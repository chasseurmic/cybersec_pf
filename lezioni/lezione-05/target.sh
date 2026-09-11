#!/usr/bin/env bash
# Lezione 05 · lato bersaglio · semina lo scenario "utenti, processi, servizi".
# Crea utenti da enumerare, un processo con la password negli argomenti, un
# servizio in ascolto su una porta insolita e una regola sudo troppo generosa.
# Idempotente: rilanciare 'lab 5' rigenera tutto. Eseguire sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 5"
  exit 1
fi
echo "== Lezione 05 (bersaglio) · scenario utenti/processi/servizi =="

# 0) Utente ospite 'studente' + SSH (come nelle lezioni precedenti)
if ! id studente >/dev/null 2>&1; then useradd -m -s /bin/bash studente; fi
echo 'studente:studente' | chpasswd
export DEBIAN_FRONTEND=noninteractive
if [ ! -x /usr/sbin/sshd ]; then apt-get update && apt-get -y install openssh-server; fi
mkdir -p /etc/ssh/sshd_config.d
printf 'PasswordAuthentication yes\n' > /etc/ssh/sshd_config.d/99-lab.conf
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true
systemctl restart ssh >/dev/null 2>&1 || systemctl restart sshd >/dev/null 2>&1 || true

# 1) FLAG 1 · utenti da enumerare in /etc/passwd
#    'webadmin' e' un utente di servizio normale; 'backup' e' l'anomalia:
#    ha una shell di login (non dovrebbe) e la flag nel campo commento (GECOS).
id webadmin >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin webadmin
if ! id backup_old >/dev/null 2>&1; then useradd -m -s /bin/bash backup_old; fi
usermod -c 'Account backup dimenticato FLAG{utente_di_troppo}' backup_old
echo 'backup_old:backup_old' | chpasswd

# 2) FLAG 2 · processo con la password negli argomenti (visibile con ps aux)
cat > /usr/local/bin/finto-daemon <<'EOF'
#!/usr/bin/env bash
# Finto demone di sincronizzazione: ignora gli argomenti e dorme.
# Serve solo a mostrare che una password passata da riga di comando
# resta visibile a chiunque con  ps aux .
while true; do sleep 3600; done
EOF
chmod 755 /usr/local/bin/finto-daemon
cat > /etc/systemd/system/lab05-daemon.service <<'EOF'
[Unit]
Description=Lab05 finto demone con credenziale negli argomenti
[Service]
ExecStart=/usr/local/bin/finto-daemon --user=sync --password=FLAG{la_password_e_nel_processo}
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# 3) FLAG 3 · servizio in ascolto su una porta insolita (31337)
mkdir -p /opt/lab/porta
cat > /opt/lab/porta/index.html <<'EOF'
<!doctype html><meta charset="utf-8"><title>servizio dimenticato</title>
<h1>Servizio interno dimenticato</h1>
<p>Nessuno sapeva che questa porta fosse ancora aperta.</p>
<p>FLAG{una_porta_dimenticata}</p>
EOF
cat > /etc/systemd/system/lab05-porta.service <<'EOF'
[Unit]
Description=Lab05 servizio dimenticato su porta 31337
[Service]
ExecStart=/usr/bin/python3 -m http.server 31337 --directory /opt/lab/porta --bind 0.0.0.0
Restart=always
[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now lab05-daemon.service >/dev/null 2>&1 || true
systemctl restart lab05-daemon.service >/dev/null 2>&1 || true
systemctl enable --now lab05-porta.service >/dev/null 2>&1 || true
systemctl restart lab05-porta.service >/dev/null 2>&1 || true

# 4) FLAG 4 · regola sudo troppo generosa (si scopre con  sudo -l )
cat > /usr/local/bin/lab05-flag <<'EOF'
#!/usr/bin/env bash
echo "Hai eseguito un comando come root grazie a una regola sudo troppo larga."
echo "FLAG{sudo_apre_le_porte}"
EOF
chmod 755 /usr/local/bin/lab05-flag
echo 'studente ALL=(root) NOPASSWD: /usr/local/bin/lab05-flag' > /etc/sudoers.d/lab05
chmod 440 /etc/sudoers.d/lab05
# controllo di sicurezza: se la sintassi sudoers e' errata, rimuovi il file
if ! visudo -cf /etc/sudoers.d/lab05 >/dev/null 2>&1; then
  echo "[!] regola sudo non valida, la rimuovo per sicurezza"; rm -f /etc/sudoers.d/lab05
fi

sleep 1
cat <<'MSG'

------------------------------------------------------------
 LEZIONE 5 (bersaglio) · scenario pronto
------------------------------------------------------------
 Dalla Kali:  ssh studente@10.10.10.20   (password: studente)
 Da trovare:
   1 utente sospetto in /etc/passwd        (grep, cut)
   2 password in un processo               (ps aux | grep)
   3 servizio su porta insolita 31337      (ss -tlnp ; curl)
   4 regola sudo troppo generosa           (sudo -l)
 Stato servizi:  systemctl status lab05-daemon lab05-porta
------------------------------------------------------------
MSG
