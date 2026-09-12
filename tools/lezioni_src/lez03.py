# -*- coding: utf-8 -*-
import comune
NUM = 3
SLUG = "filesystem-e-permessi"
TITOLO = "Filesystem e permessi: la caccia al tesoro"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** entrare nel bersaglio via SSH ed esplorarne il filesystem, "
        "trovando le cose lasciate in giro per sbaglio e capendo perché un file resta 'un "
        "muro' che non riesci a leggere.",
        "**Al termine sai:** muoverti tra le cartelle, leggere file, trovarli con `find` e "
        "`grep`, e leggere i permessi rwx capendo perché bloccano o espongono i dati.",
        "**Flag in palio:** 5 flag + 1 bonus difensivo (70 punti).",
    ])

    d.h1("Parte 1 · Il palazzo e le chiavi (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Un attaccante entra in un server con un account qualsiasi: un utente rubato, un "
        "vecchio account ospite mai cancellato. Non è amministratore. Cosa fa? Gira per le "
        "cartelle e guarda: un backup di password dimenticato, un file di configurazione con "
        "dentro le credenziali, un documento riservato reso leggibile a tutti per sbaglio. "
        "Moltissime violazioni reali nascono così, non da un exploit sofisticato ma da un "
        "file con i permessi sbagliati. Oggi facciamo questo mestiere.")

    d.h2("Il filesystem: un grande palazzo")
    d.p("In Linux tutto parte da una sola radice, la cartella `/`. Da lì si diramano tutte "
        "le altre, come i piani e le stanze di un palazzo.")
    d.table(["Cartella", "Cosa contiene"], [
        ["/home", "gli 'appartamenti' degli utenti: /home/studente è casa tua"],
        ["/etc", "la sala quadri: i file di configurazione del sistema"],
        ["/var", "il magazzino: dati che cambiano, log, siti web"],
        ["/srv", "i dati 'serviti' dalla macchina. Qui oggi c'è il tesoro"],
        ["/root", "l'attico del capo: la home dell'amministratore. Vietato agli altri"],
        ["/tmp", "il cestino condiviso: file temporanei di tutti"],
    ], widths=[2000, 7026])

    d.h2("Muoversi: i percorsi")
    d.bullets([
        "**Percorso assoluto:** parte dalla radice, es. `/srv/dati/reparto-IT`. Vale sempre.",
        "**Percorso relativo:** parte da dove sei ora (lo dice `pwd`). `.` = qui, `..` = un "
        "piano sopra, `~` = casa tua.",
    ])

    d.h2("I file nascosti")
    d.p("I nomi che iniziano con un punto (per esempio `.diario`) non compaiono con `ls`. "
        "Servono a non ingombrare la vista, non per sicurezza: basta `ls -a` per vederli "
        "tutti. **Nascondere non è proteggere.**")

    d.h2("I permessi: chi può fare cosa")
    d.p("Ogni file ha un proprietario, un gruppo e tre terzine di permessi: una per il "
        "proprietario (user), una per il gruppo (group), una per tutti gli altri (other). "
        "Ogni terzina dice se si può leggere (r), scrivere (w), eseguire (x).")
    d.p("Anatomia di una riga di `ls -l`:")
    d.code(["-rw-r--r--  1  root  root  842  12 set  config.old"])
    d.table(["Simboli", "Numero", "Significato"], [
        ["r", "4", "lettura (leggere il file, elencare la cartella)"],
        ["w", "2", "scrittura (modificare il file, creare dentro la cartella)"],
        ["x", "1", "esecuzione (lanciare il file, attraversare la cartella)"],
        ["rwx", "7", "tutti e tre (4+2+1)"],
        ["rw-", "6", "lettura e scrittura"],
        ["r--", "4", "sola lettura"],
    ], widths=[2000, 1600, 5426])
    d.p("Quindi `chmod 644 file` vuol dire: proprietario `rw-` (6), gruppo e altri `r--` "
        "(4 e 4). E `600` vuol dire: solo il proprietario legge e scrive, nessun altro può "
        "nulla. La chiave di oggi: se 'altri' ha la `r` su un segreto, chiunque lo legge "
        "(la vulnerabilità che cercheremo); se è `600`, solo il proprietario lo legge "
        "(il muro che ci fermerà).")

    d.h1("Parte 2 · La caccia al tesoro (pratica, 80 min)")
    d.p("Preparazione: sul bersaglio si lancia una volta `lab 3` (semina la caccia), poi "
        "sulla Kali `lab 3` mostra la missione. Tutti i comandi si scrivono DENTRO il "
        "bersaglio, dopo esserci entrati via SSH.")

    d.h2("Passo 0 · Entrare nel bersaglio (SSH)")
    d.p("SSH è come aprire un terminale su un altro computer, a distanza. Per oggi il "
        "bersaglio ci lascia entrare con un utente ospite.")
    d.cmdref([
        ("`ssh`", "Apre una sessione su una macchina remota. Sintassi: `ssh utente@indirizzo`. "
                  "La prima volta chiede di fidarti (scrivi `yes`); poi la password (mentre "
                  "la digiti non si vede niente, è normale)."),
    ], titolo="Il comando per entrare")
    d.code([
        "ssh studente@10.10.10.20        # password: studente",
        "whoami        # chi sei: studente",
        "hostname      # su quale macchina sei",
        "pwd           # in quale cartella sei: /home/studente",
    ])
    d.cmdref([
        ("`ls`", "Elenca file e cartelle. `-l` formato lungo (permessi, proprietario), "
                 "`-a` mostra anche i nascosti, `-la` unisce i due."),
        ("`cat`", "Stampa a schermo il contenuto di un file di testo."),
        ("`cd`", "Cambia cartella. `cd ~` torna a casa, `cd ..` sale di un livello."),
    ])

    d.h2("Passo 1 · Dove sono? (+10)")
    d.code([
        "ls",
        "ls -la        # tutto, anche nascosti, con i permessi",
        "cat README-caccia.txt",
    ])
    d.p("Leggi la prima flag nel file di benvenuto.")

    d.h2("Passo 2 · I file nascosti (+10)")
    d.p("Con `ls -a` compaiono i file col punto davanti. Uno è un diario nascosto.")
    d.code([
        "ls -a",
        "cat .diario_nascosto",
    ])

    d.h2("Passo 3 · Scavare con find (+15)")
    d.cmdref([
        ("`find`", "Cerca file dentro un ramo del filesystem. `find /srv -type f` cerca "
                   "solo i file (non le cartelle), `-name \"*.old\"` filtra per nome. "
                   "Aggiungi `2>/dev/null` per buttare via gli errori 'Permission denied'."),
        ("`grep`", "Cerca una parola dentro i file. `-r` cerca ricorsivamente in tutte le "
                   "sottocartelle. Es. `grep -r FLAG /srv`."),
    ])
    d.code([
        "find /srv -type f 2>/dev/null",
        "find /srv -name \"*.old\" 2>/dev/null",
        "grep -r FLAG /srv 2>/dev/null",
        "cat /srv/dati/reparto-IT/archivio/2021/config.old",
    ])
    d.p("Segui la pista e leggi il file dimenticato: dentro c'è la flag.")

    d.h2("Passo 4 · Un permesso di troppo (+15)")
    d.p("Guarda `password_backup.txt`: è di root, ma l'ultima terzina ('altri') ha la "
        "`r`, quindi lo leggi anche tu. Un backup di credenziali leggibile da chiunque: "
        "ecco la vulnerabilità.")
    d.code([
        "cd /srv/dati/reparto-IT",
        "ls -l",
        "cat password_backup.txt",
    ])

    d.h2("Passo 5 · Il muro (+10)")
    d.p("Questa volta ricevi `Permission denied`. Guarda i permessi: `-rw-------` root "
        "root. La terzina 'altri' è vuota (`---`): non hai nessun diritto. Qui i permessi "
        "fanno il loro dovere. Non c'è una flag da leggere: riporta al docente la riga di "
        "`ls -l` e spiega PERCHÉ sei bloccato.")
    d.code([
        "cd /srv/dati/direzione",
        "ls -l",
        "cat stipendi.csv        # Permission denied: è il muro",
    ])

    d.h2("Bonus · Metti in sicurezza la TUA password (+10)")
    d.p("Torna a casa: il tuo `mia_password.txt` è `644`, leggibile da tutti. Chiudilo.")
    d.cmdref([
        ("`chmod`", "Cambia i permessi di un file. `chmod 600 file` = solo il proprietario "
                    "legge e scrive. `chmod 644` = proprietario rw, tutti gli altri sola "
                    "lettura."),
        ("`stat`", "Mostra i dettagli di un file. `stat -c '%a' file` stampa i permessi in "
                   "numeri (es. 600)."),
    ])
    d.code([
        "cd ~",
        "ls -l mia_password.txt        # -rw-r--r--  : lo leggono tutti",
        "chmod 600 mia_password.txt    # solo tu",
        "ls -l mia_password.txt        # -rw-------  : ora è chiuso",
        "caccia-verifica",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.h2("Il principio del minimo privilegio")
    d.p("Riguarda il Passo 4: il file era la vulnerabilità. Doveva essere `600`, era "
        "`644`. Nessuno lo ha 'bucato': era semplicemente aperto. La regola che lo avrebbe "
        "evitato si chiama minimo privilegio: dai a ciascuno solo i permessi che gli "
        "servono, niente di più.")
    d.box("verde", "Regole del difensore", items=[
        "I segreti (password, chiavi, backup) vanno a `600` o `400`: solo il proprietario.",
        "Non lasciare backup di password in cartelle condivise: è il regalo più grande "
        "per un attaccante.",
        "Il difensore usa gli stessi comandi per trovare i buchi PRIMA: es. "
        "`find /srv -type f -perm -o=r` elenca i file leggibili da 'altri'.",
    ])
    d.p("Oggi hai visto la lezione più importante di tutte: spesso non serve bucare "
        "niente, basta guardare bene. La difesa è ordine e disciplina sui permessi.")
    comune.studio(
        d,
        approfondimenti=[
            ('I permessi in dettaglio: dalle lettere ai numeri', "Ogni terzina di permessi (utente, gruppo, altri) è in realta' un numero da 0 a 7, somma di r=4, w=2, x=1. Così rwx=7, rw-=6, r-x=5, r--=4. Tre terzine diventano tre cifre: 644 vuol dire proprietario rw- (6), gruppo r-- (4), altri r-- (4). Attenzione alla x sulle cartelle: lì non significa 'eseguire' ma 'attraversare', cioè poter entrare nella cartella. Per questo una cartella tipicamente è 755: tutti possono entrarci ed elencarla, ma solo il proprietario può crearci dentro. Chi assegna i permessi ragiona sempre da destra a sinistra: cosa serve davvero ad 'altri'? Quasi mai la scrittura, spesso nemmeno la lettura."),
        ],
        sintesi=[
            'In Linux tutto parte dalla radice /; le cartelle chiave sono /home, /etc, /var, /srv, /root, /tmp.',
            'I percorsi sono assoluti (da /) o relativi (da dove sei: . qui, .. sopra, ~ casa).',
            'I permessi hanno tre terzine (utente, gruppo, altri) con r=4, w=2, x=1: 644, 600, 755.',
            "La vulnerabilità più comune non è un exploit ma un permesso sbagliato: un segreto leggibile da 'altri'.",
            "Nascondere non è proteggere: i file col punto si vedono con ls -a.",
        ],
        glossario=[
            ('Filesystem', "l'insieme organizzato di cartelle e file del sistema"),
            ('Percorso assoluto', 'parte dalla radice, es. /srv/dati; vale sempre'),
            ('Percorso relativo', 'parte dalla cartella corrente (pwd)'),
            ('Permessi rwx', 'lettura (r), scrittura (w), esecuzione/attraversamento (x)'),
            ('Proprietario / gruppo', "l'utente e il gruppo a cui appartiene un file"),
            ('chmod', 'cambia i permessi (es. chmod 600 file)'),
            ('SSH', 'collegamento a un terminale su una macchina remota'),
            ('Minimo privilegio', "dare solo i permessi indispensabili, niente di più"),
        ],
        errori=[
            "Lasciare un segreto a 644: la terzina 'altri' con la r lo rende leggibile a chiunque.",
            "Confondere i numeri: 600 non è 'poco', è 'solo il proprietario'.",
            "Dimenticare 2>/dev/null con find e affogare tra i 'Permission denied'.",
            'Credere che rinominare o nascondere un file lo protegga.',
        ],
        domande=[
            "Cosa vuol dire chmod 640 in termini di chi può fare cosa?",
            'Come cerchi tutti i file che contengono la parola FLAG sotto /srv?',
            "Perché stipendi.csv (600, root) è 'un muro' e password_backup.txt (644) no?",
            "Qual è la differenza tra percorso assoluto e relativo?",
            "Cos'è il principio del minimo privilegio e perché conta?",
        ],
        collegamenti=[
            'Lezione 4: setacciare file e log con pipe e redirezioni.',
            "Lezione 5: utenti, gruppi e la regola sudo (chi può diventare root).",
            "Lezione 35: hardening, cioè chiudere i permessi di troppo in modo sistematico.",
        ],
    )


    d.h2("Punteggio della Lezione 3")
    d.table(["Obiettivo", "Prova", "Punti"], [
        ["Benvenuto nella home", "FLAG{la_caccia...}", "10"],
        ["File nascosto", "FLAG{anche_i_nascosti...}", "10"],
        ["File sepolto (find/grep)", "FLAG{con_find...}", "15"],
        ["Permesso di troppo", "FLAG{permesso_di_troppo}", "15"],
        ["Il muro (capire e spiegare)", "Passo 5", "10"],
        ["Metti in sicurezza la password", "FLAG{ora_e_al_sicuro}", "10"],
    ], widths=[3800, 3726, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 3** · Filesystem e permessi (Blocco 2).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; accesso ospite SSH (creato dal lab).",
        "**Deliverable studente:** 5 flag + 1 bonus (70 punti).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh (lab 3) crea l'utente `studente` (password `studente`), abilita SSH a "
        "password e semina i file esca coi permessi indicati; installa il verificatore "
        "`caccia-verifica`.",
        "kali.sh (lab 3) verifica la porta SSH e mostra il briefing.",
    ])
    d.h1("Soluzioni, valori delle flag e mappa del tesoro")
    d.table(["File / azione", "Permessi", "Flag / concetto"], [
        ["~/README-caccia.txt", "644", "FLAG{la_caccia_ha_inizio} (cat)"],
        ["~/.diario_nascosto", "644", "FLAG{anche_i_nascosti_si_vedono} (ls -a)"],
        ["/srv/.../2021/config.old", "644", "FLAG{con_find_scavi_a_fondo} (find/grep)"],
        ["/srv/dati/reparto-IT/password_backup.txt", "644 root", "FLAG{permesso_di_troppo}"],
        ["/srv/dati/direzione/stipendi.csv", "600 root", "IL MURO: Permission denied (no flag)"],
        ["~/mia_password.txt -> chmod 600", "da 644 a 600", "FLAG{ora_e_al_sicuro} (caccia-verifica)"],
    ], widths=[3800, 1800, 3426])
    d.h1("Rigiocare e troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["ssh rifiuta", "bersaglio spento o `lab 3` non lanciato sul bersaglio"],
        ["caccia-verifica: file ancora aperto", "lo studente deve fare `chmod 600 "
         "~/mia_password.txt` (permessi 600 o 400)"],
        ["rigiocare/azzerare", "rilanciare `lab 3` sul bersaglio (idempotente)"],
    ], widths=[3200, 5826])
    d.h1("Nota didattica")
    d.p("È la lezione chiave del blocco Linux: il messaggio 'nascondere non è proteggere' "
        "e il minimo privilegio tornano per tutto il corso. Il Passo 5 (il muro) non dà "
        "flag di proposito: si valuta la spiegazione del perché l'accesso è negato.")
