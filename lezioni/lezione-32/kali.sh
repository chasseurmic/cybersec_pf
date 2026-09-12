#!/usr/bin/env bash
# Lezione 32 · lato Kali · analisi statica di base in sandbox.
# Crea un "campione sospetto" INNOCUO (solo dati, non si esegue) da analizzare
# con file, strings, sha256sum, base64. Offline. Idempotente.
set -uo pipefail

UTENTE="${SUDO_USER:-$USER}"
HOME_UTENTE="$(getent passwd "$UTENTE" | cut -d: -f6)"
[ -z "$HOME_UTENTE" ] && HOME_UTENTE="/home/$UTENTE"
DIR="$HOME_UTENTE/lab/lezione-32"

echo "== Lezione 32 · Analisi statica in sandbox =="
mkdir -p "$DIR"

# Campione INNOCUO: e' solo un file di dati con dentro stringhe "sospette".
# NON e' un eseguibile e non fa nulla. Serve solo per esercitare l'analisi.
B64="$(printf 'esegui il payload alle 03:00 e cifra i file  FLAG{comando_nascosto}' | base64 | tr -d '\n')"
{
  printf 'DROPPER-SIM v2  (campione didattico, INNOCUO)\n'
  printf 'SEGRETO=FLAG{stringhe_rivelatrici}\n'
  printf 'C2=http://10.66.66.66/gate.php\n'
  printf 'mutex=Global\\_BancaLock\n'
  printf 'cfg_base64=%s\n' "$B64"
  # un po' di byte "binari" per rendere il file non tutto testo
  printf '\x7fELF\x01\x01\x01\x00 finto header, non eseguibile \x00\x00\x00'
} > "$DIR/campione.bin"
chown -R "$UTENTE:$UTENTE" "$HOME_UTENTE/lab" 2>/dev/null || true

cat > /usr/local/bin/lab32-verifica <<'EOF'
#!/usr/bin/env bash
set -uo pipefail
F="$HOME/lab/lezione-32/campione.bin"
case "${1:-}" in
  hash)
    [ -f "$F" ] || { echo "Manca $F. Rilancia: lab 32"; exit 1; }
    vero="$(sha256sum "$F" | awk '{print $1}')"
    if [ "$(echo "${2:-}" | tr 'A-Z' 'a-z')" = "$vero" ]; then
      echo "[OK] Impronta (IOC) corretta: e' l'identikit del file."
      echo "FLAG{impronta_del_file}"
    else
      echo "[--] No. Calcola:  sha256sum $F"
    fi ;;
  *)
    echo "Uso: lab32-verifica hash <sha256-del-campione>" ;;
esac
EOF
chmod 755 /usr/local/bin/lab32-verifica

cat <<'MSG'

------------------------------------------------------------
 MISSIONE · Studiare un file senza eseguirlo (analisi statica)
------------------------------------------------------------
 L'analisi statica guarda DENTRO un file sospetto senza avviarlo: e' il modo
 sicuro di capire cosa fa. Il campione di oggi e' innocuo (solo dati).

 Cartella:  ~/lab/lezione-32

 [ ] 1  Che tipo di file e'? Cerca le stringhe sospette        (+30)
        file campione.bin
        strings campione.bin
        strings campione.bin | grep FLAG        # una flag e' in chiaro

 [ ] 2  Calcola l'impronta del file (IOC)                      (+25)
        sha256sum campione.bin
        lab32-verifica hash <sha256>

 [ ] 3  Decodifica la configurazione nascosta (base64)         (+25)
        strings campione.bin | grep cfg_base64
        echo "<la-stringa-base64>" | base64 -d
        # dentro c'e' un'altra flag

 Concetti:  file  strings  sha256 (IOC)  base64  C2  mutex
------------------------------------------------------------
MSG
