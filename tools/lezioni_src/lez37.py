# -*- coding: utf-8 -*-
NUM = 37
SLUG = "incident-response"
TITOLO = "Incident response di base"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** sapere cosa fare quando un sistema e' stato compromesso: seguire "
        "le fasi dell'incident response per contenere il danno, cacciare l'attaccante e "
        "rimettere in sicurezza.",
        "**Al termine sai:** identificare le tracce di una compromissione, contenere "
        "(bloccare account e IP), eradicare la persistenza e documentare.",
        "**Flag in palio:** 3 flag (70 punti).",
    ])

    d.h1("Parte 1 · Un piano per il giorno peggiore (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Prima o poi qualcosa passa. La differenza tra un incidente e un disastro e' come "
        "reagisci nei primi minuti. Chi improvvisa fa danni (cancella prove, lascia "
        "porte aperte). Chi ha un piano contiene subito e recupera in fretta. Nel Blocco "
        "scorso hai scoperto la compromissione nei log; ora la gestisci.")

    d.h2("Le sei fasi (PICERL)")
    d.table(["Fase", "Cosa fai"], [
        ["Preparazione", "avere strumenti, contatti e procedure PRIMA che accada"],
        ["Identificazione", "capire cosa e' successo: account, file, connessioni sospette"],
        ["Contenimento", "fermare l'emorragia: isolare, bloccare account e IP"],
        ["Eradicazione", "rimuovere l'attaccante: persistenza, backdoor, malware"],
        ["Recupero", "ripristinare i sistemi puliti e rimetterli online con cautela"],
        ["Lezioni apprese", "capire come e' entrato e chiudere quella falla"],
    ], widths=[2400, 6626])

    d.h1("Parte 2 · Bonifica il sistema (pratica, 80 min)")
    d.p("Sul bersaglio `lab 37` prepara la scena: l'attaccante ha creato un account e "
        "lasciato una persistenza. Lavora sul bersaglio come amministratore.")

    d.h2("Passo 1 · Identifica le tracce")
    d.code([
        "grep -E 'svc|update' /etc/passwd        # account creato dall'attaccante",
        "ls -la /etc/cron.d/                      # persistenza",
        "cat /etc/cron.d/lab37-backdoor",
    ])

    d.h2("Passo 2 · Contieni l'account ostile (+25)")
    d.code([
        "sudo usermod -L svc-update        # blocca (oppure: sudo userdel -r svc-update)",
    ])

    d.h2("Passo 3 · Eradica la persistenza (+25)")
    d.code(["sudo rm /etc/cron.d/lab37-backdoor"])

    d.h2("Passo 4 · Contieni la rete (+20)")
    d.code(["sudo iptables -A INPUT -s 10.10.10.66 -j DROP"])

    d.h2("Verifica la risposta")
    d.code(["sudo lab37-verifica"])

    d.box("blu", "Recupero e lezioni apprese", items=[
        "Recupero: cambiare le password compromesse, ripristinare da backup puliti, "
        "rimettere online con monitoraggio aumentato.",
        "Lezioni apprese: come e' entrato? (nel nostro caso, brute force su un account "
        "debole) Chiudere quella falla (password forti, rate limiting, 2FA).",
        "Documentare tutto: timeline, azioni, IOC. Serve per migliorare e, se necessario, "
        "per le autorita'.",
    ])

    d.h1("Parte 3 · Ribaltamento: chiudere il cerchio (15 min)")
    d.box("verde", "Trasformare l'incidente in difesa", items=[
        "Gli IOC raccolti (IP, account, file) diventano regole di blocco e rilevamento.",
        "La falla sfruttata diventa un punto della checklist di hardening (Lezione 35).",
        "L'esperienza aggiorna il piano: la prossima volta si reagisce ancora piu' in "
        "fretta.",
        "Non colpevolizzare le persone: si migliorano i processi (blameless postmortem).",
    ])

    d.h2("Punteggio della Lezione 37")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Contieni l'account", "usermod -L / userdel", "25"],
        ["Eradica la persistenza", "rm del cron malevolo", "25"],
        ["Blocca l'attaccante", "iptables DROP dell'IP", "20"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 37** · Incident response di base (Blocco 9, chiusura).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; accesso amministratore (root/sudo).",
        "**Deliverable studente:** 3 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Conoscere e applicare le fasi dell'incident response (PICERL).",
        "Contenere ed eradicare una compromissione reale (account, cron, IP).",
        "Chiudere il cerchio: dagli IOC alla difesa e alle lezioni apprese.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh crea l'utente ostile `svc-update`, la persistenza "
        "`/etc/cron.d/lab37-backdoor` (innocua) e installa `lab37-verifica` (controlla "
        "account bloccato/rimosso, cron rimosso, IP bloccato). Flag in `/opt/lab/lab37/flags.env`.",
        "kali.sh: briefing con le fasi e i comandi.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/lab37/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["2", "sudo usermod -L svc-update (o userdel -r)", "FLAG_ACCOUNT"],
        ["3", "sudo rm /etc/cron.d/lab37-backdoor", "FLAG_PERSIST"],
        ["4", "sudo iptables -A INPUT -s 10.10.10.66 -j DROP", "FLAG_RETE"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["account risulta ancora attivo", "usare `usermod -L` (blocca) o `userdel -r` "
         "(rimuove); il verificatore accetta entrambi"],
        ["cron ancora presente", "rimuovere `/etc/cron.d/lab37-backdoor`"],
        ["IP non bloccato", "regola esatta: `INPUT -s 10.10.10.66 -j DROP`"],
        ["rigiocare", "rilanciare `lab 37` (ricrea account, cron; l'IP resta bloccato "
         "finche' non lo togli con -D)"],
    ], widths=[2800, 6226])
    d.h1("Nota di sicurezza")
    d.p("La persistenza seminata e' un cron innocuo (un echo scartato): nessun rischio. "
        "L'account `svc-update` e le regole vanno rimossi a fine corso. `lab 37` e' "
        "idempotente e ricrea la scena per rigiocare l'esercizio.")
