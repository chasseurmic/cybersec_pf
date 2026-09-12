#!/usr/bin/env bash
# Lezione 18 · lato bersaglio · mini CTF web (ripasso OWASP Top 10).
# Prepara una sfida a catena SQLi -> LFI ("svuota il caveau") sulla Banca.
# Idempotente. Sul BERSAGLIO. Prerequisito: Banca (Lezione 12).
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 18"; exit 1
fi
APPDIR=/opt/lab/banca-app
if [ ! -f "$APPDIR/banca.py" ]; then
  echo "[!] La Banca non e' installata. Esegui prima:  lab 12"; exit 1
fi
echo "== Lezione 18 (bersaglio) · mini CTF: svuota il caveau =="

systemctl restart banca.service >/dev/null 2>&1 || true
sleep 1

r() { head -c 3 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
grep -q '^FLAG_CTF1=' "$APPDIR/flags.env" || echo "FLAG_CTF1=FLAG{ho_trovato_il_caveau_$(r)}" >> "$APPDIR/flags.env"
grep -q '^FLAG_CTF2=' "$APPDIR/flags.env" || echo "FLAG_CTF2=FLAG{caveau_svuotato_$(r)}" >> "$APPDIR/flags.env"
# nome del file del caveau (una sola volta, poi stabile)
if ! grep -q '^CTF_VAULT=' "$APPDIR/flags.env"; then
  echo "CTF_VAULT=vault_$(r).txt" >> "$APPDIR/flags.env"
fi
FLAG_CTF1="$(grep '^FLAG_CTF1=' "$APPDIR/flags.env" | cut -d= -f2-)"
FLAG_CTF2="$(grep '^FLAG_CTF2=' "$APPDIR/flags.env" | cut -d= -f2-)"
VAULT="$(grep '^CTF_VAULT=' "$APPDIR/flags.env" | cut -d= -f2-)"

# 1) scrivi il file del caveau (raggiungibile via LFI con ../segreti/<VAULT>)
mkdir -p "$APPDIR/segreti"
printf 'Caveau della Banca della Scuola.\n%s\n' "$FLAG_CTF2" > "$APPDIR/segreti/$VAULT"

# 2) inserisci nel database l'indizio (path del caveau) + FLAG_CTF1
python3 - "$APPDIR/banca.db" "../segreti/$VAULT" "$FLAG_CTF1" <<'PY'
import sqlite3, sys
db, percorso, flag = sys.argv[1], sys.argv[2], sys.argv[3]
c = sqlite3.connect(db)
c.execute("CREATE TABLE IF NOT EXISTS segreti(id INTEGER PRIMARY KEY, chiave TEXT, valore TEXT)")
c.execute("DELETE FROM segreti WHERE chiave='caveau'")
c.execute("INSERT INTO segreti(chiave,valore) VALUES('caveau', ?)",
          ("percorso del caveau: %s  |  %s" % (percorso, flag),))
c.commit(); c.close()
print("indizio caveau inserito nel db")
PY

echo
if curl -s "http://localhost:8080/documenti?file=../segreti/$VAULT" | grep -q FLAG; then
  echo "[OK] Mini CTF pronto: catena SQLi -> LFI attiva sulla Banca (:8080)."
  echo "     Flag (docente):  sudo cat $APPDIR/flags.env"
else
  echo "[!] Qualcosa non torna: controlla  systemctl status banca ."
fi
