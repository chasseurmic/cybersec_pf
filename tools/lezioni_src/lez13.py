# -*- coding: utf-8 -*-
NUM = 13
SLUG = "sql-injection-avanzata-sqlmap"
TITOLO = "SQL injection avanzata e sqlmap"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** passare dal semplice bypass all'estrazione completa dei dati con "
        "la tecnica UNION, e automatizzare tutto con sqlmap.",
        "**Al termine sai:** capire quante colonne restituisce una query, usare `UNION "
        "SELECT` per leggere altre tabelle, elencare lo schema del database e lanciare "
        "sqlmap per dumparlo in automatico.",
        "**Flag in palio:** 2 flag (70 punti). Prerequisito: Banca installata (Lezione 12).",
    ])

    d.h1("Parte 1 · Far dire al database quello che vuoi (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Nella lezione scorsa siamo entrati senza password. Ma il vero bottino di una SQL "
        "injection sono i dati: elenchi di clienti, password, numeri di carta. La tecnica "
        "UNION permette di attaccare una query di ricerca e farle restituire, insieme ai "
        "risultati normali, i dati di qualunque altra tabella. E' cosi' che sono finiti "
        "online interi database di siti famosi.")

    d.h2("UNION: unire due SELECT")
    d.p("`UNION SELECT` attacca i risultati di una seconda query a quelli della prima. C'e' "
        "una regola: le due query devono restituire lo stesso numero di colonne. La "
        "ricerca della Banca ne restituisce 3 (utente, conto, nota), quindi anche la "
        "nostra UNION deve avere 3 colonne.")
    d.code([
        "' UNION SELECT chiave, valore, 'x' FROM segreti -- ",
        "# 3 colonne: chiave, valore, e un riempitivo 'x'",
    ])

    d.h2("Leggere lo schema")
    d.p("Prima di estrarre, conviene sapere quali tabelle e colonne esistono. In SQLite "
        "la mappa del database e' nella tabella speciale `sqlite_master`.")
    d.code(["' UNION SELECT name, sql, 'x' FROM sqlite_master -- "])

    d.h2("sqlmap: il pilota automatico")
    d.p("Fare tutto a mano insegna, ma nel lavoro reale si usa sqlmap: prova da solo "
        "decine di tecniche, capisce quante colonne servono, trova le tabelle e le "
        "scarica. E' potente e va usato solo dove sei autorizzato (qui, il lab).")

    d.h1("Parte 2 · Svuota il database (pratica, 80 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12) e poi `lab 13` (aggiunge una tabella "
        "'carte'). Il campo vulnerabile e' la ricerca: `/cerca?conto=...`")

    d.h2("Passo 1 · Estrai il segreto con UNION, a mano (+30)")
    d.p("Prima esplora le tabelle, poi estrai dalla tabella `segreti`.")
    d.code([
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT name,sql,'x' FROM sqlite_master -- \"",
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- \"",
    ])
    d.p("Nel valore del segreto c'e' la prima flag. Prova anche a dumpare gli utenti con "
        "le password: `' UNION SELECT username,password,ruolo FROM utenti -- `")

    d.h2("Passo 2 · Automatizza con sqlmap (+40)")
    d.p("Lascia che sqlmap trovi l'iniezione e scarichi tutto. Scoprira' anche la tabella "
        "`carte`, che a mano non avevi cercato.")
    d.code([
        "sqlmap -u \"http://10.10.10.20:8080/cerca?conto=1\" -p conto --batch --dbms=sqlite --dump",
    ])
    d.p("Tra i dati scaricati c'e' la tabella `carte`: nel campo cvv della 'Tesoreria' "
        "trovi la seconda flag. Nota quanto e' veloce rispetto al lavoro manuale.")

    d.box("blu", "Trucchi utili", items=[
        "Se non sai quante colonne servono: prova `ORDER BY 1--`, `ORDER BY 2--`, ... "
        "finche' da' errore; l'ultimo numero valido e' il numero di colonne.",
        "Il commento `-- ` (con lo spazio) elimina il resto della query.",
        "sqlmap salva i risultati in una cartella: leggila per ritrovare il bottino.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("La difesa e' la stessa della lezione scorsa, ma qui si vede quanto e' grave il "
        "danno se manca: un intero database esfiltrato in un minuto.")
    d.box("verde", "Difendere davvero", items=[
        "Query parametrizzate ovunque: e' la contromisura che chiude sia il bypass sia "
        "l'estrazione UNION.",
        "Non salvare le password in chiaro (le vedremo hashate nel Blocco 5): se il DB "
        "esce, almeno le password non sono leggibili subito.",
        "Dati sensibili (numeri di carta) cifrati e con accesso minimo.",
        "Web Application Firewall e monitoraggio: sqlmap fa rumore, si puo' rilevare.",
    ])

    d.h2("Punteggio della Lezione 13")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["UNION manuale", "estrarre da segreti con UNION SELECT", "30"],
        ["Dump con sqlmap", "sqlmap --dump, tabella carte", "40"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 13** · SQL injection avanzata e sqlmap (Blocco 4).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Banca installata (Lezione 12); sqlmap sulla Kali (Lezione 2).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Tecnica UNION: allineamento delle colonne, lettura di altre tabelle, schema.",
        "Automazione con sqlmap e consapevolezza del suo potere (uso solo autorizzato).",
        "Capire la gravita': dal bypass all'esfiltrazione totale.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh: verifica che la Banca ci sia (altrimenti chiede `lab 12`), riavvia il "
        "servizio, aggiunge `FLAG_SQLMAP` a flags.env e crea la tabella `carte` con la "
        "flag nel campo cvv della 'Tesoreria'.",
        "kali.sh: verifica Banca e sqlmap, mostra la missione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1 · UNION", "/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- ",
         "FLAG_SQLI_UNION"],
        ["2 · sqlmap", "sqlmap ... --dump ; tabella carte, cvv Tesoreria", "FLAG_SQLMAP"],
    ], widths=[1600, 5426, 2000])
    d.p("Comando sqlmap di riferimento: `sqlmap -u \"http://10.10.10.20:8080/cerca?conto=1\" "
        "-p conto --batch --dbms=sqlite --dump`. Con `--dbms=sqlite` va piu' veloce. sqlmap "
        "salva l'output in ~/.local/share/sqlmap/output (o ~/.sqlmap).")
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["UNION da' errore di colonne", "servono 3 colonne; contarle con ORDER BY o "
         "aggiungere riempitivi 'x'"],
        ["sqlmap non trova l'iniezione", "indicare il parametro con `-p conto` e "
         "`--dbms=sqlite`; usare `--batch`"],
        ["manca la tabella carte", "e' stata azzerata da un reset del DB: rilancia `lab 13`"],
        ["voglio i valori", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("La tabella `carte` con numeri e cvv finti serve a mostrare il danno concreto di "
        "una esfiltrazione. Dati inventati, solo nel lab isolato.")
