# -*- coding: utf-8 -*-
import comune
NUM = 32
SLUG = "analisi-statica-sandbox"
TITOLO = "Analisi statica di base in sandbox"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** analizzare un file sospetto SENZA eseguirlo (analisi statica), per "
        "capire cosa fa in modo sicuro, ricavando indicatori utili alla difesa.",
        "**Al termine sai:** usare `file`, `strings`, `sha256sum` e `base64` per esaminare "
        "un campione, trovare URL/comandi nascosti e calcolarne l'impronta (IOC).",
        "**Flag in palio:** 3 flag (80 punti). Sandbox isolata; il campione è innocuo.",
    ])

    d.h1("Parte 1 · Guardare senza aprire (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Un analista che riceve un file sospetto non lo apre col doppio clic: sarebbe come "
        "aprire un pacco bomba per vedere cosa c'è dentro. Prima fa l'analisi statica: "
        "guarda il file dall'esterno e legge ciò che contiene senza eseguirlo. Gia' così "
        "si scopre moltissimo: che tipo di file è, quali indirizzi contatta, quali "
        "comandi nasconde. Il campione di oggi è finto e innocuo, ma le tecniche sono "
        "quelle vere.")

    d.h2("La cassetta degli attrezzi dell'analista")
    d.table(["Comando", "Cosa rivela"], [
        ["`file`", "che tipo di file è (eseguibile, script, dati...)"],
        ["`strings`", "tutto il testo leggibile dentro il file (URL, comandi, messaggi)"],
        ["`sha256sum`", "l'impronta unica del file, l'indicatore (IOC) per riconoscerlo"],
        ["`base64 -d`", "decodifica le parti offuscate in base64"],
    ], widths=[2200, 6826])
    d.p("Un IOC (Indicator Of Compromise) è un indizio che permette di riconoscere una "
        "minaccia: l'hash di un file, un IP, un dominio. Gli antivirus e i team di sicurezza "
        "si scambiano gli IOC per proteggere tutti.")

    d.h1("Parte 2 · Smonta il campione (pratica, 80 min)")
    d.p("Sulla Kali `lab 32` crea `~/lab/lezione-32/campione.bin` (innocuo, solo dati).")

    d.h2("Passo 1 · Tipo e stringhe sospette (+30)")
    d.code([
        "cd ~/lab/lezione-32",
        "file campione.bin",
        "strings campione.bin",
        "strings campione.bin | grep FLAG      # una flag è in chiaro nel file",
    ])
    d.p("Nota anche il C2 (`http://10.66.66.66/...`) e il mutex: indizi tipici del malware.")

    d.h2("Passo 2 · L'impronta del file, l'IOC (+25)")
    d.code([
        "sha256sum campione.bin",
        "lab32-verifica hash <sha256>",
    ])

    d.h2("Passo 3 · Decodifica la parte nascosta (+25)")
    d.p("Una riga è offuscata in base64. Decodificala per leggere il comando nascosto.")
    d.code([
        "strings campione.bin | grep cfg_base64",
        "echo \"<la-stringa-base64>\" | base64 -d",
        "# dentro c'è un'altra flag",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "A cosa serve l'analisi statica, per difendere", items=[
        "Ricavare gli IOC (hash, IP, domini) e bloccarli su firewall e antivirus.",
        "Capire cosa farebbe il malware senza correre rischi (nessuna esecuzione).",
        "Condividere gli indicatori con la comunità per proteggere altri.",
        "Riconoscere l'offuscamento (base64 e simili): un file 'normale' non nasconde "
        "comandi cifrati.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("Cosa c'è dentro un eseguibile e i limiti dell'analisi", "Un programma compilato ha un formato preciso: ELF su Linux, PE su Windows. È diviso in sezioni (il codice, i dati, le stringhe) e contiene informazioni che l'analisi statica sa leggere senza eseguire nulla: che tipo di file è, quali librerie usa, quali testi contiene (URL, comandi, messaggi), qual è la sua impronta hash. Tutto questo si ricava a rischio zero. L'analisi statica ha però un limite: un malware può offuscare o cifrare le sue parti pericolose, che compaiono solo quando gira. Per questo la statica e la dinamica sono complementari: la prima dice cosa un file potrebbe fare e dà indicatori immediati (l'hash, gli URL), la seconda mostra cosa fa davvero una volta avviato in una sandbox."),
        ],
        sintesi=[
            "L'analisi statica esamina un file senza eseguirlo: è il modo sicuro di capire cosa fa.",
            'file identifica il tipo; strings mostra il testo leggibile (URL, comandi, C2).',
            "sha256sum calcola l'impronta unica del file: un IOC per riconoscerlo ovunque.",
            "base64 e simili offuscano: un file 'normale' non nasconde comandi codificati.",
            "Difesa: ricavare gli IOC e bloccarli, condividerli con la comunità.",
        ],
        glossario=[
            ('Analisi statica', 'studiare un file senza eseguirlo'),
            ('file', 'comando che identifica il tipo di un file'),
            ('strings', 'estrae il testo leggibile contenuto in un file'),
            ('sha256sum', "calcola l'impronta (hash) del file"),
            ('IOC', 'Indicator Of Compromise: indizio per riconoscere una minaccia'),
            ('base64', 'codifica reversibile spesso usata per offuscare'),
        ],
        errori=[
            'Fare doppio clic su un file sospetto invece di analizzarlo.',
            'Ignorare stringhe come URL, IP o mutex: sono indizi preziosi.',
            "Passare a base64 -d anche il prefisso 'cfg=': va decodificata solo la stringa.",
        ],
        domande=[
            'Cosa rivela strings su un file sospetto?',
            "Cos'è un IOC e perché l'hash del file ne è uno?",
            'Come riconosci una parte offuscata e come la decodifichi?',
            "Perché l'analisi statica è sicura?",
            'A cosa serve condividere gli IOC?',
        ],
        collegamenti=[
            'Lezione 31: i tipi di malware, contesto di questa analisi.',
            "Lezione 34: l'analisi dinamica, complementare alla statica.",
            'Lezione 36: usare gli IOC per il rilevamento.',
        ],
    )


    d.h2("Punteggio della Lezione 32")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Stringhe sospette", "strings | grep FLAG", "30"],
        ["Impronta IOC", "sha256sum ; lab32-verifica hash", "25"],
        ["Config offuscata", "base64 -d", "25"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 32** · Analisi statica di base in sandbox (Blocco 8).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2), ambiente isolato senza internet.",
        "**Deliverable studente:** 3 flag (80 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Analisi statica: esaminare un file senza eseguirlo.",
        "Usare file/strings/sha256sum/base64; concetto di IOC.",
        "Riconoscere offuscamento e indicatori (C2, mutex).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `campione.bin`: file di soli dati (NON eseguibile) con stringhe "
        "sospette, un C2 finto, un mutex e una config base64. Installa `lab32-verifica`.",
        "La flag delle stringhe è in chiaro; quella base64 è offuscata; l'hash si "
        "verifica ricalcolandolo (robusto).",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "strings campione.bin | grep FLAG", "FLAG{stringhe_rivelatrici}"],
        ["2", "sha256sum campione.bin ; lab32-verifica hash <valore>", "FLAG{impronta_del_file}"],
        ["3", "riga cfg_base64 ; base64 -d", "FLAG{comando_nascosto}"],
    ], widths=[700, 5626, 2700])
    d.p("La config base64 decodifica in: 'esegui il payload alle 03:00 e cifra i file "
        "FLAG{comando_nascosto}'. Su Kali usare `base64 -d`.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["base64 -d dà errore", "assicurarsi di passare SOLO la stringa base64 (senza "
         "'cfg_base64='); su Kali il flag è `-d`"],
        ["hash non combacia", "usare sha256sum sullo stesso file `campione.bin`"],
        ["strings non c'è", "è in binutils; presente su Kali"],
    ], widths=[2800, 6226])
    d.h1("Nota di sicurezza")
    d.p("Il campione è deliberatamente inerte (dati, non codice): nessun rischio anche se "
        "aperto per sbaglio. È l'occasione per ribadire che con file REALI non si fa mai "
        "il doppio clic: prima analisi statica, in sandbox.")
