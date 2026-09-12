# -*- coding: utf-8 -*-
import comune
NUM = 23
SLUG = "tcpip-wireshark"
TITOLO = "TCP/IP e Wireshark"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire come viaggiano i dati in rete (TCP/IP, pacchetti, "
        "handshake) e usare Wireshark/tcpdump per catturarli e leggerli, scoprendo quanto "
        "è esposto il traffico non cifrato.",
        "**Al termine sai:** catturare pacchetti, usare i filtri, riconoscere il "
        "three-way handshake e leggere credenziali che viaggiano in chiaro.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Come viaggiano i dati (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Su una rete condivisa (una wifi pubblica, una rete aziendale mal configurata) "
        "chi ascolta può vedere il traffico degli altri. Se quel traffico non è "
        "cifrato, legge tutto: pagine, ricerche, perfino password. Wireshark è lo "
        "strumento che rende visibile questo flusso invisibile. Impararlo serve tanto ad "
        "attaccare quanto a diagnosticare e difendere una rete.")

    d.h2("La pila TCP/IP")
    d.p("I dati vengono impacchettati a strati, come una lettera dentro buste sempre più "
        "grandi.")
    d.table(["Livello", "Cosa aggiunge", "Esempio"], [
        ["Applicazione", "il contenuto vero", "HTTP, DNS"],
        ["Trasporto", "porte e affidabilità", "TCP, UDP"],
        ["Rete", "gli indirizzi IP", "IP"],
        ["Collegamento", "gli indirizzi MAC", "Ethernet, Wi-Fi"],
    ], widths=[2000, 4026, 3000])

    d.h2("Il three-way handshake")
    d.p("Per aprire una connessione TCP servono tre pacchetti: SYN (apro), SYN-ACK "
        "(ricevuto, apro anch'io), ACK (ok). In Wireshark si vedono benissimo: sono i "
        "primi tre pacchetti di ogni connessione.")

    d.h1("Parte 2 · Cattura il traffico (pratica, 80 min)")
    d.p("Sul bersaglio `lab 23` avvia un 'beacon' che manda in chiaro, ogni 3 secondi, un "
        "messaggio con credenziali e una flag. Sulla Kali lo catturi.")
    d.p("Trova prima l'interfaccia della rete interna:")
    d.code(["ip -br addr        # di solito eth1 è la rete interna del lab"])

    d.h2("Passo 1 · Cattura il beacon in chiaro (+40)")
    d.p("Ascolta la porta UDP 9999. Con `-A` tcpdump mostra il testo dei pacchetti.")
    d.code([
        "sudo tcpdump -i any -A udp port 9999",
        "# in Wireshark, in alternativa, usa il filtro:   udp.port == 9999",
    ])
    d.p("Nel testo del pacchetto compare la prima flag.")

    d.h2("Passo 2 · Leggi la password in chiaro (+30)")
    d.p("Nello stesso messaggio c'è un campo `password=...`. Leggila e consegnala.")
    d.code(["lab23-verifica <la-password-che-hai-letto>"])

    d.box("blu", "Extra: guarda un handshake", intro=(
        "Cattura una connessione al sito e osserva i primi pacchetti:"), items=[
        "sudo tcpdump -i any -n 'tcp port 8080 and host 10.10.10.20'",
        "in un altro terminale:  curl http://10.10.10.20:8080",
        "in Wireshark: tasto destro su un pacchetto > Follow > TCP Stream.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Difendersi dallo sniffing", items=[
        "Cifrare tutto: HTTPS, SSH, VPN. Cio' che è cifrato, anche se catturato, non si "
        "legge.",
        "Reti segmentate e switch gestiti: riducono cosa un attaccante può ascoltare.",
        "Niente protocolli in chiaro per dati sensibili (HTTP, FTP, Telnet): il beacon di "
        "oggi era l'esempio da NON imitare.",
        "Monitorare la rete: anche chi difende usa Wireshark, per capire cosa succede.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Incapsulamento: le buste dentro le buste', "Quando invii un dato, ogni livello della pila TCP/IP aggiunge la propria 'busta' (header) attorno a quella del livello sopra. L'applicazione produce il contenuto (es. una richiesta HTTP); il livello di trasporto (TCP) ci mette davanti le porte di origine e destinazione; il livello di rete (IP) aggiunge gli indirizzi IP; il livello di collegamento (Ethernet) aggiunge i MAC. In ricezione si aprono le buste in ordine inverso. Ecco perché in Wireshark, cliccando un pacchetto, vedi i livelli uno dentro l'altro: Ethernet, poi IP, poi TCP, poi i dati. E capisci anche la differenza tra i tre indirizzi che hai incontrato: il MAC serve nella rete locale, l'IP per arrivare attraverso i router, la porta per consegnare al servizio giusto sul computer di destinazione."),
        ],
        sintesi=[
            'I dati viaggiano a strati (TCP/IP): applicazione, trasporto, rete, collegamento.',
            "Su una rete condivisa, chi ascolta vede il traffico altrui: se non è cifrato, lo legge tutto.",
            "Wireshark e tcpdump catturano i pacchetti; i filtri isolano ciò che interessa.",
            "Il three-way handshake (SYN, SYN-ACK, ACK) si vede all'inizio di ogni connessione TCP.",
            'Difesa: cifrare tutto; il traffico cifrato, anche catturato, resta illeggibile.',
        ],
        glossario=[
            ('Pila TCP/IP', 'i livelli con cui i dati vengono impacchettati'),
            ('Pacchetto', "l'unità di dati che viaggia in rete"),
            ('Wireshark / tcpdump', 'strumenti per catturare e leggere i pacchetti'),
            ('Filtro (BPF)', 'regola per mostrare solo certi pacchetti (es. udp port 9999)'),
            ('Sniffing', 'ascoltare il traffico di rete'),
            ('Follow TCP Stream', "ricostruire l'intera conversazione di una connessione"),
        ],
        errori=[
            "Catturare sull'interfaccia sbagliata e non vedere nulla.",
            'Far viaggiare credenziali in chiaro (HTTP, FTP, Telnet).',
            "Pensare che sniffare sia innocuo: intercettare traffico altrui è illegale fuori dal lab.",
        ],
        domande=[
            'Quali sono i livelli della pila TCP/IP?',
            "Perché su una rete condivisa si può leggere il traffico altrui?",
            'Come isoli in Wireshark solo il traffico che ti interessa?',
            'Quali sono i tre pacchetti del handshake e dove si vedono?',
            "Perché cifrare rende inutile lo sniffing?",
        ],
        collegamenti=[
            'Lezione 24: automatizzare lo sniffing con scapy.',
            'Lezione 21-22: la cifratura che protegge dal sniffing.',
            "Lezione 9: TCP e porte, già incontrati con nmap.",
        ],
    )


    d.h2("Punteggio della Lezione 23")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Cattura il beacon", "tcpdump/Wireshark udp 9999", "40"],
        ["Password in chiaro", "leggere password= ; lab23-verifica", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 23** · TCP/IP e Wireshark (Blocco 6, rete).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali con Wireshark/tcpdump; Kali e bersaglio sulla stessa "
        "rete interna.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire la pila TCP/IP e il three-way handshake.",
        "Catturare e filtrare traffico con Wireshark/tcpdump.",
        "Vedere l'esposizione del traffico in chiaro (motiva la cifratura, Blocco 5).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh avvia `lab23-beacon.service`: manda in broadcast (10.10.10.255 e "
        "255.255.255.255) su UDP :9999 un messaggio in chiaro con `password=Autunno2021` "
        "e FLAG{ho_annusato_la_rete}.",
        "kali.sh installa `lab23-verifica` (accetta la password letta) e mostra la missione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "tcpdump -A udp port 9999 (leggere la flag nel pacchetto)",
         "FLAG{ho_annusato_la_rete}"],
        ["2", "leggere password=Autunno2021 ; lab23-verifica Autunno2021",
         "FLAG{credenziali_in_chiaro}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["tcpdump non vede nulla", "usare `-i any` o l'interfaccia interna (eth1); il "
         "beacon parte ogni 3s; `systemctl status lab23-beacon` sul bersaglio"],
        ["Wireshark non lista l'interfaccia", "l'utente deve essere nel gruppo wireshark "
         "(fatto in provisioning); rilanciare o usare sudo"],
        ["broadcast non arriva", "verificare che Kali e bersaglio siano sulla stessa "
         "Rete interna labnet"],
    ], widths=[3000, 6026])
    d.h1("Nota tecnica")
    d.p("Il beacon in broadcast è semplice e affidabile per l'aula: ogni studente lo "
        "cattura senza dover generare traffico. La parte handshake usa il sito :8080 "
        "(banca): se non è attivo, va bene qualsiasi connessione TCP verso il bersaglio.")
