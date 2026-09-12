# -*- coding: utf-8 -*-
import comune
NUM = 28
SLUG = "social-engineering"
TITOLO = "Social engineering: principi e casi reali"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 30 min teoria · 75 min pratica · 15 min difesa.",
        "**Obiettivo:** capire il social engineering, cioè l'arte di ingannare le persone "
        "invece dei computer, riconoscere le tecniche di manipolazione e come l'OSINT "
        "prepara il colpo.",
        "**Al termine sai:** riconoscere urgenza, autorità, scarsità, reciprocità e "
        "riprova sociale in un messaggio, e capire come un attaccante costruisce un "
        "pretesto credibile.",
        "**Flag in palio:** 2 flag (70 punti). Lezione sulla Kali (offline).",
    ])

    d.h1("Parte 1 · Bucare le persone (teoria, 30 min)")
    d.h2("Il caso reale")
    d.p("Il modo più facile per entrare in un sistema spesso non è tecnico: è chiedere. "
        "Una telefonata che finge di essere l'assistenza, una email che sembra del capo, "
        "un messaggio che mette fretta. Molti dei grandi attacchi degli ultimi anni sono "
        "iniziati così: qualcuno ha convinto una persona a dare una password o a cliccare "
        "un link. Non serve bucare il firewall se qualcuno ti apre la porta.")

    d.h2("Le leve della manipolazione")
    d.table(["Tecnica", "Come suona"], [
        ["Urgenza", "'subito o perdi l'accesso!' (non ti lascia pensare)"],
        ["Autorità", "'sono il dirigente, esegui' (ci si fida di chi comanda)"],
        ["Scarsità", "'solo per oggi, primi 10' (paura di perdere l'occasione)"],
        ["Reciprocità", "'ti ho aiutato, ora ricambia' (ci si sente in debito)"],
        ["Riprova sociale", "'lo hanno già fatto tutti' (istinto del gregge)"],
    ], widths=[2200, 6826])

    d.h2("Prima l'OSINT, poi il colpo")
    d.p("Un buon inganno è su misura. L'attaccante raccoglie informazioni (come nel "
        "Blocco 3): il nome del capo, un progetto in corso, l'hobby della vittima. Poi "
        "costruisce un pretesto credibile. Piu' sa di te, più è convincente. Anche il "
        "nome del tuo cane, postato sui social, può diventare la password che indovina o "
        "la risposta alla domanda di sicurezza.")

    d.h1("Parte 2 · Riconosci i trucchi (pratica, 75 min)")
    d.p("Sulla Kali `lab 28` semina cinque messaggi intercettati e un dossier OSINT.")

    d.h2("Passo 1 · Abbina ogni messaggio alla tecnica (+40)")
    d.p("Leggi i cinque messaggi e assegna a ciascuno la sua leva.")
    d.code([
        "cd ~/lab/lezione-28",
        "cat messaggi.txt",
        "# tecniche: urgenza autorita scarsita reciprocita riprovasociale",
        "lab28-verifica abbina <t1> <t2> <t3> <t4> <t5>",
    ])

    d.h2("Passo 2 · Trova l'indizio per il pretesto (+30)")
    d.p("Nel dossier c'è un dettaglio che un attaccante userebbe subito. Trovalo.")
    d.code([
        "cat dossier.txt",
        "lab28-verifica indizio <parola>",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Difendersi dall'inganno", items=[
        "Fermarsi quando qualcosa mette fretta: l'urgenza è il trucco più comune.",
        "Verificare l'identità per un altro canale: se il 'capo' scrive, richiama al "
        "numero conosciuto, non a quello del messaggio.",
        "Nessuno del supporto chiede mai la tua password: è sempre una truffa.",
        "Meno informazioni pubbliche = pretesti più difficili da costruire.",
        "In azienda: procedure chiare per richieste sensibili, e una cultura in cui "
        "chiedere conferma non è maleducazione.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Il ciclo del social engineering e i casi reali', "Un attacco basato sulle persone segue un ciclo: raccolta di informazioni (OSINT), costruzione di un pretesto credibile, contatto e sfruttamento della fiducia, e infine l'azione (farsi dare una password, un bonifico, l'accesso a una stanza). I casi reali sono ovunque: la 'truffa del CEO', in cui una email che sembra del capo ordina all'ufficio contabilità un bonifico urgente; il finto tecnico che chiama per 'risolvere un problema' e si fa dettare le credenziali; l'SMS del corriere con il link al pagamento di due euro. Funzionano perché sfruttano automatismi umani, non falle tecniche: ecco perché nessun firewall li ferma e l'unica difesa è una persona informata e la buona abitudine di verificare per un secondo canale."),
        ],
        sintesi=[
            "Il social engineering inganna le persone, non i computer: spesso è la via più facile.",
            "Le leve classiche: urgenza, autorità, scarsità, reciprocità, riprova sociale.",
            "Prima l'OSINT, poi il colpo: più l'attaccante sa di te, più è credibile.",
            "Nessuno del supporto chiede la password: è sempre una truffa.",
            "Difesa: fermarsi davanti all'urgenza, verificare per un altro canale, ridurre le info pubbliche.",
        ],
        glossario=[
            ('Social engineering', 'manipolare le persone per ottenere accessi o dati'),
            ('Pretexting', 'costruire una storia credibile per ingannare'),
            ("Urgenza / autorità", 'leve che spingono ad agire senza pensare o a obbedire'),
            ("Scarsità / reciprocità", "paura di perdere l'occasione / sentirsi in debito"),
            ('Riprova sociale', "'lo fanno tutti', l'istinto del gregge"),
            ('Vishing / smishing', 'social engineering per telefono / via SMS'),
        ],
        errori=[
            'Agire di fretta quando un messaggio mette urgenza.',
            "Fidarsi di chi dice di avere autorità senza verificare.",
            'Dare informazioni personali che diventano pretesti.',
            "Comunicare password a chiunque, anche al 'supporto'.",
        ],
        domande=[
            'Cita tre leve di manipolazione e un esempio per ognuna.',
            "Perché l'OSINT rende un inganno più efficace?",
            "Come verifichi in sicurezza una richiesta 'del capo' urgente?",
            "Perché un vero supporto non chiede mai la password?",
            'Come riduci la tua esposizione al social engineering?',
        ],
        collegamenti=[
            "Lezione 7: l'OSINT che alimenta il pretexting.",
            'Lezione 29: il phishing, social engineering applicato al web.',
            'Lezione 30: riconoscere e difendersi dagli inganni.',
        ],
    )


    d.h2("Punteggio della Lezione 28")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Riconosci le tecniche", "lab28-verifica abbina", "40"],
        ["Indizio per il pretesto", "lab28-verifica indizio", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 28** · Social engineering (Blocco 7, apertura).",
        "**Tempi:** 30 min teoria · 75 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2). Nessun bersaglio.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire che l'anello debole sono le persone.",
        "Riconoscere le cinque leve classiche di manipolazione.",
        "Collegare OSINT (Blocco 3) e pretexting; preparare phishing (L29-L30).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `~/lab/lezione-28/messaggi.txt` (5 messaggi, una tecnica ciascuno) e "
        "`dossier.txt` (profilo con l'indizio 'Fido'), e installa `lab28-verifica`.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "abbina: urgenza autorita scarsita reciprocita riprovasociale (ordine 1..5)",
         "FLAG{smaschero_i_trucchi}"],
        ["2", "indizio: Fido (il nome del cane)", "FLAG{pretesto_costruito}"],
    ], widths=[700, 5926, 2400])
    d.p("Mappa messaggi->tecnica: 1 urgenza, 2 autorita, 3 scarsita, 4 reciprocita, 5 "
        "riprova sociale.")
    d.h1("Suggerimenti per la conduzione")
    d.bullets([
        "Portare casi reali recenti (truffe del finto capo, finto supporto tecnico, SMS "
        "di consegna pacchi): coinvolgono molto i ragazzi.",
        "Chiedere agli studenti di raccontare un tentativo che hanno ricevuto: quasi tutti "
        "ne hanno uno.",
    ])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["abbina non passa", "cinque parole in ordine 1..5, minuscole, senza accenti "
         "(autorita, non autorità)"],
        ["indizio non passa", "la parola è il nome del cane: Fido"],
    ], widths=[2800, 6226])
