# Brief: sviluppo di tutte le 40 lezioni del corso cybersec_pf

Sei l'assistente di sviluppo del corso "Sicurezza Informatica" (repo cybersec_pf).
Lavori nella working copy del repository (cartella corrente), che e' la copia
locale del repo pubblico chasseurmic/cybersec_pf, branch main.

## OBIETTIVO
Sviluppare TUTTE le 40 lezioni. Per ogni lezione produci tre cose:
1. Il laboratorio: gli script che lo studente scarica ed esegue sulla VM con
   `lab NN` (NN = numero lezione a due cifre).
2. La dispensa per gli studenti (Word).
3. Il manuale per il docente (Word), con soluzioni, flag e note.
Lavora in modo autonomo e continuativo: completata una lezione passa alla
successiva senza chiedere conferme, e non fermarti finche' tutte non sono
complete e verificate. Se una scelta e' ambigua, prendi la decisione piu'
ragionevole, annotala nel manuale docente e prosegui.

## PRIMA DI INIZIARE (studia il modello gia' fatto)
Le lezioni 1, 2 e 3 sono gia' fatte e sono il modello di riferimento. Leggi e
replica stile e convenzioni di: README.md; lezioni/lezione-01..03/ (script);
lezioni/Lezioni/ (Word gia' prodotti); bin/lab, bin/provision-kali.sh,
bin/provision-target.sh. Sviluppa dalla Lezione 4 alla 40. Se le lezioni 1-3
non rispettano una convenzione qui sotto, allineale.

## CONTESTO DEL CORSO
Sicurezza informatica difensiva e vulnerability assessment, 80 ore, 40 lezioni
da 2 ore, classe di terza di istituto tecnico (16 anni, poco attenti). Ente:
Progetto Formazione S.c.r.l. Docente: Michelangelo Chasseur (chasseurmic).
Impostazione pratica, prospettiva dell'attaccante per capire la difesa,
gamification stile Capture The Flag. Struttura fissa di ogni lezione da 2 ore:
circa 25 min teoria come caso reale, circa 80 min esercitazione alla tastiera,
circa 15 min ribaltamento difensivo.

## IL LABORATORIO
Lab isolato in VirtualBox, due VM per postazione su rete interna `labnet`:
Kali (attaccante) IP 10.10.10.5 con gli strumenti e il launcher `lab`; bersaglio
Ubuntu Server headless IP 10.10.10.20 con app vulnerabili in Docker (DVWA :8081,
Juice Shop :8082, "Banca della Scuola" :8080). Immagini base costruite una volta
sola (bin/). Tutto resta nel lab isolato: scansioni e attacchi solo contro il
bersaglio o dati finti seminati su di esso, mai verso internet o la rete scuola.

## MECCANISMO `lab NN`
Sulle VM c'e' /usr/local/bin/lab e /etc/lab-role ("kali" oppure "target").
`lab 7` scarica lezioni/lezione-07/<ruolo>.sh, mostra anteprima, chiede conferma,
esegue con sudo. Per ogni lezione crei in lezioni/lezione-NN/:
- kali.sh   : parte sulla Kali (briefing, strumenti, verifiche)
- target.sh : parte sul bersaglio (semina bersagli, servizi, file esca)
Se un ruolo non serve, fai comunque uno script che stampa un messaggio chiaro.

## REQUISITI DEGLI SCRIPT (obbligatori)
- Bash, `#!/usr/bin/env bash`. Idempotenti (rieseguibili senza danni: e' cosi'
  che si rigioca o si resetta). Fine riga LF, mai CRLF.
- Verifica: `set -uo pipefail` (senza -e); configurazione: `set -euo pipefail`.
- Rilevano da soli l'interfaccia interna quando serve (come i provision-*).
- Gamification: ogni esercitazione assegna flag FLAG{...} con punti; dove ha
  senso pianta un verificatore su una VM (come /usr/local/bin/caccia-verifica
  della L3) che premia il completamento con la flag.
- Verifica ogni script con `bash -n` prima di chiuderlo; prova la logica dove
  puoi. REPO_RAW = https://raw.githubusercontent.com/chasseurmic/cybersec_pf/main

## POLITICA FLAG (repo pubblico)
Prime lezioni: flag anche in chiaro (didattiche). Dalle sfide vere in poi NON
mettere i valori nel repo pubblico: generale a runtime sul bersaglio o tienile
solo nel manuale docente. Elenca sempre flag e soluzioni nel manuale docente.

## I TRE DELIVERABLE PER LEZIONE
1) LABORATORIO: script in lezioni/lezione-NN/ piu' eventuali tool custom.
2) DISPENSA STUDENTI: Word in lezioni/Lezioni/, nome
   `Lezione-NN-<slug>-Dispensa.docx`. Per gli studenti: scheda "In breve";
   teoria come caso reale (adatta a 16 anni); esercitazione passo passo con i
   comandi ESATTI e le tappe con le flag (senza rivelare i valori segreti);
   sezione difensiva; tabella punteggio. NIENTE soluzioni ne' flag segrete.
3) MANUALE DOCENTE: Word in lezioni/Lezioni/, nome
   `Lezione-NN-<slug>-Manuale.docx`. Per il docente: obiettivi e tempi; come
   funziona il lab (cosa fanno kali.sh e target.sh); TUTTE le soluzioni, i
   valori delle flag e la mappa di cosa e' seminato dove; come rigiocare o
   resettare; troubleshooting; prerequisiti. lezioni/Lezioni/ e' gia' in
   .gitignore: il manuale con le soluzioni resta fuori dal repo pubblico.

