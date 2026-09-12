#!/usr/bin/env bash
# Lezione 13 · lato bersaglio · SQL injection avanzata e sqlmap.
# Riusa la Banca della Scuola (Lezione 12) e aggiunge una tabella "carte" con una
# flag, che sqlmap scoprira' e scarichera' da solo. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 13"; exit 1
fi
APPDIR=/opt/lab/banca-app
if [ ! -f "$APPDIR/banca.py" ]; then
  echo "[!] La Banca non e' installata. Esegui prima:  lab 12"; exit 1
fi
echo "== Lezione 13 (bersaglio) · SQLi avanzata: tabella carte per sqlmap =="

# Assicura il servizio attivo
systemctl restart banca.service >/dev/null 2>&1 || true

# Aggiungi FLAG_SQLMAP alle flag se manca
if ! grep -q '^FLAG_SQLMAP=' "$APPDIR/flags.env" 2>/dev/null; then
  r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  echo "FLAG_SQLMAP=FLAG{sqlmap_ha_svuotato_il_db_$(r)}" >> "$APPDIR/flags.env"
fi
FLAG_SQLMAP="$(grep '^FLAG_SQLMAP=' "$APPDIR/flags.env" | cut -d= -f2-)"

# Crea/riempi la tabella carte (bersaglio ghiotto per sqlmap)
python3 - "$APPDIR/banca.db" "$FLAG_SQLMAP" <<'PY'
import sqlite3, sys
db, flag = sys.argv[1], sys.argv[2]
c = sqlite3.connect(db)
c.execute("CREATE TABLE IF NOT EXISTS carte(id INTEGER PRIMARY KEY, titolare TEXT, numero TEXT, cvv TEXT)")
c.execute("DELETE FROM carte")
c.executemany("INSERT INTO carte(titolare,numero,cvv) VALUES(?,?,?)", [
    ("Anna Rossi", "4111 1111 1111 1111", "123"),
    ("Luca Bianchi", "4222 2222 2222 2222", "456"),
    ("Tesoreria", "0000 0000 0000 0000", flag),
])
c.commit(); c.close()
print("tabella carte creata")
PY

sleep 1
if curl -s "http://localhost:8080/cerca?conto=x" >/dev/null 2>&1; then
  echo "[OK] Banca attiva su :8080; tabella 'carte' pronta per sqlmap."
  echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
else
  echo "[!] La Banca non risponde. Controlla:  systemctl status banca"
fi
