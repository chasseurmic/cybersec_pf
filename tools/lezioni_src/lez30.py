# -*- coding: utf-8 -*-
NUM = 30
SLUG = "riconoscere-difendersi-phishing"
TITOLO = "Riconoscere e difendersi dal phishing"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** dopo aver costruito una pagina di phishing, imparare a "
        "smascherarla: riconoscere i domini falsi, leggere davvero i link e non abboccare.",
        "**Al termine sai:** distinguere un dominio vero da un lookalike, capire "
        "sottodomini e trappole, e usare un ispettore di URL.",
        "**Flag in palio:** 2 flag (70 punti). Lezione sulla Kali (offline).",
    ])

    d.h1("Parte 1 · Leggere davvero un indirizzo (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("La maggior parte del phishing si smaschera guardando bene l'indirizzo. Gli "
        "attaccanti usano domini che assomigliano a quelli veri: aggiungono parole, "
        "cambiano una lettera, mettono il nome vero come sottodominio di un dominio loro. "
        "Chi sa leggere un indirizzo non abbocca quasi mai.")

    d.h2("Dove finisci davvero: si legge da destra")
    d.p("In un dominio, la parte che conta sono le ultime due etichette prima della prima "
        "barra singola. Tutto quello che viene prima e' sottodominio o trucco.")
    d.table(["Indirizzo", "Dove finisci davvero"], [
        ["bancadellascuola.local/login", "bancadellascuola.local (vero)"],
        ["login.bancadellascuola.local/", "bancadellascuola.local (vero, sottodominio)"],
        ["bancadellascuola-sicurezza.xyz", "un altro dominio (.xyz): FALSO"],
        ["bancadellascuola.local.verifica-conto.ru", "verifica-conto.ru: FALSO"],
        ["bancadellascuola.secure-login.com", "secure-login.com: FALSO"],
    ], widths=[4600, 4426])

    d.h1("Parte 2 · Smaschera i link (pratica, 80 min)")
    d.p("Sulla Kali `lab 30` semina una lista di URL e un ispettore. Il dominio vero della "
        "Banca e' `bancadellascuola.local`.")

    d.h2("Passo 1 · Riconosci i link falsi (+40)")
    d.p("Leggi la lista e indica i numeri dei link che NON portano alla Banca vera.")
    d.code([
        "cd ~/lab/lezione-30",
        "cat urls.txt",
        "lab30-verifica phishing <numeri dei link falsi>",
    ])

    d.h2("Passo 2 · Dove porta davvero il link 4 (+30)")
    d.p("Usa l'ispettore per vedere il vero host e dominio del link ingannevole.")
    d.code([
        "python3 url-inspector.py \"http://bancadellascuola.local.verifica-conto.ru/login\"",
        "lab30-verifica dominio <dominio-vero>",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "La checklist antiphishing", items=[
        "Guarda il dominio (ultime due etichette): e' davvero quello giusto?",
        "Non fidarti del testo del link: puo' mostrare una cosa e portare altrove "
        "(passaci sopra o ispezionalo).",
        "Diffida di urgenza e minacce (si ricollega al social engineering).",
        "Non inserire credenziali arrivando da un link: apri il sito dai preferiti o "
        "digitando l'indirizzo.",
        "Attiva l'autenticazione a due fattori: e' la rete di sicurezza se abbocchi.",
        "Segnala le email sospette: proteggi anche gli altri.",
    ])

    d.h2("Punteggio della Lezione 30")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Riconosci i link falsi", "lab30-verifica phishing", "40"],
        ["Smaschera il dominio", "url-inspector + lab30-verifica dominio", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 30** · Riconoscere e difendersi dal phishing (Blocco 7, chiusura).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2). Nessun bersaglio.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Leggere correttamente un dominio (da destra) e riconoscere i lookalike.",
        "Distinguere sottodominio del sito vero da dominio dell'attaccante.",
        "Costruire la checklist antiphishing personale.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `~/lab/lezione-30/urls.txt` (5 link) e `url-inspector.py` (mostra "
        "host e dominio), e installa `lab30-verifica`.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "link falsi = 2, 4, 5 ; lab30-verifica phishing 2 4 5 (ordine libero)",
         "FLAG{occhio_al_dominio}"],
        ["2", "dominio del link 4 = verifica-conto.ru ; lab30-verifica dominio verifica-conto.ru",
         "FLAG{link_smascherato}"],
    ], widths=[700, 6026, 2300])
    d.p("Perche': 1 e 3 sono su bancadellascuola.local (3 e' un sottodominio, vero); 2 e' "
        ".xyz, 4 finisce su verifica-conto.ru, 5 su secure-login.com.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["phishing non passa", "servono esattamente 2 4 5 (ordine libero); niente altri numeri"],
        ["dominio non passa", "e' verifica-conto.ru (ultime due etichette del link 4)"],
        ["confusione sui sottodomini", "ribadire: si legge da destra; login.banca.local e' "
         "ancora banca.local"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("Chiude il Blocco 7. La coppia L29 (costruire) + L30 (difendersi) e' molto "
        "efficace: gli studenti smontano l'inganno dopo averlo montato. Utile mostrare "
        "esempi reali di email di phishing ricevute davvero (oscurando i dati).")
