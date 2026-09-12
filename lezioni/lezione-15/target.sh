#!/usr/bin/env bash
# Lezione 15 · lato bersaglio · autenticazione, cookie e sessioni.
# Riusa la Banca (Lezione 12). Mette una flag nella nota dell'admin, cosi'
# forgiando il cookie di sessione la si legge dalla dashboard. Idempotente.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 15"; exit 1
fi
APPDIR=/opt/lab/banca-app
if [ ! -f "$APPDIR/banca.py" ]; then
  echo "[!] La Banca non e' installata. Esegui prima:  lab 12"; exit 1
fi
echo "== Lezione 15 (bersaglio) · cookie e sessioni =="

systemctl restart banca.service >/dev/null 2>&1 || true
sleep 1

if ! grep -q '^FLAG_SESSIONE=' "$APPDIR/flags.env" 2>/dev/null; then
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  echo "FLAG_SESSIONE=FLAG{sessione_rubata_$(r)}" >> "$APPDIR/flags.env"
fi
FLAG_SESSIONE="$(grep '^FLAG_SESSIONE=' "$APPDIR/flags.env" | cut -d= -f2-)"

python3 - "$APPDIR/banca.db" "$FLAG_SESSIONE" <<'PY'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
c.execute("UPDATE utenti SET nota=? WHERE username='admin'",
          ("Conto amministratore riservato. " + sys.argv[2],))
c.commit(); c.close()
print("nota admin aggiornata con la flag di sessione")
PY

if curl -s -o /dev/null "http://localhost:8080/"; then
  echo "[OK] Banca attiva su :8080. Login regolare di prova:  cliente / cliente"
  echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
else
  echo "[!] La Banca non risponde. Controlla:  systemctl status banca"
fi
