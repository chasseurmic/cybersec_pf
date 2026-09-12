# -*- coding: utf-8 -*-
import comune
NUM = 4
SLUG = "navigazione-redirezioni-pipe"
TITOLO = "Navigazione avanzata, redirezioni e pipe"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** usare la riga di comando come un vero attrezzo, combinando i "
        "comandi con le pipe e dirottando l'output con le redirezioni per setacciare "
        "log e file in pochi secondi.",
        "**Al termine sai:** filtrare con `grep`, tagliare con `cut`, ordinare con "
        "`sort`, togliere i doppioni con `uniq`, contare con `wc`, e salvare i "
        "risultati su file con `>` e `>>`.",
        "**Flag in palio:** 5 flag (70 punti): 1 di riscaldamento sulla Kali e 4 nel "
        "setaccio sul bersaglio.",
    ])

    d.h1("Parte 1 · La catena di montaggio dei comandi (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Un attaccante entra in un server e trova migliaia di file e log enormi. Non "
        "sta lì a cliccare cartella per cartella: sarebbe come cercare una parola in "
        "un dizionario leggendolo pagina per pagina. Invece costruisce una catena di "
        "comandi, tutti sulla stessa riga, che in un secondo trova la password "
        "dimenticata in mezzo a mille file, oppure smaschera l'IP che sta scansionando "
        "il sito. Questa è la vera potenza del terminale: ogni comando fa una cosa "
        "sola, ma se li colleghi ottieni uno strumento su misura.")
    d.p("La cosa importante è che gli stessi identici comandi servono a chi difende. "
        "Chi tiene d'occhio i log usa `grep`, `sort` e `uniq` per accorgersi di un "
        "attacco. Cambia solo l'intenzione, non gli attrezzi.")

    d.h2("La pipe: passare il testo da un comando all'altro")
    d.p("La pipe è il simbolo `|` (AltGr + \\ sulla tastiera italiana). Prende ciò che "
        "un comando stampa e lo passa come ingresso al comando dopo. Si leggono da "
        "sinistra a destra, come una catena di montaggio.")
    d.code([
        "cat access.log | wc -l          # conta le righe del log",
        "cat access.log | grep 404       # tiene solo le righe con 404",
        "grep 404 access.log | wc -l     # quante richieste hanno dato errore 404",
    ])
    d.p("Nota: `grep 404 access.log` legge già il file da solo, non serve `cat`. Ma la "
        "pipe diventa indispensabile quando incateni più passaggi.")

    d.h2("Le redirezioni: dirottare l'output")
    d.p("Di norma un comando scrive il risultato a schermo. Con le redirezioni lo mandi "
        "dove vuoi: in un file, oppure nel nulla.")
    d.table(["Simbolo", "Cosa fa"], [
        ["`>`", "scrive l'output in un file, cancellando quello che c'era prima"],
        ["`>>`", "aggiunge l'output in fondo al file, senza cancellare"],
        ["`2>`", "dirotta i messaggi di errore (il canale 2, stderr)"],
        ["`2>/dev/null`", "butta via gli errori (il cestino del sistema)"],
        ["`<`", "prende l'ingresso da un file invece che dalla tastiera"],
    ], widths=[2200, 6826])
    d.code([
        "grep -r FLAG /srv > trovati.txt        # salva i risultati su file",
        "find /srv -type f 2>/dev/null          # cerca e butta via gli errori",
        "cut -d' ' -f1 access.log | sort -u > ip.txt   # pipe + redirezione insieme",
    ])

    d.h2("La cassetta degli attrezzi")
    d.table(["Comando", "A cosa serve"], [
        ["`grep parola file`", "mostra solo le righe che contengono la parola"],
        ["`grep -r parola cartella/`", "cerca dentro tutti i file di una cartella"],
        ["`grep -rl parola cartella/`", "elenca solo i NOMI dei file che la contengono"],
        ["`cut -d' ' -f1`", "taglia e tiene il primo campo (separatore: spazio)"],
        ["`sort`", "mette le righe in ordine (alfabetico)"],
        ["`sort -u`", "ordina e toglie i doppioni"],
        ["`sort -rn`", "ordine numerico (`n`) e inverso (`r`): dal più grande al più piccolo"],
        ["`uniq -c`", "conta le righe uguali consecutive (va usato DOPO `sort`)"],
        ["`wc -l`", "conta le righe (`-l` = lines)"],
        ["`head` / `tail`", "mostra le prime / le ultime righe (`-n N` per sceglierne N)"],
        ["`tr ' ' '\\n'`", "traduce/ sostituisce caratteri: qui cambia ogni spazio in un "
                           "a-capo, così ogni parola va su una riga"],
    ], widths=[2600, 6426])
    d.box("blu", "La combo che smaschera lo scanner", intro=(
        "Questa catena è un classico del mestiere: prende gli IP dal log, li ordina, "
        "li conta e mette in cima chi ha fatto più richieste."), items=[
        "`cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head`",
    ])

    d.h1("Parte 2 · Il setaccio (pratica, 80 min)")
    d.p("Prima il docente lancia `lab 4` sul bersaglio (semina i dati). Poi, sulla "
        "Kali, `lab 4` prepara la palestra e mostra la missione.")

    d.h2("A · Riscaldamento sulla Kali (offline)")
    d.p("Ti serve solo la Kali. Nella cartella della palestra c'è un file di frasi: "
        "estrai le parole uniche in ordine e salvale su file.")
    d.code([
        "cd ~/lab/lezione-04",
        "cat frasi.txt",
        "tr ' ' '\\n' < frasi.txt | sort -u > parole.txt",
        "lab04-warmup",
    ])
    d.p("`tr ' ' '\\n'` sostituisce ogni spazio con un a-capo, così ogni parola finisce "
        "su una riga. Se il verificatore è contento, ottieni la **prima flag** (+10).")

    d.h2("B · Setaccio sul bersaglio (via SSH)")
    d.p("Entra nel bersaglio come nella Lezione 3 e spostati nella cartella dell'azienda.")
    d.code([
        "ssh studente@10.10.10.20        # password: studente",
        "cd /srv/azienda",
        "ls -la",
    ])

    d.h3("Passo 1 · La riga col SEGRETO (+15)")
    d.p("Nel log ci sono più di mille righe, ma una sola contiene la parola SEGRETO. "
        "Fatti aiutare da `grep`.")
    d.code(["grep SEGRETO logs/access.log"])
    d.p("Leggi la flag nascosta in quella riga e riportala al docente.")

    d.h3("Passo 2 · La password tra 200 file (+15)")
    d.p("Nella cartella `documenti/` ci sono 200 note. Una sola contiene una password "
        "dimenticata. Invece di aprirle a una a una, chiedi a `grep` di elencarti solo "
        "il file giusto.")
    d.code([
        "grep -rl password documenti/ 2>/dev/null",
        "cat documenti/nota-137.txt          # apri il file che ti ha indicato",
    ])
    d.p("Nel file trovi la password e la flag.")

    d.h3("Passo 3 · Smaschera lo scanner (+20)")
    d.p("Qualcuno ha martellato il server con centinaia di richieste, quasi tutte "
        "errori 404: è uno scanner automatico. Scoprine l'IP con la combo delle pipe.")
    d.code([
        "cut -d' ' -f1 logs/access.log | sort | uniq -c | sort -rn | head",
    ])
    d.p("L'IP in cima è il colpevole. Ora leggi il file che porta il suo nome (il "
        "sistema ne ha lasciato uno apposta).")
    d.code(["cat ip-10.10.10.66.txt          # usa l'IP che hai trovato tu"])

    d.h3("Passo 4 · Salva il report (+10)")
    d.p("Un buon analista non tiene i risultati solo a schermo: li salva. Crea un file "
        "`report.txt` con l'elenco ordinato e senza doppioni di tutti gli IP del log, "
        "poi lancia il verificatore.")
    d.code([
        "cut -d' ' -f1 logs/access.log | sort -u > report.txt",
        "lab04-verifica",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.h2("Gli stessi attrezzi, per difendere")
    d.p("Chi difende un server legge i log ogni giorno con questi comandi. La combo del "
        "Passo 3 non serve solo ad attaccare: serve soprattutto ad accorgersi di essere "
        "attaccati. Un IP con centinaia di 404 in pochi minuti è un allarme.")
    d.code([
        "# quante richieste per ogni IP (chi esagera salta all'occhio)",
        "cut -d' ' -f1 logs/access.log | sort | uniq -c | sort -rn | head",
        "# solo gli errori 404, per capire cosa stanno cercando",
        "grep ' 404 ' logs/access.log | cut -d'\"' -f2 | sort | uniq -c | sort -rn",
    ])
    d.box("verde", "Regola del difensore", items=[
        "I log vanno letti, non solo raccolti: un log che nessuno guarda non protegge.",
        "Picchi di richieste e valanghe di 404 sono i primi segni di una scansione.",
        "Le pipe trasformano un log illeggibile in una risposta in un secondo.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('I tre canali: standard input, output ed errore', "Ogni comando ha tre canali. Lo standard input (stdin, canale 0) è ciò che arriva, di solito dalla tastiera. Lo standard output (stdout, canale 1) è il risultato normale. Lo standard error (stderr, canale 2) è dove finiscono gli errori, tenuti separati apposta. La pipe | collega lo stdout di un comando allo stdin del successivo. Le redirezioni dirottano un canale: > e >> agiscono su stdout, 2> agisce su stderr, e 2>/dev/null butta via gli errori senza sporcare il risultato. Capire questa distinzione spiega perché find /srv 2>/dev/null mostra solo i file trovati e nasconde la valanga di 'Permission denied': gli errori vanno sul canale 2, che tu stai scartando."),
        ],
        sintesi=[
            "La pipe | passa l'output di un comando al comando successivo: una catena di montaggio.",
            "Le redirezioni dirottano l'output: > sovrascrive, >> aggiunge, 2>/dev/null butta gli errori.",
            'grep filtra, cut taglia campi, sort ordina, uniq -c conta, wc -l conta le righe.',
            "La combo cut | sort | uniq -c | sort -rn | head smaschera chi compare più spesso in un log.",
            "Gli stessi strumenti servono all'attaccante (setacciare il bottino) e al difensore (leggere i log).",
        ],
        glossario=[
            ('Pipe (|)', "collega due comandi passando il testo dall'uno all'altro"),
            ('stdout / stderr', "il canale dell'output normale (1) e quello degli errori (2)"),
            ('Redirezione', "dirottare l'output: > file, >> file, 2> file"),
            ('/dev/null', "il 'cestino' del sistema: ciò che ci mandi sparisce"),
            ('grep', 'filtra le righe che contengono un testo (-r ricorsivo, -l solo i nomi)'),
            ('cut', 'estrae colonne/campi (-d separatore, -f numero campo)'),
            ('sort / uniq', 'ordina le righe / rimuove o conta i doppioni (uniq dopo sort)'),
            ('Log', 'registro degli eventi di un sistema o di un servizio'),
        ],
        errori=[
            'Usare uniq senza sort prima: conta solo i doppioni consecutivi.',
            'Confondere > (sovrascrive, cancella!) con >> (aggiunge in fondo).',
            "Dimenticare le virgolette quando il separatore è uno spazio: cut -d' ' -f1.",
            'Non filtrare gli errori con 2>/dev/null e perdere il risultato nel rumore.',
        ],
        domande=[
            "Come conti quante righe di un log contengono '404'?",
            "Come salvi su file l'elenco ordinato e senza doppioni degli IP di un log?",
            "Qual è la differenza tra > e >>? Cosa rischi a sbagliarli?",
            "Perché uniq va sempre usato dopo sort?",
            "Come troveresti, tra mille file, l'unico che contiene la parola 'password'?",
        ],
        collegamenti=[
            'Lezione 3: i comandi di base (ls, cat, find) su cui si costruiscono le pipe.',
            'Lezione 36: leggere i log di sicurezza usando esattamente queste pipe.',
            'Lezione 6: automatizzare queste catene dentro uno script.',
        ],
    )


    d.h2("Punteggio della Lezione 4")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Riscaldamento pipe (Kali)", "parole.txt + lab04-warmup", "10"],
        ["Riga col SEGRETO", "grep nel log", "15"],
        ["Password tra 200 file", "grep -rl", "15"],
        ["Smaschera lo scanner", "cut | sort | uniq -c | sort -rn", "20"],
        ["Salva il report", "report.txt + lab04-verifica", "10"],
    ], widths=[4200, 3326, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 4** · Navigazione avanzata, redirezioni e pipe (Blocco 2).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** ambiente della Lezione 2 in piedi; l'accesso ospite SSH "
        "della Lezione 3 (l'utente `studente`) viene ricreato anche da questo lab.",
        "**Deliverable studente:** 5 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire il modello a catena della shell: un comando, un compito; la pipe li unisce.",
        "Padroneggiare le redirezioni (`>`, `>>`, `2>`, `2>/dev/null`) e i tre canali "
        "(stdin, stdout, stderr).",
        "Usare la cassetta degli attrezzi testuali (grep, cut, sort, uniq, wc, head) su "
        "dati realistici.",
        "Collegare l'uso offensivo (setacciare bottino) a quello difensivo (leggere i log).",
    ])

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Ricrea l'utente ospite `studente` (password `studente`) e riabilita SSH a password.",
        "Rigenera da zero `/srv/azienda/` a ogni esecuzione (quindi si rigioca e si "
        "resetta semplicemente rilanciando `lab 4`).",
        "Crea `logs/access.log` (circa 1050 righe): traffico normale + circa 450 "
        "richieste dell'IP scanner `10.10.10.66` (quasi tutte 404) + una riga col SEGRETO.",
        "Crea `documenti/` con 200 note; solo `nota-137.txt` contiene la parola "
        "`password` e la relativa flag.",
        "Crea `utenti.csv` (materiale per esercizi extra con cut/sort) e "
        "`ip-10.10.10.66.txt` (leggibile dopo aver scoperto lo scanner).",
        "Installa il verificatore `/usr/local/bin/lab04-verifica` per il passo della "
        "redirezione su file.",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Crea la palestra offline in `~/lab/lezione-04/` con `frasi.txt`.",
        "Installa il verificatore `/usr/local/bin/lab04-warmup` per il riscaldamento.",
        "Controlla che il bersaglio risponda su SSH e stampa la missione.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Comando risolutivo", "Flag"], [
        ["Riscaldamento", "tr ' ' '\\n' < frasi.txt | sort -u > parole.txt ; lab04-warmup",
         "FLAG{sono_pronto_per_le_pipe}"],
        ["1 · SEGRETO", "grep SEGRETO logs/access.log", "FLAG{le_pipe_scavano_nei_log}"],
        ["2 · password", "grep -rl password documenti/ ; cat documenti/nota-137.txt",
         "FLAG{un_file_su_mille}"],
        ["3 · scanner", "cut -d' ' -f1 logs/access.log | sort | uniq -c | sort -rn | head ; "
         "cat ip-10.10.10.66.txt", "FLAG{ho_trovato_lo_scanner}"],
        ["4 · report", "cut -d' ' -f1 logs/access.log | sort -u > report.txt ; lab04-verifica",
         "FLAG{redirezione_su_file}"],
    ], widths=[1500, 5526, 2000])

    d.h1("Mappa di cosa è seminato dove")
    d.table(["Percorso sul bersaglio", "Contenuto"], [
        ["/srv/azienda/logs/access.log", "log con lo scanner e la riga SEGRETO"],
        ["/srv/azienda/documenti/nota-137.txt", "l'unico file con `password=` e la flag 2"],
        ["/srv/azienda/ip-10.10.10.66.txt", "flag 3, in chiaro (premio per aver trovato l'IP)"],
        ["/srv/azienda/utenti.csv", "elenco utenti (esercizi extra con cut)"],
        ["~/lab/lezione-04/frasi.txt (Kali)", "palestra del riscaldamento"],
    ], widths=[4200, 4826])
    d.p("L'IP scanner è fisso a `10.10.10.66`. Se un giorno serve cambiarlo, modifica "
        "`SCANNER_IP` in `target.sh` e il nome del file `ip-...txt` si adegua da solo.")

    d.h1("Rigiocare e resettare")
    d.bullets([
        "Per rigiocare o azzerare: rilancia `lab 4` sul bersaglio (ricrea tutto da zero).",
        "Sulla Kali, per rifare il riscaldamento cancella `~/lab/lezione-04/parole.txt` "
        "e riprova; oppure rilancia `lab 4`.",
        "Nessun dato persistente fuori da `/srv/azienda` e dalla palestra.",
    ])

    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa probabile e rimedio"], [
        ["`ssh` rifiuta la connessione", "bersaglio spento o `lab 4` non lanciato sul "
         "bersaglio; verifica che la VM sia accesa"],
        ["grep non trova SEGRETO", "il file è stato riscritto? rilancia `lab 4` sul "
         "bersaglio"],
        ["lab04-verifica dice che manca report.txt", "lo studente è entrato via SSH ma "
         "ha creato report.txt in un'altra cartella; deve stare in `~/report.txt` "
         "(la home dell'utente studente)"],
        ["`|` non si trova sulla tastiera", "AltGr + \\ (tasto sopra Invio) su layout italiano"],
    ], widths=[3400, 5626])

    d.h1("Nota didattica (scelta di progetto)")
    d.p("Il lab riusa l'accesso ospite SSH introdotto nella Lezione 3: gli studenti "
        "hanno già il gesto in mano e ci si concentra sulle pipe. Le flag di questa "
        "lezione sono didattiche e restano in chiaro nel repo (coerente con la politica "
        "flag per i primi blocchi). Dalle sfide web in poi le flag saranno generate a "
        "runtime.")
