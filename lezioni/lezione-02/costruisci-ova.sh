#!/usr/bin/env bash
# costruisci-ova.sh
# Esporta le DUE VM del laboratorio (Kali + bersaglio) in un UNICO file OVA.
# Versione per host Linux con VirtualBox (su Windows usa costruisci-ova.ps1).
# Uso:
#   ./costruisci-ova.sh [nome-kali] [nome-target] [output.ova]
# Default: kali-studente  target-ubuntu  ./corso-cyber-lab.ova
set -euo pipefail

KALI="${1:-kali-studente}"
TARGET="${2:-target-ubuntu}"
OUT="${3:-./corso-cyber-lab.ova}"

command -v VBoxManage >/dev/null 2>&1 || {
  echo "[!] VBoxManage non trovato. Installa VirtualBox."; exit 1;
}

stato() { VBoxManage showvminfo "$1" --machinereadable 2>/dev/null \
          | sed -n 's/^VMState="\(.*\)"/\1/p'; }

# Controlli preliminari: le VM esistono e sono spente
for vm in "$KALI" "$TARGET"; do
  st="$(stato "$vm")"
  [ -n "$st" ] || { echo "[!] La VM '$vm' non esiste. Elenca con: VBoxManage list vms"; exit 1; }
  case "$st" in
    poweroff|saved|aborted) echo "[OK] VM '$vm' presente e spenta (stato: $st)." ;;
    *) echo "[!] La VM '$vm' non e' spenta (stato: $st). Spegnila prima di esportare."; exit 1 ;;
  esac
done

# Sovrascrivi un eventuale OVA precedente
[ -f "$OUT" ] && { echo "[i] Esiste gia' $OUT : lo sovrascrivo."; rm -f "$OUT"; }

echo "[*] Esporto '$KALI' e '$TARGET' in un unico file: $OUT"
echo "    (l'operazione puo' richiedere diversi minuti)"
VBoxManage export "$KALI" "$TARGET" --output "$OUT" --ovf20 --manifest

if [ -f "$OUT" ]; then
  sz="$(du -h "$OUT" | cut -f1)"
  echo
  echo "[OK] Creato l'OVA: $OUT  ($sz)."
  echo "    Copialo sulle postazioni e importalo con:"
  echo "    VirtualBox > File > Importa applicazione virtuale."
else
  echo "[!] Il file OVA non risulta creato."; exit 1
fi
