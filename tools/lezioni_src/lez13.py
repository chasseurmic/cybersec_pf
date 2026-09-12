# -*- coding: utf-8 -*-
import comune
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
        "risultati normali, i dati di qualunque altra tabella. È così che sono finiti "
        "online interi database di siti famosi.")

    d.h2("UNION: unire due SELECT")
    d.p("`UNION SELECT` attacca i risultati di una seconda query a quelli della prima. C'è "
        "una regola: le due query devono restituire lo stesso numero di colonne. La "
        "ricerca della Banca ne restituisce 3 (utente, conto, nota), quindi anche la "
        "nostra UNION deve avere 3 colonne.")
    d.code([
        "' UNION SELECT chiave, valore, 'x' FROM segreti -- ",
        "# 3 colonne: chiave, valore, e un riempitivo 'x'",
    ])

    d.h2("Leggere lo schema")
    d.p("Prima di estrarre, conviene sapere quali tabelle e colonne esistono. In SQLite "
        "la mappa del database è nella tabella speciale `sqlite_master`.")
    d.code(["' UNION SELECT name, sql, 'x' FROM sqlite_master -- "])

    d.h2("sqlmap: il pilota automatico")
    d.p("Fare tutto a mano insegna, ma nel lavoro reale si usa sqlmap: prova da solo "
        "decine di tecniche, capisce quante colonne servono, trova le tabelle e le "
        "scarica. È potente e va usato solo dove sei autorizzato (qui, il lab).")

    d.h1("Parte 2 · Svuota il database (pratica, 80 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12) e poi `lab 13` (aggiunge una tabella "
        "'carte'). Il campo vulnerabile è la ricerca: `/cerca?conto=...`")

    d.h2("Passo 1 · Estrai il segreto con UNION, a mano (+30)")
    d.p("Prima esplora le tabelle, poi estrai dalla tabella `segreti`.")
    d.code([
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT name,sql,'x' FROM sqlite_master -- \"",
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- \"",
    ])
    d.p("Nel valore del segreto c'è la prima flag. Prova anche a dumpare gli utenti con "
        "le password: `' UNION SELECT username,password,ruolo FROM utenti -- `")

    d.h2("Passo 2 · Automatizza con sqlmap (+40)")
    d.p("Lascia che sqlmap trovi l'iniezione e scarichi tutto. Scoprira' anche la tabella "
        "`carte`, che a mano non avevi cercato.")
    d.code([
        "sqlmap -u \"http://10.10.10.20:8080/cerca?conto=1\" -p conto --batch --dbms=sqlite --dump",
    ])
    d.p("Tra i dati scaricati c'è la tabella `carte`: nel campo cvv della 'Tesoreria' "
        "trovi la seconda flag. Nota quanto è veloce rispetto al lavoro manuale.")

    d.box("blu", "Trucchi utili", items=[
        "Se non sai quante colonne servono: prova `ORDER BY 1--`, `ORDER BY 2--`, ... "
        "finché dà errore; l'ultimo numero valido è il numero di colonne.",
        "Il commento `-- ` (con lo spazio) elimina il resto della query.",
        "sqlmap salva i risultati in una cartella: leggila per ritrovare il bottino.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("La difesa è la stessa della lezione scorsa, ma qui si vede quanto è grave il "
        "danno se manca: un intero database esfiltrato in un minuto.")
    d.box("verde", "Difendere davvero", items=[
        "Query parametrizzate ovunque: è la contromisura che chiude sia il bypass sia "
        "l'estrazione UNION.",
        "Non salvare le password in chiaro (le vedremo hashate nel Blocco 5): se il DB "
        "esce, almeno le password non sono leggibili subito.",
        "Dati sensibili (numeri di carta) cifrati e con accesso minimo.",
        "Web Application Firewall e monitoraggio: sqlmap fa rumore, si può rilevare.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Oltre la UNION: SQL injection alla cieca', "Non sempre i risultati della query si vedono in pagina. In quei casi si usa la SQL injection 'blind' (alla cieca): si pongono al database domande a risposta si'/no e si deduce il dato una lettera alla volta. Nella variante boolean-based si guarda se la pagina cambia (un risultato in più o in meno) quando la condizione è vera. Nella variante time-based si chiede al database di 'aspettare' qualche secondo se la condizione è vera, e si misura il tempo di risposta. È lento a mano, ma sqlmap lo automatizza: per questo uno strumento del genere è così potente, e per questo va usato solo dove sei autorizzato."),
        ],
        sintesi=[
            'UNION SELECT unisce i risultati e permette di leggere altre tabelle: serve lo stesso numero di colonne.',
            "sqlite_master è la mappa del database: da lì si scoprono tabelle e struttura.",
            "sqlmap automatizza tutto: trova l'iniezione, capisce le colonne, scarica le tabelle.",
            "Il danno reale della SQLi è l'esfiltrazione: interi database online in un minuto.",
            'Difesa: query parametrizzate, dati sensibili cifrati, monitoraggio (sqlmap fa rumore).',
        ],
        glossario=[
            ('UNION SELECT', 'attacca i risultati di una seconda query alla prima'),
            ('Allineamento colonne', 'la UNION richiede lo stesso numero e tipo di colonne'),
            ('sqlite_master', 'tabella speciale con lo schema del database SQLite'),
            ('sqlmap', 'strumento che automatizza lo sfruttamento della SQL injection'),
            ('Dump', "l'estrazione completa dei dati di una o più tabelle"),
            ('Esfiltrazione', 'portare fuori i dati rubati da un sistema'),
        ],
        errori=[
            "Sbagliare il numero di colonne nella UNION (usa ORDER BY o riempitivi 'x').",
            "Non indicare a sqlmap il parametro (-p) e il dbms (--dbms=sqlite): va più lento.",
            "Usare sqlmap fuori da un contesto autorizzato: è potente e va usato solo nel lab.",
            'Salvare numeri di carta o segreti in chiaro nel database.',
        ],
        domande=[
            "Perché la UNION richiede lo stesso numero di colonne?",
            'Come scopri le tabelle di un database SQLite via SQLi?',
            "Cosa fa sqlmap che a mano richiederebbe molto più tempo?",
            "Qual è il danno concreto di una SQL injection non chiusa?",
            'Quali difese rendono inutile un attacco UNION?',
        ],
        collegamenti=[
            'Lezione 12: la SQL injection di base, prerequisito di questa.',
            'Lezione 18: il mini CTF che concatena SQLi e altre falle.',
            'Lezione 20: cosa fare con le password (hashate) trovate in un dump.',
        ],
    )


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
        "Capire la gravità: dal bypass all'esfiltrazione totale.",
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
        "-p conto --batch --dbms=sqlite --dump`. Con `--dbms=sqlite` va più veloce. sqlmap "
        "salva l'output in ~/.local/share/sqlmap/output (o ~/.sqlmap).")
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["UNION dà errore di colonne", "servono 3 colonne; contarle con ORDER BY o "
         "aggiungere riempitivi 'x'"],
        ["sqlmap non trova l'iniezione", "indicare il parametro con `-p conto` e "
         "`--dbms=sqlite`; usare `--batch`"],
        ["manca la tabella carte", "è stata azzerata da un reset del DB: rilancia `lab 13`"],
        ["voglio i valori", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("La tabella `carte` con numeri e cvv finti serve a mostrare il danno concreto di "
        "una esfiltrazione. Dati inventati, solo nel lab isolato.")
