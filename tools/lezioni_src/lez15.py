# -*- coding: utf-8 -*-
import comune
NUM = 15
SLUG = "autenticazione-cookie-sessioni"
TITOLO = "Autenticazione, cookie e sessioni"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire come un sito ti riconosce dopo il login (i cookie di "
        "sessione) e perché un cookie prevedibile permette di impersonare altri utenti e "
        "di scavalcare i controlli di accesso.",
        "**Al termine sai:** ispezionare e modificare i cookie, capire cosa è una "
        "sessione, e riconoscere un controllo di accesso rotto.",
        "**Flag in palio:** 2 flag (70 punti). Prerequisito: Banca (Lezione 12).",
    ])

    d.h1("Parte 1 · Come fa il sito a ricordarsi di te (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("HTTP non ha memoria: ogni richiesta è a se'. Allora come fa un sito a sapere che "
        "hai già fatto il login? Ti dà un cookie di sessione, un biglietto che il "
        "browser rimanda a ogni richiesta. Se quel biglietto è fatto male, prevedibile o "
        "non firmato, chiunque può fabbricarne uno e diventare un altro. Molti furti di "
        "account nascono proprio da cookie deboli o rubati.")

    d.h2("Sessione e cookie")
    d.p("Al login il server crea una sessione e te ne dà l'identificativo in un cookie. "
        "Un cookie fatto bene contiene un valore lungo e casuale, impossibile da "
        "indovinare, e legato lato server alla tua identità. Un cookie fatto male "
        "contiene, per esempio, direttamente il tuo nome utente: allora basta cambiarlo.")
    d.code([
        "# cookie DEBOLE (come quello della Banca):",
        "Set-Cookie: sessione=cliente",
        "# cookie ROBUSTO (esempio):",
        "Set-Cookie: sessione=9f3a...b21; HttpOnly; Secure",
    ])

    d.h1("Parte 2 · Ruba la sessione dell'admin (pratica, 80 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12), poi `lab 15`. Prima entra "
        "regolarmente e guarda che cookie ricevi.")
    d.code([
        "curl -i -d \"utente=cliente&password=cliente\" http://10.10.10.20:8080/login",
        "# nella risposta trovi:  Set-Cookie: sessione=cliente",
    ])
    d.p("Il cookie è semplicemente il tuo nome utente. Cosa succede se lo cambio in "
        "'admin'?")

    d.h2("Passo 1 · Impersona l'amministratore (+35)")
    d.p("Manda una richiesta con il cookie forgiato. Il sito ti trattera' come l'admin.")
    d.code([
        "curl -b \"sessione=admin\" http://10.10.10.20:8080/dashboard",
    ])
    d.p("Vedi il conto e la nota dell'amministratore: dentro c'è la flag.")

    d.h2("Passo 2 · Entra nel pannello riservato (+35)")
    d.p("Il pannello admin dovrebbe essere off-limits, ma si fida del cookie.")
    d.code([
        "curl -b \"sessione=admin\" http://10.10.10.20:8080/pannello",
    ])
    d.p("In Firefox puoi fare lo stesso senza curl: F12, scheda Archiviazione, Cookie, "
        "cambia il valore di `sessione` in `admin` e ricarica la pagina.")

    d.box("rosso", "Due errori in uno", items=[
        "Cookie prevedibile: contiene il nome utente, quindi si forgia a mano.",
        "Controllo accessi rotto: il pannello admin verifica solo il cookie, che però è "
        "controllato dall'utente. Mai fidarsi di ciò che arriva dal client.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Sessioni fatte bene", items=[
        "Identificativo di sessione lungo e casuale, salvato lato server; il cookie non "
        "contiene dati sensibili né indovinabili.",
        "Cookie con `HttpOnly` (non leggibile dal JavaScript, così un XSS non lo ruba) e "
        "`Secure` (solo su HTTPS).",
        "Il ruolo (admin o no) si controlla lato server sulla sessione reale, non su un "
        "valore che l'utente può cambiare.",
        "Scadenza delle sessioni e logout che le invalida davvero.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Sessioni lato server e token: come si fa bene', "Ci sono due modi corretti per ricordarsi di un utente dopo il login. Il primo: il server crea una sessione, le dà un identificativo lungo e casuale, lo salva da se' e mette solo quel codice nel cookie; a ogni richiesta ritrova la sessione e sa chi sei. Il secondo: rilascia un token firmato (es. JWT) che contiene le informazioni e una firma che il server verifica, così non deve conservare nulla. In entrambi i casi il punto è che il client non deve poter falsificare la propria identità: col cookie casuale non lo indovina, col token firmato non lo può alterare senza rompere la firma. Il difetto della nostra Banca (il cookie che contiene il nome utente in chiaro) è proprio l'errore da non fare."),
        ],
        sintesi=[
            'HTTP non ha memoria: il sito ti riconosce con un cookie di sessione dopo il login.',
            "Un cookie fatto male (prevedibile, non firmato) si può forgiare: così si impersona un altro utente.",
            "Il controllo accessi va fatto lato server sulla sessione reale, non su un valore che l'utente può cambiare.",
            'Due errori spesso insieme: cookie prevedibile + pagina admin che si fida del cookie.',
            'Difesa: sessioni casuali lato server, cookie HttpOnly e Secure, controllo del ruolo sul server.',
        ],
        glossario=[
            ('Sessione', 'lo stato che il server tiene per un utente dopo il login'),
            ('Cookie di sessione', "il 'biglietto' che identifica la sessione a ogni richiesta"),
            ('Cookie prevedibile', "un cookie il cui valore si può indovinare o costruire"),
            ('Furto di sessione', 'usare il cookie di un altro per impersonarlo'),
            ('Controllo accessi rotto', "quando i permessi si basano su dati controllati dall'utente"),
            ('HttpOnly / Secure', 'flag che proteggono il cookie (dal JS / solo su HTTPS)'),
        ],
        errori=[
            'Mettere nel cookie dati sensibili o prevedibili (il nome utente in chiaro).',
            'Verificare il ruolo (admin?) su un valore che arriva dal client.',
            'Cookie senza HttpOnly/Secure: rubabili via XSS o su HTTP.',
            'Non invalidare davvero la sessione al logout.',
        ],
        domande=[
            "Perché HTTP ha bisogno dei cookie per 'ricordarti'?",
            'Cosa rende un cookie di sessione forgiabile?',
            "Cos'è un controllo di accesso rotto? Fai un esempio.",
            "Dove va verificato il ruolo di un utente, e perché?",
            'A cosa servono i flag HttpOnly e Secure?',
        ],
        collegamenti=[
            'Lezione 11: header e cookie, le basi di questa lezione.',
            "Lezione 14: l'XSS che ruba proprio il cookie di sessione.",
            "Lezione 16: le password deboli, l'altra via per entrare in un account.",
        ],
    )


    d.h2("Punteggio della Lezione 15")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Impersonare l'admin", "cookie sessione=admin su /dashboard", "35"],
        ["Pannello riservato", "cookie sessione=admin su /pannello", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 15** · Autenticazione, cookie e sessioni (Blocco 4).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Banca installata (Lezione 12).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire sessioni e cookie e il ruolo del cookie di sessione.",
        "Riconoscere cookie prevedibili e controllo di accesso rotto (OWASP: Broken Access "
        "Control, Identification and Authentication Failures).",
        "Collegare alla difesa: sessioni casuali, HttpOnly/Secure, controllo lato server.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh: verifica la Banca (altrimenti `lab 12`), riavvia il servizio, aggiunge "
        "`FLAG_SESSIONE` a flags.env e la scrive nella nota dell'utente admin.",
        "La Banca usa un cookie `sessione=<username>` (volutamente prevedibile) e /pannello "
        "controlla solo quel cookie.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1", "curl -b 'sessione=admin' /dashboard (nota dell'admin)", "FLAG_SESSIONE"],
        ["2", "curl -b 'sessione=admin' /pannello", "FLAG_COOKIE_ADMIN"],
    ], widths=[900, 5626, 2500])
    d.p("Login regolare di prova: `cliente / cliente`. Serve per far vedere il cookie "
        "'onesto' prima di forgiarlo.")
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["dashboard senza flag", "cookie non impostato: usare `-b 'sessione=admin'`; "
         "rilanciare `lab 15` per riscrivere la nota admin"],
        ["/pannello 403", "cookie diverso da 'admin': controllare il valore"],
        ["voglio i valori", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("La lezione unisce due debolezze OWASP (cookie prevedibile e controllo accessi "
        "rotto) che spesso vanno insieme. In Firefox l'editor dei cookie (F12 > "
        "Archiviazione) rende il concetto molto concreto per gli studenti.")
