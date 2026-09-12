# -*- coding: utf-8 -*-
NUM = 24
SLUG = "sniffing-credenziali-scapy"
TITOLO = "Sniffing di credenziali con scapy"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** automatizzare la cattura di credenziali dalla rete con scapy, "
        "invece di leggere i pacchetti a mano come nella lezione scorsa.",
        "**Al termine sai:** usare scapy per sniffare, filtrare i pacchetti ed estrarre in "
        "automatico utente e password dal traffico in chiaro.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Dall'occhio umano allo script (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Con Wireshark abbiamo letto un pacchetto. Ma un attaccante che vuole raccogliere "
        "credenziali non sta a guardare lo schermo per ore: scrive un programma che "
        "ascolta di continuo e tira fuori da solo ogni utente e password che passa. "
        "scapy e' la libreria Python che permette di costruire e ascoltare pacchetti in "
        "poche righe. Oggi trasformi lo sniffing in uno strumento automatico.")

    d.h2("scapy in due funzioni")
    d.p("Per catturare basta `sniff()`, a cui dai un filtro e una funzione da chiamare per "
        "ogni pacchetto. Dentro il pacchetto, il contenuto applicativo sta nel livello "
        "`Raw`.")
    d.code([
        "from scapy.all import sniff, Raw",
        "def analizza(pkt):",
        "    if pkt.haslayer(Raw):",
        "        dati = bytes(pkt[Raw].load)   # il contenuto, in chiaro",
        "        # ... cerca utente= e password= ...",
        "sniff(iface='eth1', filter='udp port 9998 or tcp', prn=analizza, store=0)",
    ])

    d.h1("Parte 2 · Il tuo raccoglitore di credenziali (pratica, 80 min)")
    d.p("Sul bersaglio `lab 24` avvia un beacon che manda finte login in chiaro (UDP "
        "9998): alcune frequenti, una (admin) rara. Sulla Kali `lab 24` installa "
        "`sniffer.py`. Trova prima l'interfaccia interna con `ip -br addr` (di solito "
        "eth1).")

    d.h2("Passo 1 · Cattura una credenziale frequente (+35)")
    d.code([
        "cd ~/lab/lezione-24",
        "cat sniffer.py",
        "sudo python3 sniffer.py eth1",
        "# appena compare utente=cassiere, prendi la password e consegnala:",
        "lab24-verifica comune <password>",
    ])

    d.h2("Passo 2 · Aspetta la login rara (+35)")
    d.p("La login admin passa di rado: lascia girare il sniffer. E' la lezione "
        "dell'attaccante paziente, l'automazione lavora per te mentre fai altro.")
    d.code(["lab24-verifica rara <password>"])
    d.box("blu", "Perche' automatizzare", items=[
        "A mano prenderesti solo cio' che vedi mentre guardi; lo script prende tutto.",
        "Un attaccante lascia il sniffer per ore e raccoglie centinaia di credenziali.",
        "Estrarre con una espressione regolare rende il tool utile su tanti formati.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Rendere inutile lo sniffing", items=[
        "Cifrare tutto (HTTPS, SSH, VPN): scapy catturerebbe solo dati illeggibili.",
        "Mai far viaggiare credenziali in protocolli in chiaro.",
        "Reti segmentate: meno traffico altrui raggiunge l'attaccante (Blocco difese).",
        "Su reti gestite, funzioni come il port security e la 802.1X limitano chi puo' "
        "ascoltare.",
    ])

    d.h2("Punteggio della Lezione 24")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Credenziale frequente", "sniffer.py + lab24-verifica comune", "35"],
        ["Credenziale rara", "attendere e lab24-verifica rara", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 24** · Sniffing di credenziali con scapy (Blocco 6, con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali con python3-scapy (Lezione 2); stessa rete interna.",
        "**Deliverable studente:** 2 flag (70 punti) + un sniffer scapy riutilizzabile.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Automatizzare lo sniffing (da Wireshark manuale a scapy).",
        "Usare sniff(), i filtri BPF e il livello Raw.",
        "Capire il valore dell'automazione e della persistenza per l'attaccante.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh avvia `lab24-beacon.service`: UDP :9998 in broadcast con login in "
        "chiaro; 'cassiere'/'sportello' frequenti, 'admin' rara (circa 1 su 4).",
        "kali.sh installa `~/lab/lezione-24/sniffer.py` (scapy) e `lab24-verifica`.",
        "Il sniffer estrae `utente=` e `password=` da qualsiasi pacchetto con quel "
        "pattern (UDP 9998 o TCP).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "cattura cassiere/Estate2022 ; lab24-verifica comune Estate2022",
         "FLAG{scapy_sniffa_credenziali}"],
        ["2", "attendi admin/Ammiragli0!2024 ; lab24-verifica rara Ammiragli0!2024",
         "FLAG{la_pazienza_paga}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["scapy: Operation not permitted", "serve sudo (raw socket): `sudo python3 sniffer.py eth1`"],
        ["nessun pacchetto", "interfaccia sbagliata: usare quella interna (ip -br addr); "
         "verificare il beacon sul bersaglio"],
        ["la login rara non arriva", "aspettare: compare circa ogni 12 secondi (1 su 4)"],
        ["scapy non importato", "installato in provisioning (python3-scapy); reinstallare "
         "se assente"],
    ], widths=[3200, 5826])
    d.h1("Nota tecnica (x86)")
    d.p("scapy funziona su x86 e ARM, ma sniff() richiede root e l'interfaccia giusta. Il "
        "beacon in broadcast garantisce traffico da catturare senza dipendere da altri. "
        "Da provare sul bersaglio reale x86: cattura anche di traffico TCP HTTP se gli "
        "studenti generano login verso la Banca.")
