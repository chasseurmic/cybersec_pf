# -*- coding: utf-8 -*-
import comune
NUM = 26
SLUG = "dns-spoofing"
TITOLO = "DNS spoofing e attacchi in rete locale"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire il DNS (la rubrica di internet che traduce i nomi in "
        "indirizzi) e come, controllandolo, si può mandare una vittima su un sito "
        "civetta per rubarle le credenziali.",
        "**Al termine sai:** far funzionare un DNS 'canaglia', dirottare una vittima verso "
        "un tuo sito e capire perché fidarsi del DNS sbagliato è pericoloso.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · La rubrica di internet (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Quando scrivi il nome di un sito, il computer chiede al DNS 'a quale indirizzo IP "
        "corrisponde?' e poi ci si collega. È come chiedere un numero all'elenco "
        "telefonico. Ma se qualcuno ti dà il numero sbagliato, chiami la persona "
        "sbagliata senza accorgertene. Il DNS spoofing è questo: rispondere con un IP "
        "falso, per mandare la vittima su un sito controllato dall'attaccante, magari "
        "identico all'originale, dove digitera' le sue credenziali.")

    d.h2("Perché funziona")
    d.p("Il computer si fida del DNS che gli è stato indicato (di solito dato dal router "
        "via DHCP). Se un attaccante controlla quel DNS, o si mette in mezzo (ARP "
        "spoofing della lezione scorsa) e risponde lui, decide dove vai. E se il sito "
        "civetta assomiglia a quello vero, la vittima non sospetta nulla.")

    d.h1("Parte 2 · Dirotta la vittima (pratica, 80 min)")
    d.p("Scenario: il bersaglio usa la Kali come DNS e ogni pochi secondi 'aggiorna', "
        "risolvendo `aggiornamenti.banca.local` e inviando le sue credenziali all'IP che "
        "riceve. Sul bersaglio `lab 26` avvia la vittima; sulla Kali `lab 26` installa il "
        "DNS canaglia e il sito civetta.")

    d.h2("Passo 1 · Avvia il DNS canaglia")
    d.p("Risponde a qualsiasi nome con l'indirizzo della tua Kali.")
    d.code([
        "cd ~/lab/lezione-26",
        "cat dnsspoof.py",
        "sudo python3 dnsspoof.py 10.10.10.5 53",
        "# lascialo girare in questo terminale",
    ])

    d.h2("Passo 2 · Avvia il sito civetta e cattura (+40)")
    d.p("In un ALTRO terminale, accendi il sito che raccoglie quello che la vittima invia.")
    d.code([
        "sudo python3 fakeweb.py",
        "# dopo pochi secondi comparira':  VITTIMA ... ha inviato: ... FLAG{...}",
    ])

    d.h2("Passo 3 · Leggi la password rubata (+30)")
    d.code(["lab26-verifica <la-password-catturata>"])

    d.box("blu", "Come si concatena col resto", items=[
        "Se non controlli già il DNS, ti ci metti in mezzo con l'ARP spoofing (Lezione 25).",
        "Il sito civetta può essere una copia perfetta del sito vero (Lezione 29, phishing).",
        "Con HTTPS la vittima vedrebbe un avviso sul certificato (Lezione 22): un motivo "
        "in più per non ignorarlo mai.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Difendersi dal DNS spoofing", items=[
        "Usare DNS fidati e, dove possibile, DNS cifrato (DoH/DoT): più difficile da "
        "manomettere.",
        "HTTPS ovunque: il sito civetta senza un certificato valido fa scattare l'avviso.",
        "Su reti gestite: DHCP snooping e protezioni contro i server DHCP/DNS abusivi.",
        "Diffidare degli avvisi di sicurezza del browser: non sono un fastidio, sono un "
        "allarme.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Come funziona davvero il DNS (e dove si rompe)', "Il DNS è una gerarchia. Quando chiedi un nome, si parte dai server radice, che indicano i server del dominio di primo livello (.it, .com), che a loro volta indicano i server autoritativi del dominio specifico, che danno la risposta finale. Per non rifare tutto ogni volta, le risposte vengono messe in cache per un tempo detto TTL. Ogni punto di questa catena, e ogni cache lungo la strada, è un possibile bersaglio: se un attaccante riesce a inserire una risposta falsa (o controlla il DNS che usi), ti manda dove vuole lui. La difesa moderna è DNSSEC, che firma le risposte DNS in modo che non si possano falsificare, e il DNS cifrato (DoH/DoT), che impedisce di manometterle o spiarle lungo il percorso."),
        ],
        sintesi=[
            'Il DNS traduce i nomi in indirizzi IP: se qualcuno risponde con un IP falso, ti manda dove vuole lui.',
            "Controllando il DNS (o mettendosi in mezzo), l'attaccante dirotta la vittima su un sito civetta.",
            "Un DNS canaglia risponde a ogni nome con l'IP dell'attaccante; il sito civetta cattura le credenziali.",
            'Con HTTPS valido la vittima vedrebbe un avviso sul certificato: un motivo per non ignorarlo mai.',
            'Difesa: DNS fidati e cifrati (DoH/DoT), HTTPS ovunque, protezioni contro DHCP/DNS abusivi.',
        ],
        glossario=[
            ('DNS', 'il servizio che traduce i nomi (banca.local) in indirizzi IP'),
            ('Risoluzione dei nomi', "l'operazione di trovare l'IP di un nome"),
            ('DNS spoofing', 'rispondere con un IP falso per dirottare la vittima'),
            ('DNS canaglia', "un server DNS controllato dall'attaccante"),
            ('Sito civetta', 'una copia del sito vero, fatta per rubare le credenziali'),
            ('DoH / DoT', "DNS cifrato (over HTTPS / over TLS), più difficile da manomettere"),
        ],
        errori=[
            'Usare DNS non fidati o forniti da chiunque sulla rete.',
            'Ignorare gli avvisi del browser (dominio o certificato sospetti).',
            "Non usare HTTPS: senza, il sito civetta è indistinguibile a occhio.",
        ],
        domande=[
            "Perché controllare il DNS permette di dirottare una vittima?",
            'Cosa fa un DNS canaglia?',
            'Come si combina il DNS spoofing con un sito civetta?',
            "Perché HTTPS valido aiuta a smascherare l'inganno?",
            'Quali difese riducono il rischio di DNS spoofing?',
        ],
        collegamenti=[
            "Lezione 25: l'ARP spoofing per intercettare le richieste DNS.",
            'Lezione 29: il sito civetta approfondito (phishing).',
            "Lezione 22: certificati e avvisi, l'ancora di salvezza.",
        ],
    )


    d.h2("Punteggio della Lezione 26")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Cattura sul sito civetta", "dnsspoof + fakeweb", "40"],
        ["Password rubata", "lab26-verifica", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 26** · DNS spoofing e attacchi in rete locale (Blocco 6).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali e bersaglio sulla stessa rete interna; Python3 (presente).",
        "**Deliverable studente:** 2 flag (70 punti) + un DNS canaglia e un sito civetta.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire il DNS e come il controllo del DNS permette di dirottare le vittime.",
        "Costruire un DNS canaglia e un sito civetta (solo stdlib).",
        "Collegare a ARP spoofing (L25), HTTPS (L22) e phishing (L29).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh avvia `lab26-client.service`: la vittima risolve "
        "`aggiornamenti.banca.local` usando il DNS 10.10.10.5 (la Kali) e invia in POST "
        "le credenziali all'IP ottenuto.",
        "kali.sh installa `dnsspoof.py` (server DNS che risponde a tutto con un IP fisso, "
        "porta 53) e `fakeweb.py` (sito civetta che stampa ciò che riceve), più "
        "`lab26-verifica`.",
        "Catena verificata: DNS canaglia -> la vittima risolve alla Kali -> invia le "
        "credenziali al sito civetta, che mostra la flag.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["2", "dnsspoof.py 10.10.10.5 53 + fakeweb.py ; leggere la POST della vittima",
         "FLAG{dns_spoofing_riuscito}"],
        ["3", "password catturata = HomeBanking#9 ; lab26-verifica HomeBanking#9",
         "FLAG{vittima_dirottata}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["dnsspoof: Permission denied :53", "la porta 53 richiede root: usare sudo"],
        ["porta 53 occupata", "fermare systemd-resolved sul momento: "
         "`sudo systemctl stop systemd-resolved` (sulla Kali), oppure usare un'altra porta"],
        ["il sito civetta non riceve nulla", "verificare che dnsspoof giri e che il client "
         "del bersaglio sia attivo (`systemctl status lab26-client`)"],
        ["il MITM del DNS su altra rete", "qui la vittima punta già alla Kali come DNS; "
         "per il caso reale servirebbe l'ARP spoofing della Lezione 25"],
    ], widths=[3000, 6026])
    d.h1("Nota di progetto")
    d.p("Il DNS canaglia e il sito civetta sono in sola stdlib e la catena è stata "
        "provata: la vittima punta direttamente alla Kali come DNS (scenario 'rete con "
        "attaccante che controlla il DNS/DHCP'). Il collegamento con l'ARP spoofing (per "
        "intercettare il DNS di una vittima che usa un altro server) è spiegato nel "
        "testo; l'esecuzione combinata è da provare su x86 come la Lezione 25.")
