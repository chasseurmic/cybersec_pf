# -*- coding: utf-8 -*-
NUM = 9
SLUG = "port-scanning-nmap-python"
TITOLO = "Port scanning con nmap e uno scanner in Python"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** scoprire quali porte (cioe' quali servizi) sono aperte su un host, "
        "con lo strumento professionale nmap e con uno scanner scritto da te in Python.",
        "**Al termine sai:** cos'e' una porta e il three-way handshake, usare nmap per "
        "scansionare le porte, e capire come funziona dentro un port scanner.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Porte e servizi (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Nella lezione scorsa abbiamo trovato gli host vivi. Ma un indirizzo IP da solo "
        "non basta: quello che interessa a un attaccante e' cosa sta girando su quel "
        "computer. Un server web? Un database? Un vecchio servizio pieno di falle? Ogni "
        "servizio ascolta su una porta, e la mappa delle porte aperte e' la lista delle "
        "possibili vie d'ingresso. Il port scanning e' bussare a tutte le porte per "
        "vedere quali si aprono.")

    d.h2("Cos'e' una porta")
    d.p("Un computer ha un solo indirizzo IP ma migliaia di porte (da 1 a 65535). Ogni "
        "servizio ne usa una: e' come un grande palazzo con un solo indirizzo civico ma "
        "tante porte numerate. Alcune sono standard.")
    d.table(["Porta", "Servizio"], [
        ["22", "SSH (terminale remoto)"],
        ["80", "HTTP (siti web)"],
        ["443", "HTTPS (siti web cifrati)"],
        ["3306", "MySQL (database)"],
        ["8080 / 8081 / 8082", "app web del nostro laboratorio (Banca, DVWA, Juice Shop)"],
    ], widths=[2200, 6826])

    d.h2("Il three-way handshake")
    d.p("Per aprire una connessione TCP i due computer si scambiano tre messaggi: SYN "
        "(io voglio parlare), SYN-ACK (va bene, parliamo), ACK (perfetto). Se dall'altra "
        "parte c'e' un servizio in ascolto, la porta e' aperta. Uno scanner sfrutta "
        "proprio questo: prova ad aprire la connessione e guarda cosa risponde.")
    d.table(["Stato", "Significato"], [
        ["aperta (open)", "c'e' un servizio in ascolto: possibile via d'ingresso"],
        ["chiusa (closed)", "nessun servizio, ma l'host risponde"],
        ["filtrata (filtered)", "un firewall blocca: non si capisce se aperta o chiusa"],
    ], widths=[2400, 6626])

    d.h1("Parte 2 · Scansiona il bersaglio (pratica, 80 min)")
    d.p("Sul bersaglio `lab 9` apre un servizio segreto su una porta insolita; sulla Kali "
        "`lab 9` installa lo scanner Python e mostra la missione.")

    d.h2("Passo 1 · Il tuo scanner in Python (+35)")
    d.p("Apri e leggi `portscan.py`: prova a connettersi a ogni porta e, se la "
        "connessione riesce, la porta e' aperta. Usa tanti thread per essere veloce. "
        "Lancialo sul bersaglio.")
    d.code([
        "cd ~/lab/lezione-09",
        "cat portscan.py",
        "python3 portscan.py 10.10.10.20 1 10000",
    ])
    d.p("Tra le porte aperte ne trovi una insolita: 7777. Il tuo scanner ti premia con "
        "la prima flag.")

    d.h2("Passo 2 · Il servizio segreto (+35)")
    d.p("Ora che sai che 7777 e' aperta, collegati per vedere cosa nasconde.")
    d.code(["curl http://10.10.10.20:7777"])

    d.h2("Cross-check con nmap")
    d.p("Lo strumento professionale fa la stessa cosa, ma con molte piu' opzioni. "
        "Confronta i risultati con il tuo scanner.")
    d.code([
        "sudo nmap -sS -p- -T4 10.10.10.20     # SYN scan di TUTTE le porte, veloce",
        "nmap --top-ports 20 10.10.10.20       # solo le 20 porte piu' comuni",
        "nmap -Pn 10.10.10.20                  # scansiona anche se il ping e' ignorato",
    ])
    d.box("blu", "Perche' scrivere il proprio scanner", items=[
        "Capisci davvero cosa fa nmap sotto il cofano (una connessione per porta).",
        "In un ambiente ridotto, senza strumenti installati, sai arrangiarti con Python.",
        "Vedi il compromesso tra velocita' (tanti thread) e precisione (timeout).",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Una scansione completa delle porte e' molto rumorosa: centinaia o migliaia di "
        "tentativi di connessione in pochi secondi da un solo IP. Il difensore la nota.")
    d.box("verde", "Difendersi dal port scanning", items=[
        "Chiudere e disattivare i servizi che non servono: meno porte aperte, meno "
        "superficie d'attacco (era il servizio 7777 di oggi: nessuno lo usava piu').",
        "Un firewall che filtra le porte rende la scansione piu' lenta e meno chiara.",
        "Un IDS rileva il pattern di un port scan (tante porte toccate in poco tempo).",
        "La regola d'oro: se un servizio non serve, spegnilo. Il servizio piu' sicuro e' "
        "quello che non e' acceso.",
    ])

    d.h2("Punteggio della Lezione 9")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Scanner Python", "portscan.py trova la porta 7777", "35"],
        ["Servizio segreto", "curl http://10.10.10.20:7777", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 9** · Port scanning con nmap e scanner Python (Blocco 3, con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; Python3 sul bersaglio (presente su Ubuntu).",
        "**Deliverable studente:** 2 flag (70 punti) + uno scanner Python riutilizzabile.",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire porte, servizi e three-way handshake.",
        "Usare nmap (SYN scan, -p-, --top-ports, -Pn) e leggere gli stati open/closed/filtered.",
        "Costruire e capire un port scanner TCP in Python (socket + thread).",
    ])

    d.h1("Come funziona il lab")
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Crea `~/lab/lezione-09/portscan.py`: scanner TCP con 200 thread e "
        "`socket.connect_ex`; se trova la porta 7777 stampa FLAG{scanner_python_funziona}.",
        "Verifica bersaglio e mostra la missione (con cross-check nmap).",
    ])
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Avvia `lab09-porta.service`: `python3 -m http.server 7777` che serve "
        "FLAG{porta_segreta_scoperta}.",
        "Assicura SSH (22) e il container banca (8080) attivi come altre porte da trovare.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "python3 portscan.py 10.10.10.20 1 10000 (trova 7777)", "FLAG{scanner_python_funziona}"],
        ["2", "curl http://10.10.10.20:7777", "FLAG{porta_segreta_scoperta}"],
    ], widths=[900, 5626, 2500])
    d.p("Ports attesi aperti sul bersaglio: 22 (SSH), 8080 (banca), e i container 8081 "
        "(DVWA) / 8082 (Juice Shop) se avviati, piu' 7777 (servizio della lezione). "
        "Se una lezione precedente ha lasciato attivi lab05-porta (31337) o lab09, "
        "compariranno anche quelli: e' coerente, non un errore.")

    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["portscan.py lentissimo", "molte porte filtrate: e' normale su reti con "
         "firewall; sul lab i chiusi rispondono subito (RST)"],
        ["7777 non compare", "`systemctl status lab09-porta` sul bersaglio; rilanciare `lab 9`"],
        ["nmap -sS chiede root", "SYN scan richiede privilegi: usare sudo, oppure "
         "`nmap -sT` (connect scan) senza root"],
        ["fermare il servizio a fine blocco", "`systemctl disable --now lab09-porta`"],
    ], widths=[2800, 6226])

    d.h1("Nota tecnica (x86)")
    d.p("Lo scanner Python e nmap funzionano identici su x86 e ARM. Da provare sul "
        "bersaglio reale x86: la presenza dei container DVWA/Juice Shop sulle porte "
        "8081/8082 (non partono su ARM), che rende la mappa delle porte piu' ricca.")
