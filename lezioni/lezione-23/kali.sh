#!/usr/bin/env bash
# Lezione 23 · lato Kali · TCP/IP e Wireshark. Installa un verificatore. Idempotente.
set -uo pipefail

echo "== Lezione 23 · TCP/IP e Wireshark =="

cat > /usr/local/bin/lab23-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
if [ "$(echo "${1:-}" | tr 'A-Z' 'a-z')" = "autunno2021" ]; then
  echo "[OK] Esatto: hai letto la password in chiaro dal traffico catturato."
  echo "FLAG{credenziali_in_chiaro}"
else
  echo "[--] No. Cattura il beacon e leggi il campo password (poi: lab23-verifica <password>)."
fi
EOF
chmod 755 /usr/local/bin/lab23-verifica

command -v wireshark >/dev/null 2>&1 && echo "[OK] Wireshark presente." || echo "[--] Wireshark mancante."
command -v tcpdump  >/dev/null 2>&1 && echo "[OK] tcpdump presente."  || echo "[--] tcpdump mancante."

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Guardare i pacchetti che viaggiano
------------------------------------------------------------
 Wireshark cattura e mostra ogni pacchetto sulla rete. Il traffico NON
 cifrato si legge in chiaro: e' il cuore di questa lezione.

 Trova l'interfaccia interna (di solito eth1):
        ip -br addr

 [ ] 1  Cattura il beacon in chiaro del bersaglio              (+40)
        sudo tcpdump -i any -A udp port 9999
        # (oppure in Wireshark: filtro   udp.port == 9999 )
        # nel testo del pacchetto c'e' una flag

 [ ] 2  Leggi la password che viaggia in chiaro                (+30)
        # nello stesso pacchetto c'e' password=...
        lab23-verifica <la-password-che-hai-letto>

 Extra (handshake): cattura una connessione al sito e osserva SYN, SYN-ACK, ACK
        sudo tcpdump -i any -n 'tcp port 8080 and host 10.10.10.20'
        # in un altro terminale:  curl http://10.10.10.20:8080
        # in Wireshark: tasto destro > Follow > TCP Stream per leggere lo scambio

 Concetti:  pacchetto  TCP/IP  filtri  three-way handshake  follow stream
------------------------------------------------------------
MSG
