#!/usr/bin/env bash
# Lezione 02 · lato bersaglio (target) · avvio e verifica dei servizi.
# Accende le app web vulnerabili e mostra lo stato. Idempotente: si puo'
# eseguire piu' volte senza danni. Va lanciato sul BERSAGLIO, che ha Docker.
set -uo pipefail

LAB_IP="10.10.10.20"   # IP del bersaglio sulla rete interna del laboratorio

if ! command -v docker >/dev/null 2>&1; then
  echo "[!] Docker non e' presente qui."
  echo "    Questo script va eseguito sul BERSAGLIO, non sulla Kali."
  exit 1
fi

echo "== Lezione 02 · bersaglio · avvio dei servizi =="

# 1) (Ri)avvia i container professionali definiti nell'immagine base
if [ -f /opt/lab/docker-compose.yml ]; then
  docker compose -f /opt/lab/docker-compose.yml up -d 2>/dev/null || true
fi

# 2) (Ri)avvia la "Banca della Scuola" (pagina statica su nginx)
if ! docker ps --format '{{.Names}}' | grep -q '^banca$'; then
  if [ -d /opt/lab/banca ] && docker image inspect nginx:alpine >/dev/null 2>&1; then
    docker run -d --name banca --restart unless-stopped -p 8080:80 \
      -v /opt/lab/banca:/usr/share/nginx/html:ro nginx:alpine >/dev/null 2>&1 || true
  fi
fi

# 3) Stato dei servizi
sleep 2
echo
printf '%-12s %-30s %s\n' "SERVIZIO" "INDIRIZZO (dalla Kali)" "STATO"
printf '%-12s %-30s %s\n' "--------" "----------------------" "-----"
tutti_ok=1
for voce in 8080:Banca 8081:DVWA 8082:JuiceShop; do
  porta="${voce%%:*}"; nome="${voce##*:}"
  if curl -s -o /dev/null -m 4 "http://localhost:$porta"; then
    stato="attivo"
  else
    stato="NON attivo"; tutti_ok=0
  fi
  printf '%-12s %-30s %s\n' "$nome" "http://$LAB_IP:$porta" "$stato"
done

echo
if [ "$tutti_ok" -eq 1 ]; then
  echo "[OK] Bersaglio pronto: le tre app rispondono."
  echo "     Flag lato bersaglio: FLAG{bersaglio_online}"
else
  echo "[!] Non tutti i servizi sono attivi."
  echo "    Diagnostica:  docker ps    e    docker logs <nome-container>"
  echo "    Su ARM (Mac/Parallels) DVWA non parte: e' atteso, l'aula e' x86."
fi
