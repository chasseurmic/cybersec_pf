#!/usr/bin/env bash
#
# provision-kali.sh
# Prepara l'immagine Kali per il corso di Sicurezza Informatica.
# Rileva da solo l'interfaccia della rete interna: funziona su
# VirtualBox, Parallels e UTM senza modifiche.
#
# Uso (dentro la VM Kali, con la scheda NAT/Condivisa attiva per internet):
#   sudo ./provision-kali.sh studente
#   sudo ./provision-kali.sh docente
#
set -euo pipefail

RUOLO="${1:-studente}"
LAB_IP="10.10.10.5"        # IP di Kali sulla rete interna
LAB_CON="labnet"           # nome del profilo di rete

if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo."; exit 1; fi

# --- Rilevamento automatico dell'interfaccia interna ---
# La scheda con internet (NAT/Condivisa) ha il gateway di default.
# L'interfaccia interna e' l'altra scheda ethernet (en* o eth*).
DEFAULT_IF="$(ip route show default 2>/dev/null | awk '{print $5; exit}')"
IFACE="$(ip -o link show | awk -F': ' '{print $2}' | sed 's/@.*//' \
         | grep -E '^(en|eth)' | grep -v "^${DEFAULT_IF}$" | head -n1)"
if [ -z "$IFACE" ]; then
  echo "[!] Non ho trovato l'interfaccia interna. Verifica con 'ip a' e impostala a mano."
  exit 1
fi
echo "[*] Provisioning Kali - ruolo: $RUOLO - interfaccia interna: $IFACE"

export DEBIAN_FRONTEND=noninteractive
echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections

# 1) Aggiornamento e strumenti del corso
apt-get update
# apt-get -y full-upgrade
apt-get -y install \
  nmap wireshark tshark bettercap john hashcat hydra \
  gobuster dirb whatweb netcat-traditional curl wget git \
  python3 python3-pip python3-scapy sqlmap cmatrix tmux jq
usermod -aG wireshark kali 2>/dev/null || true

# 2) IP statico sulla rete interna (senza gateway: nessuna uscita a internet)
nmcli connection delete "$LAB_CON" 2>/dev/null || true
nmcli connection add type ethernet ifname "$IFACE" con-name "$LAB_CON" \
  ipv4.method manual ipv4.addresses "${LAB_IP}/24" ipv6.method ignore autoconnect yes
echo "[*] IP interno impostato: ${LAB_IP} su ${IFACE}"

# 3) Flag introduttive della Lezione 1
cat > /home/kali/README-corso.txt <<'EOF'
Benvenuto nel corso di Sicurezza Informatica.
Regola d'oro: si attacca SOLO dentro questo laboratorio isolato.
FLAG{benvenuto_nel_gioco}
EOF
printf 'FLAG{i_file_nascosti_non_bastano}\n' > /home/kali/.segreto
chown kali:kali /home/kali/README-corso.txt /home/kali/.segreto

# 4) Banner di sistema
cat > /etc/motd <<'EOF'
==== LABORATORIO DI SICUREZZA INFORMATICA - AMBIENTE ISOLATO ====
 Uso esclusivamente didattico.
 Attaccare sistemi fuori da questo laboratorio e' un reato (art. 615 ter c.p.).
=================================================================
EOF

# 5) Cartella di lavoro
sudo -u kali mkdir -p /home/kali/lab/{tool,loot,note}

# 6) Extra riservati all'immagine docente
if [ "$RUOLO" = "docente" ]; then
  mkdir -p /root/soluzioni
  echo "Cartella soluzioni del docente." > /root/soluzioni/LEGGIMI.txt
  echo "[*] Extra docente installati in /root/soluzioni"
fi

echo "[OK] Provisioning completato. Spegni, stacca la NAT, esporta in OVA (o clona in Parallels)."