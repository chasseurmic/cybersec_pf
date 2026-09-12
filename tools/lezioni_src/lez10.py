# -*- coding: utf-8 -*-
import comune
NUM = 10
SLUG = "enumerazione-servizi-banner"
TITOLO = "Enumerazione servizi e banner grabbing"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** dopo aver trovato le porte aperte, capire quale servizio gira e "
        "quale versione, perché la versione è la chiave per cercare vulnerabilità note.",
        "**Al termine sai:** catturare i banner a mano con netcat, far identificare i "
        "servizi a nmap (`-sV`), leggere le versioni e collegarle al concetto di CVE.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Chi sei e che versione hai (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Sapere che la porta 21 è aperta dice poco. Sapere che dietro c'è 'ProFTPD "
        "1.3.5' cambia tutto: quella versione ha una falla famosa, e a quel punto "
        "l'attaccante cerca l'exploit già pronto. Il passaggio dalla porta al "
        "servizio-con-versione si chiama enumerazione, ed è il ponte tra la "
        "ricognizione e l'attacco vero e proprio.")

    d.h2("Il banner")
    d.p("Molti servizi, appena ti colleghi, mandano un messaggio di saluto: il banner. "
        "Spesso contiene nome e versione del software. Leggerlo si chiama banner "
        "grabbing, e nel caso più semplice basta collegarsi con netcat e guardare cosa "
        "arriva.")
    d.code([
        "nc 10.10.10.20 2121        # collegati e leggi il saluto del servizio",
        "nc 10.10.10.20 22          # il banner di SSH mostra la versione di OpenSSH",
    ])

    d.h2("Enumerazione automatica con nmap")
    d.p("Fare banner grabbing a mano su decine di porte è lungo. nmap con `-sV` prova a "
        "identificare da solo servizio e versione di ogni porta aperta.")
    d.code([
        "nmap -sV -p 2121,2525 10.10.10.20    # identifica servizio e versione",
        "nmap -sV 10.10.10.20                 # su tutte le porte comuni",
    ])

    d.h2("Perché la versione è oro")
    d.p("Ogni software ha vulnerabilità scoperte nel tempo, catalogate con un codice CVE "
        "(Common Vulnerabilities and Exposures). Conoscere nome e versione permette di "
        "cercare se esistono falle note e strumenti pronti. Per questo un servizio che "
        "grida la propria versione fa un regalo all'attaccante.")

    d.h1("Parte 2 · Enumera la Banca (pratica, 80 min)")
    d.p("Sul bersaglio `lab 10` avvia due servizi con banner parlanti (uno stile FTP, uno "
        "stile SMTP); sulla Kali `lab 10` mostra la missione.")

    d.h2("Passo 1 · Banner grabbing a mano (+35)")
    d.p("Collegati al servizio sulla porta 2121 e leggi il suo banner: contiene la flag.")
    d.code([
        "nc 10.10.10.20 2121",
        "# se resta in attesa, premi Invio; per uscire, Ctrl+C",
    ])

    d.h2("Passo 2 · Identificazione con nmap (+35)")
    d.p("Fai identificare a nmap i due servizi. Nel banner del servizio SMTP-like sulla "
        "porta 2525 trovi versione e flag.")
    d.code([
        "nmap -sV -p 2121,2525 10.10.10.20",
    ])

    d.h2("Altri banner da esplorare (senza punti)")
    d.code([
        "nc 10.10.10.20 22                 # versione di OpenSSH",
        "curl -I http://10.10.10.20:8080   # header Server del sito",
        "whatweb http://10.10.10.20:8080   # tecnologie del sito",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Ogni banner è un'informazione regalata. Il difensore riduce al minimo ciò che "
        "i servizi raccontano di se'.")
    d.box("verde", "Meno chiacchiere, più sicurezza", items=[
        "Nascondere o ridurre i banner (togliere la versione dall'header Server, dai "
        "saluti dei servizi).",
        "Tenere i software aggiornati: se la versione trapela ma è l'ultima, le CVE note "
        "sono già chiuse.",
        "Spegnere i servizi inutili (meno banner, meno superficie): come i servizi "
        "2121 e 2525 di oggi, che non servivano a nessuno.",
        "Monitorare: una raffica di connessioni brevi a tante porte è un banner grabbing "
        "in corso.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("Dalla versione alla vulnerabilità: CVE e CVSS", "Quando conosci nome e versione di un servizio puoi cercare se ha falle note. Le vulnerabilità pubbliche hanno un codice CVE (es. CVE-2021-41773) e un punteggio di gravità CVSS da 0 a 10. Esistono database consultabili e strumenti che, data una versione, elencano le CVE che la riguardano. Ecco perché un banner che grida 'Apache 2.4.49' è un regalo: l'attaccante cerca la CVE, trova magari un exploit già pronto e lo prova. Il difensore ragiona al contrario: nasconde o riduce i banner, ma soprattutto aggiorna, perché se la versione è l'ultima le CVE note sono già chiuse e conoscere la versione non aiuta più l'attaccante."),
        ],
        sintesi=[
            "Sapere che una porta è aperta non basta: serve capire quale servizio gira e quale versione.",
            "Il banner è il saluto che molti servizi mandano appena ci si collega: spesso rivela nome e versione.",
            'Banner grabbing manuale con nc; automatico con nmap -sV; per il web con curl -I e whatweb.',
            "Nome + versione permettono di cercare vulnerabilità note (CVE): la versione è oro per l'attaccante.",
            'Difendersi: ridurre i banner e tenere il software aggiornato.',
        ],
        glossario=[
            ('Enumerazione servizi', "capire quale software e versione c'è dietro una porta"),
            ('Banner', 'il messaggio iniziale che un servizio invia alla connessione'),
            ('Banner grabbing', 'leggere il banner per identificare il servizio'),
            ('nc (netcat)', "il 'coltellino svizzero' TCP: si collega e mostra ciò che arriva"),
            ('nmap -sV', 'identifica automaticamente servizio e versione'),
            ('CVE', "codice che identifica una vulnerabilità nota (Common Vulnerabilities and Exposures)"),
        ],
        errori=[
            'Fermarsi alla porta senza identificare il servizio e la versione.',
            'Esporre banner con versioni dettagliate: un regalo a chi cerca CVE.',
            'Confondere nc (client) con un server: qui ci si collega per leggere.',
            "Non aggiornare: se la versione trapela ed è vecchia, le CVE sono aperte.",
        ],
        domande=[
            "Cos'è un banner e perché è utile a un attaccante?",
            'Come catturi a mano il banner di un servizio su una porta?',
            'Cosa aggiunge nmap -sV rispetto a una semplice scansione delle porte?',
            "Perché conoscere la versione di un servizio è così importante?",
            'Come riduce un difensore le informazioni rivelate dai banner?',
        ],
        collegamenti=[
            'Lezione 9: prima le porte aperte, qui il servizio dietro ciascuna.',
            "Lezione 7: whatweb e curl -I già visti sul web.",
            'Lezione 12+: sfruttare i servizi web identificati.',
        ],
    )


    d.h2("Punteggio della Lezione 10")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Banner grabbing a mano", "nc 10.10.10.20 2121", "35"],
        ["Identificazione con nmap", "nmap -sV -p 2121,2525", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 10** · Enumerazione servizi e banner grabbing (Blocco 3, chiude la recon).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; Python3 sul bersaglio.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Passare da 'porta aperta' a 'servizio X versione Y'.",
        "Fare banner grabbing manuale (nc) e automatico (nmap -sV).",
        "Collegare versione e vulnerabilità note (CVE); motivare la riduzione dei banner.",
    ])

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Installa `/usr/local/bin/lab10-banner` (server Python che invia un banner e chiude).",
        "Avvia `lab10-ftp.service` (porta 2121) e `lab10-smtp.service` (porta 2525), con "
        "banner che contengono le flag.",
        "Assicura SSH attivo (banner OpenSSH, esempio reale).",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Briefing di sola lettura (nc, nmap -sV, curl -I) e verifica bersaglio.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "nc 10.10.10.20 2121", "FLAG{banner_svela_il_servizio}"],
        ["2", "nmap -sV -p 2121,2525 10.10.10.20 (banner 2525)", "FLAG{versione_esposta}"],
    ], widths=[900, 5626, 2500])

    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["nc resta appeso senza banner", "il server invia subito il banner; premere Invio; "
         "se nulla, `systemctl status lab10-ftp` sul bersaglio"],
        ["nmap -sV non mostra il testo del banner", "usare `nc` per leggerlo per intero; "
         "nmap ne mostra una sintesi (servizio/versione)"],
        ["porte 2121/2525 chiuse", "rilanciare `lab 10` sul bersaglio"],
        ["fermare a fine blocco", "`systemctl disable --now lab10-ftp lab10-smtp`"],
    ], widths=[3000, 6026])

    d.h1("Nota didattica")
    d.p("I servizi 2121/2525 sono finti (solo banner) ma verosimili: bastano a insegnare "
        "il banner grabbing senza esporre servizi reali vulnerabili. Chiude il Blocco 3 "
        "(reconnaissance): host, porte, servizi. Dal Blocco 4 si passa all'attacco alle "
        "applicazioni web.")
