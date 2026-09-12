# -*- coding: utf-8 -*-
NUM = 31
SLUG = "malware-tipi-ciclo-di-vita"
TITOLO = "Cos'e il malware: tipi e ciclo di vita"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 30 min teoria · 75 min pratica · 15 min difesa.",
        "**Obiettivo:** capire cos'e' il malware, i suoi tipi principali e le fasi di un "
        "attacco (ciclo di vita), senza mai eseguire codice pericoloso.",
        "**Al termine sai:** distinguere virus, worm, trojan, ransomware e spyware, e "
        "riconoscere le fasi consegna, esecuzione, persistenza, comando, azione.",
        "**Flag in palio:** 2 flag (70 punti). Lezione in sandbox (solo descrizioni).",
    ])

    d.box("rosso", "Regola del blocco malware", items=[
        "In questo blocco NON si esegue mai malware vero. Si analizzano descrizioni e "
        "simulazioni innocue, in una sandbox isolata SENZA internet (si stacca la rete "
        "anche dalla Kali). Serve a capire il nemico per difendersi, in totale sicurezza.",
    ])

    d.h1("Parte 1 · La famiglia del malware (teoria, 30 min)")
    d.h2("Il caso reale")
    d.p("Malware vuol dire software malevolo: programmi scritti per danneggiare, rubare o "
        "prendere il controllo. Non e' tutto uguale: cambia come si diffonde, come si "
        "nasconde e cosa fa. Conoscere i tipi aiuta a riconoscere i sintomi e a scegliere "
        "la difesa giusta.")

    d.h2("I tipi principali")
    d.table(["Tipo", "Come si comporta"], [
        ["Virus", "si attacca ad altri file e si diffonde quando li esegui o li condividi"],
        ["Worm", "si copia da solo attraverso la rete, senza bisogno di aprirlo"],
        ["Trojan", "si traveste da programma utile; dentro nasconde il codice malevolo"],
        ["Ransomware", "cifra i tuoi file e chiede un riscatto"],
        ["Spyware", "spia di nascosto (tasti, password, schermo) e invia i dati"],
    ], widths=[2000, 7026])

    d.h2("Il ciclo di vita di un attacco")
    d.p("Quasi ogni attacco malware segue le stesse fasi, in ordine:")
    d.table(["Fase", "Cosa succede"], [
        ["1. Consegna", "arriva sul PC (email, chiavetta, download, link)"],
        ["2. Esecuzione", "viene avviato e prende piede"],
        ["3. Persistenza", "si assicura di ripartire a ogni riavvio"],
        ["4. Comando (C2)", "si collega all'attaccante per ricevere ordini"],
        ["5. Azione", "fa il danno: cifra, ruba, distrugge, si diffonde"],
    ], widths=[2200, 6826])

    d.h1("Parte 2 · Riconoscere senza rischiare (pratica, 75 min)")
    d.p("Sulla Kali `lab 31` semina descrizioni di comportamenti (nessun file eseguibile). "
        "Il tuo compito e' classificarli.")

    d.h2("Passo 1 · Classifica i campioni (+40)")
    d.code([
        "cd ~/lab/lezione-31",
        "cat campioni.txt",
        "lab31-verifica tipi <t1> <t2> <t3> <t4> <t5>",
    ])

    d.h2("Passo 2 · Rimetti in ordine il ciclo di vita (+30)")
    d.code([
        "cat ciclo.txt",
        "lab31-verifica ciclo <f1> <f2> <f3> <f4> <f5>",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Difese di base contro il malware", items=[
        "Aggiornare sistema e programmi: chiude le falle che il malware sfrutta per "
        "entrare (consegna/esecuzione).",
        "Antivirus e EDR: riconoscono e bloccano i comportamenti sospetti.",
        "Backup regolari e staccati: l'unica vera difesa contro il ransomware.",
        "Non aprire allegati e link sospetti (si ricollega a phishing e social "
        "engineering).",
        "Minimo privilegio: un malware con pochi permessi fa pochi danni.",
    ])

    d.h2("Punteggio della Lezione 31")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Classifica i tipi", "lab31-verifica tipi", "40"],
        ["Ordina il ciclo di vita", "lab31-verifica ciclo", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 31** · Malware, tipi e ciclo di vita (Blocco 8, apertura).",
        "**Tempi:** 30 min teoria · 75 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2). Ambiente da tenere ISOLATO (staccare "
        "internet anche dalla Kali per tutto il blocco).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Introdurre il blocco malware e la regola della sandbox senza internet.",
        "Distinguere i tipi di malware e le fasi del ciclo di vita.",
        "Collegare alle difese di base (aggiornamenti, antivirus, backup).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `~/lab/lezione-31/campioni.txt` e `ciclo.txt` (solo testo) e "
        "installa `lab31-verifica`. Nessun file eseguibile e' coinvolto.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "tipi: trojan worm ransomware virus spyware (ordine 1..5)",
         "FLAG{classifico_i_malware}"],
        ["2", "ciclo: consegna esecuzione persistenza comando azione", "FLAG{ciclo_di_vita}"],
    ], widths=[700, 6026, 2300])
    d.p("Mappa campioni->tipo: 1 trojan, 2 worm, 3 ransomware, 4 virus, 5 spyware.")
    d.h1("Nota organizzativa (importante per tutto il blocco)")
    d.p("Da qui alla Lezione 34 l'ambiente va tenuto isolato: staccare la scheda NAT anche "
        "dalla Kali. Le simulazioni delle lezioni seguenti (analisi statica, ransomware "
        "didattico, IOC) sono innocue e non richiedono internet. Ribadire agli studenti "
        "che non si scaricano ne' si eseguono mai malware reali.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["le risposte non passano", "parole minuscole, senza accenti, nell'ordine 1..5"],
        ["voglio rigiocare", "rilanciare `lab 31`"],
    ], widths=[2600, 6426])
