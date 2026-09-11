# -*- coding: utf-8 -*-
NUM = 7
SLUG = "footprinting-osint"
TITOLO = "Footprinting e OSINT (simulati nel lab)"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** raccogliere informazioni su un bersaglio prima di attaccarlo, "
        "usando solo cio' che il bersaglio stesso espone (footprinting) e le fonti "
        "aperte (OSINT), qui simulate dentro il laboratorio isolato.",
        "**Al termine sai:** fare fingerprint di un sito, leggere le intestazioni HTTP, "
        "spulciare il codice sorgente e robots.txt, scovare cartelle nascoste con un "
        "dir buster, e ricostruire il formato delle email aziendali.",
        "**Flag in palio:** 4 flag (70 punti).",
    ])

    d.h1("Parte 1 · Guardare prima di toccare (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Prima di ogni attacco serio c'e' una fase silenziosa: la raccolta di "
        "informazioni. Chi attacca vuole sapere che tecnologie usi, chi lavora nella tua "
        "azienda, che email avete, cosa avete pubblicato per sbaglio. Spesso non serve "
        "bucare niente: le informazioni sono gia' li', in un commento nel codice, in una "
        "cartella lasciata online, in un vecchio backup. Questo mestiere si chiama OSINT "
        "(Open Source INTelligence): intelligence dalle fonti aperte.")
    d.p("Nel nostro laboratorio non usciamo su internet: mai. Abbiamo pero' seminato sul "
        "bersaglio un finto footprint pubblico, cosi' potete allenare le stesse tecniche "
        "in sicurezza, contro dati inventati.")

    d.h2("Footprinting attivo vs OSINT passivo")
    d.bullets([
        "**OSINT passivo:** guardare cio' che e' gia' pubblico senza toccare il bersaglio "
        "(motori di ricerca, social, registri). Il bersaglio non se ne accorge.",
        "**Footprinting attivo:** interrogare direttamente il bersaglio (visitare il "
        "sito, leggere robots.txt, cercare cartelle). Lascia qualche traccia.",
    ])

    d.h2("Le briciole che lascia un sito web")
    d.table(["Dove guardare", "Cosa puo' rivelare"], [
        ["Intestazioni HTTP", "server, tecnologie, a volte header di debug dimenticati"],
        ["Codice sorgente (HTML)", "commenti degli sviluppatori, percorsi, note interne"],
        ["robots.txt", "cartelle che il sito preferisce non far indicizzare"],
        ["Directory listing", "elenco dei file quando manca la pagina indice"],
        ["Pagina 'chi siamo'", "nomi, ruoli, email (da cui si deduce il formato)"],
        ["File di backup (.old, .bak)", "vecchie credenziali e configurazioni"],
    ], widths=[3000, 6026])

    d.h1("Parte 2 · Profila la Banca della Scuola (pratica, 80 min)")
    d.p("Il docente lancia `lab 7` sul bersaglio (arricchisce il sito), poi sulla Kali "
        "`lab 7` prepara una piccola wordlist e mostra la missione.")

    d.h2("Passo 1 · Fingerprint e intestazioni (+15)")
    d.p("Chiedi al server chi e' e guarda le intestazioni HTTP: a volte contengono piu' "
        "del dovuto.")
    d.code([
        "whatweb http://10.10.10.20:8080",
        "curl -I http://10.10.10.20:8080",
    ])
    d.p("Un header di debug dimenticato ti regala la prima flag.")

    d.h2("Passo 2 · I commenti nel codice (+15)")
    d.p("Il browser mostra la pagina, ma il codice sorgente mostra anche i commenti. "
        "Scaricalo e cerca.")
    d.code([
        "curl -s http://10.10.10.20:8080/chi-siamo.html",
        "curl -s http://10.10.10.20:8080/chi-siamo.html | grep -i flag",
    ])
    d.p("Nota anche i nomi e il formato delle email: `nome.cognome@bancadellascuola.local`. "
        "Ti servira' nelle lezioni sul login.")

    d.h2("Passo 3 · robots.txt (+20)")
    d.p("robots.txt dice ai motori di ricerca cosa non indicizzare. Per un attaccante e' "
        "una mappa delle cartelle che qualcuno vorrebbe tenere nascoste.")
    d.code([
        "curl -s http://10.10.10.20:8080/robots.txt",
        "curl -s http://10.10.10.20:8080/riservato/promemoria.txt",
    ])

    d.h2("Passo 4 · Cartelle nascoste col dir buster (+20)")
    d.p("robots.txt non elenca tutto. Un dir buster prova tanti nomi di cartella e ti "
        "dice quali esistono. Usa la wordlist preparata.")
    d.code([
        "cd ~/lab/lezione-07",
        "gobuster dir -u http://10.10.10.20:8080 -w parole.txt",
        "# gobuster trova /backup : aprila (il listing e' attivo)",
        "curl -s http://10.10.10.20:8080/backup/",
        "curl -s http://10.10.10.20:8080/backup/credenziali.old",
    ])
    d.box("blu", "Profilazione (bonus, senza punti)", intro=(
        "Metti insieme i pezzi come farebbe un attaccante:"), items=[
        "Dai nomi in 'chi siamo' e dal formato email, ricava l'indirizzo della direttrice.",
        "Nel backup c'e' una password che la direttrice riusa: annotala per le lezioni "
        "sul login e sul brute force.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Tutte le flag di oggi erano informazioni che non dovevano stare online. Il "
        "difensore fa footprinting sulla PROPRIA azienda, per trovare e togliere queste "
        "briciole prima che lo faccia un attaccante.")
    d.box("verde", "Igiene del footprint", items=[
        "Niente commenti sensibili nel codice che va in produzione.",
        "Disattivare il directory listing; niente file .old o .bak sui server pubblici.",
        "Rivedere le intestazioni HTTP: togliere header di debug e versioni troppo "
        "dettagliate.",
        "robots.txt non e' una protezione: cio' che deve stare privato va protetto con "
        "autenticazione, non solo nascosto.",
    ])

    d.h2("Punteggio della Lezione 7")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Intestazioni HTTP", "whatweb / curl -I", "15"],
        ["Commento nel codice", "curl chi-siamo | grep", "15"],
        ["robots.txt", "curl robots.txt -> /riservato/", "20"],
        ["Cartella nascosta", "gobuster -> /backup/", "20"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 7** · Footprinting e OSINT simulati (Blocco 3, Reconnaissance).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; container `banca` su :8080 (ricreato dal lab).",
        "**Deliverable studente:** 4 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Introdurre la fase di reconnaissance: raccogliere prima di attaccare.",
        "Distinguere OSINT passivo e footprinting attivo, tutto dentro il lab isolato.",
        "Usare whatweb, curl, gobuster/dirb su un sito realistico ma finto.",
    ])

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Riscrive `/opt/lab/banca/` con: index, chi-siamo (commento con flag e formato "
        "email), robots.txt, /riservato/promemoria.txt, /backup/credenziali.old.",
        "Scrive `/opt/lab/banca-nginx.conf` con `autoindex on` e due header custom, tra "
        "cui `X-Debug-Flag`.",
        "Riavvia il container `banca` (nginx:alpine, offline) montando html e conf.",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Crea `~/lab/lezione-07/parole.txt` (wordlist piccola e deterministica per "
        "gobuster/dirb).",
        "Verifica che il sito risponda e mostra la missione.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "curl -I http://10.10.10.20:8080 (header X-Debug-Flag)", "FLAG{intestazioni_parlano}"],
        ["2", "curl -s .../chi-siamo.html | grep -i flag", "FLAG{commenti_nel_codice}"],
        ["3", "curl .../robots.txt ; curl .../riservato/promemoria.txt", "FLAG{robots_non_nasconde}"],
        ["4", "gobuster ... -> /backup/ ; curl .../backup/credenziali.old",
         "FLAG{directory_dimenticata}"],
    ], widths=[900, 5426, 2700])

    d.h1("Mappa di cosa e' seminato dove")
    d.table(["URL", "Contenuto"], [
        ["/ (header)", "X-Debug-Flag (flag 1) + X-Powered-By"],
        ["/chi-siamo.html", "team, formato email, commento con flag 2"],
        ["/robots.txt", "Disallow /riservato/ e /admin/"],
        ["/riservato/promemoria.txt", "flag 3"],
        ["/backup/credenziali.old", "admin:Estate2021! (riuso) + flag 4"],
    ], widths=[3200, 5826])
    d.p("La password `Estate2021!` e l'account `admin` sono riusati apposta: torneranno "
        "nelle lezioni su login e brute force (continuita' della narrazione).")

    d.h1("Rigiocare, resettare, troubleshooting")
    d.bullets([
        "Rigioca/reset: rilancia `lab 7` sul bersaglio (ricrea file e container).",
        "Se manca l'header: `docker logs banca`; verificare che la conf sia montata.",
        "Se gobuster e' lento: usare la wordlist `parole.txt` fornita (piccola).",
        "Se /backup/ non elenca i file: verificare `autoindex on` nella conf montata.",
    ])

    d.h1("Nota didattica")
    d.p("L'OSINT reale usa internet; qui e' vietato per legge e per policy. Abbiamo "
        "quindi ricreato un footprint verosimile sul bersaglio, cosi' le tecniche sono "
        "quelle vere ma i dati sono inventati e confinati al laboratorio.")
