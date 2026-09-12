# -*- coding: utf-8 -*-
import comune
NUM = 27
SLUG = "difese-di-rete"
TITOLO = "Difese di rete: segmentazione, firewall, IDS"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** passare dalla parte del difensore (blue team): chiudere ciò che "
        "è esposto con un firewall e accorgersi di chi scansiona con un IDS.",
        "**Al termine sai:** scrivere una regola di firewall per bloccare una porta, "
        "capire la segmentazione della rete e come un IDS a porte esca rileva le scansioni.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Difendere una rete (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Nei blocchi scorsi hai attaccato: scoperto host, scansionato porte, sniffato "
        "traffico, dirottato vittime. Ora giri la medaglia. Un buon difensore riduce la "
        "superficie d'attacco (meno porte aperte), separa le reti (se una parte cade, le "
        "altre reggono) e mette dei sensori che avvisano quando qualcuno prova ad "
        "attaccare. Difendere non è un muro solo: sono più strati.")

    d.h2("I tre pilastri")
    d.table(["Difesa", "Cosa fa", "Esempio"], [
        ["Firewall", "decide quale traffico passa e quale no", "iptables, nftables, ufw"],
        ["Segmentazione", "divide la rete in zone isolate", "VLAN, sottoreti separate"],
        ["IDS/IPS", "rileva (e blocca) attività sospette", "Snort, Suricata, porte esca"],
    ], widths=[1800, 4226, 3000])

    d.h2("Il firewall in una riga")
    d.p("Un firewall è una lista di regole: per ogni pacchetto decide se accettarlo "
        "(ACCEPT) o buttarlo (DROP). Bloccare una porta significa aggiungere una regola "
        "di DROP per quella porta.")
    d.code([
        "sudo iptables -A INPUT -p tcp --dport 9099 -j DROP   # blocca la porta 9099",
        "sudo iptables -L INPUT -n --line-numbers             # elenca le regole",
    ])

    d.h1("Parte 2 · Difendi il bersaglio (pratica, 80 min)")
    d.p("Oggi lavori SUL bersaglio (via SSH, come amministratore). Sul bersaglio `lab 27` "
        "accende un servizio insicuro su :9099 e un IDS a porte esca.")

    d.h2("Passo 1 · Chiudi la porta insicura (+40)")
    d.p("Il servizio su :9099 non serve a nessuno ed è esposto. Chiudilo col firewall e "
        "verifica.")
    d.code([
        "# sul bersaglio (come root):",
        "sudo iptables -A INPUT -p tcp --dport 9099 -j DROP",
        "sudo lab27-verifica firewall",
        "",
        "# dalla Kali, controlla l'effetto:",
        "nmap -p 9099 10.10.10.20      # prima: open ; dopo la regola: filtered",
    ])

    d.h2("Passo 2 · Cogli lo scanner con l'IDS (+30)")
    d.p("L'IDS tiene aperte alcune porte esca (finti servizi): nessun utente vero le "
        "tocca, solo uno scanner. Provoca l'allarme scansionando da Kali, poi leggilo sul "
        "bersaglio.")
    d.code([
        "# dalla Kali, una scansione connect:",
        "nmap -sT -p 1-45000 10.10.10.20",
        "",
        "# sul bersaglio, leggi l'allarme (con la flag):",
        "cat /opt/lab/lab27/allarmi.log",
    ])
    d.box("blu", "Perché le porte esca funzionano", items=[
        "Sono porte che nessun servizio reale usa: una connessione lì è quasi sempre "
        "ostile.",
        "Toccare più porte esca in pochi secondi è la firma di una scansione.",
        "È l'idea dei veri IDS e degli honeypot: attirare e riconoscere l'attaccante.",
    ])

    d.h1("Parte 3 · Ribaltamento: la difesa in profondità (15 min)")
    d.box("verde", "Mettere insieme le difese", items=[
        "Chiudi tutto ciò che non serve: ogni porta aperta è una possibile porta "
        "d'ingresso.",
        "Segmenta: se il bersaglio fosse in una VLAN separata, uno scanner nella rete "
        "studenti non lo vedrebbe nemmeno.",
        "Rileva: un IDS che avvisa in tempo fa la differenza tra un tentativo e un "
        "disastro.",
        "Aggiorna e cifra (dai blocchi scorsi): il firewall non basta da solo.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Firewall, IDS e IPS: chi ferma e chi avvisa', "Un firewall decide quali pacchetti passano in base a regole; quelli moderni sono 'stateful', cioè ricordano le connessioni già aperte e lasciano passare le risposte attese. La strategia migliore è 'default-deny': si blocca tutto e si aprono solo le poche cose necessarie, l'opposto di aprire tutto e chiudere qualche buco. Accanto al firewall ci sono l'IDS, che rileva le attività sospette e avvisa, e l'IPS, che le rileva e le blocca automaticamente. La segmentazione, infine, divide la rete in zone (VLAN): se un attaccante entra in una zona non raggiunge le altre. Difesa in profondità vuol dire proprio questo: più strati diversi, così che superarne uno non basti a vincere."),
        ],
        sintesi=[
            "Difendere una rete significa ridurre la superficie d'attacco e accorgersi degli attacchi.",
            'Tre pilastri: firewall (cosa passa), segmentazione (dividere in zone), IDS (rilevare le minacce).',
            "Un firewall è una lista di regole: bloccare una porta = aggiungere una regola di DROP.",
            'Un IDS a porte esca (honeypot) rileva le scansioni: nessun utente vero tocca quelle porte.',
            "La difesa è a strati: chiudere l'inutile, segmentare, rilevare, aggiornare e cifrare.",
        ],
        glossario=[
            ('Firewall', 'filtra il traffico secondo regole (ACCEPT/DROP)'),
            ('iptables', 'lo strumento classico per gestire il firewall di Linux'),
            ('DROP', 'regola che scarta silenziosamente i pacchetti'),
            ('Segmentazione', 'dividere la rete in zone isolate (VLAN)'),
            ('IDS', "Intrusion Detection System: rileva attività sospette"),
            ('Honeypot / porta esca', "trappola che attira e smaschera l'attaccante"),
            ("Superficie d'attacco", "l'insieme dei punti da cui si può essere attaccati"),
        ],
        errori=[
            'Lasciare aperte porte e servizi inutili.',
            'Raccogliere log e regole ma non guardarli mai.',
            "Aprire una regola di firewall troppo larga 'per comodità'.",
            "Bloccare per sbaglio la porta 22 (SSH) e perdere l'accesso.",
        ],
        domande=[
            "Come blocchi una porta con iptables e come verifichi l'effetto?",
            "Cos'è la segmentazione e perché aiuta?",
            'Come fa un honeypot a porte esca a rilevare una scansione?',
            "Perché con -sS l'honeypot non scatta e con -sT si?",
            "Cosa vuol dire 'difesa in profondità'?",
        ],
        collegamenti=[
            'Lezione 8-9: le scansioni che qui impari a rilevare e bloccare.',
            'Lezione 35: hardening del singolo sistema.',
            'Lezione 36-37: log, rilevamento e risposta agli incidenti.',
        ],
    )


    d.h2("Punteggio della Lezione 27")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Chiudi la porta col firewall", "iptables DROP 9099 ; lab27-verifica", "40"],
        ["Rileva la scansione", "nmap da Kali ; allarmi.log sul bersaglio", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 27** · Difese di rete (Blocco 6, chiusura, blue team).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; accesso amministratore al bersaglio (per "
        "iptables serve root).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Vestire i panni del difensore: firewall, segmentazione, IDS.",
        "Scrivere una regola iptables e verificarne l'effetto da Kali.",
        "Capire il rilevamento delle scansioni con porte esca (honeypot).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh avvia `lab27-insicuro.service` (:9099, da chiudere) e "
        "`lab27-ids.service` (porte esca 2323/33060/44445). Genera le flag in "
        "`/opt/lab/lab27/flags.env`. Installa `lab27-verifica`.",
        "L'IDS scrive in `/opt/lab/lab27/allarmi.log` quando un IP tocca >=2 porte esca "
        "(firma di scansione).",
        "kali.sh: briefing e scansione per innescare l'IDS.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/lab27/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1", "sudo iptables -A INPUT -p tcp --dport 9099 -j DROP ; sudo lab27-verifica firewall",
         "FLAG_FW"],
        ["2", "nmap -sT ... da Kali ; cat /opt/lab/lab27/allarmi.log", "FLAG_IDS"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["lab27-verifica dice manca la regola", "la regola deve essere esattamente "
         "`INPUT -p tcp --dport 9099 -j DROP`"],
        ["l'IDS non scatta", "usare `nmap -sT` (connect scan) da Kali; con `-sS` (SYN) "
         "l'handshake non si completa e l'honeypot non accetta"],
        ["allarmi.log vuoto", "servono >=2 porte esca toccate; una scansione ampia le "
         "prende tutte; `systemctl status lab27-ids`"],
        ["ripristinare il firewall", "`sudo iptables -D INPUT -p tcp --dport 9099 -j DROP`"],
    ], widths=[3000, 6026])
    d.h1("Da PROVARE sul bersaglio reale x86")
    d.p("La logica dell'IDS è verificata in locale. La parte firewall usa iptables sul "
        "bersaglio (Ubuntu): da provare in aula che `iptables -C` riconosca la regola e "
        "che da Kali la porta 9099 risulti 'filtered'. Con `-sS` da root l'honeypot non "
        "scatta: indicare agli studenti `-sT`.")
    d.h1("Nota di sicurezza")
    d.p("La regola iptables non tocca SSH (porta 22), quindi non c'è rischio di perdere "
        "l'accesso. A fine lezione si può ripristinare con la regola -D indicata sopra.")
