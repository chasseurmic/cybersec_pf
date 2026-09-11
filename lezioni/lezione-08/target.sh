#!/usr/bin/env bash
# Lezione 08 · lato bersaglio · scoperta host. Questa lezione si svolge sulla Kali.
# Qui garantiamo solo che il bersaglio sia visibile in rete (ping e ARP).
# Idempotente.
set -uo pipefail

echo "== Lezione 08 (bersaglio) =="
echo "Questa lezione si svolge sulla Kali (scoperta host e ARP)."
echo "Il bersaglio deve solo essere raggiungibile in rete."

# Non blocchiamo ICMP: il ping deve rispondere.
if command -v sysctl >/dev/null 2>&1; then
  sysctl -w net.ipv4.icmp_echo_ignore_all=0 >/dev/null 2>&1 || true
fi

IP="$(hostname -I | awk '{print $1}')"
MAC="$(ip link show | grep -oE '([0-9a-f]{2}:){5}[0-9a-f]{2}' | head -n1)"
echo
echo "[OK] Bersaglio in rete: IP ${IP:-10.10.10.20}  MAC ${MAC:-sconosciuto}"
echo "     Dalla Kali:  sudo nmap -sn 10.10.10.0/24   e   ip neigh show ${IP:-10.10.10.20}"
