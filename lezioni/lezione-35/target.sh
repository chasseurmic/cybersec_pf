#!/usr/bin/env bash
# Lezione 35 · lato bersaglio · hardening di sistema (blue team).
# Semina tre debolezze da sistemare: un servizio inutile acceso, SSH permissivo,
# un file segreto leggibile da tutti. Verificatore incluso. Idempotente.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 35"; exit 1
fi
echo "== Lezione 35 (bersaglio) · hardening: tre cose da mettere a posto =="

DIR=/opt/lab/lab35
mkdir -p "$DIR"
[ -f "$DIR/flags.env" ] || {
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  { echo "FLAG_SERVIZIO=FLAG{servizio_inutile_spento_$(r)}"
    echo "FLAG_SSH=FLAG{ssh_blindato_$(r)}"
    echo "FLAG_PERMESSI=FLAG{permessi_corretti_$(r)}"; } > "$DIR/flags.env"
  chmod 600 "$DIR/flags.env"
}

# 1) Servizio inutile acceso (da disabilitare)
cat > /etc/systemd/system/lab35-inutile.service <<'EOF'
[Unit]
Description=Lab35 vecchio servizio inutile (da spegnere)
After=network.target
[Service]
ExecStart=/usr/bin/python3 -m http.server 9111 --bind 0.0.0.0
Restart=always
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now lab35-inutile.service >/dev/null 2>&1 || true

# 2) File segreto leggibile da tutti (permessi da chiudere)
echo "Credenziali di servizio: non devono essere leggibili da tutti." > "$DIR/segreti.txt"
chmod 666 "$DIR/segreti.txt"

# 3) SSH: assicura che esista la cartella drop-in (lo studente aggiunge la regola)
mkdir -p /etc/ssh/sshd_config.d

# Verificatore
cat > /usr/local/bin/lab35-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo:  sudo lab35-verifica"; exit 1; fi
. /opt/lab/lab35/flags.env 2>/dev/null || true
echo "== Controllo hardening =="

# 1) servizio inutile spento
if systemctl is-active --quiet lab35-inutile.service; then
  echo "[--] Il servizio inutile e' ancora acceso. Spegnilo:"
  echo "     sudo systemctl disable --now lab35-inutile"
else
  echo "[OK] Servizio inutile disattivato."
  echo "     ${FLAG_SERVIZIO:-FLAG{servizio_inutile_spento_demo}}"
fi

# 2) SSH: login di root disabilitato
if grep -rqiE '^\s*PermitRootLogin\s+no' /etc/ssh/sshd_config /etc/ssh/sshd_config.d/ 2>/dev/null; then
  echo "[OK] SSH: login diretto di root disabilitato."
  echo "     ${FLAG_SSH:-FLAG{ssh_blindato_demo}}"
else
  echo "[--] SSH ancora permissivo. Aggiungi PermitRootLogin no, per esempio:"
  echo "     echo 'PermitRootLogin no' | sudo tee /etc/ssh/sshd_config.d/hardening.conf"
fi

# 3) permessi del file segreto
modo="$(stat -c '%a' /opt/lab/lab35/segreti.txt 2>/dev/null || echo '')"
if [ "$modo" = "600" ] || [ "$modo" = "400" ]; then
  echo "[OK] Il file segreto ora e' protetto (permessi $modo)."
  echo "     ${FLAG_PERMESSI:-FLAG{permessi_corretti_demo}}"
else
  echo "[--] Il file segreto e' leggibile da altri (permessi $modo). Chiudilo:"
  echo "     sudo chmod 600 /opt/lab/lab35/segreti.txt"
fi
EOF
chmod 755 /usr/local/bin/lab35-verifica

echo "[OK] Seminati: servizio inutile (:9111), SSH da blindare, /opt/lab/lab35/segreti.txt (666)."
echo "     Flag (docente):  sudo cat $DIR/flags.env"
