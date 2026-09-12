# -*- coding: utf-8 -*-
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
        "famosi (nmap e compagnia) sono nati cosi', da qualcuno che ha automatizzato un "
        "gesto ripetitivo. Oggi fai lo stesso: costruisci il tuo scanner. Capire come e' "
        "fatto dentro vale piu' che usarne uno pronto senza sapere cosa fa.")

    d.h2("Un vero script")
    d.p("Uno script e' un file di testo con dei comandi. La prima riga, lo shebang, dice "
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
    d.p("Per scoprire chi e' vivo in una rete /24 basta pingare tutti gli indirizzi da "
        "`.1` a `.254`. Se pingassimo uno alla volta ci vorrebbero minuti; lanciando i "
        "ping in parallelo (con `&`) e aspettando con `wait`, si finisce in un paio di "
        "secondi.")
    d.code([
        "for i in $(seq 1 254); do",
        "  ( ping -c1 -W1 10.10.10.$i >/dev/null 2>&1 && echo 10.10.10.$i ) &",
        "done",
        "wait",
    ])

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
    d.p("Prima di usare lo strumento pronto, scrivilo tu, un pezzo alla volta. Cosi' "
        "capisci davvero cosa fa. Crea il file `mio-scanner.sh` e costruiscilo in tre "
        "mosse.")

    d.h3("Mossa 1 · pingare UN host e capire se e' vivo")
    d.p("`ping -c1` manda un solo pacchetto; il suo codice di uscita e' 0 se l'host "
        "risponde. Con `if` decidi cosa stampare.")
    d.code([
        "#!/usr/bin/env bash",
        "if ping -c1 -W1 10.10.10.20 >/dev/null 2>&1; then",
        "  echo \"10.10.10.20 e' vivo\"",
        "fi",
    ])
    d.p("Provalo: `bash mio-scanner.sh`. Se il bersaglio e' acceso, stampa la riga.")

    d.h3("Mossa 2 · ripetere su tanti indirizzi con un ciclo for")
    d.p("Invece di un solo IP, scorri gli ultimi numeri da 1 a 30 con una variabile.")
    d.code([
        "#!/usr/bin/env bash",
        "for n in $(seq 1 30); do",
        "  ip=\"10.10.10.$n\"",
        "  if ping -c1 -W1 \"$ip\" >/dev/null 2>&1; then",
        "    echo \"$ip e' vivo\"",
        "  fi",
        "done",
    ])

    d.h3("Mossa 3 · provarlo davvero")
    d.p("Lancialo e verifica. Deve elencare la tua Kali (`.5`) e il bersaglio (`.20`). "
        "Noterai che e' lentino: prova un indirizzo alla volta e aspetta ogni ping. "
        "Tienilo a mente, al Passo 3 vedrai come si fa a renderlo veloce.")
    d.code([
        "bash mio-scanner.sh",
        "lab06-scanner        # ti da' la flag se il tuo scanner trova 10.10.10.20",
    ])

    d.h2("Passo 3 · Lo scanner professionale (+15)")
    d.p("Ora che sai come funziona, apri quello gia' pronto: fa la stessa cosa ma su "
        "tutti i 254 indirizzi e in PARALLELO (lancia i ping insieme con `&` e aspetta con "
        "`wait`), quindi finisce in un paio di secondi invece che in mezzo minuto.")
    d.code([
        "cat scanner-host.sh      # leggi le differenze: & , wait , /dev/tcp",
        "./scanner-host.sh 10.10.10",
    ])
    d.p("Quando individua `10.10.10.20`, ti consegna la flag. Confronta la velocita' con "
        "il tuo mini scanner.")

    d.h2("Passo 4 · Controlla anche una porta (+15)")
    d.p("Lo scanner pro sa anche dire se una porta e' aperta, usando la funzione "
        "`/dev/tcp` di bash. Rilancialo chiedendo la porta 8080.")
    d.code(["./scanner-host.sh 10.10.10 8080"])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Uno scanner che pinga tutta la rete e prova le porte lascia tracce: tanti ping "
        "e tanti tentativi di connessione in pochi secondi. Chi difende puo' accorgersene.")
    d.box("verde", "Dal lato del difensore", items=[
        "Un firewall puo' non rispondere al ping, rendendo gli host meno visibili "
        "(security through minimal exposure, non e' invisibilita' vera ma alza l'asticella).",
        "Un sistema di rilevamento nota il pattern: un solo IP che tocca centinaia di "
        "indirizzi o porte in pochi secondi.",
        "La segmentazione della rete (VLAN) limita quanto lontano puo' arrivare uno "
        "scanner: lo vedremo nel blocco sulle difese di rete.",
    ])

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
        "Lo strumento vive dentro kali.sh (heredoc): e' cosi' che arriva sulla VM tramite "
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
        ["porta 8080 sempre chiusa", "container banca giu': sul bersaglio `docker ps`; "
         "rilanciare `lab 6`"],
        ["scanner lentissimo", "manca il parallelismo: verificare `&` e `wait` (nella "
         "versione fornita ci sono)"],
        ["/dev/tcp: No such file", "usare bash, non sh: lo script ha lo shebang giusto, "
         "lanciarlo con `./scanner-host.sh` o `bash scanner-host.sh`"],
    ], widths=[2800, 6226])

    d.h1("Nota tecnica (x86)")
    d.p("Ping sweep e /dev/tcp funzionano identici su x86 e ARM. Su una /24 con due soli "
        "host lo scanner trova `.5` (Kali) e `.20` (bersaglio); e' il comportamento "
        "atteso. Da provare sul bersaglio reale x86: il controllo della porta 8080, che "
        "dipende dal container nginx della Banca.")
