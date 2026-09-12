# -*- coding: utf-8 -*-
import comune
NUM = 38
SLUG = "preparazione-ripasso-ctf"
TITOLO = "Preparazione e ripasso per il CTF"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 15 min ripasso · 90 min allenamento · 15 min strategia.",
        "**Obiettivo:** ripassare tutte le abilità del corso con un allenamento a sfide, "
        "per arrivare pronti al CTF finale a squadre (Lezione 39).",
        "**Al termine sai:** muoverti in fretta tra pipe, base64, cracking e analisi log, "
        "e sai come organizzarti in squadra per un CTF.",
        "**Flag in palio:** 4 flag di allenamento (70 punti).",
    ])

    d.h1("Parte 1 · La mappa delle abilità (15 min)")
    d.p("Un CTF (Capture The Flag) è una gara di sicurezza a sfide: ogni flag vale punti. "
        "Vince chi ne raccoglie di più. Per riuscirci devi sapere dove cercare. Ecco cosa "
        "hai imparato, per blocco.")
    d.table(["Area", "Cosa sai fare", "Lezioni"], [
        ["Linux/bash", "muoverti, pipe, redirezioni, script", "3-6"],
        ["Recon", "scoprire host, porte, servizi, footprint", "7-10"],
        ["Web", "SQLi, XSS, cookie, brute force, LFI", "11-18"],
        ["Password/cripto", "hash, cracking, cifratura, TLS", "19-22"],
        ["Rete", "sniffing, ARP/DNS spoofing, difese", "23-27"],
        ["Social/phishing", "riconoscere inganni e pagine civetta", "28-30"],
        ["Malware", "analisi statica e dinamica, IOC", "31-34"],
        ["Difesa", "hardening, log, incident response", "35-37"],
    ], widths=[1900, 4626, 2500])

    d.h1("Parte 2 · Allenamento a sfide (pratica, 90 min)")
    d.p("Sulla Kali `lab 38` prepara quattro mini sfide in `~/lab/lezione-38`, una per "
        "abilità. Falle tutte a tempo, come al CTF.")

    d.h2("Sfida A · Pipe e grep (+15)")
    d.code([
        "cd ~/lab/lezione-38",
        "grep FLAG rumore.txt",
    ])

    d.h2("Sfida B · Base64 (+15)")
    d.code(["cat segreto.b64 | base64 -d"])

    d.h2("Sfida C · Cracking MD5 (+20)")
    d.code([
        "cat hash.txt",
        "for w in $(cat wordlist.txt); do echo \"$(printf %s \"$w\" | md5sum | cut -d' ' -f1) $w\"; done | grep -f hash.txt",
        "lab38-verifica cracking <password>",
    ])

    d.h2("Sfida D · Analisi log (+20)")
    d.code([
        "grep FALLITO accessi.log | grep -oE \"10[0-9.]+\" | sort | uniq -c | sort -rn | head",
        "lab38-verifica log <ip>",
    ])

    d.box("blu", "Ripasso sul bersaglio (consigliato)", intro=(
        "Per il CTF web, rigioca le sfide del Blocco 4 sul bersaglio:"), items=[
        "lab 12 (SQLi), lab 14 (XSS), lab 15 (cookie), lab 16 (brute force), lab 17 (LFI).",
        "Rivedi anche la recon (lab 8-10) e la rete (lab 23-27).",
    ])

    d.h1("Parte 3 · Strategia di squadra (15 min)")
    d.box("verde", "Come si vince un CTF a squadre", items=[
        "Dividetevi per aree: chi è forte sul web, chi sui log, chi sul cracking.",
        "Leggete SEMPRE bene il testo della sfida: spesso il suggerimento è lì.",
        "Tenete un foglio condiviso con flag trovate e cose provate: non ripetete il lavoro.",
        "Partite dalle sfide facili (punti sicuri), poi le difficili.",
        "Annotate i comandi utili: al CTF non c'è tempo di reinventarli.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Un metodo per affrontare un CTF', "In un CTF non conta solo sapere le tecniche, conta il metodo. Regola numero uno: enumerare sempre e a fondo, perché quasi ogni sfida si sblocca con un'informazione trovata guardando meglio (una porta, un file, un commento). Regola due: leggere per intero il testo della sfida, spesso il suggerimento è lì. Regola tre: tenere appunti dei comandi e dei tentativi, per non ripetere il lavoro e per riusare ciò che funziona. Regola quattro: non fissarsi; se una sfida ti blocca, passa a un'altra e torna dopo con occhi freschi. Regola cinque: partire dalle sfide che danno punti sicuri prima di lanciarsi su quelle difficili. È lo stesso metodo, ordinato e paziente, che serve nel lavoro vero."),
        ],
        sintesi=[
            "Un CTF è una gara a sfide di sicurezza: ogni flag vale punti, vince chi ne fa di più.",
            "Per riuscirci devi sapere DOVE cercare: la mappa delle abilità del corso, per blocco.",
            'Allenarsi a tempo su sfide brevi (pipe, base64, cracking, log) rende automatici i gesti.',
            'In squadra: dividersi per aree, leggere bene i testi, tenere un foglio condiviso, partire dalle facili.',
            "Annotare i comandi utili: al CTF non c'è tempo di reinventarli.",
        ],
        glossario=[
            ('CTF', 'Capture The Flag: gara a sfide, ogni flag vale punti'),
            ('Flag', 'la stringa FLAG{...} che dimostra una sfida risolta'),
            ('Wordlist', 'lista usata per il cracking a dizionario'),
            ('Base64', 'codifica reversibile da riconoscere e decodificare'),
            ('Strategia di squadra', 'dividersi i compiti e condividere i risultati'),
        ],
        errori=[
            'Non leggere bene il testo della sfida (spesso contiene il suggerimento).',
            "Ripetere il lavoro già fatto da un compagno (serve un foglio condiviso).",
            'Buttarsi sulle sfide difficili prima di prendere i punti facili.',
        ],
        domande=[
            'Come troveresti una flag nascosta tra tante righe di rumore?',
            'Come decodifichi un messaggio in base64?',
            'Come rompi un hash MD5 con una wordlist?',
            "Come trovi l'IP di un attaccante in un log?",
            'Quali regole rendono efficace una squadra al CTF?',
        ],
        collegamenti=[
            "Tutte le lezioni: qui si ripassano le abilità del corso.",
            'Lezione 39: il CTF finale a squadre.',
            "Lezione 4, 20, 32, 36: pipe, cracking, base64, log usati nell'allenamento.",
        ],
    )


    d.h2("Punteggio della Lezione 38")
    d.table(["Sfida", "Abilità", "Punti"], [
        ["A", "pipe/grep", "15"],
        ["B", "base64", "15"],
        ["C", "cracking", "20"],
        ["D", "log", "20"],
    ], widths=[1500, 6026, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 38** · Preparazione e ripasso per il CTF (Blocco 10).",
        "**Tempi:** 15 min ripasso · 90 min allenamento · 15 min strategia.",
        "**Prerequisiti:** Kali (Lezione 2); utile la Banca (Lezione 12) per il ripasso web.",
        "**Deliverable studente:** 4 flag di allenamento (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Ripassare le abilità chiave con sfide rapide e autovalutanti.",
        "Introdurre il formato CTF e la strategia di squadra.",
        "Far sentire gli studenti pronti per la gara (Lezione 39).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea 4 sfide in `~/lab/lezione-38/` (rumore.txt, segreto.b64, "
        "hash.txt+wordlist.txt, accessi.log) e installa `lab38-verifica`.",
        "target.sh riavvia la Banca (per il ripasso web).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Sfida", "Soluzione", "Flag"], [
        ["A", "grep FLAG rumore.txt", "FLAG{ripasso_pipe}"],
        ["B", "base64 -d di segreto.b64", "FLAG{ripasso_base64}"],
        ["C", "hash MD5 = girasole2012 ; lab38-verifica cracking girasole2012", "FLAG{ripasso_cracking}"],
        ["D", "IP = 10.10.10.77 ; lab38-verifica log 10.10.10.77", "FLAG{ripasso_log}"],
    ], widths=[900, 5626, 2500])
    d.h1("Suggerimenti per la conduzione")
    d.bullets([
        "Cronometrare le sfide: crea l'atmosfera della gara.",
        "Formare già le squadre per la Lezione 39 e farle allenare insieme.",
        "Assegnare come compito il ripasso delle sfide web sul bersaglio.",
    ])
