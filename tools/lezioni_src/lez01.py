# -*- coding: utf-8 -*-
NUM = 1
SLUG = "triade-cia-primo-accesso"
TITOLO = "Triade CIA e primo accesso"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire cosa protegge la sicurezza informatica (la triade CIA), "
        "perché in questo corso studiamo il punto di vista dell'attaccante, e muovere i "
        "primi passi nel terminale della Kali.",
        "**Al termine sai:** cos'è la triade CIA, le regole etiche e legali del corso, e "
        "i comandi base per orientarti nel terminale (chi sei, dove sei, cosa c'è).",
        "**Flag in palio:** 3 flag (70 punti).",
    ])

    d.h1("Parte 1 · Cosa protegge la sicurezza (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Ogni giorno aziende, ospedali e scuole vengono attaccati: dati rubati, siti "
        "bloccati, richieste di riscatto. Dietro quasi ogni notizia c'è la stessa storia: "
        "qualcosa che doveva restare segreto è stato letto, qualcosa che doveva restare "
        "intatto è stato modificato, oppure un servizio che doveva restare acceso è "
        "stato spento. Questi tre 'doveva' sono esattamente ciò che la sicurezza "
        "informatica cerca di proteggere.")

    d.h2("La triade CIA")
    d.p("CIA non c'entra con i servizi segreti: è l'acronimo dei tre pilastri della "
        "sicurezza. Ogni attacco colpisce almeno uno di questi tre.")
    d.table(["Pilastro", "Cosa garantisce", "Esempio di violazione"], [
        ["Confidenzialità (C)", "solo chi ha diritto può leggere i dati",
         "un attaccante ruba l'elenco delle password"],
        ["Integrità (I)", "i dati non vengono alterati di nascosto",
         "qualcuno modifica un voto o un bonifico"],
        ["Disponibilità (A)", "il servizio è accessibile quando serve",
         "un sito viene messo offline (ransomware, DDoS)"],
    ], widths=[2400, 3626, 3000])
    d.p("Tenere a mente la triade aiuta a ragionare: davanti a qualunque scenario, "
        "chiediti quale pilastro è a rischio. È la bussola di tutto il corso.")

    d.h2("Perché studiamo il punto di vista dell'attaccante")
    d.p("Per difendere una casa devi sapere come entra un ladro: quali finestre lascia "
        "aperte la gente, quali serrature sono deboli. In sicurezza è lo stesso. Impariamo "
        "le tecniche di chi attacca (in inglese si dice pensare da 'red team') non per fare "
        "danni, ma per capire dove sono i punti deboli e chiuderli (il 'blue team', la "
        "difesa). Alla fine di ogni lezione c'è sempre un 'ribaltamento difensivo': la "
        "stessa cosa vista dal lato di chi protegge.")

    d.box("rosso", "Regola d'oro (etica e legge)", items=[
        "Tutto quello che impari si usa SOLO dentro il laboratorio isolato del corso.",
        "Attaccare, scansionare o provare password su computer altrui è un REATO "
        "(accesso abusivo a sistema informatico, art. 615-ter del codice penale).",
        "Le stesse competenze, usate bene, sono un lavoro molto richiesto; usate male, "
        "portano in tribunale. La differenza è il permesso.",
    ])

    d.h2("Il laboratorio in due parole")
    d.p("Lavorerai con due macchine virtuali isolate: la **Kali** (il computer "
        "dell'attaccante, con tutti gli strumenti) e il **bersaglio** (una macchina "
        "vittima con dei servizi da studiare). Sono collegate da una rete privata che vive "
        "dentro il tuo PC: non tocca internet né la rete della scuola. La Kali ha "
        "indirizzo `10.10.10.5`, il bersaglio `10.10.10.20`.")

    d.h1("Parte 2 · Primi passi nel terminale (pratica, 80 min)")
    d.p("Il terminale è la finestra dove si scrivono i comandi. Fa un po' paura all'inizio, "
        "ma è solo un modo per dire al computer cosa fare a parole invece che a clic. Sulla "
        "Kali, il docente lancia `lab 1` (prepara i file di benvenuto) e sul bersaglio "
        "`lab 1` (accende la pagina della Banca). Poi tocca a te.")

    d.h2("Chi sono e dove sono")
    d.p("I primi comandi servono a orientarsi: chi sei, che indirizzo hai, cosa c'è "
        "intorno a te.")
    d.cmdref([
        ("`whoami`", "Stampa il nome dell'utente con cui sei collegato (es. `kali`)."),
        ("`id`", "Mostra il tuo numero utente (UID), il gruppo (GID) e i gruppi a cui "
                 "appartieni. Serve a capire quanti poteri hai."),
        ("`ip a`", "Elenca le schede di rete e i loro indirizzi IP (`a` sta per address). "
                   "Cerca l'indirizzo `10.10.10.5`: è la tua Kali nella rete del lab."),
        ("`pwd`", "Print Working Directory: dice in quale cartella ti trovi adesso."),
    ])
    d.code([
        "whoami",
        "id",
        "ip a",
        "pwd",
    ])

    d.h2("Guardare cosa c'è e leggere i file")
    d.cmdref([
        ("`ls`", "Elenca i file e le cartelle. `-a` mostra anche i file nascosti, `-l` usa "
                 "il formato lungo (permessi, proprietario, dimensione), `-la` unisce i due."),
        ("`cat`", "Concatena e stampa a schermo il contenuto di uno o più file di testo."),
    ])

    d.h3("Flag 1 · Il file di benvenuto (+20)")
    d.p("Nella tua cartella c'è un file di benvenuto. Elenca i file e leggilo.")
    d.code([
        "ls",
        "cat README-corso.txt",
    ])
    d.p("In fondo al file c'è la prima flag (una scritta tipo `FLAG{...}`). Le flag sono "
        "il modo con cui dimostri di aver completato un compito: le consegni al docente per "
        "guadagnare punti. Non rivelano nulla di segreto qui, ma più avanti dovrai proprio "
        "guadagnartele.")

    d.h3("Flag 2 · I file nascosti (+20)")
    d.p("I file il cui nome inizia con un punto (per esempio `.segreto`) non compaiono con "
        "`ls` normale: servono a non ingombrare la vista, non a proteggere davvero. Con "
        "`-a` li vedi tutti. Ricorda questa lezione: **nascondere non è proteggere**.")
    d.code([
        "ls -a",
        "cat .segreto",
    ])

    d.h2("Parlare con un'altra macchina in rete")
    d.cmdref([
        ("`ping`", "Verifica se un altro computer è raggiungibile in rete e quanto ci "
                   "mette a rispondere. `-c N` invia solo N pacchetti e poi si ferma "
                   "(senza `-c` andrebbe all'infinito)."),
        ("`curl`", "Scarica il contenuto di una pagina web da riga di comando. `-s` = "
                   "silenzioso (niente barra di avanzamento), `-I` = solo le intestazioni "
                   "della risposta."),
        ("`grep`", "Filtra un testo e mostra solo le righe che contengono una parola. `-i` "
                   "ignora maiuscole/minuscole. Qui lo usiamo dopo una pipe `|`, che passa "
                   "l'output di un comando a quello successivo."),
    ])

    d.h3("Flag 3 · Ho parlato col server (+30)")
    d.p("Il bersaglio ospita la pagina web della 'Banca della Scuola'. Prima controlla che "
        "risponda, poi scarica la pagina e cerca la flag nascosta nel suo codice.")
    d.code([
        "ping -c 3 10.10.10.20",
        "curl -s http://10.10.10.20:8080",
        "curl -s http://10.10.10.20:8080 | grep FLAG",
    ])
    d.p("La pagina web nasconde la flag in un commento del codice HTML: la vedi scaricando "
        "la pagina, anche se nel browser non comparirebbe.")

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Rileggi le tre flag con gli occhi del difensore, usando la triade CIA:")
    d.box("verde", "La triade all'opera", items=[
        "La flag nascosta (`.segreto`) insegna che nascondere non è proteggere: la "
        "confidenzialità vera si ottiene coi permessi e la cifratura, non nascondendo.",
        "La flag nella pagina web ricorda che tutto ciò che il server manda al client può "
        "essere letto: non mettere segreti nel codice delle pagine.",
        "Chi difende parte sempre dalla domanda: quale pilastro (C, I, A) sto proteggendo, "
        "e cosa succederebbe se cadesse?",
    ])

    d.h2("Punteggio della Lezione 1")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["File di benvenuto", "cat README-corso.txt", "20"],
        ["File nascosto", "ls -a ; cat .segreto", "20"],
        ["Pagina della Banca", "curl :8080 | grep FLAG", "30"],
    ], widths=[3800, 3726, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 1** · Triade CIA e primo accesso (Blocco 1, apertura del corso).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** ambiente del corso importato (Kali + bersaglio).",
        "**Deliverable studente:** 3 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Introdurre la triade CIA come bussola concettuale del corso.",
        "Motivare la prospettiva dell'attaccante e fissare le regole etiche/legali.",
        "Rompere il ghiaccio col terminale: orientarsi, leggere file, parlare in rete.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea nella home dell'utente `README-corso.txt` (flag 1) e `.segreto` "
        "(flag 2) e mostra il briefing dei primi comandi.",
        "target.sh serve la pagina 'Banca della Scuola' su :8080 (nginx) con la flag 3 in "
        "un commento HTML.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "cat README-corso.txt", "FLAG{benvenuto_nel_gioco}"],
        ["2", "ls -a ; cat .segreto", "FLAG{i_file_nascosti_non_bastano}"],
        ["3", "curl -s http://10.10.10.20:8080 | grep FLAG", "FLAG{ho_parlato_col_server}"],
    ], widths=[700, 5626, 2700])
    d.p("Sono flag introduttive, in chiaro (didattiche): va bene che restino leggibili.")
    d.h1("Rigiocare e troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["curl non risponde", "il bersaglio è spento o `lab 1` non è stato lanciato sul "
         "bersaglio; verificare la pagina con `docker ps` (container `banca`)"],
        ["ip a non mostra 10.10.10.5", "la scheda 'Rete interna labnet' della Kali non è "
         "attiva; vedi Lezione 2"],
        ["rigiocare", "rilanciare `lab 1` su Kali e bersaglio"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("È la prima volta al terminale per molti: andare piano, far digitare tutti, "
        "spiegare che gli errori non rompono niente. Il messaggio etico va ripetuto e "
        "collegato al patto che si firma nella Lezione 2.")
