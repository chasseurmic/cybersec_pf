# -*- coding: utf-8 -*-
NUM = 16
SLUG = "brute-force-login-difesa"
TITOLO = "Brute force del login e la sua difesa"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire il brute force (provare tante password finche' una "
        "funziona), scrivere un piccolo strumento che lo fa, e vedere dal vivo come una "
        "difesa (il rate limiting) lo ferma.",
        "**Al termine sai:** usare una wordlist, forzare un login con un tuo tool e con "
        "hydra, e spiegare perche' limiti e lockout sono efficaci.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Provare tutte le chiavi (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Molti attacchi non sfruttano falle sofisticate: provano solo tante password. Se "
        "un sito accetta tentativi illimitati e gli utenti usano password deboli, prima o "
        "poi una passa. Gli elenchi di password piu' comuni (come il famoso rockyou, "
        "milioni di password trapelate da un vero sito) rendono il gioco molto veloce. "
        "Oggi costruiamo il nostro forzatore e poi vediamo come si difende un login.")

    d.h2("Wordlist e attacco a dizionario")
    d.p("Il brute force 'puro' prova ogni combinazione possibile: lentissimo. L'attacco a "
        "dizionario e' piu' furbo: prova solo password probabili, prese da una lista. E' "
        "cosi' che funzionano gli strumenti veri.")

    d.h1("Parte 2 · Forza il login (pratica, 80 min)")
    d.p("Sul bersaglio `lab 16` avvia un servizio di login su :8095 con due porte: "
        "`/debole` (senza protezioni) e `/forte` (con difesa). Sulla Kali `lab 16` "
        "installa il tuo tool e una wordlist in `~/lab/lezione-16`.")

    d.h2("Passo 1 · Buca il login debole (+45)")
    d.p("Leggi il tuo strumento e lancialo: prova ogni password della lista finche' una "
        "funziona.")
    d.code([
        "cd ~/lab/lezione-16",
        "cat bruteforce.py",
        "python3 bruteforce.py http://10.10.10.20:8095/debole sara.verdi passwords.txt",
    ])
    d.p("Quando trova la password, il servizio risponde con la flag. Lo stesso si fa con "
        "lo strumento professionale hydra:")
    d.code([
        "hydra -l sara.verdi -P passwords.txt 10.10.10.20 -s 8095 \\",
        "  http-post-form \"/debole:utente=^USER^&password=^PASS^:Credenziali errate\"",
    ])

    d.h2("Passo 2 · Sbatti contro la difesa (+25)")
    d.p("Ora prova lo stesso attacco contro il login forte. Dopo pochi tentativi ti "
        "blocca: e' il rate limiting.")
    d.code([
        "python3 bruteforce.py http://10.10.10.20:8095/forte sara.verdi passwords.txt",
    ])
    d.p("Il blocco ti consegna la seconda flag: hai fatto scattare la difesa.")

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Come si ferma un brute force", items=[
        "Rate limiting: limitare i tentativi per utente e per IP in un certo tempo.",
        "Lockout temporaneo dopo N tentativi falliti (come il login forte di oggi).",
        "Password robuste e diverse: se non sono nelle wordlist, l'attacco a dizionario "
        "fallisce.",
        "Autenticazione a due fattori (2FA): anche con la password giusta, serve il "
        "secondo fattore.",
        "CAPTCHA e monitoraggio: rendono l'attacco automatico lento e visibile.",
    ])
    d.p("Nota la differenza vista dal vivo: contro `/debole` il tool vince in pochi "
        "secondi; contro `/forte`, con la stessa lista, non arriva nemmeno alla password "
        "giusta.")

    d.h2("Punteggio della Lezione 16")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Login debole forzato", "bruteforce.py su /debole", "45"],
        ["Difesa attivata", "bruteforce.py su /forte (blocco)", "25"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 16** · Brute force del login e difesa (Blocco 4, con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; hydra sulla Kali (Lezione 2). Non richiede la "
        "Banca (il servizio :8095 e' autonomo).",
        "**Deliverable studente:** 2 flag (70 punti) + un brute forcer riutilizzabile.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire attacco a dizionario e wordlist.",
        "Scrivere e usare un brute forcer; conoscere hydra.",
        "Vedere dal vivo l'efficacia del rate limiting / lockout.",
    ])
    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Aggiunge FLAG_BRUTE e FLAG_DIFESA a `/opt/lab/banca-app/flags.env` (creandolo se "
        "manca).",
        "Avvia `lab16-login.service` su :8095: `/debole` (nessuna protezione) e `/forte` "
        "(blocca dopo 5 tentativi falliti in 60s, restituendo la flag della difesa).",
        "Credenziali valide: `sara.verdi` / `primavera` (e `cassa` / `estate2019`).",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Crea `~/lab/lezione-16/bruteforce.py` (tool) e `passwords.txt` (wordlist con la "
        "password giusta in settima posizione, dopo 6 distrattori: cosi' contro /forte il "
        "blocco scatta prima di trovarla).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1", "bruteforce.py .../debole sara.verdi passwords.txt (trova primavera)",
         "FLAG_BRUTE"],
        ["2", "bruteforce.py .../forte ... (blocco dopo 5 tentativi)", "FLAG_DIFESA"],
    ], widths=[900, 5626, 2500])
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["/forte non blocca", "il blocco e' per IP e dura 60s; se sono passati 60s si "
         "sblocca; rilanciare l'attacco subito"],
        ["/debole non trova la password", "verificare che passwords.txt contenga "
         "'primavera' (lo crea kali.sh)"],
        ["hydra segna tutte valide", "la stringa di fallimento deve essere 'Credenziali "
         "errate' (come nel comando fornito)"],
        ["voglio i valori", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2800, 6226])
    d.h1("Nota di progetto")
    d.p("Il login e' un servizio dedicato (:8095), non quello della Banca, perche' il "
        "cookie della Banca e' prevedibile (Lezione 15) e renderebbe inutile il brute "
        "force. Cosi' la lezione resta pulita: qui si vince solo indovinando la password.")
