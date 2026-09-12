# -*- coding: utf-8 -*-
NUM = 14
SLUG = "xss-reflected-stored"
TITOLO = "XSS: reflected e stored"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire il Cross-Site Scripting (XSS), la vulnerabilita' che "
        "permette di far eseguire il proprio JavaScript nel browser di altri utenti, e "
        "distinguere la versione riflessa da quella memorizzata.",
        "**Al termine sai:** iniettare uno script in un campo non filtrato, capire la "
        "differenza tra XSS riflesso e memorizzato, e perche' il secondo e' piu' "
        "pericoloso.",
        "**Flag in palio:** 2 flag (70 punti). Prerequisito: Banca (Lezione 12).",
    ])

    d.h1("Parte 1 · Quando il sito esegue le tue parole (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Il furto di sessioni sui social, i commenti che rubano i dati di chi li legge, i "
        "finti moduli che compaiono dentro un sito vero: dietro c'e' quasi sempre l'XSS. "
        "Succede quando un sito prende quello che scrivi e lo rimette nella pagina senza "
        "ripulirlo. Il browser non distingue il testo scritto dallo sviluppatore da "
        "quello scritto da te: se ci metti un `<script>`, lo esegue.")

    d.h2("Riflesso contro memorizzato")
    d.table(["Tipo", "Come funziona", "Chi colpisce"], [
        ["Riflesso", "lo script e' nella URL/richiesta e torna subito nella risposta",
         "chi apre il link che gli mandi"],
        ["Memorizzato", "lo script viene salvato dal sito (un commento, un messaggio)",
         "chiunque visiti la pagina, in automatico"],
    ], widths=[1600, 4826, 2600])
    d.p("Il memorizzato e' piu' pericoloso: lo carichi una volta e colpisce tutti, "
        "compreso l'amministratore quando apre la bacheca.")

    d.h2("Un payload semplice")
    d.code([
        "<script>alert('xss')</script>       # fa comparire un pop-up: prova che gira JS",
        "<img src=x onerror=alert(1)>        # variante senza la parola script",
    ])

    d.h1("Parte 2 · Buca la Banca con l'XSS (pratica, 80 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12), poi `lab 14`. Lavora in Firefox sulla "
        "Kali: `http://10.10.10.20:8080`.")

    d.h2("Passo 1 · XSS riflesso nella ricerca (+30)")
    d.p("La pagina 'Cerca conto' rimette in pagina quello che scrivi, senza ripulirlo.")
    d.code([
        "nel campo di ricerca:   <script>alert('xss')</script>",
        "",
        "per leggere la flag (nel sorgente della risposta):",
        "curl \"http://10.10.10.20:8080/cerca?conto=<script>alert(1)</script>\" | grep FLAG",
    ])
    d.p("In Firefox vedi il pop-up: e' la prova che il tuo codice e' stato eseguito.")

    d.h2("Passo 2 · XSS memorizzato nella bacheca (+40)")
    d.p("La bacheca salva i messaggi e li mostra a tutti, senza ripulirli. Pubblica uno "
        "script: da quel momento parte per ogni visitatore.")
    d.code([
        "nel messaggio della bacheca:   <script>alert('bucato')</script>",
        "",
        "ricarica la pagina in Firefox: il pop-up riparte da solo.",
        "leggi la flag:",
        "curl \"http://10.10.10.20:8080/bacheca\" | grep FLAG",
    ])
    d.box("rosso", "Perche' e' grave", items=[
        "Un vero payload non fa un pop-up: ruba il cookie di sessione e lo manda "
        "all'attaccante (`document.cookie`), oppure compie azioni al posto tuo.",
        "Con l'XSS memorizzato basta che l'admin apra la pagina per farsi rubare la sessione.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Come si ferma l'XSS", items=[
        "Escape dell'output: ogni dato dell'utente va 'neutralizzato' prima di finire in "
        "pagina (i `<` diventano `&lt;`), cosi' e' testo e non codice.",
        "Validare l'input, ma la difesa vera e' l'escape in uscita, sempre.",
        "Content Security Policy (CSP): dice al browser quali script puo' eseguire.",
        "Cookie di sessione con HttpOnly: il JavaScript non li puo' leggere, cosi' un XSS "
        "non li ruba.",
    ])
    d.p("La stessa bacheca, fatta bene, mostrerebbe `<script>...</script>` come testo "
        "innocuo, non come codice.")

    d.h2("Punteggio della Lezione 14")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["XSS riflesso", "script nel campo ricerca", "30"],
        ["XSS memorizzato", "script pubblicato in bacheca", "40"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 14** · XSS riflesso e memorizzato (Blocco 4).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Banca installata (Lezione 12); Firefox sulla Kali.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire l'XSS come esecuzione di codice altrui nel browser della vittima.",
        "Distinguere riflesso e memorizzato e la diversa gravita'.",
        "Collegare alla difesa: escape in output, CSP, cookie HttpOnly.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh: verifica la Banca (altrimenti chiede `lab 12`), riavvia il servizio e "
        "azzera la bacheca (un solo messaggio di benvenuto), cosi' la flag del "
        "memorizzato compare solo dopo l'iniezione dello studente.",
        "L'app premia il payload: quando la ricerca riflette uno script, o la bacheca ne "
        "salva uno, aggiunge la flag in un commento HTML della risposta (oltre a "
        "eseguirlo davvero in Firefox).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1 · riflesso", "/cerca?conto=<script>alert(1)</script>  (curl ... | grep FLAG)",
         "FLAG_XSS_REFLECTED"],
        ["2 · memorizzato", "pubblicare <script>...</script> in /bacheca", "FLAG_XSS_STORED"],
    ], widths=[1800, 5226, 2000])
    d.p("La flag arriva come commento HTML quando il payload contiene `<script`, "
        "`onerror=` o `<img`. In Firefox il pop-up conferma l'esecuzione reale.")
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["il pop-up non parte in Firefox", "verificare di essere sulla Banca :8080 e non "
         "sul portale :8090 (che escapa l'input)"],
        ["la flag memorizzato non appare", "il messaggio non conteneva uno script: "
         "ripubblicare con `<script>`; `lab 14` ripulisce la bacheca"],
        ["voglio ripulire la bacheca", "rilanciare `lab 14` (azzera i messaggi)"],
    ], widths=[3000, 6026])
    d.h1("Nota didattica")
    d.p("Il portale della Lezione 11 (:8090) escapa correttamente l'input: e' l'esempio "
        "'giusto'. La Banca (:8080) no: e' l'esempio 'sbagliato' da bucare. Il confronto "
        "aiuta a far vedere la differenza tra codice sicuro e insicuro.")
