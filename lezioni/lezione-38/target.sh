#!/usr/bin/env bash
# Lezione 38 · lato bersaglio · ripasso. Assicura che le app web siano su per
# rigiocare le sfide del Blocco 4. Idempotente.
set -uo pipefail
echo "== Lezione 38 (bersaglio) · ripasso =="
if command -v systemctl >/dev/null 2>&1; then
  systemctl restart banca.service >/dev/null 2>&1 || true
fi
echo "Se hai gia' fatto 'lab 12', la Banca su :8080 e' di nuovo pronta per il ripasso."
echo "Il grosso del ripasso di oggi si fa sulla Kali (lab 38)."
