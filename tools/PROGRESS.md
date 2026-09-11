# Avanzamento sviluppo lezioni (cybersec_pf)

Legenda stato: `da fare` · `script` (kali.sh/target.sh pronti, `bash -n` ok) ·
`dispensa` · `manuale` · `verificata` (tutti e tre i deliverable pronti e
controllati, PROGRESS aggiornato, commit fatto).

Generatore Word: `tools/docxgen.py` (solo stdlib Python). Sorgenti dei documenti
in `tools/lezioni_src/lezNN.py`. Build con `python3 tools/build_lezioni.py`
(rende Dispensa e Manuale in `lezioni/Lezioni/`, che e' in .gitignore).

| N | Titolo | Blocco | Script | Dispensa | Manuale | Stato |
|---|---|---|---|---|---|---|
| 01 | Triade CIA e primo accesso | B1 | ok | ok | (in dispensa) | verificata (preesistente) |
| 02 | Allestimento del laboratorio | B1 | ok | ok | (in dispensa) | verificata (preesistente) |
| 03 | Filesystem e permessi | B2 | ok | ok | (in dispensa) | verificata (preesistente) |
| 04 | Navigazione avanzata, redirezioni e pipe | B2 | ok | ok | ok | verificata |
| 05 | Utenti, gruppi, processi e servizi | B2 | ok | ok | ok | verificata |
| 06 | Bash scripting offensivo (host scanner) | B2 | ok | ok | ok | verificata |
| 07 | Footprinting e OSINT (simulati) | B3 | ok | ok | ok | verificata |
| 08 | Scoperta host e rete locale | B3 | ok | ok | ok | verificata |
| 09 | Port scanning con nmap e Python | B3 | ok | ok | ok | verificata |
| 10 | Enumerazione servizi e banner grabbing | B3 | ok | ok | ok | verificata |
| 11 | Come funziona il web (HTTP, curl) | B4 | - | - | - | da fare |
| 12 | Banca della Scuola e SQL injection base | B4 | - | - | - | da fare |
| 13 | SQL injection avanzata e sqlmap | B4 | - | - | - | da fare |
| 14 | XSS reflected e stored | B4 | - | - | - | da fare |
| 15 | Autenticazione, cookie e sessioni | B4 | - | - | - | da fare |
| 16 | Brute force del login e difesa | B4 | - | - | - | da fare |
| 17 | File upload, path traversal e LFI | B4 | - | - | - | da fare |
| 18 | OWASP Top 10 e mini CTF web | B4 | - | - | - | da fare |
| 19 | Password: hash e salt | B5 | - | - | - | da fare |
| 20 | Cracking a dizionario, john e hashcat | B5 | - | - | - | da fare |
| 21 | Cifratura simmetrica e asimmetrica | B5 | - | - | - | da fare |
| 22 | HTTPS e TLS, certificati | B5 | - | - | - | da fare |
| 23 | TCP/IP e Wireshark | B6 | - | - | - | da fare |
| 24 | Sniffing di credenziali con scapy | B6 | - | - | - | da fare |
| 25 | ARP spoofing e MITM con scapy | B6 | - | - | - | da fare |
| 26 | DNS spoofing in rete locale | B6 | - | - | - | da fare |
| 27 | Difese di rete (firewall, IDS) | B6 | - | - | - | da fare |
| 28 | Social engineering, principi e casi | B7 | - | - | - | da fare |
| 29 | Pagina di phishing didattica | B7 | - | - | - | da fare |
| 30 | Riconoscere e difendersi dal phishing | B7 | - | - | - | da fare |
| 31 | Malware: tipi e ciclo di vita | B8 | - | - | - | da fare |
| 32 | Analisi statica di base in sandbox | B8 | - | - | - | da fare |
| 33 | Ransomware didattico in sandbox | B8 | - | - | - | da fare |
| 34 | Analisi dinamica e IOC | B8 | - | - | - | da fare |
| 35 | Hardening di sistema | B9 | - | - | - | da fare |
| 36 | Log, monitoraggio e rilevamento | B9 | - | - | - | da fare |
| 37 | Incident response di base | B9 | - | - | - | da fare |
| 38 | Preparazione e ripasso CTF | B10 | - | - | - | da fare |
| 39 | CTF finale a squadre | B10 | - | - | - | da fare |
| 40 | Debrief e valutazione | B10 | - | - | - | da fare |

## Note di avanzamento
- (2026-09-12) Creato il generatore Word condiviso `tools/docxgen.py` e
  l'orchestratore `tools/build_lezioni.py`. Stile allineato a L2/L3
  (intestazione, riquadri con accento, codice su sfondo scuro, tabelle a righe
  alternate; H1 blu, H2 verde, H3 blu).
