#!/usr/bin/env bash
# Lezione 10 · lato bersaglio · servizi con banner "parlanti" da enumerare.
# Avvia due servizi finti (stile FTP e SMTP) che annunciano nome e versione nel
# banner iniziale, materiale per il banner grabbing. Idempotente. Sul BERSAGLIO.
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "[!] Va eseguito come root. Sul bersaglio lancia:  lab 10"
  exit 1
fi
echo "== Lezione 10 (bersaglio) · servizi con banner da enumerare =="

# Piccolo server di banner: invia una riga di saluto e chiude
cat > /usr/local/bin/lab10-banner <<'PY'
#!/usr/bin/env python3
import socket, sys
port = int(sys.argv[1]); banner = (sys.argv[2] + "\r\n").encode()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", port)); s.listen(8)
while True:
    try:
        c, _ = s.accept()
        c.sendall(banner)
        c.settimeout(2)
        try:
            c.recv(256)
        except Exception:
            pass
        c.close()
    except Exception:
        pass
PY
chmod 755 /usr/local/bin/lab10-banner

# Servizio 1 · stile FTP (porta 2121)
cat > /etc/systemd/system/lab10-ftp.service <<'EOF'
[Unit]
Description=Lab10 finto FTP con banner
[Service]
ExecStart=/usr/local/bin/lab10-banner 2121 "220 BancaScuola FTP Server pronto FLAG{banner_svela_il_servizio}"
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# Servizio 2 · stile SMTP (porta 2525) con versione esposta
cat > /etc/systemd/system/lab10-smtp.service <<'EOF'
[Unit]
Description=Lab10 finto SMTP con banner e versione
[Service]
ExecStart=/usr/local/bin/lab10-banner 2525 "220 mail.bancadellascuola.local ESMTP Postfix 2.4.1 FLAG{versione_esposta}"
Restart=always
[Install]
WantedBy=multi-user.target
EOF

# Assicura SSH (banner di OpenSSH: un altro servizio da identificare)
export DEBIAN_FRONTEND=noninteractive
if [ ! -x /usr/sbin/sshd ]; then apt-get update && apt-get -y install openssh-server; fi
systemctl enable --now ssh >/dev/null 2>&1 || systemctl enable --now sshd >/dev/null 2>&1 || true

systemctl daemon-reload
for u in lab10-ftp lab10-smtp; do
  systemctl enable --now "$u.service" >/dev/null 2>&1 || true
  systemctl restart "$u.service" >/dev/null 2>&1 || true
done

sleep 1
echo
ok=1
for p in 2121 2525; do
  if (exec 3<>/dev/tcp/127.0.0.1/$p) 2>/dev/null; then echo "[OK] banner attivo su :$p"; else echo "[!] :$p non risponde"; ok=0; fi
done
[ "$ok" -eq 1 ] && echo "Servizi pronti." || echo "Controlla: systemctl status lab10-ftp lab10-smtp"
echo "     Dalla Kali:  nc 10.10.10.20 2121   e   nmap -sV -p 2121,2525 10.10.10.20"
