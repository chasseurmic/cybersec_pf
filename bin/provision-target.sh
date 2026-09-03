#!/usr/bin/env bash
#
# provision-target.sh
# Prepara la VM bersaglio (Ubuntu Server, senza grafica) con le app web
# vulnerabili in Docker. Da eseguire con internet attivo, poi esportare in OVA.
# Rileva da solo l'interfaccia della rete interna: funziona su VirtualBox,
# Parallels e UTM senza modifiche.
#
# Uso (dentro la VM Ubuntu, con la scheda NAT attiva per internet):
#   sudo ./provision-target.sh
#
set -euo pipefail

LAB_IP="10.10.10.20"       # IP del target sulla rete interna

if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo."; exit 1; fi

# --- Rilevamento automatico dell'interfaccia interna ---
# La scheda con internet (NAT) ha il gateway di default; l'interfaccia
# interna e' l'altra scheda ethernet (en* o eth*).
DEFAULT_IF="$(ip route show default 2>/dev/null | awk '{print $5; exit}')"
IFACE="$(ip -o link show | awk -F': ' '{print $2}' | sed 's/@.*//' \
         | grep -E '^(en|eth)' | grep -v "^${DEFAULT_IF}$" | head -n1)"
if [ -z "$IFACE" ]; then
  echo "[!] Non ho trovato l'interfaccia interna. Verifica con 'ip a' e impostala a mano."
  exit 1
fi
echo "[*] Provisioning target - Ubuntu + Docker - interfaccia interna: $IFACE"

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y install docker.io docker-compose-v2 curl
systemctl enable --now docker

# 1) IP statico sulla rete interna (netplan)
cat > /etc/netplan/60-labnet.yaml <<EOF
network:
  version: 2
  ethernets:
    ${IFACE}:
      dhcp4: no
      addresses: [${LAB_IP}/24]
EOF
chmod 600 /etc/netplan/60-labnet.yaml
netplan apply || true
echo "[*] IP interno impostato: ${LAB_IP} su ${IFACE}"

# 2) App web vulnerabili "professionali" (bersagli del Blocco 4)
mkdir -p /opt/lab
cat > /opt/lab/docker-compose.yml <<'EOF'
services:
  dvwa:
    image: vulnerables/web-dvwa
    ports: ["8081:80"]
    restart: unless-stopped
  juiceshop:
    image: bkimminich/juice-shop
    ports: ["8082:3000"]
    restart: unless-stopped
  # banca-scuola: app Flask custom, la aggiungiamo con la Lezione 12
EOF
docker compose -f /opt/lab/docker-compose.yml pull
docker compose -f /opt/lab/docker-compose.yml up -d

# 3) Immagine nginx in cache: serve alla "Banca della Scuola" quando il
#    bersaglio e' isolato (senza internet non si potrebbe scaricare).
docker pull nginx:alpine

# 4) Pagina segnaposto "Banca della Scuola" con la flag della Lezione 1 (porta 8080)
mkdir -p /opt/lab/banca
cat > /opt/lab/banca/index.html <<'EOF'
<!doctype html>
<html lang="it">
<head><meta charset="utf-8"><title>Banca della Scuola</title></head>
<body>
  <h1>Banca della Scuola</h1>
  <h2>Accesso clienti</h2>
  <form>
    <input placeholder="utente">
    <input type="password" placeholder="password">
    <button>Entra</button>
  </form>
  <!-- FLAG{ho_parlato_col_server} -->
</body>
</html>
EOF
docker rm -f banca 2>/dev/null || true
docker run -d --name banca --restart unless-stopped -p 8080:80 \
  -v /opt/lab/banca:/usr/share/nginx/html:ro nginx:alpine

echo "[OK] Target pronto:"
echo "     Banca della Scuola  http://${LAB_IP}:8080  (flag Lezione 1)"
echo "     DVWA                http://${LAB_IP}:8081"
echo "     Juice Shop          http://${LAB_IP}:8082"
echo "     Ora: spegni la VM ed esporta in OVA."
