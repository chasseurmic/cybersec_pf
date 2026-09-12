# -*- coding: utf-8 -*-
import comune
NUM = 6
SLUG = "bash-scripting-offensivo"
TITOLO = "Bash scripting offensivo: il tuo primo scanner"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** smettere di digitare comandi a mano e iniziare a scriverli in "
        "uno script, fino a costruire un vero strumento: uno scanner che trova gli host "
        "vivi nella rete del laboratorio.",
        "**Al termine sai:** variabili, cicli `for`, condizioni `if`, sostituzione di "
        "comando `$(...)`, codici di uscita, esecuzione in parallelo, e leggere/scrivere "
        "uno script bash.",
        "**Flag in palio:** 4 flag (70 punti): scrivi TU un mini scanner, poi usa quello pronto.",
    ])

    d.h1("Parte 1 · Dare ordini in serie (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Un attaccante che deve controllare 254 indirizzi non li prova a mano uno per "
        "uno: scrive tre righe di bash e lascia lavorare il computer. Gli strumenti "
        "famosi (nmap e compagnia) sono nati così, da qualcuno che ha automatizzato un "
        "gesto ripetitivo. Oggi fai lo stesso: costruisci il tuo scanner. Capire come è "
        "fatto dentro vale più che usarne uno pronto senza sapere cosa fa.")

    d.h2("Un vero script")
    d.p("Uno script è un file di testo con dei comandi. La prima riga, lo shebang, dice "
        "quale interprete usare. Poi lo rendi eseguibile e lo lanci.")
    d.code([
        "#!/usr/bin/env bash",
        "echo \"Ciao dal mio script\"",
        "",
        "# poi, nel terminale:",
        "chmod +x esempio.sh    # rendilo eseguibile",
        "./esempio.sh           # eseguilo",
    ])

    d.h2("I tre mattoni: variabili, cicli, condizioni")
    d.code([
        "nome=\"mondo\"           # variabile (niente spazi attorno all'=)",
        "echo \"Ciao, $nome\"     # si usa con il $",
        "",
        "for n in 1 2 3; do      # ciclo: ripete per ogni valore",
        "  echo \"giro $n\"",
        "done",
        "",
        "if [ -f /etc/hostname ]; then      # condizione",
        "  echo \"il file esiste\"",
        "fi",
    ])
    d.p("La sostituzione di comando `$(...)` mette il risultato di un comando dentro una "
        "variabile o una stringa: `oggi=$(date)`. Ogni comando lascia un codice di "
        "uscita: 0 vuol dire riuscito, diverso da 0 vuol dire fallito. Gli `if` sui "
        "comandi si basano proprio su quel codice.")

    d.h2("Come funziona un ping sweep")
    d.p("Per scoprire chi è vivo in una rete /24 basta pingare tutti gli indirizzi da "
        "`.1` a `.254`. Se pingassimo uno alla volta ci vorrebbero minuti; lanciando i "
        "ping in parallelo (con `&`) e aspettando con `wait`, si finisce in un paio di "
        "secondi.")
    d.code([
        "for i in $(seq 1 254); do",
        "  ( ping -c1 -W1 10.10.10.$i >/dev/null 2>&1 && echo 10.10.10.$i ) &",
        "done",
        "wait",
    ])

    d.cmdref([
        ("`nano`", "Editor di testo semplice nel terminale, per scrivere gli script. Si "
                   "salva con Ctrl+O e Invio, si esce con Ctrl+X."),
        ("`chmod +x`", "Rende un file eseguibile, così puoi lanciarlo con `./nome.sh`. In "
                       "alternativa: `bash nome.sh` (non serve renderlo eseguibile)."),
        ("`seq`", "Genera una sequenza di numeri: `seq 1 254` stampa 1, 2, ... 254. Serve a "
                  "far girare un ciclo `for`."),
        ("`ping`", "Verifica se un host risponde. `-c1` un solo pacchetto, `-W1` aspetta al "
                   "massimo 1 secondo (senza si perderebbe troppo tempo sugli host spenti)."),
        ("`&` e `wait`", "`&` avvia un comando in background (in parallelo); `wait` aspetta "
                         "che tutti i comandi lanciati così abbiano finito."),
    ], titolo="I comandi nuovi di oggi")

    d.h1("Parte 2 · Costruisci lo scanner (pratica, 80 min)")
    d.p("Sulla Kali `lab 6` prepara la cartella `~/lab/lezione-06` con un esempio "
        "commentato e lo strumento `scanner-host.sh`. Sul bersaglio `lab 6` garantisce "
        "che risponda al ping e tenga aperta la porta 8080.")

    d.h2("Passo 1 · Il tuo primo script (+10)")
    d.p("Scrivi `saluta.sh` che stampa cinque righe usando un ciclo, poi verifica.")
    d.code([
        "cd ~/lab/lezione-06",
        "nano saluta.sh",
        "# dentro, scrivi:",
        "#   #!/usr/bin/env bash",
        "#   for n in 1 2 3 4 5; do echo \"riga $n\"; done",
        "bash saluta.sh",
        "lab06-verifica",
    ])

    d.h2("Passo 2 · Costruisci TU un mini scanner, passo passo (+30)")
    d.p("Prima di usare lo strumento pronto, scrivilo tu, un pezzo alla volta. Così "
        "capisci davvero cosa fa. Crea il file `mio-scanner.sh` e costruiscilo in tre "
        "mosse.")

    d.h3("Mossa 1 · pingare UN host e capire se è vivo")
    d.p("`ping -c1` manda un solo pacchetto; il suo codice di uscita è 0 se l'host "
        "risponde. Con `if` decidi cosa stampare.")
    d.code([
        "#!/usr/bin/env bash",
        "if ping -c1 -W1 10.10.10.20 >/dev/null 2>&1; then",
        "  echo \"10.10.10.20 è vivo\"",
        "fi",
    ])
    d.p("Provalo: `bash mio-scanner.sh`. Se il bersaglio è acceso, stampa la riga.")

    d.h3("Mossa 2 · ripetere su tanti indirizzi con un ciclo for")
    d.p("Invece di un solo IP, scorri gli ultimi numeri da 1 a 30 con una variabile.")
    d.code([
        "#!/usr/bin/env bash",
        "for n in $(seq 1 30); do",
        "  ip=\"10.10.10.$n\"",
        "  if ping -c1 -W1 \"$ip\" >/dev/null 2>&1; then",
        "    echo \"$ip è vivo\"",
        "  fi",
        "done",
    ])

    d.h3("Mossa 3 · provarlo davvero")
    d.p("Lancialo e verifica. Deve elencare la tua Kali (`.5`) e il bersaglio (`.20`). "
        "Noterai che è lentino: prova un indirizzo alla volta e aspetta ogni ping. "
        "Tienilo a mente, al Passo 3 vedrai come si fa a renderlo veloce.")
    d.code([
        "bash mio-scanner.sh",
        "lab06-scanner        # ti dà la flag se il tuo scanner trova 10.10.10.20",
    ])

    d.h2("Passo 3 · Lo scanner professionale (+15)")
    d.p("Ora che sai come funziona, apri quello già pronto: fa la stessa cosa ma su "
        "tutti i 254 indirizzi e in PARALLELO (lancia i ping insieme con `&` e aspetta con "
        "`wait`), quindi finisce in un paio di secondi invece che in mezzo minuto.")
    d.code([
        "cat scanner-host.sh      # leggi le differenze: & , wait , /dev/tcp",
        "./scanner-host.sh 10.10.10",
    ])
    d.p("Quando individua `10.10.10.20`, ti consegna la flag. Confronta la velocità con "
        "il tuo mini scanner.")

    d.h2("Passo 4 · Controlla anche una porta (+15)")
    d.p("Lo scanner pro sa anche dire se una porta è aperta, usando la funzione "
        "`/dev/tcp` di bash. Rilancialo chiedendo la porta 8080.")
    d.code(["./scanner-host.sh 10.10.10 8080"])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Uno scanner che pinga tutta la rete e prova le porte lascia tracce: tanti ping "
        "e tanti tentativi di connessione in pochi secondi. Chi difende può accorgersene.")
    d.box("verde", "Dal lato del difensore", items=[
        "Un firewall può non rispondere al ping, rendendo gli host meno visibili "
        "(security through minimal exposure, non è invisibilità vera ma alza l'asticella).",
        "Un sistema di rilevamento nota il pattern: un solo IP che tocca centinaia di "
        "indirizzi o porte in pochi secondi.",
        "La segmentazione della rete (VLAN) limita quanto lontano può arrivare uno "
        "scanner: lo vedremo nel blocco sulle difese di rete.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("bash, sh e perché lo scripting conta", "bash è la shell più diffusa su Linux, ma non l'unica: sh (dash su Ubuntu) è più minimale e NON conosce gli array né /dev/tcp. Per questo uno script che usa queste funzioni deve girare con bash: lanciarlo con sh darà errori strani. Nello scripting contano molto i codici di uscita: 0 vuol dire riuscito, diverso da 0 fallito, ed è ciò che usano if e gli operatori && (esegui il secondo solo se il primo riesce) e || (solo se fallisce). Automatizzare non è solo comodità: è il modo in cui sono nati tutti gli strumenti di sicurezza. Capire come è fatto uno scanner dentro ti rende capace di modificarlo e di non dipendere da tool pronti che non controlli."),
        ],
        sintesi=[
            'Uno script bash automatizza comandi ripetitivi: shebang, chmod +x, esecuzione.',
            'I mattoni sono variabili, ciclo for, condizione if e i codici di uscita (0 = ok).',
            "Un ping sweep sequenziale è lento; con & (background) e wait diventa velocissimo.",
            "La funzione /dev/tcp di bash permette di verificare se una porta è aperta senza altri strumenti.",
            "Capire come è fatto uno strumento vale più che usarne uno pronto senza saperlo.",
        ],
        glossario=[
            ('Script', 'un file di comandi eseguibili in sequenza'),
            ('Shebang', "la prima riga #!/usr/bin/env bash che indica l'interprete"),
            ('Variabile', 'un contenitore per un valore (nome=valore, si usa con $nome)'),
            ('Ciclo for', 'ripete dei comandi per ogni elemento di una lista'),
            ("Codice di uscita", "0 se un comando riesce, diverso da 0 se fallisce"),
            ('& e wait', 'avviare in parallelo (&) e aspettare la fine di tutti (wait)'),
            ('/dev/tcp', 'funzione di bash per aprire una connessione TCP (test di porta)'),
            ('Ping sweep', 'pingare tutti gli indirizzi di una rete per trovare gli host vivi'),
        ],
        errori=[
            "Mettere spazi attorno all'= in una variabile (nome = valore): errore.",
            'Lanciare uno script con sh invece di bash: /dev/tcp e gli array non funzionano.',
            'Dimenticare wait dopo aver lanciato i ping in background: risultati incompleti.',
            'Non gestire il timeout del ping (-W): lo scanner si impianta sugli host spenti.',
        ],
        domande=[
            "Perché lo scanner parallelo è così più veloce di quello sequenziale?",
            'Come rendi eseguibile uno script e come lo lanci?',
            'A cosa servono & e wait in un ping sweep?',
            "Come verifichi se una porta è aperta usando solo bash (/dev/tcp)?",
            'Cosa stampa il codice di uscita di un comando e come lo usa un if?',
        ],
        collegamenti=[
            'Lezione 4: le pipe e le redirezioni che usi dentro gli script.',
            'Lezione 8-9: gli stessi concetti con gli strumenti professionali (nmap).',
            'Lezione 9: uno scanner di porte scritto in Python.',
        ],
    )


    d.h2("Punteggio della Lezione 6")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Primo script", "saluta.sh + lab06-verifica", "10"],
        ["Il TUO mini scanner", "mio-scanner.sh + lab06-scanner", "30"],
        ["Scanner pro: trova il bersaglio", "scanner-host.sh 10.10.10", "15"],
        ["Scanner pro: porta aperta", "scanner-host.sh 10.10.10 8080", "15"],
    ], widths=[4200, 3326, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 6** · Bash scripting offensivo, host alive scanner (Blocco 2, lezione con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali della Lezione 2; bersaglio acceso e raggiungibile.",
        "**Deliverable studente:** 4 flag (70 punti). Lo studente scrive un mini scanner e poi usa quello pronto.",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Passare dall'uso dei comandi alla loro automazione in script.",
        "Far scrivere allo studente un mini scanner sequenziale (for + if + exit code), "
        "passo passo, PRIMA di dargli lo strumento pronto.",
        "Poi confrontarlo con lo scanner professionale: capire la parallelizzazione "
        "(`&` + `wait`) e `/dev/tcp` di bash.",
    ])

    d.h1("Come funziona il lab")
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Crea `~/lab/lezione-06/` con `esempio.sh` (commentato) e `scanner-host.sh` (lo "
        "strumento pronto, con ping sweep parallelo e controllo porta via /dev/tcp).",
        "Lo studente scrive da solo `mio-scanner.sh` (sequenziale) seguendo la dispensa.",
        "Installa `/usr/local/bin/lab06-verifica` (primo script) e "
        "`/usr/local/bin/lab06-scanner` (esegue il mio-scanner dello studente e controlla "
        "che trovi 10.10.10.20).",
        "Lo strumento vive dentro kali.sh (heredoc): è così che arriva sulla VM tramite "
        "`lab`, che scarica solo kali.sh/target.sh.",
    ])
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Lezione lato Kali: il target garantisce solo di rispondere al ping e di tenere "
        "la porta 8080 attiva (riavvia il container banca se serve).",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "saluta.sh con for che stampa 'riga 1'..'riga 5' ; lab06-verifica",
         "FLAG{primo_script_bash}"],
        ["2", "mio-scanner.sh (for su seq 1 30 + if ping) che elenca 10.10.10.20 ; lab06-scanner",
         "FLAG{il_mio_primo_scanner}"],
        ["3", "./scanner-host.sh 10.10.10 (trova 10.10.10.20)", "FLAG{ho_trovato_il_bersaglio}"],
        ["4", "./scanner-host.sh 10.10.10 8080", "FLAG{porta_aperta_trovata}"],
    ], widths=[700, 5826, 2500])

    d.h1("Rigiocare e resettare")
    d.bullets([
        "Rilanciare `lab 6` sulla Kali ricrea esempio e scanner (sovrascrive).",
        "Per rifare il passo 1: cancellare `~/lab/lezione-06/saluta.sh`.",
    ])

    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["lo scanner non trova .20", "bersaglio spento o ping bloccato; lanciare `lab 6` "
         "sul bersaglio; provare `ping 10.10.10.20`"],
        ["porta 8080 sempre chiusa", "container banca giù: sul bersaglio `docker ps`; "
         "rilanciare `lab 6`"],
        ["scanner lentissimo", "manca il parallelismo: verificare `&` e `wait` (nella "
         "versione fornita ci sono)"],
        ["/dev/tcp: No such file", "usare bash, non sh: lo script ha lo shebang giusto, "
         "lanciarlo con `./scanner-host.sh` o `bash scanner-host.sh`"],
    ], widths=[2800, 6226])

    d.h1("Nota tecnica (x86)")
    d.p("Ping sweep e /dev/tcp funzionano identici su x86 e ARM. Su una /24 con due soli "
        "host lo scanner trova `.5` (Kali) e `.20` (bersaglio); è il comportamento "
        "atteso. Da provare sul bersaglio reale x86: il controllo della porta 8080, che "
        "dipende dal container nginx della Banca.")
