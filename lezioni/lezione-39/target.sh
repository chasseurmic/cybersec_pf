#!/usr/bin/env bash
# Lezione 39 · lato bersaglio · CTF finale a squadre. Semina 6 sfide con flag
# generate a runtime (segrete, nel repo NON compaiono i valori). Installa il
# verificatore per il docente. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 39"; exit 1
fi
echo "== Lezione 39 (bersaglio) · CTF finale: semina delle sfide =="

CTF=/opt/lab/ctf
mkdir -p "$CTF"
if [ ! -f "$CTF/flags.env" ]; then
  r() { head -c 4 /dev/urandom | od -An -tx1 | tr -d ' \n'; }
  cat > "$CTF/flags.env" <<EOF
FLAG_RECON=FLAG{recon_$(r)}
FLAG_FIND=FLAG{scava_a_fondo_$(r)}
FLAG_PERM=FLAG{permesso_di_troppo_$(r)}
FLAG_WEB_SQLI=FLAG{sqli_finale_$(r)}
FLAG_WEB_LFI=FLAG{lfi_finale_$(r)}
FLAG_B64=FLAG{decodificato_$(r)}
EOF
  chmod 600 "$CTF/flags.env"
fi
. "$CTF/flags.env"

# 0) Utente ospite per l'accesso SSH
if ! id studente >/dev/null 2>&1; then useradd -m -s /bin/bash studente; fi
echo 'studente:studente' | chpasswd
export DEBIAN_FRONTEND=noninteractive
[ -x /usr/sbin/sshd ] || { apt-get update && apt-get -y install openssh-server; }
mkdir -p /etc/ssh/sshd_config.d
printf 'PasswordAuthentication yes\n' > /etc/ssh/sshd_config.d/99-lab.conf
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true
systemctl restart ssh >/dev/null 2>&1 || systemctl restart sshd >/dev/null 2>&1 || true

# 1) SFIDA RECON: servizio nascosto su :13337
mkdir -p "$CTF/recon"
printf '<h1>Servizio nascosto</h1><p>%s</p>\n' "$FLAG_RECON" > "$CTF/recon/index.html"
cat > /etc/systemd/system/ctf-recon.service <<'EOF'
[Unit]
Description=CTF servizio nascosto (:13337)
[Service]
ExecStart=/usr/bin/python3 -m http.server 13337 --directory /opt/lab/ctf/recon --bind 0.0.0.0
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# 2) SFIDA FIND: flag sepolta in profondita' in /srv/ctf
BASE=/srv/ctf
rm -rf "$BASE"; mkdir -p "$BASE/archivio/2019/vecchio"
printf 'file dimenticato\n%s\n' "$FLAG_FIND" > "$BASE/archivio/2019/vecchio/note.old"

# 3) SFIDA PERMESSI: segreto di root ma leggibile da tutti
printf 'backup credenziali (non doveva essere leggibile!)\n%s\n' "$FLAG_PERM" > "$BASE/backup_root.txt"
chown root:root "$BASE/backup_root.txt"; chmod 644 "$BASE/backup_root.txt"

# 6) SFIDA BASE64: messaggio offuscato
printf '%s' "$FLAG_B64" | base64 > "$BASE/messaggio.b64"

chmod -R a+rX "$BASE"
chown -R root:root "$BASE"; chmod 644 "$BASE/archivio/2019/vecchio/note.old" "$BASE/messaggio.b64"

# 4-5) SFIDE WEB: richiedono la Banca (Lezione 12)
if [ -f /opt/lab/banca-app/banca.py ]; then
  systemctl restart banca.service >/dev/null 2>&1 || true
  # SQLi: nuova riga nei segreti
  python3 - /opt/lab/banca-app/banca.db "$FLAG_WEB_SQLI" <<'PY'
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
c.execute("CREATE TABLE IF NOT EXISTS segreti(id INTEGER PRIMARY KEY, chiave TEXT, valore TEXT)")
c.execute("DELETE FROM segreti WHERE chiave='ctf'")
c.execute("INSERT INTO segreti(chiave,valore) VALUES('ctf', ?)", (sys.argv[2],))
c.commit(); c.close()
PY
  # LFI: file raggiungibile con path traversal
  mkdir -p /opt/lab/banca-app/segreti
  printf 'CTF finale - file riservato\n%s\n' "$FLAG_WEB_LFI" > /opt/lab/banca-app/segreti/ctf_lfi.txt
  WEB="pronte"
else
  WEB="NON pronte (esegui prima: lab 12)"
fi

systemctl daemon-reload
systemctl enable --now ctf-recon.service >/dev/null 2>&1 || true
systemctl restart ctf-recon.service >/dev/null 2>&1 || true

# Verificatore per il docente
cat > /usr/local/bin/ctf-verifica <<'EOF'
#!/usr/bin/env bash
# Uso (docente):  sudo ctf-verifica <flag>
set -uo pipefail
[ "$(id -u)" -eq 0 ] || { echo "Esegui con sudo."; exit 1; }
f="${1:-}"; [ -z "$f" ] && { echo "Uso: sudo ctf-verifica FLAG{...}"; exit 1; }
. /opt/lab/ctf/flags.env 2>/dev/null || true
nome=""; punti=0
if   [ "$f" = "${FLAG_RECON:-_}" ];    then nome="RECON";    punti=10
elif [ "$f" = "${FLAG_FIND:-_}" ];     then nome="FIND";     punti=10
elif [ "$f" = "${FLAG_PERM:-_}" ];     then nome="PERMESSI"; punti=10
elif [ "$f" = "${FLAG_WEB_SQLI:-_}" ]; then nome="WEB_SQLI"; punti=20
elif [ "$f" = "${FLAG_WEB_LFI:-_}" ];  then nome="WEB_LFI";  punti=20
elif [ "$f" = "${FLAG_B64:-_}" ];      then nome="BASE64";   punti=10
fi
if [ -n "$nome" ]; then
  echo "[OK] Flag valida: $nome  (+$punti punti)"
else
  echo "[--] Flag non valida."
fi
EOF
chmod 755 /usr/local/bin/ctf-verifica

echo
echo "[OK] CTF pronto. Sfide web: $WEB"
echo "     Servizi: recon :13337 ; /srv/ctf via SSH (studente/studente) ; Banca :8080"
echo "     Flag e punteggi (docente):  sudo cat $CTF/flags.env"
echo "     Verifica una flag:          sudo ctf-verifica FLAG{...}"
