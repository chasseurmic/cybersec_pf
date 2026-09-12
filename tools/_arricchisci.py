#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-off: arricchisce le dispense (lezNN.py) con la sezione "Per lo studio a casa"
(sintesi, glossario, errori comuni, domande di autoverifica, collegamenti, e
approfondimenti facoltativi). Genera codice Python valido via repr() e lo inserisce
prima della tabella "Punteggio della Lezione". Idempotente: salta se gia' presente.
Uso:  python3 tools/_arricchisci.py
"""
import os
import re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lezioni_src")

# DATA[num] = dict con chiavi: sintesi, glossario (lista di coppie), errori,
# domande, collegamenti, approfondimenti (lista di coppie titolo/testo).
DATA = {}

DATA[2] = dict(
    sintesi=[
        "Il laboratorio sono due VM (Kali attaccante 10.10.10.5, bersaglio 10.10.10.20) su una rete interna isolata chiamata labnet.",
        "Ogni VM ha due schede: NAT (internet) e Rete interna (labnet). Se sbagli qui, niente comunica.",
        "Il comando lab NN scarica lo script della lezione per il ruolo della macchina, ne mostra un'anteprima e chiede conferma.",
        "Ordine di accensione: prima il bersaglio, poi la Kali. L'isolamento della rete e' gia' una forma di difesa (segmentazione).",
    ],
    glossario=[
        ("Macchina virtuale (VM)", "un computer simulato che gira dentro il tuo PC"),
        ("ISO", "il file immagine di un disco di installazione (di Kali o Ubuntu)"),
        ("OVA", "un unico file che impacchetta una o piu' VM pronte da importare"),
        ("NAT", "modalita' di rete che da' internet alla VM condividendo l'IP dell'host"),
        ("Rete interna (labnet)", "rete privata tra le VM, isolata da internet e dalla scuola"),
        ("Porta", "numero che identifica un servizio su un IP (es. 8080 = web)"),
        ("Container Docker", "app impacchettata con tutto cio' che le serve, avviabile in un istante"),
        ("/etc/lab-role", "file che dice a lab se la macchina e' 'kali' o 'target'"),
    ],
    errori=[
        "Mettere la seconda scheda su reti interne con NOMI diversi tra le due VM: non si vedranno.",
        "Accendere la Kali prima del bersaglio e poi stupirsi che i controlli falliscano.",
        "Eseguire uno script senza leggerne l'anteprima: pessima abitudine di sicurezza.",
        "Distribuire un OVA costruito su Mac ARM per PC x86 (non si avvia).",
    ],
    domande=[
        "A cosa servono le due schede di rete di ogni VM?",
        "Perche' lab mostra un'anteprima e chiede conferma prima di eseguire?",
        "Cos'e' una porta e come fa un solo IP a offrire piu' servizi?",
        "Che differenza c'e' tra NAT e Rete interna?",
        "Con quali comandi verifichi che la Kali veda il bersaglio?",
    ],
    collegamenti=[
        "Lezione 1: i primi comandi che qui usi per la diagnostica.",
        "Lezione 8: scoprire gli host della rete labnet con nmap.",
        "Lezione 12: la 'Banca della Scuola' su :8080 diventa il bersaglio del blocco web.",
    ],
)

DATA[3] = dict(
    sintesi=[
        "In Linux tutto parte dalla radice /; le cartelle chiave sono /home, /etc, /var, /srv, /root, /tmp.",
        "I percorsi sono assoluti (da /) o relativi (da dove sei: . qui, .. sopra, ~ casa).",
        "I permessi hanno tre terzine (utente, gruppo, altri) con r=4, w=2, x=1: 644, 600, 755.",
        "La vulnerabilita' piu' comune non e' un exploit ma un permesso sbagliato: un segreto leggibile da 'altri'.",
        "Nascondere non e' proteggere: i file col punto si vedono con ls -a.",
    ],
    glossario=[
        ("Filesystem", "l'insieme organizzato di cartelle e file del sistema"),
        ("Percorso assoluto", "parte dalla radice, es. /srv/dati; vale sempre"),
        ("Percorso relativo", "parte dalla cartella corrente (pwd)"),
        ("Permessi rwx", "lettura (r), scrittura (w), esecuzione/attraversamento (x)"),
        ("Proprietario / gruppo", "l'utente e il gruppo a cui appartiene un file"),
        ("chmod", "cambia i permessi (es. chmod 600 file)"),
        ("SSH", "collegamento a un terminale su una macchina remota"),
        ("Minimo privilegio", "dare solo i permessi indispensabili, niente di piu'"),
    ],
    errori=[
        "Lasciare un segreto a 644: la terzina 'altri' con la r lo rende leggibile a chiunque.",
        "Confondere i numeri: 600 non e' 'poco', e' 'solo il proprietario'.",
        "Dimenticare 2>/dev/null con find e affogare tra i 'Permission denied'.",
        "Credere che rinominare o nascondere un file lo protegga.",
    ],
    domande=[
        "Cosa vuol dire chmod 640 in termini di chi puo' fare cosa?",
        "Come cerchi tutti i file che contengono la parola FLAG sotto /srv?",
        "Perche' stipendi.csv (600, root) e' 'un muro' e password_backup.txt (644) no?",
        "Qual e' la differenza tra percorso assoluto e relativo?",
        "Cos'e' il principio del minimo privilegio e perche' conta?",
    ],
    collegamenti=[
        "Lezione 4: setacciare file e log con pipe e redirezioni.",
        "Lezione 5: utenti, gruppi e la regola sudo (chi puo' diventare root).",
        "Lezione 35: hardening, cioe' chiudere i permessi di troppo in modo sistematico.",
    ],
)

DATA[4] = dict(
    sintesi=[
        "La pipe | passa l'output di un comando al comando successivo: una catena di montaggio.",
        "Le redirezioni dirottano l'output: > sovrascrive, >> aggiunge, 2>/dev/null butta gli errori.",
        "grep filtra, cut taglia campi, sort ordina, uniq -c conta, wc -l conta le righe.",
        "La combo cut | sort | uniq -c | sort -rn | head smaschera chi compare piu' spesso in un log.",
        "Gli stessi strumenti servono all'attaccante (setacciare il bottino) e al difensore (leggere i log).",
    ],
    glossario=[
        ("Pipe (|)", "collega due comandi passando il testo dall'uno all'altro"),
        ("stdout / stderr", "il canale dell'output normale (1) e quello degli errori (2)"),
        ("Redirezione", "dirottare l'output: > file, >> file, 2> file"),
        ("/dev/null", "il 'cestino' del sistema: cio' che ci mandi sparisce"),
        ("grep", "filtra le righe che contengono un testo (-r ricorsivo, -l solo i nomi)"),
        ("cut", "estrae colonne/campi (-d separatore, -f numero campo)"),
        ("sort / uniq", "ordina le righe / rimuove o conta i doppioni (uniq dopo sort)"),
        ("Log", "registro degli eventi di un sistema o di un servizio"),
    ],
    errori=[
        "Usare uniq senza sort prima: conta solo i doppioni consecutivi.",
        "Confondere > (sovrascrive, cancella!) con >> (aggiunge in fondo).",
        "Dimenticare le virgolette quando il separatore e' uno spazio: cut -d' ' -f1.",
        "Non filtrare gli errori con 2>/dev/null e perdere il risultato nel rumore.",
    ],
    domande=[
        "Come conti quante righe di un log contengono '404'?",
        "Come salvi su file l'elenco ordinato e senza doppioni degli IP di un log?",
        "Qual e' la differenza tra > e >>? Cosa rischi a sbagliarli?",
        "Perche' uniq va sempre usato dopo sort?",
        "Come troveresti, tra mille file, l'unico che contiene la parola 'password'?",
    ],
    collegamenti=[
        "Lezione 3: i comandi di base (ls, cat, find) su cui si costruiscono le pipe.",
        "Lezione 36: leggere i log di sicurezza usando esattamente queste pipe.",
        "Lezione 6: automatizzare queste catene dentro uno script.",
    ],
)

DATA[5] = dict(
    sintesi=[
        "Dopo un accesso, la prima mossa non e' attaccare: e' enumerare (utenti, processi, servizi, privilegi).",
        "root ha UID 0 e puo' tutto; /etc/passwd elenca gli utenti; le password stanno in /etc/shadow.",
        "ps aux mostra i processi con la riga di comando: una password passata come argomento e' visibile a tutti.",
        "ss -tlnp mostra le porte in ascolto; systemctl gestisce i servizi; sudo -l dice cosa puoi fare da root.",
        "Dal processo al servizio: dal PID risali all'unita' con systemctl status <PID>.",
    ],
    glossario=[
        ("UID / GID", "numero identificativo dell'utente / del gruppo (root = 0)"),
        ("/etc/passwd", "elenco degli utenti (7 campi separati da :)"),
        ("Processo / PID", "un programma in esecuzione / il suo numero identificativo"),
        ("Servizio (daemon)", "programma che parte da solo e resta attivo in background"),
        ("systemd / systemctl", "il gestore dei servizi di Linux e il suo comando"),
        ("Porta in ascolto", "porta su cui un servizio aspetta connessioni"),
        ("sudo", "eseguire comandi come root; sudo -l elenca cosa e' permesso"),
        ("Enumerazione", "raccogliere informazioni su un sistema dopo esservi entrati"),
    ],
    errori=[
        "Passare password come argomenti di un comando: restano in chiaro in ps aux.",
        "Lasciare utenti di servizio con shell di login invece di nologin.",
        "Regole sudo troppo larghe (NOPASSWD su comandi potenti): via all'escalation.",
        "Tenere accesi servizi inutili: ogni porta aperta e' una porta d'ingresso in piu'.",
    ],
    domande=[
        "Come trovi una password lasciata negli argomenti di un processo?",
        "Dato un PID, come scopri quale servizio systemd lo ha avviato?",
        "Perche' un utente di servizio dovrebbe avere shell nologin?",
        "Cosa mostra sudo -l e perche' e' importante per un attaccante?",
        "Con quale comando elenchi le porte TCP in ascolto e chi le tiene?",
    ],
    collegamenti=[
        "Lezione 3: i permessi, l'altra faccia dei privilegi.",
        "Lezione 9-10: scoprire dall'esterno le porte e i servizi che qui vedi dall'interno.",
        "Lezione 35: hardening, cioe' spegnere servizi e stringere le regole sudo.",
    ],
)

DATA[6] = dict(
    sintesi=[
        "Uno script bash automatizza comandi ripetitivi: shebang, chmod +x, esecuzione.",
        "I mattoni sono variabili, ciclo for, condizione if e i codici di uscita (0 = ok).",
        "Un ping sweep sequenziale e' lento; con & (background) e wait diventa velocissimo.",
        "La funzione /dev/tcp di bash permette di verificare se una porta e' aperta senza altri strumenti.",
        "Capire come e' fatto uno strumento vale piu' che usarne uno pronto senza saperlo.",
    ],
    glossario=[
        ("Script", "un file di comandi eseguibili in sequenza"),
        ("Shebang", "la prima riga #!/usr/bin/env bash che indica l'interprete"),
        ("Variabile", "un contenitore per un valore (nome=valore, si usa con $nome)"),
        ("Ciclo for", "ripete dei comandi per ogni elemento di una lista"),
        ("Codice di uscita", "0 se un comando riesce, diverso da 0 se fallisce"),
        ("& e wait", "avviare in parallelo (&) e aspettare la fine di tutti (wait)"),
        ("/dev/tcp", "funzione di bash per aprire una connessione TCP (test di porta)"),
        ("Ping sweep", "pingare tutti gli indirizzi di una rete per trovare gli host vivi"),
    ],
    errori=[
        "Mettere spazi attorno all'= in una variabile (nome = valore): errore.",
        "Lanciare uno script con sh invece di bash: /dev/tcp e gli array non funzionano.",
        "Dimenticare wait dopo aver lanciato i ping in background: risultati incompleti.",
        "Non gestire il timeout del ping (-W): lo scanner si impianta sugli host spenti.",
    ],
    domande=[
        "Perche' lo scanner parallelo e' cosi' piu' veloce di quello sequenziale?",
        "Come rendi eseguibile uno script e come lo lanci?",
        "A cosa servono & e wait in un ping sweep?",
        "Come verifichi se una porta e' aperta usando solo bash (/dev/tcp)?",
        "Cosa stampa il codice di uscita di un comando e come lo usa un if?",
    ],
    collegamenti=[
        "Lezione 4: le pipe e le redirezioni che usi dentro gli script.",
        "Lezione 8-9: gli stessi concetti con gli strumenti professionali (nmap).",
        "Lezione 9: uno scanner di porte scritto in Python.",
    ],
)

DATA[7] = dict(
    sintesi=[
        "La reconnaissance e' la raccolta di informazioni prima dell'attacco: spesso i dati sono gia' esposti.",
        "OSINT passivo (fonti aperte, non tocca il bersaglio) vs footprinting attivo (interroga il bersaglio).",
        "Un sito rivela molto: intestazioni HTTP, commenti nel codice, robots.txt, directory listing, file .bak.",
        "robots.txt non protegge: elenca proprio le cartelle che qualcuno vorrebbe nascondere.",
        "Un dir buster prova tanti nomi e trova cio' che non e' linkato da nessuna parte.",
    ],
    glossario=[
        ("Reconnaissance", "la fase di raccolta informazioni su un bersaglio"),
        ("OSINT", "intelligence da fonti aperte (Open Source Intelligence)"),
        ("Footprinting", "profilazione attiva del bersaglio (visitare il sito, ecc.)"),
        ("Intestazioni HTTP", "coppie nome-valore nella risposta (Server, header custom)"),
        ("robots.txt", "file che chiede ai motori di non indicizzare certe cartelle"),
        ("Directory listing", "elenco automatico dei file di una cartella senza indice"),
        ("Dir busting", "provare tanti nomi di cartelle/file per scoprirli (gobuster, dirb)"),
        ("whatweb", "strumento che identifica tecnologie e versioni di un sito"),
    ],
    errori=[
        "Credere che robots.txt nasconda: al contrario, indica dove guardare.",
        "Lasciare il directory listing attivo o file .old/.bak sui server pubblici.",
        "Mettere commenti sensibili nel codice HTML che va in produzione.",
        "Fare OSINT su bersagli reali fuori dal lab: qui e' tutto simulato apposta.",
    ],
    domande=[
        "Che differenza c'e' tra OSINT passivo e footprinting attivo?",
        "Come leggi le intestazioni HTTP di un sito e perche' possono tradirlo?",
        "Perche' robots.txt aiuta l'attaccante invece di proteggere?",
        "Come trovi una cartella che non e' linkata da nessuna pagina?",
        "Dal formato delle email aziendali, cosa puo' dedurre un attaccante?",
    ],
    collegamenti=[
        "Lezione 8-10: la ricognizione a livello di rete (host, porte, servizi).",
        "Lezione 28: come l'OSINT alimenta gli attacchi di social engineering.",
        "Lezione 12+: gli attacchi web contro il sito che qui hai profilato.",
    ],
)

DATA[8] = dict(
    sintesi=[
        "La scoperta host mappa chi e' vivo in una rete; e' la base di tutto cio' che segue.",
        "Due metodi: ping (ICMP), che un host puo' ignorare, e ARP, che sulla rete locale e' piu' affidabile.",
        "nmap -sn fa host discovery; sulla rete locale, da root, usa ARP e mostra anche i MAC.",
        "L'ARP lega IP e MAC; la cache si legge con ip neigh dopo un ping.",
        "Una scansione e' rumorosa: un IP che tocca centinaia di indirizzi salta all'occhio.",
    ],
    glossario=[
        ("Host discovery", "scoprire quali indirizzi sono attivi in una rete"),
        ("ICMP / ping", "protocollo e comando per verificare la raggiungibilita'"),
        ("ARP", "protocollo che traduce un IP nel MAC corrispondente sulla LAN"),
        ("Indirizzo MAC", "identificativo fisico e unico di una scheda di rete"),
        ("Cache ARP", "la 'rubrica' IP-MAC del sistema (ip neigh)"),
        ("/24", "notazione CIDR: 24 bit di rete, 254 host utilizzabili (10.10.10.1-254)"),
        ("nmap -sn", "scansione di sola scoperta host, senza scansione delle porte"),
    ],
    errori=[
        "Lanciare nmap -sn senza sudo e non ottenere i MAC (niente ARP).",
        "Leggere ip neigh senza aver prima pingato l'host (cache vuota).",
        "Pensare che ignorare il ping renda un host invisibile: l'ARP lo scopre lo stesso.",
        "Copiare male il MAC (scambiare 0 e O, aggiungere spazi).",
    ],
    domande=[
        "Perche' l'ARP e' piu' affidabile del ping sulla rete locale?",
        "Cosa significa /24 e quanti host utilizzabili contiene?",
        "Come leggi il MAC di un host dalla tua macchina?",
        "Perche' nmap -sn richiede i privilegi di root per usare l'ARP?",
        "Come contrasta un difensore la mappatura della rete?",
    ],
    collegamenti=[
        "Lezione 6: il ping sweep artigianale in bash, qui fatto con nmap.",
        "Lezione 9: dopo gli host, la scoperta delle porte.",
        "Lezione 25: l'ARP sfruttato in modo offensivo (spoofing e MITM).",
    ],
)

DATA[9] = dict(
    sintesi=[
        "Un host ha 65535 porte; ognuna puo' ospitare un servizio, cioe' una possibile via d'ingresso.",
        "Il three-way handshake (SYN, SYN-ACK, ACK) apre una connessione TCP: gli scanner lo sfruttano.",
        "Gli stati di una porta: aperta (servizio attivo), chiusa, filtrata (un firewall blocca).",
        "nmap scansiona le porte (-sS SYN, -p- tutte, --top-ports le comuni, -Pn ignora il ping).",
        "Uno scanner in Python (socket + thread) fa la stessa cosa: capire come, vale piu' che usarlo.",
    ],
    glossario=[
        ("Porta", "numero (1-65535) che identifica un servizio su un host"),
        ("Three-way handshake", "SYN, SYN-ACK, ACK: l'apertura di una connessione TCP"),
        ("Porta aperta/chiusa/filtrata", "servizio attivo / nessun servizio / bloccata da firewall"),
        ("SYN scan (-sS)", "scansione veloce che non completa la connessione"),
        ("socket", "l'estremita' di una connessione di rete in programmazione"),
        ("Thread", "flusso di esecuzione parallelo: velocizza lo scanner"),
        ("connect_ex", "funzione Python che ritorna 0 se la porta e' aperta"),
    ],
    errori=[
        "Lanciare -sS senza root: usare invece -sT (connect scan) oppure sudo.",
        "Scandire una sola porta e credere di conoscere tutto il bersaglio.",
        "Timeout troppo alti: lo scanner diventa lentissimo sulle porte filtrate.",
        "Scandire sistemi non autorizzati: qui e' tutto nel lab isolato.",
    ],
    domande=[
        "Cosa distingue una porta 'chiusa' da una 'filtrata'?",
        "Quali sono i tre pacchetti del three-way handshake?",
        "Come fa uno scanner Python a capire se una porta e' aperta?",
        "Perche' -sS richiede privilegi mentre -sT no?",
        "Come cerchi tutte le porte aperte, non solo quelle comuni?",
    ],
    collegamenti=[
        "Lezione 8: prima gli host, poi (qui) le loro porte.",
        "Lezione 10: dalla porta al servizio-con-versione (banner grabbing).",
        "Lezione 27: come un firewall rende 'filtrate' le porte per difendersi.",
    ],
)

DATA[10] = dict(
    sintesi=[
        "Sapere che una porta e' aperta non basta: serve capire quale servizio gira e quale versione.",
        "Il banner e' il saluto che molti servizi mandano appena ci si collega: spesso rivela nome e versione.",
        "Banner grabbing manuale con nc; automatico con nmap -sV; per il web con curl -I e whatweb.",
        "Nome + versione permettono di cercare vulnerabilita' note (CVE): la versione e' oro per l'attaccante.",
        "Difendersi: ridurre i banner e tenere il software aggiornato.",
    ],
    glossario=[
        ("Enumerazione servizi", "capire quale software e versione c'e' dietro una porta"),
        ("Banner", "il messaggio iniziale che un servizio invia alla connessione"),
        ("Banner grabbing", "leggere il banner per identificare il servizio"),
        ("nc (netcat)", "il 'coltellino svizzero' TCP: si collega e mostra cio' che arriva"),
        ("nmap -sV", "identifica automaticamente servizio e versione"),
        ("CVE", "codice che identifica una vulnerabilita' nota (Common Vulnerabilities and Exposures)"),
    ],
    errori=[
        "Fermarsi alla porta senza identificare il servizio e la versione.",
        "Esporre banner con versioni dettagliate: un regalo a chi cerca CVE.",
        "Confondere nc (client) con un server: qui ci si collega per leggere.",
        "Non aggiornare: se la versione trapela ed e' vecchia, le CVE sono aperte.",
    ],
    domande=[
        "Cos'e' un banner e perche' e' utile a un attaccante?",
        "Come catturi a mano il banner di un servizio su una porta?",
        "Cosa aggiunge nmap -sV rispetto a una semplice scansione delle porte?",
        "Perche' conoscere la versione di un servizio e' cosi' importante?",
        "Come riduce un difensore le informazioni rivelate dai banner?",
    ],
    collegamenti=[
        "Lezione 9: prima le porte aperte, qui il servizio dietro ciascuna.",
        "Lezione 7: whatweb e curl -I gia' visti sul web.",
        "Lezione 12+: sfruttare i servizi web identificati.",
    ],
)

DATA[11] = dict(
    sintesi=[
        "Il web e' fatto di richieste e risposte HTTP: testo che viaggia, che si puo' leggere e manipolare.",
        "GET chiede una pagina (parametri nella URL); POST invia dati (nel corpo, es. i login).",
        "I codici di stato: 200 ok, 301/302 redirect, 403 vietato, 404 non trovato, 500 errore server.",
        "Header e cookie accompagnano ogni richiesta; il cookie fa riconoscere l'utente dopo il login.",
        "Regola d'oro: i dati del client (parametri, header, cookie) non sono fidati, si falsificano con curl.",
    ],
    glossario=[
        ("HTTP", "il protocollo del web: richieste e risposte testuali"),
        ("GET / POST", "chiedere una risorsa / inviare dati al server"),
        ("Codice di stato", "numero che dice l'esito (200, 404, 500, ...)"),
        ("Header", "coppie nome-valore che accompagnano richiesta e risposta"),
        ("Cookie", "header speciale che il browser rimanda per farti riconoscere"),
        ("curl", "client HTTP da terminale (-d dati/POST, -H header, -b cookie, -I intestazioni)"),
        ("DevTools", "gli Strumenti per sviluppatori del browser (F12)"),
    ],
    errori=[
        "Credere che nascondere un pulsante nel browser impedisca l'azione: si rifa' con curl.",
        "Mettere i controlli di sicurezza solo lato client invece che sul server.",
        "Confondere parametri GET (nella URL) con dati POST (nel corpo).",
        "Fidarsi di header e cookie ricevuti: sono controllati dall'utente.",
    ],
    domande=[
        "Che differenza c'e' tra GET e POST?",
        "Cosa significano i codici 200, 403 e 302?",
        "A cosa serve un cookie e come lo invii con curl?",
        "Perche' i dati che arrivano dal client non sono fidati?",
        "Come invii un header personalizzato in una richiesta?",
    ],
    collegamenti=[
        "Lezione 12-18: tutti gli attacchi web partono dal manipolare queste richieste.",
        "Lezione 15: i cookie e le sessioni approfonditi.",
        "Lezione 1: curl gia' usato per leggere la pagina della Banca.",
    ],
)

DATA[12] = dict(
    sintesi=[
        "La SQL injection nasce quando un sito incolla l'input dell'utente dentro una query senza controllarlo.",
        "Con ' OR '1'='1' -- o admin' -- si altera il senso della query: si entra senza password.",
        "Il commento -- (con lo spazio) elimina il resto della query, compreso il controllo della password.",
        "La stessa falla nella ricerca permette di leggere dati riservati (dump).",
        "La difesa definitiva sono le query parametrizzate: i dati viaggiano separati dal comando.",
    ],
    glossario=[
        ("SQL", "il linguaggio con cui si interroga un database"),
        ("Query", "una richiesta al database (es. SELECT ... WHERE ...)"),
        ("SQL injection", "iniettare SQL tramite un input non controllato"),
        ("Login bypass", "entrare senza credenziali sfruttando la SQLi"),
        ("Commento SQL (--)", "tutto cio' che segue viene ignorato dal database"),
        ("Query parametrizzata", "i dati passano a parte (?), non possono diventare codice"),
        ("Banca della Scuola", "l'app web vulnerabile del corso, su :8080"),
    ],
    errori=[
        "Dimenticare lo spazio dopo -- : il commento non funziona.",
        "Costruire query concatenando stringhe con l'input: e' la causa della SQLi.",
        "Salvare le password in chiaro nel database (le vedremo hashate).",
        "Provare SQLi su siti reali: qui e' solo la Banca del laboratorio.",
    ],
    domande=[
        "Perche' admin' -- permette di entrare senza conoscere la password?",
        "A cosa serve il commento -- in un payload SQLi?",
        "Come faresti a leggere tutti i conti dalla pagina di ricerca?",
        "Qual e' la difesa che chiude sia il bypass sia il dump?",
        "Perche' concatenare l'input nella query e' pericoloso?",
    ],
    collegamenti=[
        "Lezione 11: le richieste HTTP che qui manipoli.",
        "Lezione 13: SQL injection avanzata (UNION) e sqlmap.",
        "Lezione 19-20: perche' le password non vanno salvate in chiaro.",
    ],
)

DATA[13] = dict(
    sintesi=[
        "UNION SELECT unisce i risultati e permette di leggere altre tabelle: serve lo stesso numero di colonne.",
        "sqlite_master e' la mappa del database: da li' si scoprono tabelle e struttura.",
        "sqlmap automatizza tutto: trova l'iniezione, capisce le colonne, scarica le tabelle.",
        "Il danno reale della SQLi e' l'esfiltrazione: interi database online in un minuto.",
        "Difesa: query parametrizzate, dati sensibili cifrati, monitoraggio (sqlmap fa rumore).",
    ],
    glossario=[
        ("UNION SELECT", "attacca i risultati di una seconda query alla prima"),
        ("Allineamento colonne", "la UNION richiede lo stesso numero e tipo di colonne"),
        ("sqlite_master", "tabella speciale con lo schema del database SQLite"),
        ("sqlmap", "strumento che automatizza lo sfruttamento della SQL injection"),
        ("Dump", "l'estrazione completa dei dati di una o piu' tabelle"),
        ("Esfiltrazione", "portare fuori i dati rubati da un sistema"),
    ],
    errori=[
        "Sbagliare il numero di colonne nella UNION (usa ORDER BY o riempitivi 'x').",
        "Non indicare a sqlmap il parametro (-p) e il dbms (--dbms=sqlite): va piu' lento.",
        "Usare sqlmap fuori da un contesto autorizzato: e' potente e va usato solo nel lab.",
        "Salvare numeri di carta o segreti in chiaro nel database.",
    ],
    domande=[
        "Perche' la UNION richiede lo stesso numero di colonne?",
        "Come scopri le tabelle di un database SQLite via SQLi?",
        "Cosa fa sqlmap che a mano richiederebbe molto piu' tempo?",
        "Qual e' il danno concreto di una SQL injection non chiusa?",
        "Quali difese rendono inutile un attacco UNION?",
    ],
    collegamenti=[
        "Lezione 12: la SQL injection di base, prerequisito di questa.",
        "Lezione 18: il mini CTF che concatena SQLi e altre falle.",
        "Lezione 20: cosa fare con le password (hashate) trovate in un dump.",
    ],
)

DATA[14] = dict(
    sintesi=[
        "L'XSS avviene quando un sito mostra l'input dell'utente senza ripulirlo: diventa codice eseguito dal browser.",
        "Riflesso: lo script torna subito nella risposta (colpisce chi apre il link). Memorizzato: viene salvato (colpisce tutti).",
        "Il memorizzato e' piu' grave: caricato una volta, colpisce ogni visitatore, admin compreso.",
        "Un XSS reale ruba il cookie di sessione o compie azioni al posto della vittima.",
        "Difesa: escape dell'output, Content Security Policy, cookie HttpOnly.",
    ],
    glossario=[
        ("XSS", "Cross-Site Scripting: esecuzione di codice altrui nel browser della vittima"),
        ("XSS riflesso", "lo script e' nella richiesta e torna nella risposta immediata"),
        ("XSS memorizzato", "lo script viene salvato dal sito e servito a tutti"),
        ("Payload", "il codice iniettato (es. <script>alert(1)</script>)"),
        ("Escape dell'output", "trasformare < in &lt; cosi' il testo non diventa codice"),
        ("HttpOnly", "flag del cookie che lo rende illeggibile dal JavaScript"),
        ("CSP", "Content Security Policy: dice al browser quali script eseguire"),
    ],
    errori=[
        "Mostrare l'input dell'utente senza escape: e' la causa dell'XSS.",
        "Difendersi solo filtrando l'input: la difesa vera e' l'escape in uscita.",
        "Tenere i cookie di sessione senza HttpOnly: un XSS li ruba.",
        "Sottovalutare il memorizzato: basta che l'admin apra la pagina.",
    ],
    domande=[
        "Qual e' la differenza tra XSS riflesso e memorizzato? Quale e' piu' grave?",
        "Cosa fa in pratica un payload XSS piu' pericoloso di un alert?",
        "Perche' l'escape dell'output ferma l'XSS?",
        "A cosa serve il flag HttpOnly sui cookie?",
        "Perche' fidarsi dei dati del client e' all'origine anche dell'XSS?",
    ],
    collegamenti=[
        "Lezione 11: le richieste in cui inietti il payload.",
        "Lezione 15: il furto del cookie di sessione, spesso obiettivo dell'XSS.",
        "Lezione 29: pagine civetta e inganni, cugini del XSS memorizzato.",
    ],
)

DATA[15] = dict(
    sintesi=[
        "HTTP non ha memoria: il sito ti riconosce con un cookie di sessione dopo il login.",
        "Un cookie fatto male (prevedibile, non firmato) si puo' forgiare: cosi' si impersona un altro utente.",
        "Il controllo accessi va fatto lato server sulla sessione reale, non su un valore che l'utente puo' cambiare.",
        "Due errori spesso insieme: cookie prevedibile + pagina admin che si fida del cookie.",
        "Difesa: sessioni casuali lato server, cookie HttpOnly e Secure, controllo del ruolo sul server.",
    ],
    glossario=[
        ("Sessione", "lo stato che il server tiene per un utente dopo il login"),
        ("Cookie di sessione", "il 'biglietto' che identifica la sessione a ogni richiesta"),
        ("Cookie prevedibile", "un cookie il cui valore si puo' indovinare o costruire"),
        ("Furto di sessione", "usare il cookie di un altro per impersonarlo"),
        ("Controllo accessi rotto", "quando i permessi si basano su dati controllati dall'utente"),
        ("HttpOnly / Secure", "flag che proteggono il cookie (dal JS / solo su HTTPS)"),
    ],
    errori=[
        "Mettere nel cookie dati sensibili o prevedibili (il nome utente in chiaro).",
        "Verificare il ruolo (admin?) su un valore che arriva dal client.",
        "Cookie senza HttpOnly/Secure: rubabili via XSS o su HTTP.",
        "Non invalidare davvero la sessione al logout.",
    ],
    domande=[
        "Perche' HTTP ha bisogno dei cookie per 'ricordarti'?",
        "Cosa rende un cookie di sessione forgiabile?",
        "Cos'e' un controllo di accesso rotto? Fai un esempio.",
        "Dove va verificato il ruolo di un utente, e perche'?",
        "A cosa servono i flag HttpOnly e Secure?",
    ],
    collegamenti=[
        "Lezione 11: header e cookie, le basi di questa lezione.",
        "Lezione 14: l'XSS che ruba proprio il cookie di sessione.",
        "Lezione 16: le password deboli, l'altra via per entrare in un account.",
    ],
)

DATA[16] = dict(
    sintesi=[
        "Il brute force prova tante password finche' una funziona; l'attacco a dizionario usa liste di password probabili.",
        "Con hash veloci e password comuni (rockyou), un PC ne prova milioni al secondo.",
        "Un tool proprio (o hydra) automatizza l'invio dei tentativi al login.",
        "La difesa efficace e' il rate limiting/lockout: dopo pochi errori si blocca.",
        "Password robuste, 2FA e CAPTCHA rendono l'attacco impraticabile.",
    ],
    glossario=[
        ("Brute force", "provare molte password finche' una e' corretta"),
        ("Attacco a dizionario", "brute force mirato che usa una lista di password probabili"),
        ("Wordlist", "l'elenco di password da provare (es. rockyou)"),
        ("hydra", "strumento che automatizza il brute force di login"),
        ("Rate limiting", "limitare i tentativi in un dato tempo"),
        ("Lockout", "bloccare l'accesso dopo N tentativi falliti"),
        ("2FA", "autenticazione a due fattori: serve un secondo elemento oltre la password"),
    ],
    errori=[
        "Permettere tentativi illimitati sul login: invito al brute force.",
        "Usare password comuni o corte: sono nelle wordlist.",
        "Sbagliare la stringa di fallimento in hydra e segnare tutto come valido.",
        "Fidarsi solo della password: senza 2FA, se cade, si e' dentro.",
    ],
    domande=[
        "Che differenza c'e' tra brute force puro e attacco a dizionario?",
        "Perche' hash veloci e password comuni rendono il brute force facile?",
        "Come ferma un attacco il rate limiting?",
        "Perche' il 2FA protegge anche se la password viene indovinata?",
        "Cosa cambia, nell'attacco, tra il login /debole e quello /forte del lab?",
    ],
    collegamenti=[
        "Lezione 15: l'altra via per entrare in un account (cookie/sessioni).",
        "Lezione 19-20: hash delle password e cracking a dizionario.",
        "Lezione 36: come i tentativi falliti appaiono nei log del difensore.",
    ],
)

DATA[17] = dict(
    sintesi=[
        "Il path traversal usa ../ per uscire dalla cartella prevista e leggere file altrove (LFI).",
        "Se un sito apre file in base a un parametro non controllato, si arriva a /etc/passwd o a segreti.",
        "L'upload non validato accetta qualunque tipo/nome di file: su un server reale puo' portare a esecuzione di codice.",
        "Non fidarsi mai del nome file scelto dall'utente.",
        "Difesa: whitelist dei file/estensioni, normalizzare i percorsi, permessi minimi del processo web.",
    ],
    glossario=[
        ("Path traversal", "risalire le cartelle con ../ per uscire dai confini previsti"),
        ("LFI", "Local File Inclusion: far leggere/includere al sito un file locale"),
        ("Upload non validato", "accettare file senza controllarne tipo, nome, contenuto"),
        ("Whitelist", "elenco chiuso di cio' che e' permesso (l'opposto della blacklist)"),
        ("Webshell", "un file caricato che permette di eseguire comandi sul server"),
        ("Normalizzazione del percorso", "ridurre un percorso alla forma reale per verificarlo"),
    ],
    errori=[
        "Costruire percorsi concatenando l'input senza verificare i ../.",
        "Accettare upload senza controllare l'estensione e il tipo reale.",
        "Salvare gli upload in una cartella web con permesso di esecuzione.",
        "Fidarsi del nome file: puo' contenere ../ o estensioni pericolose.",
    ],
    domande=[
        "Come useresti ../ per leggere un file fuori dalla cartella dei documenti?",
        "Che differenza c'e' tra path traversal e LFI?",
        "Perche' un upload non validato e' pericoloso anche senza esecuzione?",
        "Cos'e' una whitelist e perche' e' meglio di una blacklist?",
        "Come limita i danni un processo web con permessi minimi?",
    ],
    collegamenti=[
        "Lezione 3: i permessi dei file, che qui fanno la differenza.",
        "Lezione 18: il caveau del CTF, raggiunto con path traversal.",
        "Lezione 12-13: altre falle della stessa app (SQLi).",
    ],
)

DATA[18] = dict(
    sintesi=[
        "OWASP pubblica la Top 10: la classifica delle vulnerabilita' web piu' diffuse e gravi.",
        "Tutto il blocco rientra in poche categorie: Injection (SQLi, XSS), Broken Access Control, Auth Failures, Misconfiguration.",
        "Gli attacchi reali sono a catena: il risultato di uno serve al successivo (SQLi -> LFI).",
        "La difesa e' a strati: basta chiudere un anello per spezzare la catena.",
        "Difesa in profondita': input validato, query parametrizzate, output escappato, accessi lato server, permessi minimi.",
    ],
    glossario=[
        ("OWASP", "organizzazione che pubblica la Top 10 delle vulnerabilita' web"),
        ("Top 10", "la classifica delle falle web piu' comuni e pericolose"),
        ("Attacco a catena", "concatenare piu' vulnerabilita' per un obiettivo"),
        ("Difesa in profondita'", "piu' strati di protezione, cosi' se uno cede reggono gli altri"),
        ("CTF", "Capture The Flag: gara a sfide di sicurezza, ogni flag vale punti"),
    ],
    errori=[
        "Pensare che chiudere una sola falla basti: gli attacchi combinano piu' errori.",
        "Trascurare la 'noiosa' configurazione: molte compromissioni nascono da li'.",
        "Non validare l'input e non escappare l'output insieme.",
    ],
    domande=[
        "Cita tre categorie OWASP e un attacco del corso per ognuna.",
        "Cosa vuol dire attacco 'a catena'? Fai l'esempio del caveau.",
        "Perche' basta chiudere un anello per fermare una catena?",
        "Cos'e' la difesa in profondita'?",
    ],
    collegamenti=[
        "Lezioni 12-17: le singole falle che qui si combinano.",
        "Lezione 39: il CTF finale, che riprende queste tecniche.",
        "Lezione 27 e 35: le difese lato server e di rete.",
    ],
)

DATA[19] = dict(
    sintesi=[
        "Le password non si salvano mai in chiaro: si salva il loro hash, una funzione a senso unico.",
        "Stesso testo -> stesso hash; da testi diversi -> hash diversi; dall'hash non si torna al testo.",
        "Hash uguali = password uguali: senza sale, due utenti con la stessa password hanno lo stesso hash.",
        "Il sale (salt) e' una stringa casuale per utente aggiunta prima dell'hash: rende gli hash tutti diversi.",
        "Difesa vera: funzioni lente e salate (bcrypt, scrypt, Argon2), non MD5/SHA nudi.",
    ],
    glossario=[
        ("Hash", "funzione a senso unico che trasforma un testo in una stringa fissa"),
        ("A senso unico", "dall'hash non si ricava il testo di partenza"),
        ("MD5 / SHA-256", "algoritmi di hash (veloci, non adatti da soli alle password)"),
        ("Sale (salt)", "stringa casuale per utente aggiunta prima dell'hash"),
        ("Rainbow table", "tabella precalcolata hash->testo, resa inutile dal sale"),
        ("bcrypt / Argon2", "funzioni di hash lente e salate, adatte alle password"),
    ],
    errori=[
        "Salvare le password in chiaro (o cifrarle in modo reversibile).",
        "Usare MD5/SHA nudi: troppo veloci, cadono al cracking.",
        "Non usare un sale diverso per ogni utente.",
        "Usare echo invece di printf '%s': echo aggiunge un a-capo e cambia l'hash.",
    ],
    domande=[
        "Qual e' la differenza tra hash e cifratura?",
        "Perche' due utenti con la stessa password possono tradirsi senza sale?",
        "A cosa serve il sale e perche' rende inutili le rainbow table?",
        "Perche' MD5 non e' adatto a proteggere le password?",
        "Quali funzioni si usano oggi per le password e perche' sono lente?",
    ],
    collegamenti=[
        "Lezione 20: come si craccano gli hash deboli.",
        "Lezione 21: hashing vs cifratura, due cose diverse.",
        "Lezione 12-13: perche' un dump di password in chiaro e' un disastro.",
    ],
)

DATA[20] = dict(
    sintesi=[
        "Dagli hash rubati si ritrovano le password 'indovinando': si fa l'hash di tante parole e si confronta.",
        "L'attacco a dizionario usa liste di password reali (rockyou, 14 milioni di voci).",
        "Un cracker Python (hashlib) fa la cosa base; john e hashcat sono gli strumenti professionali.",
        "Hash veloci e senza sale cadono in fretta; bcrypt/Argon2 rendono il cracking troppo costoso.",
        "Password lunghe e non comuni non sono nelle wordlist: sfuggono all'attacco a dizionario.",
    ],
    glossario=[
        ("Cracking", "ritrovare la password a partire dal suo hash"),
        ("Attacco a dizionario", "provare l'hash di parole prese da una wordlist"),
        ("rockyou", "famosa wordlist di password reali trapelate"),
        ("john / hashcat", "gli strumenti standard per il cracking degli hash"),
        ("hashlib", "libreria Python per calcolare gli hash"),
        ("Modalita' hashcat (-m 0)", "indica il tipo di hash (0 = MD5)"),
    ],
    errori=[
        "Aspettarsi di 'decifrare' un hash: non si decifra, si indovina.",
        "Dimenticare --format=raw-md5 in john o -m 0 in hashcat.",
        "Provare a crackare hash altrui fuori dal lab.",
        "Confondere velocita' e sicurezza: un hash veloce e' un male, per le password.",
    ],
    domande=[
        "Perche' si dice che l'hash non si decifra ma si indovina?",
        "Cos'e' rockyou e perche' rende il cracking cosi' efficace?",
        "Quali passi fa un cracker a dizionario, in tre righe?",
        "Perche' bcrypt/Argon2 rendono il cracking impraticabile?",
        "Che tipo di password sfugge a un attacco a dizionario?",
    ],
    collegamenti=[
        "Lezione 19: hash e sale, i concetti che qui si sfruttano.",
        "Lezione 16: il brute force, cugino del cracking (online vs offline).",
        "Lezione 35-36: proteggere e sorvegliare gli account.",
    ],
)

DATA[21] = dict(
    sintesi=[
        "Cifrare e' reversibile con la chiave giusta; l'hash no. Non vanno confusi.",
        "Cifratura simmetrica (AES): una sola chiave cifra e decifra; veloce, ma bisogna scambiare la chiave.",
        "Cifratura asimmetrica (RSA): coppia pubblica/privata; cio' che cifri con la pubblica apre solo con la privata.",
        "La firma digitale: firmi con la privata, tutti verificano con la pubblica (autenticita' e non ripudio).",
        "La sicurezza sta nella chiave, non nel segreto dell'algoritmo (principio di Kerckhoffs).",
    ],
    glossario=[
        ("Cifratura simmetrica", "stessa chiave per cifrare e decifrare (es. AES)"),
        ("Cifratura asimmetrica", "coppia di chiavi pubblica/privata (es. RSA)"),
        ("Chiave pubblica/privata", "una si distribuisce, l'altra resta segreta"),
        ("Firma digitale", "prova che un messaggio viene da te e non e' alterato"),
        ("openssl", "strumento a riga di comando per crittografia"),
        ("Kerckhoffs", "principio: la sicurezza sta nella chiave, non nell'algoritmo segreto"),
    ],
    errori=[
        "Confondere cifratura (reversibile) e hash (a senso unico).",
        "Condividere la chiave privata: va tenuta segretissima.",
        "Inventare algoritmi propri invece di usare standard collaudati.",
        "Usare chiavi corte o prevedibili.",
    ],
    domande=[
        "Qual e' la differenza tra cifrare e fare l'hash?",
        "Vantaggi e limiti della cifratura simmetrica?",
        "Come fa la cifratura asimmetrica a far ricevere segreti senza scambiare una chiave prima?",
        "Come funziona una firma digitale?",
        "Cosa dice il principio di Kerckhoffs?",
    ],
    collegamenti=[
        "Lezione 19: l'hash, da non confondere con la cifratura.",
        "Lezione 22: HTTPS/TLS, che combina simmetrica e asimmetrica.",
        "Lezione 23-24: perche' il traffico cifrato non si legge sniffando.",
    ],
)

DATA[22] = dict(
    sintesi=[
        "HTTPS e' HTTP dentro un tunnel cifrato (TLS): riservatezza del traffico e identita' del sito.",
        "TLS usa l'asimmetrica per scambiare in sicurezza una chiave simmetrica, poi la simmetrica per i dati.",
        "Il certificato e' la carta d'identita' del sito, firmata da una CA di cui il browser si fida.",
        "Un certificato self-signed non e' garantito da nessuna CA: il browser avvisa (giustamente).",
        "Un avviso sul certificato non va MAI ignorato: e' il segnale di un possibile MITM.",
    ],
    glossario=[
        ("TLS/SSL", "il protocollo che cifra il traffico (la S di HTTPS)"),
        ("Certificato", "documento con l'identita' e la chiave pubblica del sito"),
        ("CA", "Certificate Authority: l'ente che firma e garantisce i certificati"),
        ("Self-signed", "certificato firmato da se stesso, non garantito da una CA"),
        ("Catena di fiducia", "il browser si fida delle CA, che garantiscono i siti"),
        ("HSTS", "regola che impone al browser di usare sempre HTTPS"),
    ],
    errori=[
        "Ignorare l'avviso del browser sul certificato ('accetta il rischio').",
        "Usare curl -k su siti reali: salta il controllo del certificato.",
        "Usare certificati self-signed su siti pubblici.",
        "Tenere versioni vecchie e bucate di TLS/SSL.",
    ],
    domande=[
        "Cosa garantisce il lucchetto di HTTPS, oltre alla cifratura?",
        "Come fa TLS a unire i vantaggi di simmetrica e asimmetrica?",
        "Cos'e' una CA e cosa cambia con un certificato self-signed?",
        "Perche' un avviso sul certificato e' un allarme e non un fastidio?",
        "Cosa fa curl -k e perche' e' pericoloso fuori dal lab?",
    ],
    collegamenti=[
        "Lezione 21: le due cifrature che TLS mette insieme.",
        "Lezione 25-26: il MITM da cui HTTPS (con certificato valido) protegge.",
        "Lezione 29-30: perche' controllare dominio e lucchetto sventa il phishing.",
    ],
)

DATA[23] = dict(
    sintesi=[
        "I dati viaggiano a strati (TCP/IP): applicazione, trasporto, rete, collegamento.",
        "Su una rete condivisa, chi ascolta vede il traffico altrui: se non e' cifrato, lo legge tutto.",
        "Wireshark e tcpdump catturano i pacchetti; i filtri isolano cio' che interessa.",
        "Il three-way handshake (SYN, SYN-ACK, ACK) si vede all'inizio di ogni connessione TCP.",
        "Difesa: cifrare tutto; il traffico cifrato, anche catturato, resta illeggibile.",
    ],
    glossario=[
        ("Pila TCP/IP", "i livelli con cui i dati vengono impacchettati"),
        ("Pacchetto", "l'unita' di dati che viaggia in rete"),
        ("Wireshark / tcpdump", "strumenti per catturare e leggere i pacchetti"),
        ("Filtro (BPF)", "regola per mostrare solo certi pacchetti (es. udp port 9999)"),
        ("Sniffing", "ascoltare il traffico di rete"),
        ("Follow TCP Stream", "ricostruire l'intera conversazione di una connessione"),
    ],
    errori=[
        "Catturare sull'interfaccia sbagliata e non vedere nulla.",
        "Far viaggiare credenziali in chiaro (HTTP, FTP, Telnet).",
        "Pensare che sniffare sia innocuo: intercettare traffico altrui e' illegale fuori dal lab.",
    ],
    domande=[
        "Quali sono i livelli della pila TCP/IP?",
        "Perche' su una rete condivisa si puo' leggere il traffico altrui?",
        "Come isoli in Wireshark solo il traffico che ti interessa?",
        "Quali sono i tre pacchetti del handshake e dove si vedono?",
        "Perche' cifrare rende inutile lo sniffing?",
    ],
    collegamenti=[
        "Lezione 24: automatizzare lo sniffing con scapy.",
        "Lezione 21-22: la cifratura che protegge dal sniffing.",
        "Lezione 9: TCP e porte, gia' incontrati con nmap.",
    ],
)

DATA[24] = dict(
    sintesi=[
        "scapy permette di costruire e catturare pacchetti in poche righe di Python.",
        "sniff() con un filtro e una funzione per pacchetto; il contenuto sta nel livello Raw.",
        "Un attaccante non legge i pacchetti a mano: scrive un tool che estrae le credenziali da solo.",
        "L'automazione e la persistenza pagano: lasciando girare il tool si catturano anche i dati rari.",
        "Difesa: cifrare tutto, niente protocolli in chiaro, segmentare la rete.",
    ],
    glossario=[
        ("scapy", "libreria Python per costruire, inviare e catturare pacchetti"),
        ("sniff()", "funzione di scapy che cattura i pacchetti"),
        ("Filtro BPF", "espressione per selezionare i pacchetti (es. udp port 9998)"),
        ("Livello Raw", "il contenuto applicativo grezzo del pacchetto"),
        ("Harvesting", "raccolta automatica di credenziali dal traffico"),
        ("Espressione regolare", "schema per estrarre dati (es. utente= e password=)"),
    ],
    errori=[
        "Lanciare sniff() senza root: serve l'accesso ai raw socket.",
        "Ascoltare l'interfaccia sbagliata (usa quella interna, es. eth1).",
        "Guardare i pacchetti a mano invece di automatizzare l'estrazione.",
    ],
    domande=[
        "Quali due elementi bastano a scapy per catturare (sniff)?",
        "Dove si trova il contenuto applicativo di un pacchetto in scapy?",
        "Perche' l'automazione batte la lettura manuale dei pacchetti?",
        "Perche' sniff() richiede i privilegi di root?",
        "Come rende inutile lo sniffing una rete ben progettata?",
    ],
    collegamenti=[
        "Lezione 23: la cattura manuale con Wireshark, qui automatizzata.",
        "Lezione 25: dallo sniffing passivo al MITM attivo.",
        "Lezione 6: costruire i propri strumenti (qui in Python con scapy).",
    ],
)

DATA[25] = dict(
    sintesi=[
        "L'ARP non ha autenticazione: chiunque puo' rispondere 'quell'IP ce l'ho io' (spoofing).",
        "Avvelenando la cache ARP della vittima, il suo traffico verso un IP arriva all'attaccante (MITM).",
        "Con scapy si inviano risposte ARP false in continuazione per mantenere l'inganno.",
        "Per un MITM completo si avvelenano entrambi i lati e si attiva l'inoltro dei pacchetti.",
        "Difesa: cifrare tutto, switch gestiti (Dynamic ARP Inspection), voci ARP statiche.",
    ],
    glossario=[
        ("ARP spoofing", "inviare risposte ARP false per farsi passare per un altro IP"),
        ("Cache poisoning", "avvelenare la rubrica IP-MAC della vittima"),
        ("MITM", "man-in-the-middle: mettersi in mezzo a una comunicazione"),
        ("Gratuitous ARP", "annuncio ARP non richiesto, usato per mantenere l'inganno"),
        ("ip_forward", "impostazione che permette all'attaccante di inoltrare i pacchetti"),
        ("Dynamic ARP Inspection", "difesa degli switch contro le risposte ARP false"),
    ],
    errori=[
        "Lanciare l'arpspoof senza root o sull'interfaccia sbagliata.",
        "Dimenticare di rinfrescare l'ARP: l'inganno decade.",
        "Fare ARP spoofing su reti altrui: e' un reato serio, solo nel lab.",
    ],
    domande=[
        "Perche' l'ARP e' facilmente falsificabile?",
        "Come fa l'attaccante a mettersi in mezzo (MITM) tramite ARP?",
        "A cosa serve inviare risposte ARP di continuo?",
        "Cosa serve in piu' per un MITM 'trasparente' completo?",
        "Quali difese fermano l'ARP spoofing?",
    ],
    collegamenti=[
        "Lezione 8: l'ARP visto in modo legittimo (scoperta host).",
        "Lezione 24: lo sniffing che il MITM rende possibile anche fuori dal proprio traffico.",
        "Lezione 26: il DNS spoofing, spesso combinato con l'ARP.",
    ],
)

DATA[26] = dict(
    sintesi=[
        "Il DNS traduce i nomi in indirizzi IP: se qualcuno risponde con un IP falso, ti manda dove vuole lui.",
        "Controllando il DNS (o mettendosi in mezzo), l'attaccante dirotta la vittima su un sito civetta.",
        "Un DNS canaglia risponde a ogni nome con l'IP dell'attaccante; il sito civetta cattura le credenziali.",
        "Con HTTPS valido la vittima vedrebbe un avviso sul certificato: un motivo per non ignorarlo mai.",
        "Difesa: DNS fidati e cifrati (DoH/DoT), HTTPS ovunque, protezioni contro DHCP/DNS abusivi.",
    ],
    glossario=[
        ("DNS", "il servizio che traduce i nomi (banca.local) in indirizzi IP"),
        ("Risoluzione dei nomi", "l'operazione di trovare l'IP di un nome"),
        ("DNS spoofing", "rispondere con un IP falso per dirottare la vittima"),
        ("DNS canaglia", "un server DNS controllato dall'attaccante"),
        ("Sito civetta", "una copia del sito vero, fatta per rubare le credenziali"),
        ("DoH / DoT", "DNS cifrato (over HTTPS / over TLS), piu' difficile da manomettere"),
    ],
    errori=[
        "Usare DNS non fidati o forniti da chiunque sulla rete.",
        "Ignorare gli avvisi del browser (dominio o certificato sospetti).",
        "Non usare HTTPS: senza, il sito civetta e' indistinguibile a occhio.",
    ],
    domande=[
        "Perche' controllare il DNS permette di dirottare una vittima?",
        "Cosa fa un DNS canaglia?",
        "Come si combina il DNS spoofing con un sito civetta?",
        "Perche' HTTPS valido aiuta a smascherare l'inganno?",
        "Quali difese riducono il rischio di DNS spoofing?",
    ],
    collegamenti=[
        "Lezione 25: l'ARP spoofing per intercettare le richieste DNS.",
        "Lezione 29: il sito civetta approfondito (phishing).",
        "Lezione 22: certificati e avvisi, l'ancora di salvezza.",
    ],
)

DATA[27] = dict(
    sintesi=[
        "Difendere una rete significa ridurre la superficie d'attacco e accorgersi degli attacchi.",
        "Tre pilastri: firewall (cosa passa), segmentazione (dividere in zone), IDS (rilevare le minacce).",
        "Un firewall e' una lista di regole: bloccare una porta = aggiungere una regola di DROP.",
        "Un IDS a porte esca (honeypot) rileva le scansioni: nessun utente vero tocca quelle porte.",
        "La difesa e' a strati: chiudere l'inutile, segmentare, rilevare, aggiornare e cifrare.",
    ],
    glossario=[
        ("Firewall", "filtra il traffico secondo regole (ACCEPT/DROP)"),
        ("iptables", "lo strumento classico per gestire il firewall di Linux"),
        ("DROP", "regola che scarta silenziosamente i pacchetti"),
        ("Segmentazione", "dividere la rete in zone isolate (VLAN)"),
        ("IDS", "Intrusion Detection System: rileva attivita' sospette"),
        ("Honeypot / porta esca", "trappola che attira e smaschera l'attaccante"),
        ("Superficie d'attacco", "l'insieme dei punti da cui si puo' essere attaccati"),
    ],
    errori=[
        "Lasciare aperte porte e servizi inutili.",
        "Raccogliere log e regole ma non guardarli mai.",
        "Aprire una regola di firewall troppo larga 'per comodita''.",
        "Bloccare per sbaglio la porta 22 (SSH) e perdere l'accesso.",
    ],
    domande=[
        "Come blocchi una porta con iptables e come verifichi l'effetto?",
        "Cos'e' la segmentazione e perche' aiuta?",
        "Come fa un honeypot a porte esca a rilevare una scansione?",
        "Perche' con -sS l'honeypot non scatta e con -sT si?",
        "Cosa vuol dire 'difesa in profondita''?",
    ],
    collegamenti=[
        "Lezione 8-9: le scansioni che qui impari a rilevare e bloccare.",
        "Lezione 35: hardening del singolo sistema.",
        "Lezione 36-37: log, rilevamento e risposta agli incidenti.",
    ],
)

DATA[28] = dict(
    sintesi=[
        "Il social engineering inganna le persone, non i computer: spesso e' la via piu' facile.",
        "Le leve classiche: urgenza, autorita', scarsita', reciprocita', riprova sociale.",
        "Prima l'OSINT, poi il colpo: piu' l'attaccante sa di te, piu' e' credibile.",
        "Nessuno del supporto chiede la password: e' sempre una truffa.",
        "Difesa: fermarsi davanti all'urgenza, verificare per un altro canale, ridurre le info pubbliche.",
    ],
    glossario=[
        ("Social engineering", "manipolare le persone per ottenere accessi o dati"),
        ("Pretexting", "costruire una storia credibile per ingannare"),
        ("Urgenza / autorita'", "leve che spingono ad agire senza pensare o a obbedire"),
        ("Scarsita' / reciprocita'", "paura di perdere l'occasione / sentirsi in debito"),
        ("Riprova sociale", "'lo fanno tutti', l'istinto del gregge"),
        ("Vishing / smishing", "social engineering per telefono / via SMS"),
    ],
    errori=[
        "Agire di fretta quando un messaggio mette urgenza.",
        "Fidarsi di chi dice di avere autorita' senza verificare.",
        "Dare informazioni personali che diventano pretesti.",
        "Comunicare password a chiunque, anche al 'supporto'.",
    ],
    domande=[
        "Cita tre leve di manipolazione e un esempio per ognuna.",
        "Perche' l'OSINT rende un inganno piu' efficace?",
        "Come verifichi in sicurezza una richiesta 'del capo' urgente?",
        "Perche' un vero supporto non chiede mai la password?",
        "Come riduci la tua esposizione al social engineering?",
    ],
    collegamenti=[
        "Lezione 7: l'OSINT che alimenta il pretexting.",
        "Lezione 29: il phishing, social engineering applicato al web.",
        "Lezione 30: riconoscere e difendersi dagli inganni.",
    ],
)

DATA[29] = dict(
    sintesi=[
        "Il phishing e' l'attacco piu' diffuso: una pagina identica a quella vera che cattura le credenziali.",
        "Tre ingredienti: il clone (aspetto), la cattura (salva utente/password), il redirect al sito vero (non insospettire).",
        "Il link arriva con un'email di social engineering; col DNS spoofing la vittima ci finisce anche digitando l'indirizzo.",
        "Senza HTTPS valido, la barra degli indirizzi e' l'unico indizio.",
        "E' un reato: si usa SOLO nel laboratorio, contro il finto utente.",
    ],
    glossario=[
        ("Phishing", "ingannare l'utente con una pagina/e-mail falsa per rubare dati"),
        ("Pagina civetta / clone", "copia del sito vero fatta per catturare credenziali"),
        ("Cattura credenziali", "salvare utente e password inseriti dalla vittima"),
        ("Redirect", "rimandare la vittima al sito vero dopo la cattura"),
        ("Spear phishing", "phishing mirato su una persona specifica"),
    ],
    errori=[
        "Usare queste tecniche fuori dal lab: e' un reato (sostituzione di persona, frode).",
        "Dimenticare il redirect: la vittima si insospettisce.",
        "Pensare che un utente attento non abbocchi mai: capita a tutti, prima o poi.",
    ],
    domande=[
        "Quali sono i tre ingredienti di una pagina di phishing?",
        "Perche' il redirect al sito vero rende l'inganno piu' efficace?",
        "Come si combina il phishing con social engineering e DNS spoofing?",
        "Perche' l'HTTPS valido aiuta a smascherarlo?",
        "Perche' questa tecnica va usata solo nel laboratorio?",
    ],
    collegamenti=[
        "Lezione 28: le leve psicologiche che fanno cliccare il link.",
        "Lezione 26: dirottare la vittima sul sito civetta col DNS.",
        "Lezione 30: come non abboccare.",
    ],
)

DATA[30] = dict(
    sintesi=[
        "La maggior parte del phishing si smaschera leggendo bene l'indirizzo.",
        "Il dominio che conta sono le ultime due etichette prima della prima barra singola.",
        "login.banca.local e' ancora banca.local; banca.local.truffa.ru e' truffa.ru.",
        "Non fidarsi del testo di un link: puo' mostrare una cosa e portare altrove.",
        "Difese personali: controlla il dominio, apri i siti dai preferiti, attiva il 2FA.",
    ],
    glossario=[
        ("Dominio", "le ultime due etichette dell'host (es. esempio.com)"),
        ("Sottodominio", "una parte a sinistra del dominio (login.esempio.com)"),
        ("Lookalike", "dominio somigliante a quello vero, usato per ingannare"),
        ("Barra degli indirizzi", "dove il browser mostra il vero URL"),
        ("2FA", "secondo fattore: rete di sicurezza se la password viene rubata"),
    ],
    errori=[
        "Leggere il dominio da sinistra invece che da destra.",
        "Fidarsi del testo del link senza controllarne la destinazione.",
        "Inserire credenziali arrivando da un link ricevuto.",
        "Ignorare gli avvisi del browser.",
    ],
    domande=[
        "Come si legge un dominio per capire dove porta davvero?",
        "banca.local.verifica-conto.ru: qual e' il dominio reale?",
        "Perche' non ci si deve fidare del testo di un link?",
        "Quali abitudini ti proteggono dal phishing?",
        "Perche' il 2FA e' una rete di sicurezza?",
    ],
    collegamenti=[
        "Lezione 29: la pagina di phishing, qui vista dal lato della difesa.",
        "Lezione 22: certificati e avvisi del browser.",
        "Lezione 28: riconoscere le leve dell'inganno.",
    ],
)

DATA[31] = dict(
    sintesi=[
        "Malware = software malevolo: cambia come si diffonde, come si nasconde e cosa fa.",
        "Tipi principali: virus, worm, trojan, ransomware, spyware.",
        "Ciclo di vita: consegna, esecuzione, persistenza, comando (C2), azione.",
        "In questo blocco non si esegue mai malware vero: solo descrizioni e simulazioni innocue, in sandbox isolata.",
        "Difese di base: aggiornamenti, antivirus, backup staccati, minimo privilegio.",
    ],
    glossario=[
        ("Malware", "software creato per danneggiare, rubare o prendere il controllo"),
        ("Virus / worm", "si attacca ad altri file / si copia da solo in rete"),
        ("Trojan", "si traveste da programma utile ma nasconde codice malevolo"),
        ("Ransomware", "cifra i file e chiede un riscatto"),
        ("Spyware", "spia di nascosto e invia i dati"),
        ("Persistenza", "il meccanismo con cui il malware riparte a ogni riavvio"),
        ("C2 (comando e controllo)", "il server da cui il malware riceve ordini"),
        ("Sandbox", "ambiente isolato e usa-e-getta per analizzare in sicurezza"),
    ],
    errori=[
        "Scaricare o eseguire malware reale: mai, nemmeno 'per prova'.",
        "Confondere virus e worm (il worm non ha bisogno che tu apra nulla).",
        "Non fare backup: e' l'unica vera difesa contro il ransomware.",
    ],
    domande=[
        "Che differenza c'e' tra virus, worm e trojan?",
        "Quali sono le fasi del ciclo di vita di un attacco malware?",
        "Cos'e' la persistenza e cos'e' il C2?",
        "Perche' l'analisi si fa in una sandbox isolata?",
        "Quali sono le difese di base contro il malware?",
    ],
    collegamenti=[
        "Lezione 32: analisi statica (guardare senza eseguire).",
        "Lezione 34: analisi dinamica e indicatori di compromissione.",
        "Lezione 35-37: hardening, monitoraggio e risposta.",
    ],
)

DATA[32] = dict(
    sintesi=[
        "L'analisi statica esamina un file senza eseguirlo: e' il modo sicuro di capire cosa fa.",
        "file identifica il tipo; strings mostra il testo leggibile (URL, comandi, C2).",
        "sha256sum calcola l'impronta unica del file: un IOC per riconoscerlo ovunque.",
        "base64 e simili offuscano: un file 'normale' non nasconde comandi codificati.",
        "Difesa: ricavare gli IOC e bloccarli, condividerli con la comunita'.",
    ],
    glossario=[
        ("Analisi statica", "studiare un file senza eseguirlo"),
        ("file", "comando che identifica il tipo di un file"),
        ("strings", "estrae il testo leggibile contenuto in un file"),
        ("sha256sum", "calcola l'impronta (hash) del file"),
        ("IOC", "Indicator Of Compromise: indizio per riconoscere una minaccia"),
        ("base64", "codifica reversibile spesso usata per offuscare"),
    ],
    errori=[
        "Fare doppio clic su un file sospetto invece di analizzarlo.",
        "Ignorare stringhe come URL, IP o mutex: sono indizi preziosi.",
        "Passare a base64 -d anche il prefisso 'cfg=': va decodificata solo la stringa.",
    ],
    domande=[
        "Cosa rivela strings su un file sospetto?",
        "Cos'e' un IOC e perche' l'hash del file ne e' uno?",
        "Come riconosci una parte offuscata e come la decodifichi?",
        "Perche' l'analisi statica e' sicura?",
        "A cosa serve condividere gli IOC?",
    ],
    collegamenti=[
        "Lezione 31: i tipi di malware, contesto di questa analisi.",
        "Lezione 34: l'analisi dinamica, complementare alla statica.",
        "Lezione 36: usare gli IOC per il rilevamento.",
    ],
)

DATA[34] = dict(
    sintesi=[
        "L'analisi dinamica osserva il comportamento del programma mentre gira, in una sandbox isolata.",
        "Si guardano connessioni (strace, ss), file creati (ls) e processi (ps).",
        "Da qui si ricavano gli IOC concreti: l'IP/porta del C2, gli artefatti su disco.",
        "Statica e dinamica insieme danno il quadro completo: cosa POTREBBE fare e cosa FA.",
        "Difesa: bloccare il C2, cercare gli artefatti su tutti i PC, isolare le macchine compromesse.",
    ],
    glossario=[
        ("Analisi dinamica", "osservare un programma in esecuzione, in sandbox"),
        ("strace", "mostra le chiamate di sistema di un processo (incluse le connessioni)"),
        ("ss / lsof", "mostrano le connessioni di rete aperte"),
        ("Artefatto", "traccia lasciata dal malware (file, chiave, processo)"),
        ("C2", "server di comando e controllo che il malware contatta"),
        ("IOC", "indicatori concreti per riconoscere la minaccia"),
    ],
    errori=[
        "Eseguire un campione fuori da una sandbox isolata.",
        "Guardare solo i file e non le connessioni di rete (o viceversa).",
        "Non annotare gli IOC: sono cio' che poi protegge l'intera rete.",
    ],
    domande=[
        "Cosa aggiunge l'analisi dinamica rispetto alla statica?",
        "Come scopri con chi 'parla' un campione (il C2)?",
        "Quali artefatti cerchi e come?",
        "Perche' statica e dinamica vanno usate insieme?",
        "Come si passa dagli IOC alla difesa dell'intera rete?",
    ],
    collegamenti=[
        "Lezione 32: l'analisi statica, il primo passo.",
        "Lezione 27 e 36: usare gli IOC su firewall e sistemi di rilevamento.",
        "Lezione 37: isolare e bonificare una macchina compromessa.",
    ],
)

DATA[35] = dict(
    sintesi=[
        "L'hardening riduce la superficie d'attacco: si spegne l'inutile e si stringe cio' che resta.",
        "Regola: minimo indispensabile su servizi, porte, account, permessi.",
        "SSH piu' sicuro: niente login diretto di root, password forti, meglio le chiavi.",
        "I segreti a 600/400; niente file sensibili leggibili da tutti.",
        "Hardening + monitoraggio + piano di risposta sono i tre pilastri della difesa.",
    ],
    glossario=[
        ("Hardening", "irrobustire un sistema riducendone le debolezze"),
        ("Superficie d'attacco", "l'insieme dei punti attaccabili di un sistema"),
        ("systemctl disable", "disabilita un servizio perche' non riparta"),
        ("PermitRootLogin no", "impedisce il login diretto di root via SSH"),
        ("Baseline / benchmark", "una lista di controllo di sicurezza (es. CIS)"),
        ("Minimo privilegio", "concedere solo i permessi indispensabili"),
    ],
    errori=[
        "Lasciare acceso 'per comodita'' un servizio che non serve.",
        "Permettere il login di root via SSH.",
        "Segreti con permessi larghi (644 invece di 600).",
        "Fare modifiche senza documentarle o senza modo di tornare indietro.",
    ],
    domande=[
        "Cosa significa ridurre la superficie d'attacco?",
        "Come disabiliti un servizio inutile e come lo verifichi?",
        "Perche' conviene vietare il login diretto di root via SSH?",
        "Quali permessi deve avere un file di segreti?",
        "Quali sono i tre pilastri della difesa di un sistema?",
    ],
    collegamenti=[
        "Lezione 3 e 5: permessi e servizi, che qui si mettono in sicurezza.",
        "Lezione 27: le difese a livello di rete.",
        "Lezione 36-37: sorvegliare e rispondere quando qualcosa passa.",
    ],
)

DATA[36] = dict(
    sintesi=[
        "I log registrano tutto: chi si collega, cosa succede, cosa va storto. Un log che nessuno guarda non protegge.",
        "Quasi ogni attacco lascia una traccia: una raffica di accessi falliti, un login a un'ora strana.",
        "Le stesse pipe della Lezione 4 (grep, sort, uniq) diventano gli strumenti del difensore.",
        "Un rilevamento e' solo una ricerca fatta in automatico (fail2ban, un SIEM).",
        "Dalla scoperta nei log parte la risposta all'incidente.",
    ],
    glossario=[
        ("Log", "registro degli eventi di un sistema o servizio"),
        ("auth.log", "il log degli accessi (SSH, sudo) su Linux"),
        ("Correlazione", "collegare eventi da piu' fonti per capire un attacco"),
        ("fail2ban", "strumento che blocca gli IP con troppi accessi falliti"),
        ("SIEM", "sistema che raccoglie e correla i log per rilevare le minacce"),
        ("Baseline", "cosa e' 'normale', per far risaltare l'anomalo"),
    ],
    errori=[
        "Raccogliere i log ma non guardarli mai.",
        "Non centralizzare i log: diventano difficili da correlare.",
        "Ignorare i picchi di accessi falliti da un solo IP.",
    ],
    domande=[
        "Come trovi l'IP con piu' accessi falliti in un auth.log?",
        "Come capisci quale account e' stato infine compromesso?",
        "Quali pipe della Lezione 4 riusi qui?",
        "Cos'e' un rilevamento automatico (es. fail2ban)?",
        "Cosa fai quando i log rivelano una compromissione?",
    ],
    collegamenti=[
        "Lezione 4: le pipe, qui usate in difesa.",
        "Lezione 16 e 27: gli attacchi che qui si vedono 'dal lato del difensore'.",
        "Lezione 37: la risposta all'incidente scoperto nei log.",
    ],
)

DATA[37] = dict(
    sintesi=[
        "La differenza tra un incidente e un disastro e' come reagisci nei primi minuti: serve un piano.",
        "Le sei fasi (PICERL): Preparazione, Identificazione, Contenimento, Eradicazione, Recupero, Lezioni apprese.",
        "Contenere: isolare, bloccare account e IP. Eradicare: rimuovere persistenza e backdoor.",
        "Recupero: password nuove, ripristino da backup puliti, monitoraggio aumentato.",
        "Lezioni apprese: capire come e' entrato e chiudere quella falla; migliorare i processi, non colpevolizzare.",
    ],
    glossario=[
        ("Incident response", "la gestione strutturata di una compromissione"),
        ("PICERL", "le sei fasi: Preparazione, Identificazione, Contenimento, Eradicazione, Recupero, Lezioni"),
        ("Contenimento", "fermare l'emorragia: isolare, bloccare"),
        ("Eradicazione", "rimuovere l'attaccante (account, cron, backdoor)"),
        ("Persistenza", "il meccanismo con cui l'attaccante resta (es. un cron)"),
        ("Postmortem", "l'analisi finale, senza colpevolizzare (blameless)"),
    ],
    errori=[
        "Improvvisare: cancellare prove o lasciare porte aperte.",
        "Eradicare senza aver prima contenuto: l'attaccante rientra.",
        "Non capire la falla d'ingresso: si ripresenta uguale.",
        "Cercare un colpevole invece di migliorare i processi.",
    ],
    domande=[
        "Quali sono le sei fasi dell'incident response?",
        "Come contieni un account ostile e un IP attaccante?",
        "Cosa significa eradicare la persistenza?",
        "Cosa comprende la fase di recupero?",
        "Perche' un postmortem deve essere 'senza colpe'?",
    ],
    collegamenti=[
        "Lezione 36: scoprire la compromissione nei log.",
        "Lezione 35: chiudere la falla sfruttata (hardening).",
        "Lezione 34: gli IOC che guidano la bonifica.",
    ],
)

DATA[38] = dict(
    sintesi=[
        "Un CTF e' una gara a sfide di sicurezza: ogni flag vale punti, vince chi ne fa di piu'.",
        "Per riuscirci devi sapere DOVE cercare: la mappa delle abilita' del corso, per blocco.",
        "Allenarsi a tempo su sfide brevi (pipe, base64, cracking, log) rende automatici i gesti.",
        "In squadra: dividersi per aree, leggere bene i testi, tenere un foglio condiviso, partire dalle facili.",
        "Annotare i comandi utili: al CTF non c'e' tempo di reinventarli.",
    ],
    glossario=[
        ("CTF", "Capture The Flag: gara a sfide, ogni flag vale punti"),
        ("Flag", "la stringa FLAG{...} che dimostra una sfida risolta"),
        ("Wordlist", "lista usata per il cracking a dizionario"),
        ("Base64", "codifica reversibile da riconoscere e decodificare"),
        ("Strategia di squadra", "dividersi i compiti e condividere i risultati"),
    ],
    errori=[
        "Non leggere bene il testo della sfida (spesso contiene il suggerimento).",
        "Ripetere il lavoro gia' fatto da un compagno (serve un foglio condiviso).",
        "Buttarsi sulle sfide difficili prima di prendere i punti facili.",
    ],
    domande=[
        "Come troveresti una flag nascosta tra tante righe di rumore?",
        "Come decodifichi un messaggio in base64?",
        "Come rompi un hash MD5 con una wordlist?",
        "Come trovi l'IP di un attaccante in un log?",
        "Quali regole rendono efficace una squadra al CTF?",
    ],
    collegamenti=[
        "Tutte le lezioni: qui si ripassano le abilita' del corso.",
        "Lezione 39: il CTF finale a squadre.",
        "Lezione 4, 20, 32, 36: pipe, cracking, base64, log usati nell'allenamento.",
    ],
)

DATA[39] = dict(
    sintesi=[
        "Il CTF finale mette alla prova tutto il corso: sei sfide sul bersaglio, dalla recon al web.",
        "Le flag sono generate a runtime (diverse per macchina) e le convalida il docente.",
        "Recon, find, permessi, SQLi, LFI, base64: ogni sfida usa un'abilita' diversa.",
        "Vale tutto cio' che hai imparato; conta metodo, non fortuna.",
        "Solo nel laboratorio isolato: le stesse tecniche fuori sono reato.",
    ],
    glossario=[
        ("CTF a squadre", "gara di sicurezza a squadre, a punti"),
        ("Flag a runtime", "flag generate al momento, diverse per ogni macchina"),
        ("Recon", "ricognizione: trovare host, porte, servizi"),
        ("SQLi / LFI", "SQL injection / Local File Inclusion"),
        ("Path traversal", "risalire le cartelle con ../"),
    ],
    errori=[
        "Non rileggere il testo della sfida.",
        "Consegnare una flag di un'altra postazione (sono diverse per macchina).",
        "Perdere tempo su una sfida difficile trascurando quelle sicure.",
    ],
    domande=[
        "Come trovi un servizio nascosto su una porta insolita?",
        "Come estrai un segreto dal database con una UNION?",
        "Come leggi un file riservato con il path traversal?",
        "Come decodifichi un messaggio offuscato?",
        "Quali abilita' di recon usi nella prima sfida?",
    ],
    collegamenti=[
        "Lezione 38: la preparazione e la strategia di squadra.",
        "Lezioni 8-9, 12-13, 17, 32: le tecniche richieste dalle sfide.",
        "Lezione 40: il debrief e le difese apprese.",
    ],
)

DATA[40] = dict(
    sintesi=[
        "Il filo di tutto il corso: si impara ad attaccare per capire come si difende.",
        "Per ogni attacco c'e' una difesa principale: SQLi->query parametrizzate, XSS->escape, sniffing->cifratura, ecc.",
        "Un attacco a catena si spezza chiudendo anche un solo anello.",
        "Le buone abitudini digitali valgono piu' di molti strumenti: password, 2FA, aggiornamenti, backup, attenzione ai link.",
        "Le competenze si usano per proteggere, mai per attaccare sistemi altrui.",
    ],
    glossario=[
        ("Debrief", "l'analisi finale di cio' che si e' imparato"),
        ("Query parametrizzate", "la difesa contro la SQL injection"),
        ("Escape dell'output", "la difesa contro l'XSS"),
        ("Rate limiting / 2FA", "difese contro il brute force"),
        ("Difesa in profondita'", "piu' strati di protezione"),
    ],
    errori=[
        "Riusare la stessa password su piu' siti.",
        "Ignorare gli aggiornamenti di sistema e app.",
        "Cliccare link e allegati senza controllare il dominio.",
        "Usare le competenze acquisite fuori da un contesto autorizzato.",
    ],
    domande=[
        "Abbina: SQLi, XSS, brute force, sniffing, phishing alle loro difese principali.",
        "Perche' basta chiudere un anello per fermare una catena d'attacco?",
        "Quali abitudini digitali proteggono di piu' nella vita di tutti i giorni?",
        "Perche' l'uso etico e legale di queste competenze e' parte della professione?",
    ],
    collegamenti=[
        "Tutte le lezioni: qui si tirano le fila.",
        "Lezione 2: il patto etico firmato all'inizio.",
        "Lezioni 27, 35, 36, 37: il blocco difensivo del corso.",
    ],
)


def snippet(num):
    """Genera il codice della chiamata comune.studio(...) via repr() (sempre valido)."""
    d = DATA[num]
    def lst(items):
        return "[\n            " + ",\n            ".join(repr(x) for x in items) + ",\n        ]"
    def gloss(items):
        return "[\n            " + ",\n            ".join("(%r, %r)" % (a, b) for a, b in items) + ",\n        ]"
    parts = ["    comune.studio(\n        d,"]
    if d.get("sintesi"):
        parts.append("        sintesi=%s," % lst(d["sintesi"]))
    if d.get("glossario"):
        parts.append("        glossario=%s," % gloss(d["glossario"]))
    if d.get("errori"):
        parts.append("        errori=%s," % lst(d["errori"]))
    if d.get("domande"):
        parts.append("        domande=%s," % lst(d["domande"]))
    if d.get("collegamenti"):
        parts.append("        collegamenti=%s," % lst(d["collegamenti"]))
    parts.append("    )\n")
    return "\n".join(parts)


def process(num):
    path = os.path.join(SRC, "lez%02d.py" % num)
    src = open(path, encoding="utf-8").read()
    if "comune.studio(" in src:
        return "gia' presente, salto"
    if "import comune" not in src:
        src = src.replace("# -*- coding: utf-8 -*-\n",
                          "# -*- coding: utf-8 -*-\nimport comune\n", 1)
    # inserisci prima della riga d.h2("Punteggio della Lezione ...")
    m = re.search(r'^\s*d\.h2\("Punteggio del', src, re.M)
    if not m:
        return "ANCORA 'Punteggio' non trovata!"
    ins = snippet(num) + "\n"
    src = src[:m.start()] + ins + src[m.start():]
    open(path, "w", encoding="utf-8").write(src)
    return "arricchita"


if __name__ == "__main__":
    for num in sorted(DATA):
        print("L%02d: %s" % (num, process(num)))
