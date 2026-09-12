# -*- coding: utf-8 -*-
import comune
NUM = 11
SLUG = "come-funziona-il-web"
TITOLO = "Come funziona il web (HTTP, DevTools, curl)"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire il protocollo HTTP (richieste, risposte, metodi, header, "
        "codici di stato, cookie) e imparare a parlarlo con curl e con gli Strumenti per "
        "sviluppatori del browser. È la base di tutto il blocco sulle web application.",
        "**Al termine sai:** leggere e costruire richieste HTTP, distinguere GET e POST, "
        "usare header e cookie, e riconoscere i codici di stato.",
        "**Flag in palio:** 4 flag (70 punti).",
    ])

    d.h1("Parte 1 · Il dialogo del web (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Ogni volta che apri un sito, il tuo browser manda una richiesta HTTP e il server "
        "risponde. Sembra magia, ma è solo testo che viaggia. Gli attacchi web (che "
        "vedremo nelle prossime lezioni) nascono tutti dal manipolare quel testo: "
        "cambiare un parametro, aggiungere un header, riutilizzare un cookie. Per farlo "
        "bisogna prima capire com'è fatto il dialogo. Oggi impariamo a parlare HTTP a "
        "mano, senza browser, con curl.")

    d.h2("Richiesta e risposta")
    d.p("Una richiesta HTTP ha un metodo (cosa voglio fare), un percorso, degli header "
        "(informazioni aggiuntive) e a volte un corpo (i dati). La risposta ha un codice "
        "di stato, degli header e un corpo (la pagina).")
    d.table(["Metodo", "Serve per"], [
        ["GET", "chiedere una pagina; i parametri vanno nella URL (?nome=valore)"],
        ["POST", "inviare dati (login, form); i dati vanno nel corpo, non nella URL"],
    ], widths=[1600, 7426])
    d.table(["Codice", "Significato"], [
        ["200", "OK, tutto bene"],
        ["301 / 302", "spostato / redirect verso un'altra pagina"],
        ["403", "vietato: non hai i permessi"],
        ["404", "non trovato"],
        ["500", "errore del server"],
    ], widths=[1600, 7426])

    d.h2("Header e cookie")
    d.p("Gli header sono coppie nome-valore che accompagnano richiesta e risposta (per "
        "esempio `Content-Type`, `Server`, header personalizzati). Il cookie è un header "
        "speciale: il server te lo dà, il browser lo rimanda a ogni richiesta. È così "
        "che un sito ti riconosce dopo il login (lo approfondiamo nella lezione su "
        "sessioni e cookie).")

    d.h1("Parte 2 · Parla HTTP con curl (pratica, 80 min)")
    d.p("Sul bersaglio `lab 11` avvia il portale didattico su :8090; sulla Kali `lab 11` "
        "mostra la missione. Parti guardando una richiesta intera:")
    d.code(["curl -v http://10.10.10.20:8090/"])

    d.h2("Passo 1 · Parametri nella URL, GET (+15)")
    d.p("Con GET i parametri viaggiano nella URL dopo il `?`. Salutati come 'admin'.")
    d.code(['curl "http://10.10.10.20:8090/saluta?nome=admin"'])

    d.h2("Passo 2 · Inviare dati con POST (+20)")
    d.p("Un form di login manda i dati con POST. `-d` mette i dati nel corpo e rende la "
        "richiesta una POST in automatico.")
    d.code(["curl -d \"utente=admin&password=banca123\" http://10.10.10.20:8090/login"])

    d.h2("Passo 3 · Aggiungere un header (+15)")
    d.p("Alcune aree pretendono un header particolare. `-H` lo aggiunge.")
    d.code(["curl -H \"X-Ruolo: dipendente\" http://10.10.10.20:8090/staff"])
    d.p("Prova prima senza header: ricevi 403 (vietato). Con l'header, arriva la flag.")

    d.h2("Passo 4 · Mandare un cookie (+20)")
    d.p("L'area clienti vuole un cookie di sessione. `-b` lo invia.")
    d.code([
        "curl -i http://10.10.10.20:8090/area-clienti     # senza cookie: 302 redirect",
        "curl -b \"sessione=valida\" http://10.10.10.20:8090/area-clienti",
    ])

    d.box("blu", "In aula, con Firefox", intro=(
        "Apri http://10.10.10.20:8090 in Firefox e premi F12 (Strumenti per "
        "sviluppatori):"), items=[
        "Scheda Rete: vedi ogni richiesta, i suoi header e la risposta.",
        "Scheda Archiviazione: vedi i cookie salvati.",
        "Tasto destro su una richiesta, 'Copia come cURL': ti dà il comando curl pronto.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Se un attaccante può ricostruire ogni richiesta a mano, la sicurezza non può "
        "basarsi su ciò che il browser 'nasconde'. Tutto ciò che arriva dal client va "
        "considerato non fidato.")
    d.box("verde", "Principi per chi sviluppa", items=[
        "Non fidarsi mai dei dati del client: parametri, header e cookie possono essere "
        "falsificati con un solo comando curl.",
        "I controlli di sicurezza vanno fatti sul server, non nascondendo pulsanti nel "
        "browser.",
        "I cookie di sessione vanno protetti (li vedremo: HttpOnly, Secure, valori non "
        "indovinabili).",
        "Gli header di risposta non devono rivelare più del necessario.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Anatomia di una richiesta e di una risposta HTTP', "Una richiesta HTTP è testo in chiaro fatto di: una riga iniziale (metodo, percorso, versione, es. GET /login HTTP/1.1), una serie di header (Host, User-Agent, Cookie, Content-Type...), una riga vuota e, solo per POST/PUT, un corpo con i dati. La risposta ha la stessa forma: riga di stato (HTTP/1.1 200 OK), header (Server, Set-Cookie, Content-Type) e il corpo (la pagina). Un dettaglio fondamentale: HTTP è senza stato (stateless), cioè ogni richiesta è indipendente e il server di per se' non ricorda le precedenti. Per 'ricordarti' dopo il login serve un trucco, il cookie. Vedere queste parti con curl -v ti fa capire che tutto ciò che il browser invia lo puoi costruire e modificare tu."),
        ],
        sintesi=[
            "Il web è fatto di richieste e risposte HTTP: testo che viaggia, che si può leggere e manipolare.",
            'GET chiede una pagina (parametri nella URL); POST invia dati (nel corpo, es. i login).',
            'I codici di stato: 200 ok, 301/302 redirect, 403 vietato, 404 non trovato, 500 errore server.',
            "Header e cookie accompagnano ogni richiesta; il cookie fa riconoscere l'utente dopo il login.",
            "Regola d'oro: i dati del client (parametri, header, cookie) non sono fidati, si falsificano con curl.",
        ],
        glossario=[
            ('HTTP', 'il protocollo del web: richieste e risposte testuali'),
            ('GET / POST', 'chiedere una risorsa / inviare dati al server'),
            ('Codice di stato', "numero che dice l'esito (200, 404, 500, ...)"),
            ('Header', 'coppie nome-valore che accompagnano richiesta e risposta'),
            ('Cookie', 'header speciale che il browser rimanda per farti riconoscere'),
            ('curl', 'client HTTP da terminale (-d dati/POST, -H header, -b cookie, -I intestazioni)'),
            ('DevTools', 'gli Strumenti per sviluppatori del browser (F12)'),
        ],
        errori=[
            "Credere che nascondere un pulsante nel browser impedisca l'azione: si rifa' con curl.",
            'Mettere i controlli di sicurezza solo lato client invece che sul server.',
            'Confondere parametri GET (nella URL) con dati POST (nel corpo).',
            "Fidarsi di header e cookie ricevuti: sono controllati dall'utente.",
        ],
        domande=[
            "Che differenza c'è tra GET e POST?",
            'Cosa significano i codici 200, 403 e 302?',
            'A cosa serve un cookie e come lo invii con curl?',
            "Perché i dati che arrivano dal client non sono fidati?",
            'Come invii un header personalizzato in una richiesta?',
        ],
        collegamenti=[
            'Lezione 12-18: tutti gli attacchi web partono dal manipolare queste richieste.',
            'Lezione 15: i cookie e le sessioni approfonditi.',
            "Lezione 1: curl già usato per leggere la pagina della Banca.",
        ],
    )


    d.h2("Punteggio della Lezione 11")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Parametro GET", "curl .../saluta?nome=admin", "15"],
        ["Richiesta POST", "curl -d ... /login", "20"],
        ["Header custom", "curl -H 'X-Ruolo: dipendente' /staff", "15"],
        ["Cookie", "curl -b 'sessione=valida' /area-clienti", "20"],
    ], widths=[3400, 4126, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 11** · Come funziona il web (Blocco 4, apertura web application).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; Python3 sul bersaglio; Firefox sulla Kali.",
        "**Deliverable studente:** 4 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Fondamenti HTTP: metodi, header, cookie, codici di stato, redirect.",
        "Usare curl come strumento principe per costruire richieste a mano.",
        "Introdurre gli Strumenti per sviluppatori del browser e 'Copia come cURL'.",
        "Instillare il principio: i dati del client non sono fidati (base di tutto il blocco).",
    ])

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Installa `/opt/lab/portale/portale.py` (app Python stdlib) e il servizio "
        "`lab11-portale.service` su :8090.",
        "Rotte: `/saluta` (GET param), `/login` (POST), `/staff` (header X-Ruolo), "
        "`/area-clienti` (cookie sessione), `/vecchio` (301), 404 di default.",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets(["Briefing di sola lettura con tutti i comandi curl e verifica del portale."])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", 'curl "http://10.10.10.20:8090/saluta?nome=admin"', "FLAG{parametri_nella_url}"],
        ["2", "curl -d 'utente=admin&password=banca123' .../login", "FLAG{ho_inviato_una_post}"],
        ["3", "curl -H 'X-Ruolo: dipendente' .../staff", "FLAG{gli_header_contano}"],
        ["4", "curl -b 'sessione=valida' .../area-clienti", "FLAG{i_cookie_ti_seguono}"],
    ], widths=[900, 5626, 2500])
    d.p("Credenziali POST: utente `admin`, password `banca123` (didattiche, in chiaro). "
        "Il login del portale è finto (confronto fisso); il login con database "
        "vulnerabile a SQL injection arriva nella Lezione 12.")

    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["portale :8090 non risponde", "`systemctl status lab11-portale`; rilanciare `lab 11`"],
        ["curl -d non fa una POST", "verificare la sintassi: `-d 'a=1&b=2'` senza spazi"],
        ["l'header non ha effetto", "attenzione a maiuscole nel valore: `X-Ruolo: dipendente`"],
        ["fermare a fine lezione", "`systemctl disable --now lab11-portale`"],
    ], widths=[3000, 6026])

    d.h1("Nota di continuità")
    d.p("Il portale su :8090 resta separato dalla Banca transazionale su :8080 (Lezione "
        "12) per non sovrapporsi. Firefox sulla Kali permette di mostrare gli stessi "
        "scambi con gli Strumenti per sviluppatori, utile per gli studenti più visivi.")
