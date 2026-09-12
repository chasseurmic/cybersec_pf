#!/usr/bin/env bash
# Lezione 37 · lato bersaglio · scena di una compromissione da gestire (IR).
# Semina un account creato dall'attaccante, una persistenza (cron) e installa il
# verificatore che controlla le azioni di risposta. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 37"; exit 1
fi
echo "== Lezione 37 (bersaglio) · sistema compromesso da bonificare =="

DIR=/opt/lab/lab37
mkdir -p "$DIR"
[ -f "$DIR/flags.env" ] || {
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  { echo "FLAG_ACCOUNT=FLAG{account_ostile_neutralizzato_$(r)}"
    echo "FLAG_PERSIST=FLAG{persistenza_rimossa_$(r)}"
    echo "FLAG_RETE=FLAG{attaccante_bloccato_$(r)}"; } > "$DIR/flags.env"
  chmod 600 "$DIR/flags.env"
}

# 1) Account ostile creato dall'attaccante (da neutralizzare)
if ! id svc-update >/dev/null 2>&1; then useradd -m -s /bin/bash svc-update; fi
usermod -U svc-update 2>/dev/null || true          # scenario: account attivo
echo 'svc-update:backdoor123' | chpasswd

# 2) Persistenza: un cron "che chiama casa" (INNOCUO, non fa nulla di dannoso)
cat > /etc/cron.d/lab37-backdoor <<'EOF'
# persistenza lasciata dall'attaccante (simulata, innocua)
*/5 * * * * root /bin/echo attaccante-presente >/dev/null 2>&1
EOF
chmod 644 /etc/cron.d/lab37-backdoor

# Verificatore delle azioni di risposta
cat > /usr/local/bin/lab37-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo:  sudo lab37-verifica"; exit 1; fi
. /opt/lab/lab37/flags.env 2>/dev/null || true
echo "== Controllo della risposta all'incidente =="

# 1) account ostile: rimosso oppure bloccato
if ! id svc-update >/dev/null 2>&1; then
  stato="rimosso"
else
  stato="$(passwd -S svc-update 2>/dev/null | awk '{print $2}')"
fi
if [ "$stato" = "rimosso" ] || [ "$stato" = "L" ]; then
  echo "[OK] Account ostile neutralizzato ($stato)."
  echo "     ${FLAG_ACCOUNT:-FLAG{account_ostile_neutralizzato_demo}}"
else
  echo "[--] L'account svc-update e' ancora attivo. Bloccalo o rimuovilo:"
  echo "     sudo usermod -L svc-update     (oppure: sudo userdel -r svc-update)"
fi

# 2) persistenza rimossa
if [ ! -f /etc/cron.d/lab37-backdoor ]; then
  echo "[OK] Persistenza (cron) rimossa."
  echo "     ${FLAG_PERSIST:-FLAG{persistenza_rimossa_demo}}"
else
  echo "[--] Il cron malevolo e' ancora li'. Rimuovilo:"
  echo "     sudo rm /etc/cron.d/lab37-backdoor"
fi

# 3) IP attaccante bloccato
if iptables -C INPUT -s 10.10.10.66 -j DROP 2>/dev/null; then
  echo "[OK] IP dell'attaccante bloccato."
  echo "     ${FLAG_RETE:-FLAG{attaccante_bloccato_demo}}"
else
  echo "[--] L'attaccante (10.10.10.66) non e' bloccato. Contienilo:"
  echo "     sudo iptables -A INPUT -s 10.10.10.66 -j DROP"
fi
EOF
chmod 755 /usr/local/bin/lab37-verifica

echo "[OK] Scena pronta: account 'svc-update', cron /etc/cron.d/lab37-backdoor, IP 10.10.10.66."
echo "     Flag (docente):  sudo cat $DIR/flags.env"
