# -*- coding: utf-8 -*-
NUM = 29
SLUG = "pagina-phishing-didattica"
TITOLO = "Pagina di phishing didattica nel lab"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 20 min teoria · 85 min pratica · 15 min difesa.",
        "**Obiettivo:** capire come funziona una pagina di phishing costruendone una nel "
        "laboratorio: un clone del login della Banca che cattura le credenziali e rimanda "
        "al sito vero, cosi' la vittima non si accorge di nulla.",
        "**Al termine sai:** clonare una pagina di login, capire come cattura i dati e "
        "perche' il redirect al sito vero rende l'inganno credibile.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.box("rosso", "Regola assoluta", items=[
        "Il phishing e' un reato (sostituzione di persona, frode informatica). Questa "
        "pagina si usa SOLO nel laboratorio isolato, contro il finto utente del lab. Mai, "
        "in nessun caso, verso persone reali.",
    ])

    d.h1("Parte 1 · L'esca perfetta (teoria, 20 min)")
    d.h2("Il caso reale")
    d.p("Il phishing e' l'attacco piu' diffuso al mondo. Arriva una email che sembra della "
        "banca, con un link a una pagina identica a quella vera. La vittima inserisce "
        "utente e password, che finiscono all'attaccante. Poi la pagina la rimanda al "
        "sito vero: la vittima pensa di aver solo sbagliato a digitare, riprova, entra, e "
        "non sospetta nulla. Oggi costruisci esattamente questo meccanismo, per capirlo e "
        "smontarlo.")

    d.h2("I tre ingredienti di una pagina di phishing")
    d.bullets([
        "**Il clone:** una copia dell'aspetto del sito vero (spesso basta salvare la "
        "pagina).",
        "**La cattura:** un form che, invece di far entrare, salva utente e password "
        "dall'attaccante.",
        "**Il redirect:** dopo la cattura rimanda al sito vero, per non insospettire la "
        "vittima.",
    ])

    d.h1("Parte 2 · Costruisci la pagina civetta (pratica, 85 min)")
    d.p("Sulla Kali `lab 29` installa il kit di phishing; sul bersaglio `lab 29` avvia un "
        "finto utente che 'abbocca' inviando le sue credenziali alla pagina.")

    d.h2("Passo 1 · Avvia la pagina di phishing")
    d.p("Leggi il codice: nota la cattura e il redirect al sito vero. Poi avviala e "
        "guardala in Firefox: sembra il login vero.")
    d.code([
        "cd ~/lab/lezione-29",
        "cat phish.py",
        "sudo python3 phish.py",
    ])

    d.h2("Passo 2 · La vittima abbocca (+40)")
    d.p("Il finto utente del bersaglio invia le sue credenziali alla tua pagina. Guardale "
        "arrivare.")
    d.code([
        "tail -f ~/lab/lezione-29/catturate.log",
        "# ogni riga catturata mostra utente, password e una flag",
    ])

    d.h2("Passo 3 · Leggi la password pescata (+30)")
    d.code(["lab29-verifica <la-password-catturata>"])

    d.box("blu", "Come si combina con gli altri attacchi", items=[
        "Il link alla pagina arriva con una email di social engineering (Lezione 28).",
        "Con il DNS spoofing (Lezione 26) la vittima ci finisce anche digitando l'indirizzo "
        "giusto.",
        "Senza HTTPS valido, la barra degli indirizzi e' l'unico indizio: da qui la difesa.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Non abboccare", items=[
        "Guardare sempre l'indirizzo nella barra: il dominio e' quello giusto? (banca vera "
        "vs banca-verifica-account.xyz)",
        "Diffidare dei link nelle email e nei messaggi: meglio digitare l'indirizzo a mano "
        "o usare i preferiti.",
        "Il lucchetto HTTPS con dominio corretto; un avviso sul certificato e' un allarme.",
        "L'autenticazione a due fattori: anche se rubano la password, manca il secondo "
        "fattore.",
        "In azienda: segnalare le email sospette; filtri anti-phishing sulla posta.",
    ])

    d.h2("Punteggio della Lezione 29")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["La vittima abbocca", "phish.py cattura le credenziali", "40"],
        ["Password pescata", "lab29-verifica", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 29** · Pagina di phishing didattica (Blocco 7, con tool).",
        "**Tempi:** 20 min teoria · 85 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali e bersaglio sulla stessa rete interna; Python3.",
        "**Deliverable studente:** 2 flag (70 punti) + un kit di phishing didattico.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire il meccanismo del phishing costruendone uno (clone, cattura, redirect).",
        "Collegare a social engineering (L28) e DNS spoofing (L26).",
        "Insistere sull'uso etico e sulla difesa (dominio, HTTPS, 2FA).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh installa `~/lab/lezione-29/phish.py`: clone del login su :8080 che salva "
        "le credenziali in `catturate.log` (campi decodificati e leggibili) e rimanda al "
        "sito vero. Installa `lab29-verifica`.",
        "target.sh genera FLAG_PHISH e avvia `lab29-vittima.service`: invia ogni 5s a "
        "10.10.10.5:8080 le credenziali `vittima`/`Pesc3Rosso!` con la flag nel campo nota.",
        "Catena verificata in locale: la vittima invia -> phish.py cattura (flag + password).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("FLAG_PHISH e' generata a runtime sul bersaglio: `sudo cat /opt/lab/lab29/flags.env`.")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["2", "phish.py in ascolto ; leggere catturate.log (campo nota)", "FLAG_PHISH (nota catturata)"],
        ["3", "password catturata = Pesc3Rosso! ; lab29-verifica Pesc3Rosso!", "FLAG{credenziali_pescate}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["porta 8080 occupata sulla Kali", "chiudere altri servizi o cambiare porta in "
         "phish.py e nella vittima"],
        ["catturate.log vuoto", "phish.py deve girare; il servizio vittima sul bersaglio "
         "deve essere attivo (`systemctl status lab29-vittima`) e puntare a 10.10.10.5"],
        ["la vittima non raggiunge la Kali", "verificare l'IP interno della Kali (10.10.10.5)"],
    ], widths=[3000, 6026])
    d.h1("Nota etica e di sicurezza")
    d.p("E' fondamentale ripetere agli studenti che questa tecnica e' illegale fuori dal "
        "laboratorio. Il valore didattico e' capire l'inganno per difendersi. A fine "
        "lezione: `systemctl disable --now lab29-vittima` sul bersaglio.")
