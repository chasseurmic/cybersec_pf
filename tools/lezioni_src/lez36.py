# -*- coding: utf-8 -*-
import comune
NUM = 36
SLUG = "log-monitoraggio-rilevamento"
TITOLO = "Log, monitoraggio e rilevamento"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** usare i log per accorgersi di un attacco. Leggere un log di "
        "autenticazione, trovare un brute force nascosto tra centinaia di righe e capire "
        "quando e come è avvenuta la compromissione.",
        "**Al termine sai:** analizzare i log con le pipe (grep, cut, sort, uniq), "
        "individuare l'attaccante e l'account compromesso, e impostare un rilevamento.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · I log raccontano tutto (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Ogni sistema scrive log: chi si collega, cosa succede, cosa va storto. Il "
        "problema è che sono tanti e nessuno li guarda. Eppure quasi ogni attacco lascia "
        "una traccia: una raffica di accessi falliti, un login a un'ora strana, un IP mai "
        "visto. Un difensore che sa leggere i log si accorge dell'attacco mentre accade, "
        "non mesi dopo. Oggi diventi tu quel difensore.")

    d.h2("Dove guardare, cosa cercare")
    d.table(["Log", "Cosa contiene", "Sintomo d'attacco"], [
        ["auth.log / secure", "accessi SSH e sudo", "tanti 'Failed password' da un IP"],
        ["access.log web", "richieste al sito", "valanga di 404, path da scanner"],
        ["syslog / journal", "eventi di sistema", "servizi che partono/cadono a caso"],
    ], widths=[2400, 3626, 3000])
    d.p("Gli stessi comandi della Lezione 4 (grep, cut, sort, uniq) diventano qui gli "
        "strumenti del difensore.")

    d.h1("Parte 2 · Caccia all'attacco nei log (pratica, 80 min)")
    d.p("Sulla Kali `lab 36` semina `~/lab/lezione-36/auth.log`: dentro c'è un attacco "
        "brute force e la compromissione che ne è seguita. Trovali.")

    d.h2("Passo 1 · Chi è l'attaccante? (+35)")
    d.p("L'attaccante ha provato centinaia di password: nel log lascia tanti 'Failed "
        "password'. Conta i falliti per IP.")
    d.code([
        "cd ~/lab/lezione-36",
        "grep \"Failed password\" auth.log | grep -oE \"from [0-9.]+\" \\",
        "  | sort | uniq -c | sort -rn | head",
        "lab36-verifica ip <indirizzo>",
    ])

    d.h2("Passo 2 · Quale account è caduto? (+35)")
    d.p("Dopo tanti tentativi, uno è andato a segno: cerca l'accesso RIUSCITO dall'IP "
        "dell'attaccante.")
    d.code([
        "grep \"Accepted password\" auth.log | grep \"10.10.10.66\"",
        "lab36-verifica account <utente>",
    ])
    d.box("blu", "Costruisci il tuo allarme", intro=(
        "Un rilevamento è solo una ricerca che fai in automatico. Esempio: quanti "
        "falliti per IP, ordinati:"), items=[
        "grep 'Failed password' auth.log | grep -oE 'from [0-9.]+' | sort | uniq -c | sort -rn",
        "In produzione, uno strumento (fail2ban, un SIEM) fa questo di continuo e "
        "avvisa/blocca da solo.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Dal log alla difesa", items=[
        "Centralizzare i log (un posto solo): più facili da guardare e da correlare.",
        "Automatizzare il rilevamento: fail2ban blocca gli IP che sbagliano troppo; un "
        "SIEM correla eventi da più fonti.",
        "Definire cosa è 'anomalo' per te (baseline): così l'insolito salta all'occhio.",
        "Un attacco trovato nei log fa partire l'incident response (prossima lezione).",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Cosa loggare, come correlare, ATT&CK', "Un buon monitoraggio non registra tutto a caso: sceglie gli eventi che contano (accessi, cambi di privilegio, errori, connessioni) e li centralizza in un unico posto, così da poterli correlare tra fonti diverse. Correlare significa collegare indizi: un accesso fallito ripetuto, seguito da un accesso riuscito, seguito da un comando insolito, raccontano una storia che i singoli eventi non mostrano. Per ragionare in modo sistematico su cosa cercare esiste MITRE ATT&CK, una mappa delle tattiche e tecniche usate dagli attaccanti: aiuta a chiedersi 'ho visibilità su questa mossa?'. E i log servono a poco se non c'è ritenzione (li si conserva a sufficienza) e qualcuno o qualcosa che li guardi davvero."),
        ],
        sintesi=[
            'I log registrano tutto: chi si collega, cosa succede, cosa va storto. Un log che nessuno guarda non protegge.',
            "Quasi ogni attacco lascia una traccia: una raffica di accessi falliti, un login a un'ora strana.",
            'Le stesse pipe della Lezione 4 (grep, sort, uniq) diventano gli strumenti del difensore.',
            "Un rilevamento è solo una ricerca fatta in automatico (fail2ban, un SIEM).",
            "Dalla scoperta nei log parte la risposta all'incidente.",
        ],
        glossario=[
            ('Log', 'registro degli eventi di un sistema o servizio'),
            ('auth.log', 'il log degli accessi (SSH, sudo) su Linux'),
            ('Correlazione', "collegare eventi da più fonti per capire un attacco"),
            ('fail2ban', 'strumento che blocca gli IP con troppi accessi falliti'),
            ('SIEM', 'sistema che raccoglie e correla i log per rilevare le minacce'),
            ('Baseline', "cosa è 'normale', per far risaltare l'anomalo"),
        ],
        errori=[
            'Raccogliere i log ma non guardarli mai.',
            'Non centralizzare i log: diventano difficili da correlare.',
            'Ignorare i picchi di accessi falliti da un solo IP.',
        ],
        domande=[
            "Come trovi l'IP con più accessi falliti in un auth.log?",
            "Come capisci quale account è stato infine compromesso?",
            'Quali pipe della Lezione 4 riusi qui?',
            "Cos'è un rilevamento automatico (es. fail2ban)?",
            'Cosa fai quando i log rivelano una compromissione?',
        ],
        collegamenti=[
            'Lezione 4: le pipe, qui usate in difesa.',
            "Lezione 16 e 27: gli attacchi che qui si vedono 'dal lato del difensore'.",
            "Lezione 37: la risposta all'incidente scoperto nei log.",
        ],
    )


    d.h2("Punteggio della Lezione 36")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["IP dell'attaccante", "grep|sort|uniq ; lab36-verifica ip", "35"],
        ["Account compromesso", "grep Accepted ; lab36-verifica account", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 36** · Log, monitoraggio e rilevamento (Blocco 9).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2). Utile aver fatto la Lezione 4 (pipe).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Usare i log per rilevare attacchi (brute force e compromissione).",
        "Riusare le pipe come strumento difensivo.",
        "Introdurre rilevamento automatico (fail2ban/SIEM) e il ponte con l'IR.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh genera `~/lab/lezione-36/auth.log`: traffico normale + circa 300 'Failed "
        "password' da 10.10.10.66 + un 'Accepted password for backup from 10.10.10.66' "
        "(la compromissione). Installa `lab36-verifica`.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "IP con più Failed = 10.10.10.66 ; lab36-verifica ip 10.10.10.66",
         "FLAG{attaccante_smascherato}"],
        ["2", "grep Accepted | grep 10.10.10.66 -> backup ; lab36-verifica account backup",
         "FLAG{account_compromesso}"],
    ], widths=[700, 6026, 2300])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["nessun IP dominante", "il log è rigenerato a ogni `lab 36`; l'IP è sempre "
         "10.10.10.66"],
        ["l'Accepted non si trova", "filtrare per l'IP attaccante: `grep 10.10.10.66`"],
        ["voglio rigiocare", "rilanciare `lab 36` (rigenera il log)"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("Ottimo collegamento con la Lezione 4 (pipe) e con L16/L27 (l'attacco che qui si "
        "vede 'dal lato del difensore'). Se in aula c'è tempo, mostrare fail2ban su "
        "Ubuntu come rilevamento automatico reale.")
