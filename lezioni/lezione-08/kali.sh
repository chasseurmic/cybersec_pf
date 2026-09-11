#!/usr/bin/env bash
# Lezione 08 · lato Kali · scoperta host e rete locale (ping sweep, ARP, nmap).
# Installa un verificatore che non richiede root (usa ping + ip neigh) e mostra
# la missione. Idempotente. Lanciato con sudo dal launcher 'lab'.
set -uo pipefail

TARGET_IP="10.10.10.20"

echo "== Lezione 08 · Scoperta host e rete locale =="

# Verificatore (eseguibile dallo studente senza sudo)
cat > /usr/local/bin/lab08-verifica <<'EOF'
#!/usr/bin/env bash
# Uso:
#   lab08-verifica scoperta          -> il bersaglio e' vivo?
#   lab08-verifica mac <MAC>         -> il MAC del bersaglio e' corretto?
#   lab08-verifica conta <N>         -> quanti host vivi ci sono sulla /24?
set -uo pipefail
PREFISSO="10.10.10"; TARGET="$PREFISSO.20"
cmd="${1:-}"
case "$cmd" in
  scoperta)
    if ping -c1 -W1 "$TARGET" >/dev/null 2>&1; then
      echo "[OK] Il bersaglio $TARGET risponde: e' stato scoperto."
      echo "FLAG{host_vivo_trovato}"
    else
      echo "[--] Non raggiungo $TARGET. E' acceso? Hai fatto la scansione?"
    fi
    ;;
  mac)
    dato="${2:-}"
    [ -z "$dato" ] && { echo "Uso: lab08-verifica mac <MAC>"; exit 1; }
    ping -c1 -W1 "$TARGET" >/dev/null 2>&1 || true
    vero="$(ip neigh show "$TARGET" 2>/dev/null | grep -oE '([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}' | head -n1)"
    [ -z "$vero" ] && { echo "[--] MAC non ancora nella cache ARP. Prova prima:  ping -c1 $TARGET"; exit 1; }
    if [ "$(echo "$dato" | tr 'A-Z' 'a-z')" = "$(echo "$vero" | tr 'A-Z' 'a-z')" ]; then
      echo "[OK] MAC corretto: $vero"
      echo "FLAG{arp_rivela_il_mac}"
    else
      echo "[--] Non coincide. Trova il MAC con:  ip neigh show $TARGET"
    fi
    ;;
  conta)
    n="${2:-}"
    [ -z "$n" ] && { echo "Uso: lab08-verifica conta <numero>"; exit 1; }
    tmp="$(mktemp)"
    for i in $(seq 1 254); do ( ping -c1 -W1 "$PREFISSO.$i" >/dev/null 2>&1 && echo x >> "$tmp" ) & done
    wait
    veri="$(wc -l < "$tmp" | tr -d ' ')"; rm -f "$tmp"
    if [ "$n" = "$veri" ]; then
      echo "[OK] Esatto: $veri host vivi sulla rete del laboratorio."
      echo "FLAG{quanti_siamo_in_rete}"
    else
      echo "[--] Non ci siamo: riconta con la scansione (ne trovi $veri)."
    fi
    ;;
  *)
    echo "Uso: lab08-verifica {scoperta | mac <MAC> | conta <N>}"
    ;;
esac
EOF
chmod 755 /usr/local/bin/lab08-verifica

echo
if command -v nmap >/dev/null 2>&1; then
  echo "[OK] nmap presente."
else
  echo "[--] nmap non trovato (dovrebbe esserci dalla Lezione 2)."
fi

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Chi c'e' nella rete del laboratorio?
------------------------------------------------------------
 La rete interna e' 10.10.10.0/24. Scopri chi e' vivo.

 [ ] 1  Scoperta host con nmap (ping scan)                     (+20)
        sudo nmap -sn 10.10.10.0/24
        lab08-verifica scoperta

 [ ] 2  Il MAC del bersaglio (ARP)                             (+30)
        ping -c1 10.10.10.20
        ip neigh show 10.10.10.20          # IP -> MAC (ARP)
        lab08-verifica mac <il-MAC-che-hai-letto>

 [ ] 3  Quanti host vivi ci sono?                              (+20)
        sudo nmap -sn 10.10.10.0/24 | grep -c 'Nmap scan report'
        lab08-verifica conta <numero>

 Confronto: com'e' andato il tuo scanner bash della Lezione 6?
 Attrezzi:  nmap -sn   ping   ip neigh   arp   grep -c
------------------------------------------------------------
MSG
