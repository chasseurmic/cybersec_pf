# -*- coding: utf-8 -*-
import comune
NUM = 25
SLUG = "arp-spoofing-mitm"
TITOLO = "ARP spoofing e MITM con scapy"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire l'attacco man-in-the-middle basato su ARP spoofing: "
        "fingersi un altro host per far passare da te il traffico altrui, e intercettarlo.",
        "**Al termine sai:** avvelenare una cache ARP con scapy, mettersi in mezzo a una "
        "comunicazione e leggere il traffico dirottato.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Mettersi in mezzo (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Su una rete locale, quando un computer vuole parlare con un altro, chiede via ARP "
        "'chi ha questo IP?' e si fida della prima risposta. Non c'è nessun controllo. "
        "Un attaccante può rispondere 'ce l'ho io!' anche se non è vero, e da quel "
        "momento il traffico destinato a quell'IP arriva a lui. Se si mette tra due "
        "interlocutori, li ascolta entrambi: è il man-in-the-middle, alla base di molti "
        "attacchi su wifi e reti aziendali.")

    d.h2("ARP non verifica niente")
    d.p("L'ARP è nato per essere semplice e veloce, in tempi in cui la rete era fidata. "
        "Non ha autenticazione: chiunque può mandare una risposta ARP falsa (spoofing) e "
        "avvelenare la cache degli altri. Questo difetto è ancora sfruttabile su moltissime "
        "reti locali.")

    d.h1("Parte 2 · Dirotta il traffico (pratica, 80 min)")
    d.p("Scenario: il bersaglio manda in continuazione credenziali a un 'server centrale' "
        "10.10.10.30 che in realta' non esiste. Finche' nessuno risponde per quell'IP, "
        "quei pacchetti non vanno da nessuna parte. Se ti fingi tu 10.10.10.30, arrivano a "
        "te. Sul bersaglio `lab 25` avvia il client; sulla Kali `lab 25` installa il tuo "
        "arpspoof. Trova l'interfaccia interna con `ip -br addr` (di solito eth1).")

    d.h2("Passo 1 · Avvelena la cache ARP del bersaglio")
    d.code([
        "cd ~/lab/lezione-25",
        "cat arpspoof.py",
        "sudo python3 arpspoof.py 10.10.10.20 10.10.10.30 eth1",
        "# lascialo girare: dice al bersaglio che 10.10.10.30 ha il TUO MAC",
    ])

    d.h2("Passo 2 · Intercetta il traffico dirottato (+40)")
    d.p("In un ALTRO terminale, ascolta i pacchetti che ora arrivano a te.")
    d.code([
        "sudo tcpdump -i eth1 -A udp port 9997",
        "# tra i pacchetti del bersaglio verso 'il server' c'è la flag",
    ])

    d.h2("Passo 3 · Leggi la password dirottata (+30)")
    d.code(["lab25-verifica <la-password-che-hai-intercettato>"])

    d.box("blu", "Per un MITM completo (teoria)", items=[
        "Si avvelenano entrambi i lati (vittima e gateway) e si attiva l'inoltro dei "
        "pacchetti (ip_forward) per non interrompere la comunicazione.",
        "Così l'attaccante è invisibile: le due parti continuano a parlarsi tramite lui.",
        "Se il traffico è cifrato (HTTPS), l'attaccante vede passare i dati ma non li "
        "legge (torna utile la Lezione 22).",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Difendersi dall'ARP spoofing", items=[
        "Cifrare tutto: anche intercettato, il traffico HTTPS/SSH resta illeggibile.",
        "Switch gestiti con Dynamic ARP Inspection e DHCP snooping: bloccano le risposte "
        "ARP false.",
        "Voci ARP statiche per gli host critici (gateway).",
        "Monitoraggio: strumenti che notano quando un MAC cambia IP di colpo (segno di "
        "spoofing).",
    ])
    d.p("Etica e legge: l'ARP spoofing intercetta le comunicazioni altrui. Farlo fuori dal "
        "laboratorio è un reato. Qui si fa solo tra le nostre due VM isolate.")
    comune.studio(
        d,
        approfondimenti=[
            ("Perché l'ARP è così facile da ingannare", "L'ARP è stato progettato in un'epoca in cui la rete locale era considerata fidata: per questo non ha alcuna autenticazione. Chiunque può inviare una risposta ARP anche senza che nessuno l'abbia chiesta (gratuitous ARP), e i computer aggiornano la loro cache fidandosi dell'ultima risposta ricevuta. L'attaccante ne approfitta mandando in continuazione risposte false che dicono 'quell'IP ce l'ho io', così il traffico della vittima verso quell'IP arriva a lui. Per un man-in-the-middle completo si avvelenano entrambi i lati e si attiva l'inoltro dei pacchetti, in modo che le due parti continuino a parlarsi senza accorgersi del passaggio in mezzo. Si rileva notando che uno stesso MAC risponde per più IP, o con strumenti come arpwatch."),
        ],
        sintesi=[
            "L'ARP non ha autenticazione: chiunque può rispondere 'quell'IP ce l'ho io' (spoofing).",
            "Avvelenando la cache ARP della vittima, il suo traffico verso un IP arriva all'attaccante (MITM).",
            "Con scapy si inviano risposte ARP false in continuazione per mantenere l'inganno.",
            "Per un MITM completo si avvelenano entrambi i lati e si attiva l'inoltro dei pacchetti.",
            'Difesa: cifrare tutto, switch gestiti (Dynamic ARP Inspection), voci ARP statiche.',
        ],
        glossario=[
            ('ARP spoofing', 'inviare risposte ARP false per farsi passare per un altro IP'),
            ('Cache poisoning', 'avvelenare la rubrica IP-MAC della vittima'),
            ('MITM', 'man-in-the-middle: mettersi in mezzo a una comunicazione'),
            ('Gratuitous ARP', "annuncio ARP non richiesto, usato per mantenere l'inganno"),
            ('ip_forward', "impostazione che permette all'attaccante di inoltrare i pacchetti"),
            ('Dynamic ARP Inspection', 'difesa degli switch contro le risposte ARP false'),
        ],
        errori=[
            "Lanciare l'arpspoof senza root o sull'interfaccia sbagliata.",
            "Dimenticare di rinfrescare l'ARP: l'inganno decade.",
            "Fare ARP spoofing su reti altrui: è un reato serio, solo nel lab.",
        ],
        domande=[
            "Perché l'ARP è facilmente falsificabile?",
            "Come fa l'attaccante a mettersi in mezzo (MITM) tramite ARP?",
            'A cosa serve inviare risposte ARP di continuo?',
            "Cosa serve in più per un MITM 'trasparente' completo?",
            "Quali difese fermano l'ARP spoofing?",
        ],
        collegamenti=[
            "Lezione 8: l'ARP visto in modo legittimo (scoperta host).",
            'Lezione 24: lo sniffing che il MITM rende possibile anche fuori dal proprio traffico.',
            "Lezione 26: il DNS spoofing, spesso combinato con l'ARP.",
        ],
    )


    d.h2("Punteggio della Lezione 25")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Intercetta il traffico", "arpspoof + tcpdump udp 9997", "40"],
        ["Password dirottata", "lab25-verifica", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 25** · ARP spoofing e MITM con scapy (Blocco 6, con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali con scapy; Kali e bersaglio sulla stessa rete interna.",
        "**Deliverable studente:** 2 flag (70 punti) + un ARP spoofer riutilizzabile.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire perché l'ARP è spoofabile e cosa comporta il MITM.",
        "Usare scapy per costruire e inviare risposte ARP false.",
        "Intercettare traffico dirottato e collegare alla difesa (cifratura, switch gestiti).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh avvia `lab25-client.service`: manda ogni 3s a 10.10.10.30:9997 (host "
        "inesistente) credenziali in chiaro con FLAG{traffico_dirottato}.",
        "kali.sh installa `~/lab/lezione-25/arpspoof.py` (scapy) e `lab25-verifica`.",
        "L'arpspoof dice alla vittima che 10.10.10.30 ha il MAC della Kali: da lì i "
        "pacchetti arrivano alla Kali, che li cattura con tcpdump/Wireshark.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["2", "arpspoof 10.10.10.20 10.10.10.30 + tcpdump udp 9997 (flag nel pacchetto)",
         "FLAG{traffico_dirottato}"],
        ["3", "leggere password=CasseforT3! ; lab25-verifica CasseforT3!", "FLAG{mitm_riuscito}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["tcpdump non vede nulla", "l'arpspoof deve girare in un altro terminale; "
         "controllare l'interfaccia (eth1) e che il client sul bersaglio sia attivo"],
        ["getmacbyip None", "il bersaglio deve essere raggiungibile: pingare prima 10.10.10.20"],
        ["scapy: permessi", "eseguire con sudo"],
        ["il traffico si ferma", "l'ARP va rinfrescato: l'arpspoof rimanda ogni 2s (già fatto)"],
    ], widths=[3000, 6026])
    d.h1("Da PROVARE sul bersaglio reale x86 (importante)")
    d.p("Sintassi scapy e logica verificate; l'effetto reale dell'ARP spoofing dipende "
        "dalla rete e va provato in aula sulle due VM x86: avviare arpspoof, poi tcpdump, "
        "e controllare che i pacchetti verso 10.10.10.30 arrivino alla Kali. Se lo switch "
        "virtuale filtra, verificare che entrambe le schede siano sulla stessa Rete "
        "interna labnet. In casi rari servono `sysctl net.ipv4.ip_forward=1` (per il MITM "
        "completo) e la disattivazione di eventuali protezioni ARP.")
