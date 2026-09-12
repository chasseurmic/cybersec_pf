#!/usr/bin/env bash
# Lezione 27 · lato Kali · difese di rete. Sola lettura + scansione per l'IDS.
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 27 · Difese di rete (firewall, IDS) =="
echo
ping -c1 -W2 "$TARGET_IP" >/dev/null 2>&1 && echo "[OK] Bersaglio raggiungibile." \
  || echo "[--] Bersaglio non raggiungibile: sul bersaglio lancia  lab 27 ."
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Vestire i panni del difensore (blue team)
------------------------------------------------------------
 Oggi difendi il bersaglio: chiudi cio' che e' esposto e accorgiti di chi
 ti scansiona. Lavori SUL BERSAGLIO via SSH:  ssh studente@10.10.10.20
 (per iptables serve sudo/root: usa l'utente amministratore del bersaglio)

 [ ] 1  Chiudi la porta insicura 9099 col firewall             (+40)
        # sul bersaglio, come root:
        sudo iptables -A INPUT -p tcp --dport 9099 -j DROP
        sudo lab27-verifica firewall
        # dalla Kali verifica che ora sia filtrata:
        nmap -p 9099 10.10.10.20        # prima: open ; dopo: filtered

 [ ] 2  Fai scattare l'IDS a porte esca                        (+30)
        # dalla KALI, scansiona il bersaglio (connect scan):
        nmap -sT -p 1-45000 10.10.10.20
        # sul BERSAGLIO leggi l'allarme con la flag:
        cat /opt/lab/lab27/allarmi.log

 Concetti:  firewall (iptables)  regole di DROP  porte esca  IDS  segmentazione
------------------------------------------------------------
MSG
