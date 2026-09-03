#!/usr/bin/env bash
# Lezione 02 · lato Kali · "La rete e' viva".
# Diagnostica di sola lettura: verifica che la Kali veda il bersaglio e le
# app web. Non modifica il sistema. Idempotente.
set -uo pipefail

TARGET_IP="10.10.10.20"   # il bersaglio
MIO_IP="10.10.10.5"       # IP atteso della Kali sulla rete interna

ok=0; ko=0
check() {  # $1 = descrizione ; $2 = esito (0 = passato)
  if [ "$2" -eq 0 ]; then
    printf '  [OK]  %s\n' "$1"; ok=$((ok+1))
  else
    printf '  [--]  %s\n' "$1"; ko=$((ko+1))
  fi
}

echo "== Lezione 02 · diagnostica lato Kali =="
echo

# 1) La Kali ha l'IP giusto sulla rete interna?
ip -4 addr show | grep -q " ${MIO_IP}/"
check "La Kali ha l'IP interno ${MIO_IP}" $?

# 2) Il bersaglio risponde al ping?
ping -c 1 -W 2 "$TARGET_IP" >/dev/null 2>&1
check "Il bersaglio ${TARGET_IP} risponde al ping" $?

# 3) Le tre app web rispondono?
for voce in 8080:Banca 8081:DVWA 8082:JuiceShop; do
  porta="${voce%%:*}"; nome="${voce##*:}"
  curl -s -o /dev/null -m 4 "http://${TARGET_IP}:${porta}"
  check "App ${nome} raggiungibile su :${porta}" $?
done

echo
echo "Punteggio connettivita': ${ok} su $((ok+ko))"
echo
if [ "$ko" -eq 0 ]; then
  echo "  La rete e' viva: la Kali parla col bersaglio."
  echo "  Comunica la flag al docente:  FLAG{la_rete_e_viva}"
else
  echo "  Qualcosa non torna. Controlla in questo ordine:"
  echo "   1. La VM bersaglio e' accesa?"
  echo "   2. Su ENTRAMBE le VM la seconda scheda e' 'Rete interna' con nome labnet?"
  echo "   3. Sul bersaglio hai lanciato prima:  lab 2"
fi
