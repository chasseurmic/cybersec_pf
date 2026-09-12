#!/usr/bin/env bash
# Lezione 37 · lato Kali · incident response di base. Briefing (si lavora sul bersaglio).
set -uo pipefail
TARGET_IP="10.10.10.20"
echo "== Lezione 37 · Incident response di base =="
echo
ping -c1 -W2 "$TARGET_IP" >/dev/null 2>&1 && echo "[OK] Bersaglio raggiungibile." \
  || echo "[--] Bersaglio non raggiungibile: sul bersaglio lancia  lab 37 ."
cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Gestire una compromissione (blue team)
------------------------------------------------------------
 Il bersaglio e' stato bucato (Lezione 36). Ora rispondi seguendo le fasi
 dell'incident response. Lavori SUL bersaglio come amministratore.

 Le 6 fasi (PICERL):
   Preparazione · Identificazione · Contenimento · Eradicazione ·
   Recupero · Lezioni apprese

 [ ] 1  IDENTIFICA cosa ha lasciato l'attaccante
        cat /etc/passwd | grep -E 'svc|update'      # account sospetto
        ls -la /etc/cron.d/                          # persistenza (cron)
        sudo crontab -l ; cat /etc/cron.d/lab37-backdoor

 [ ] 2  CONTIENI: blocca l'account ostile                       (+25)
        sudo usermod -L svc-update        # (oppure: sudo userdel -r svc-update)

 [ ] 3  ERADICA: rimuovi la persistenza                         (+25)
        sudo rm /etc/cron.d/lab37-backdoor

 [ ] 4  CONTIENI la rete: blocca l'IP dell'attaccante           (+20)
        sudo iptables -A INPUT -s 10.10.10.66 -j DROP

 Poi verifica la tua risposta:
        sudo lab37-verifica

 RECUPERO e LEZIONI APPRESE: nella dispensa (cosa ripristinare e come evitare
 che riaccada).
------------------------------------------------------------
MSG
