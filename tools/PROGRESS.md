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
| 11 | Come funziona il web (HTTP, curl) | B4 | ok | ok | ok | verificata |
| 12 | Banca della Scuola e SQL injection base | B4 | ok | ok | ok | verificata |
| 13 | SQL injection avanzata e sqlmap | B4 | ok | ok | ok | verificata |
| 14 | XSS reflected e stored | B4 | ok | ok | ok | verificata |
| 15 | Autenticazione, cookie e sessioni | B4 | ok | ok | ok | verificata |
| 16 | Brute force del login e difesa | B4 | ok | ok | ok | verificata |
| 17 | File upload, path traversal e LFI | B4 | ok | ok | ok | verificata |
| 18 | OWASP Top 10 e mini CTF web | B4 | ok | ok | ok | verificata |
| 19 | Password: hash e salt | B5 | ok | ok | ok | verificata |
| 20 | Cracking a dizionario, john e hashcat | B5 | ok | ok | ok | verificata |
| 21 | Cifratura simmetrica e asimmetrica | B5 | ok | ok | ok | verificata |
| 22 | HTTPS e TLS, certificati | B5 | ok | ok | ok | verificata |
| 23 | TCP/IP e Wireshark | B6 | ok | ok | ok | verificata |
| 24 | Sniffing di credenziali con scapy | B6 | ok | ok | ok | verificata |
| 25 | ARP spoofing e MITM con scapy | B6 | ok | ok | ok | verificata |
| 26 | DNS spoofing in rete locale | B6 | ok | ok | ok | verificata |
| 27 | Difese di rete (firewall, IDS) | B6 | ok | ok | ok | verificata |
| 28 | Social engineering, principi e casi | B7 | ok | ok | ok | verificata |
| 29 | Pagina di phishing didattica | B7 | ok | ok | ok | verificata |
| 30 | Riconoscere e difendersi dal phishing | B7 | ok | ok | ok | verificata |
| 31 | Malware: tipi e ciclo di vita | B8 | ok | ok | ok | verificata |
| 32 | Analisi statica di base in sandbox | B8 | ok | ok | ok | verificata |
| 33 | Ransomware didattico in sandbox | B8 | - | - | - | SALTATA (richiesta docente) |
| 34 | Analisi dinamica e IOC | B8 | ok | ok | ok | verificata |
| 35 | Hardening di sistema | B9 | ok | ok | ok | verificata |
| 36 | Log, monitoraggio e rilevamento | B9 | ok | ok | ok | verificata |
| 37 | Incident response di base | B9 | ok | ok | ok | verificata |
| 38 | Preparazione e ripasso CTF | B10 | ok | ok | ok | verificata |
| 39 | CTF finale a squadre | B10 | ok | ok | ok | verificata |
| 40 | Debrief e valutazione | B10 | - | - | - | da fare |

## Note di avanzamento
- (2026-09-12) Creato il generatore Word condiviso `tools/docxgen.py` e
  l'orchestratore `tools/build_lezioni.py`. Stile allineato a L2/L3
  (intestazione, riquadri con accento, codice su sfondo scuro, tabelle a righe
  alternate; H1 blu, H2 verde, H3 blu).
