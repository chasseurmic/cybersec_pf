# -*- coding: utf-8 -*-
import comune
NUM = 35
SLUG = "hardening-di-sistema"
TITOLO = "Hardening di sistema"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** ridurre la superficie d'attacco di un sistema (hardening): "
        "spegnere ciò che non serve, blindare i servizi e sistemare i permessi, "
        "chiudendo le porte che negli scorsi blocchi avevamo sfruttato.",
        "**Al termine sai:** disabilitare servizi inutili, mettere in sicurezza SSH e "
        "correggere permessi pericolosi.",
        "**Flag in palio:** 3 flag (70 punti).",
    ])

    d.h1("Parte 1 · Meno superficie, meno rischio (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Nei blocchi scorsi hai attaccato sfruttando servizi dimenticati, login "
        "permissivi e permessi sbagliati. Il difensore fa il contrario: passa in rassegna "
        "il sistema e chiude tutto ciò che non serve. Ogni servizio spento, ogni porta "
        "chiusa, ogni permesso corretto è una porta d'ingresso in meno. Questo lavoro si "
        "chiama hardening, e vale più di molti strumenti costosi.")

    d.h2("La regola d'oro: minimo indispensabile")
    d.table(["Ambito", "Da fare"], [
        ["Servizi", "spegnere e disabilitare tutto ciò che non serve davvero"],
        ["Porte", "chiudere col firewall quelle non necessarie (Lezione 27)"],
        ["Account", "niente utenti inutili; niente login di root via SSH; password forti"],
        ["Permessi", "segreti a 600/400; niente file sensibili leggibili da tutti"],
        ["Aggiornamenti", "sistema e programmi sempre aggiornati"],
    ], widths=[1800, 7226])

    d.h1("Parte 2 · Blinda il bersaglio (pratica, 80 min)")
    d.p("Oggi lavori SUL bersaglio come amministratore. Sul bersaglio `lab 35` semina tre "
        "debolezze; tu le sistemi e verifichi con `sudo lab35-verifica`.")

    d.h2("Passo 1 · Spegni il servizio inutile (+25)")
    d.p("C'è un vecchio servizio acceso sulla porta 9111 che non usa nessuno.")
    d.code(["sudo systemctl disable --now lab35-inutile"])

    d.h2("Passo 2 · Blinda SSH (+25)")
    d.p("Impedisci il login diretto dell'amministratore (root) via SSH: si entra come "
        "utente normale e poi si usa sudo.")
    d.code([
        "echo 'PermitRootLogin no' | sudo tee /etc/ssh/sshd_config.d/hardening.conf",
        "sudo systemctl restart ssh        # oppure sshd",
    ])

    d.h2("Passo 3 · Correggi i permessi (+20)")
    d.p("Un file di credenziali è leggibile da tutti (permessi 666). Chiudilo.")
    d.code([
        "ls -l /opt/lab/lab35/segreti.txt",
        "sudo chmod 600 /opt/lab/lab35/segreti.txt",
    ])

    d.h2("Verifica finale")
    d.code(["sudo lab35-verifica     # ti dà una flag per ogni cosa sistemata"])

    d.h1("Parte 3 · Ribaltamento: la mentalità del difensore (15 min)")
    d.box("verde", "Hardening come abitudine", items=[
        "Parti da una lista (baseline/benchmark, es. CIS) e verifica ogni voce.",
        "Automatizza i controlli: uno script che ripassa i punti chiave (come "
        "lab35-verifica) evita dimenticanze.",
        "Documenta cosa hai cambiato: serve per capire e per tornare indietro se qualcosa "
        "si rompe.",
        "Hardening + monitoraggio (Lezione 36) + piano di risposta (Lezione 37) sono i tre "
        "pilastri della difesa.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("Superficie d'attacco, baseline e minimo privilegio", "L'hardening ruota attorno a tre idee. La superficie d'attacco è la somma di tutti i punti da cui si potrebbe entrare: ogni servizio acceso, porta aperta, account, permesso. Ridurla vuol dire spegnere l'inutile: ciò che non esiste non si può bucare. La baseline (o benchmark, come quelli del CIS) è una lista di controllo concreta di configurazioni sicure, da verificare voce per voce e, meglio ancora, in automatico. Il minimo privilegio, infine, dice di dare a ogni utente e ogni processo solo i permessi indispensabili: se qualcosa viene compromesso, i danni restano limitati. Insieme, questi principi trasformano la sicurezza da 'sperare che vada bene' a 'disciplina verificabile'."),
        ],
        sintesi=[
            "L'hardening riduce la superficie d'attacco: si spegne l'inutile e si stringe ciò che resta.",
            'Regola: minimo indispensabile su servizi, porte, account, permessi.',
            "SSH più sicuro: niente login diretto di root, password forti, meglio le chiavi.",
            'I segreti a 600/400; niente file sensibili leggibili da tutti.',
            'Hardening + monitoraggio + piano di risposta sono i tre pilastri della difesa.',
        ],
        glossario=[
            ('Hardening', 'irrobustire un sistema riducendone le debolezze'),
            ("Superficie d'attacco", "l'insieme dei punti attaccabili di un sistema"),
            ('systemctl disable', "disabilita un servizio perché non riparta"),
            ('PermitRootLogin no', 'impedisce il login diretto di root via SSH'),
            ('Baseline / benchmark', 'una lista di controllo di sicurezza (es. CIS)'),
            ('Minimo privilegio', 'concedere solo i permessi indispensabili'),
        ],
        errori=[
            "Lasciare acceso 'per comodità' un servizio che non serve.",
            'Permettere il login di root via SSH.',
            'Segreti con permessi larghi (644 invece di 600).',
            'Fare modifiche senza documentarle o senza modo di tornare indietro.',
        ],
        domande=[
            "Cosa significa ridurre la superficie d'attacco?",
            'Come disabiliti un servizio inutile e come lo verifichi?',
            "Perché conviene vietare il login diretto di root via SSH?",
            'Quali permessi deve avere un file di segreti?',
            'Quali sono i tre pilastri della difesa di un sistema?',
        ],
        collegamenti=[
            'Lezione 3 e 5: permessi e servizi, che qui si mettono in sicurezza.',
            'Lezione 27: le difese a livello di rete.',
            'Lezione 36-37: sorvegliare e rispondere quando qualcosa passa.',
        ],
    )


    d.h2("Punteggio della Lezione 35")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Servizio inutile spento", "systemctl disable --now", "25"],
        ["SSH blindato", "PermitRootLogin no", "25"],
        ["Permessi corretti", "chmod 600", "20"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 35** · Hardening di sistema (Blocco 9, blue team).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; accesso amministratore (root/sudo).",
        "**Deliverable studente:** 3 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Ridurre la superficie d'attacco: servizi, porte, account, permessi.",
        "Mettere in sicurezza SSH e correggere permessi.",
        "Introdurre l'idea di baseline/benchmark e verifiche automatiche.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh genera le flag in `/opt/lab/lab35/flags.env`, accende "
        "`lab35-inutile.service` (:9111), crea `segreti.txt` a 666 e installa "
        "`lab35-verifica` (controlla i tre punti e rivela la flag di ciascuno).",
        "kali.sh: briefing (si lavora sul bersaglio).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/lab35/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1", "sudo systemctl disable --now lab35-inutile", "FLAG_SERVIZIO"],
        ["2", "PermitRootLogin no in /etc/ssh/sshd_config.d/", "FLAG_SSH"],
        ["3", "sudo chmod 600 /opt/lab/lab35/segreti.txt", "FLAG_PERMESSI"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["verifica: servizio ancora acceso", "usare `disable --now` (ferma e disabilita)"],
        ["verifica: SSH permissivo", "il file drop-in deve contenere `PermitRootLogin no`; "
         "il verificatore controlla la config (non serve riavviare per la flag)"],
        ["verifica: permessi", "servono 600 o 400 su segreti.txt"],
        ["ripristinare per rigiocare", "rilanciare `lab 35` (riaccende il servizio e "
         "rimette i permessi 666)"],
    ], widths=[2800, 6226])
    d.h1("Nota di sicurezza")
    d.p("Le modifiche sono sicure: disabilitare `PermitRootLogin` non blocca l'accesso "
        "come utente normale + sudo. Non si tocca la porta 22. `lab 35` è idempotente e "
        "ripristina lo scenario per rigiocare.")
