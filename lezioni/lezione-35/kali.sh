#!/usr/bin/env bash
# Lezione 35 · lato Kali · hardening di sistema. Briefing (si lavora sul bersaglio).
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 35 · Hardening di sistema =="
echo
ping -c1 -W2 "$TARGET_IP" >/dev/null 2>&1 && echo "[OK] Bersaglio raggiungibile." \
  || echo "[--] Bersaglio non raggiungibile: sul bersaglio lancia  lab 35 ."
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Blindare il sistema (blue team)
------------------------------------------------------------
 Oggi difendi il bersaglio: riduci la superficie d'attacco. Lavori SUL
 bersaglio come amministratore (root/sudo):  ssh <admin>@10.10.10.20

 [ ] 1  Spegni il servizio inutile su :9111                    (+25)
        sudo systemctl disable --now lab35-inutile

 [ ] 2  Blinda SSH: niente login diretto di root               (+25)
        echo 'PermitRootLogin no' | sudo tee /etc/ssh/sshd_config.d/hardening.conf
        sudo systemctl restart ssh    # (o sshd)

 [ ] 3  Chiudi il file segreto leggibile da tutti              (+20)
        ls -l /opt/lab/lab35/segreti.txt      # ora e' 666 (male)
        sudo chmod 600 /opt/lab/lab35/segreti.txt

 Poi verifica tutto in una volta:
        sudo lab35-verifica

 Concetti:  superficie d'attacco  servizi minimi  SSH sicuro  minimo privilegio
------------------------------------------------------------
MSG
