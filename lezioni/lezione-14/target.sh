#!/usr/bin/env bash
# Lezione 14 · lato bersaglio · XSS riflesso e memorizzato sulla Banca.
# Riusa la Banca (Lezione 12), azzera la bacheca per una partenza pulita.
# Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 14"; exit 1
fi
APPDIR=/opt/lab/banca-app
if [ ! -f "$APPDIR/banca.py" ]; then
  echo "[!] La Banca non e' installata. Esegui prima:  lab 12"; exit 1
fi
echo "== Lezione 14 (bersaglio) · XSS riflesso e memorizzato =="

systemctl restart banca.service >/dev/null 2>&1 || true
sleep 1

python3 - "$APPDIR/banca.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
try:
    c.execute("DELETE FROM messaggi")
    c.execute("INSERT INTO messaggi(autore,testo) VALUES('staff','Benvenuti nella bacheca della Banca!')")
    c.commit()
except Exception as e:
    print("nota:", e)
c.close()
PY

if curl -s "http://localhost:8080/bacheca" >/dev/null 2>&1; then
  echo "[OK] Banca attiva; bacheca ripulita e pronta su :8080."
  echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
else
  echo "[!] La Banca non risponde. Controlla:  systemctl status banca"
fi
