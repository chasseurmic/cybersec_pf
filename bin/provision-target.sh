#!/usr/bin/env bash
#
# provision-target.sh
# Prepara la VM bersaglio (Ubuntu Server, senza grafica) con le app web
# vulnerabili in Docker. Da eseguire con internet attivo, poi esportare in OVA.
#
# Uso (dentro la VM Ubuntu):
#   sudo ./provision-target.sh
#
set -euo pipefail

LAB_IP="10.10.10.20"       # IP del target sulla rete interna
IFACE="enp0s8"             # secondo adattatore = rete interna (verifica con: ip a)

if [ "$(id -u)" -ne 0 ]; then echo "Esegui con sudo."; exit 1; fi
echo "[*] Provisioning target - Ubuntu + Docker"

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

# 3) Pagina segnaposto "Banca della Scuola" con la flag della Lezione 1 (porta 8080)
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