Per i Word usa un generatore riutilizzabile: come PRIMO passo crea uno strumento
condiviso sotto tools/ (Node con la libreria `docx`, oppure Python con
python-docx) che renda dispensa e manuale di OGNI lezione con lo stesso stile
delle lezioni 2 e 3 (intestazione, riquadri colorati, blocchi di codice su
sfondo scuro, tabelle a righe alternate; colori blu 1F3A5F, verde 2E7D32, rosso
B71C1C). Genera i .docx da una sorgente per lezione, cosi' gli 80 documenti
restano uniformi. Rendi ogni .docx e verifica impaginazione (anche via PDF).

## MAPPA DELLE 40 LEZIONI (10 blocchi) - guida, affinabile
B1 Setup e mindset (L1-L2): L1 Triade CIA e primo accesso [fatta]; L2
  Allestimento del laboratorio [fatta].
B2 Linux e bash offensivo (L3-L6): L3 Filesystem e permessi [fatta]; L4
  Navigazione avanzata, redirezioni e pipe; L5 Utenti, gruppi, processi e
  servizi; L6 Bash scripting offensivo, host alive scanner in bash [tool].
B3 Reconnaissance (L7-L10): L7 Footprinting e OSINT (simulati nel lab); L8
  Scoperta host e rete locale (ping sweep, ARP); L9 Port scanning con nmap e un
  port scanner in Python [tool]; L10 Enumerazione servizi e banner grabbing.
B4 Web application (L11-L18): L11 Come funziona il web (HTTP, DevTools, curl);
  L12 "Banca della Scuola" app Flask vulnerabile in docker-compose [tool] e SQL
  injection base; L13 SQL injection avanzata e sqlmap; L14 XSS reflected e
  stored; L15 Autenticazione, cookie e sessioni; L16 Brute force del login e la
  sua difesa [tool]; L17 File upload, path traversal e LFI; L18 Ripasso OWASP
  Top 10 e mini CTF web.
B5 Password e crittografia (L19-L22): L19 Come sono conservate le password (hash
  e salt); L20 Cracking a dizionario di hash MD5 [tool], john e hashcat; L21
  Cifratura simmetrica e asimmetrica, hashing vs cifratura; L22 HTTPS e TLS,
  certificati e attacchi nel lab.
B6 Rete (L23-L27): L23 TCP/IP e Wireshark; L24 Sniffing credenziali con scapy
  [tool]; L25 ARP spoofing e MITM con scapy [tool]; L26 DNS spoofing e attacchi
  in rete locale; L27 Difese di rete (segmentazione, firewall, IDS).
B7 Ingegneria sociale e phishing (L28-L30): L28 Social engineering, principi e
  casi reali; L29 Pagina di phishing didattica nel lab [tool]; L30 Riconoscere e
  difendersi dal phishing.
B8 Malware in sandbox (L31-L34): L31 Cos'e' il malware, tipi e ciclo di vita;
  L32 Analisi statica di base in sandbox; L33 Ransomware didattico in sandbox
  [tool]; L34 Analisi dinamica e indicatori di compromissione. Ambiente senza
  internet.
B9 Difesa e blue team (L35-L37): L35 Hardening di sistema; L36 Log, monitoraggio
  e rilevamento; L37 Incident response di base.
B10 CTF finale e valutazione (L38-L40): L38 Preparazione e ripasso; L39 CTF
  finale a squadre; L40 Debrief, valutazione e difese apprese.

## MODALITA' DI LAVORO AUTONOMA
- Tieni tools/PROGRESS.md con lo stato di ogni lezione (da fare / script / 
  dispensa / manuale / verificata). Aggiornalo mano a mano: serve a riprendere
  dopo un'interruzione.
- Procedi in ordine dalla L4 alla L40, una lezione alla volta e completa (tutti
  e tre i deliverable) prima della successiva.
- Dopo ogni lezione fai un commit git chiaro (es. "Lezione 07: reconnaissance
  OSINT (lab + dispensa + manuale)"). NON fare push. lezioni/Lezioni/ e'
  ignorato: i Word restano solo in locale, va bene.
- Quando una lezione richiede un tool [tool], sviluppalo in quella lezione e
  documentalo nel manuale. Per la L12 costruisci l'app Flask "Banca della
  Scuola" (vulnerabile a SQLi e XSS di proposito) in docker-compose sul
  bersaglio, che sostituisce la pagina statica :8080 e diventa il bersaglio del
  Blocco 4.
- Non chiedere conferme intermedie.

## DEFINIZIONE DI "FATTO" (per lezione)
lezioni/lezione-NN/ con gli script idempotenti e `bash -n` ok; dispensa e
manuale .docx in lezioni/Lezioni/ ben impaginati e coerenti con L2/L3; flag e
punteggi coerenti fra script, dispensa e manuale; PROGRESS.md aggiornato e
commit fatto.

## VERIFICA FINALE (a tutte e 40 fatte)
Rileggi PROGRESS.md e conferma completamento; verifica che ogni lezione abbia i
tre deliverable con i nomi giusti; aggiorna la tabella "Lezioni disponibili" nel
README.md con tutte e 40; scrivi un riepilogo finale e i punti che il docente
deve provare a mano (per esempio i tool sul bersaglio x86 reale).

## VINCOLI SEMPRE
Italiano, tono pragmatico, materiali adatti a 16 anni. Nel testo discorsivo
niente trattini lunghi ne' lineette (usa virgole o parentesi). Uso solo
didattico nel lab isolato. Malware e ransomware solo simulati in sandbox
isolata. Aula x86: scrivi gli script per x86 e segnala nel manuale dove un tool
va provato sul bersaglio reale.
