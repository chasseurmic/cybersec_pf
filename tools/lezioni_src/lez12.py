# -*- coding: utf-8 -*-
NUM = 12
SLUG = "banca-della-scuola-sqli"
TITOLO = "Banca della Scuola e SQL injection base"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** conoscere la Banca della Scuola (la web app bersaglio del blocco) "
        "e sfruttare la vulnerabilita' piu' famosa del web: la SQL injection, per entrare "
        "senza password e per leggere dati riservati.",
        "**Al termine sai:** cos'e' una query SQL, come nasce la SQL injection, e come "
        "bypassare un login e far 'parlare' un database vulnerabile.",
        "**Flag in palio:** 2 flag (70 punti). I valori sono diversi su ogni macchina.",
    ])

    d.h1("Parte 1 · Quando il sito si fida troppo (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("La SQL injection e' una delle cause piu' comuni di grandi furti di dati nella "
        "storia di internet. Il meccanismo e' sempre lo stesso: un sito prende quello che "
        "scrivi in un campo (per esempio l'utente del login) e lo incolla dentro un "
        "comando per il database, senza controllarlo. Se scrivi qualcosa di furbo, quel "
        "qualcosa non viene trattato come testo, ma come parte del comando: e a quel "
        "punto comandi tu.")

    d.h2("Cos'e' una query e dove nasce il problema")
    d.p("Per controllare il login, il sito chiede al database una cosa del tipo: 'dammi "
        "l'utente che ha questo nome e questa password'. In SQL:")
    d.code([
        "SELECT * FROM utenti WHERE username='mario' AND password='segreta'",
    ])
    d.p("Se il sito costruisce questa frase incollando direttamente cio' che scrivi, tu "
        "puoi cambiarne il senso. Scrivendo come nome utente `admin' --` la frase diventa:")
    d.code([
        "SELECT * FROM utenti WHERE username='admin' -- ' AND password='...'",
    ])
    d.p("Il `--` in SQL avvia un commento: tutto quello che viene dopo (il controllo "
        "della password) viene ignorato. Risultato: il database restituisce l'utente "
        "admin e il sito ti fa entrare, senza che tu conosca la password.")

    d.h1("Parte 2 · Attacca la Banca della Scuola (pratica, 80 min)")
    d.p("Il docente lancia `lab 12` sul bersaglio (installa la Banca su :8080). Aprila in "
        "Firefox sulla Kali: `http://10.10.10.20:8080`.")

    d.h2("Passo 1 · Bypassa il login (+40)")
    d.p("Nel modulo di accesso, nel campo utente scrivi il payload e una password "
        "qualsiasi.")
    d.code([
        "utente:    admin' --",
        "password:  qualsiasi",
    ])
    d.p("Oppure dallo stesso terminale, con curl:")
    d.code(["curl -d \"utente=admin' -- &password=x\" http://10.10.10.20:8080/login"])
    d.p("Entri come amministratore e compare la prima flag. Prova anche il payload "
        "classico `' OR '1'='1' --` : e' vero per qualsiasi riga.")

    d.h2("Passo 2 · Fai parlare il database (+30)")
    d.p("Vai nella pagina 'Cerca conto'. Anche la ricerca costruisce male la query. "
        "Inserendo una condizione sempre vera, il database ti restituisce tutti i conti, "
        "compreso uno nascosto.")
    d.code([
        "nel campo di ricerca:   ' OR '1'='1' --",
        "",
        "oppure con curl:",
        "curl \"http://10.10.10.20:8080/cerca?conto=' OR '1'='1' -- \"",
    ])
    d.p("Nella riga del conto nascosto (la 'tesoreria') trovi la seconda flag.")

    d.box("blu", "Perche' funziona", items=[
        "Il dato dell'utente viene incollato nella query come se fosse codice.",
        "Gli apici `'` chiudono la stringa e permettono di aggiungere condizioni.",
        "Il commento `--` elimina il resto del controllo.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("La SQL injection e' un problema noto da vent'anni e ha una soluzione precisa e "
        "definitiva: non incollare mai i dati dentro la query.")
    d.box("verde", "Come si chiude, davvero", items=[
        "Usare le query parametrizzate (prepared statement): i dati viaggiano separati "
        "dal comando, il database non li confonde mai con codice.",
        "Non costruire query concatenando stringhe con l'input dell'utente.",
        "Validare i dati in ingresso, ma la difesa vera sono le query parametrizzate.",
        "Dare al database un utente con i minimi permessi: se qualcosa sfugge, limita i danni.",
    ])
    d.p("Esempio della stessa query, fatta in modo sicuro (i `?` sono riempiti dal "
        "database, non dalla stringa):")
    d.code([
        "SELECT * FROM utenti WHERE username=? AND password=?",
        "# i valori 'mario' e 'segreta' passano a parte: non possono diventare codice",
    ])

    d.h2("Punteggio della Lezione 12")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Bypass del login", "utente: admin' --", "40"],
        ["Lettura di tutti i conti", "cerca: ' OR '1'='1' --", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 12** · Banca della Scuola e SQL injection base (Blocco 4, con tool: la "
        "web app e' la piattaforma di tutto il blocco).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso, Python3 (presente su Ubuntu). Questa lezione "
        "installa la piattaforma usata anche dalle Lezioni 13-18.",
        "**Deliverable studente:** 2 flag (70 punti), valori diversi per macchina.",
    ])

    d.h1("Scelta di progetto (importante)")
    d.p("Il brief prevedeva un'app Flask in docker-compose. Per garantire il "
        "funzionamento OFFLINE nel laboratorio isolato (senza pip ne' pull di immagini) "
        "la Banca e' realizzata in Python della sola libreria standard (http.server + "
        "sqlite3) e gira come servizio systemd `banca` sul bersaglio, sulla porta 8080, "
        "al posto della pagina statica nginx. Le vulnerabilita' (SQLi, XSS, controllo "
        "accessi, path traversal) sono identiche a quelle di una vera app vulnerabile; "
        "cambia solo il motore. Il sorgente e' in `/opt/lab/banca-app/banca.py` sul "
        "bersaglio (ed e' incorporato in `lezioni/lezione-12/target.sh`).")

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Genera (una sola volta) `/opt/lab/banca-app/flags.env` con i valori delle flag "
        "casuali e la password admin casuale; poi li riusa (flag stabili nel blocco).",
        "Scrive l'app `banca.py`, azzera il database, ferma il vecchio container nginx su "
        ":8080, installa il servizio `banca` (systemd) e l'helper `banca-ctl`.",
        "Il database viene ricreato e seminato al primo avvio (utenti, segreti, conto "
        "nascosto 'tesoreria').",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets(["Verifica che la Banca risponda e mostra la missione (payload SQLi)."])

    d.h1("Vulnerabilita' della piattaforma (usate nel blocco)")
    d.table(["Endpoint", "Vulnerabilita'", "Lezione"], [
        ["POST /login", "SQL injection (bypass) ", "12"],
        ["GET /cerca", "SQL injection (dump, UNION) + XSS riflesso", "12, 13, 14"],
        ["/bacheca", "XSS memorizzato", "14"],
        ["cookie sessione, /pannello", "controllo accessi rotto", "15"],
        ["login", "forzabile a dizionario", "16"],
        ["GET /documenti?file=", "path traversal / LFI", "17"],
    ], widths=[2800, 4226, 2000])

    d.h1("Soluzioni e valori delle flag")
    d.p("I valori sono generati a runtime e sono diversi su ogni macchina. Leggili sul "
        "bersaglio con:")
    d.code(["sudo cat /opt/lab/banca-app/flags.env"])
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1 · login bypass", "utente: admin' --  (oppure ' OR '1'='1' --)", "FLAG_SQLI_LOGIN"],
        ["2 · dump conti", "cerca: ' OR '1'='1' --  (mostra il conto 'tesoreria')",
         "FLAG_SQLI_DUMP"],
    ], widths=[2000, 5026, 2000])
    d.p("Utenti nel database: admin (password casuale, in flags.env), cliente/cliente "
        "(login regolare di prova), sara.verdi (password `primavera`, per il brute force "
        "della Lezione 16), tesoreria (conto nascosto con la flag del dump).")

    d.h1("Rigiocare e resettare")
    d.bullets([
        "Reset completo del database: `banca-ctl reset` (oppure rilancia `lab 12`).",
        "Le flag restano stabili (flags.env non viene rigenerato). Per cambiarle: "
        "`sudo rm /opt/lab/banca-app/flags.env` e rilancia `lab 12`.",
        "Stato del servizio: `banca-ctl stato` oppure `systemctl status banca`.",
    ])

    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        [":8080 non risponde", "`systemctl status banca`; se la porta e' occupata dal "
         "vecchio nginx, `docker rm -f banca` e rilancia `lab 12`"],
        ["il payload non entra", "attenzione allo spazio dopo `--`; nei form del browser "
         "va bene, con curl usare `-d \"...\"` mantenendo lo spazio"],
        ["le flag non compaiono", "database non seminato: `banca-ctl reset`"],
        ["voglio leggere le flag", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2600, 6426])

    d.h1("Nota di sicurezza")
    d.p("L'app e' volutamente insicura: va usata SOLO sul bersaglio del laboratorio "
        "isolato. Non esporla mai su reti reali. A fine corso: `systemctl disable --now "
        "banca`.")
