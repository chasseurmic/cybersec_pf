# -*- coding: utf-8 -*-
import comune
NUM = 17
SLUG = "file-upload-path-traversal-lfi"
TITOLO = "File upload, path traversal e LFI"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** far leggere al sito file che non dovrebbe (path traversal / LFI) e "
        "caricare file che non dovrebbe accettare (upload non validato).",
        "**Al termine sai:** usare `../` per risalire le cartelle, leggere file riservati e "
        "di sistema attraverso un parametro vulnerabile, e riconoscere i pericoli di un "
        "upload senza controlli.",
        "**Flag in palio:** 2 flag (70 punti). Prerequisito: Banca (Lezione 12).",
    ])

    d.h1("Parte 1 · Uscire dai confini (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Molti siti aprono file in base a un parametro (per esempio `?file=relazione.pdf`). "
        "Se il sito incolla quel nome in un percorso senza controllarlo, tu puoi scrivere "
        "`../` per risalire le cartelle e leggere file fuori da quelli previsti: "
        "configurazioni, password, l'elenco degli utenti del sistema. Questo si chiama "
        "path traversal, e quando il file viene 'incluso' o mostrato si parla di LFI "
        "(Local File Inclusion).")
    d.p("L'altra faccia della medaglia è l'upload: se un sito accetta qualunque file "
        "senza controllare tipo e nome, un attaccante può caricare un programma "
        "malevolo, e su un server reale potrebbe perfino farlo eseguire.")

    d.h2("Il potere di ../")
    d.code([
        "?file=relazione.pdf              # uso previsto",
        "?file=../segreti/lfi.txt         # esco dalla cartella prevista",
        "?file=../../../../etc/passwd     # risalgo fino alla radice e leggo un file di sistema",
    ])

    d.h1("Parte 2 · Leggi e carica ciò che non dovresti (pratica, 80 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12), poi `lab 17` (avvia anche un servizio "
        "di upload su :8096).")

    d.h2("Passo 1 · Path traversal e LFI (+35)")
    d.p("La pagina 'Documenti' apre i file in base al parametro `file`. Guarda cosa "
        "mostra normalmente, poi esci dai confini con `../`.")
    d.code([
        "curl \"http://10.10.10.20:8080/documenti\"",
        "curl \"http://10.10.10.20:8080/documenti?file=../segreti/lfi.txt\"",
        "curl \"http://10.10.10.20:8080/documenti?file=../../../../etc/passwd\"",
    ])
    d.p("Nel file riservato trovi la flag. Con /etc/passwd vedi che puoi leggere anche "
        "file del sistema: è la prova della gravità.")

    d.h2("Passo 2 · Upload non validato (+35)")
    d.p("Il servizio su :8096 accetta file senza controllare il tipo. Carica un file con "
        "estensione pericolosa.")
    d.code([
        "echo \"codice cattivo\" > shell.php",
        "curl --data-binary @shell.php \"http://10.10.10.20:8096/upload?nome=shell.php\"",
    ])
    d.p("Il server accetta il `.php` e ti avvisa che un server reale avrebbe potuto "
        "eseguirlo: ecco la flag. Prova anche a caricare con un nome tipo "
        "`../altrodir/file` per capire il rischio del path traversal in scrittura.")

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Come si chiudono queste falle", items=[
        "Non costruire percorsi con l'input dell'utente: usare un elenco fisso di file "
        "permessi, o normalizzare e verificare che il percorso resti dentro la cartella "
        "consentita.",
        "Upload: whitelist delle estensioni permesse, rinominare i file, salvarli fuori "
        "dalla cartella web e senza permesso di esecuzione, controllare il tipo reale.",
        "Limitare i permessi del processo web: se legge poco, un LFI ruba poco.",
        "Mai fidarsi del nome file scelto dall'utente.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("Perché upload e path traversal sono così pericolosi", "Un upload non validato non è solo 'un file di troppo': su un server reale può trasformarsi in esecuzione di codice. Se il sito salva un file .php in una cartella servita dal web server, aprirlo lo esegue: l'attaccante ottiene una 'webshell', cioè una porta per lanciare comandi sul server. Per questo non basta guardare l'estensione (si può mascherare) né il tipo dichiarato dal browser (si falsifica): serve una whitelist, rinominare i file e salvarli fuori dalla cartella eseguibile. Il path traversal è l'altra faccia: se un percorso si costruisce con l'input dell'utente, i ../ permettono di uscire dalla cartella prevista. La difesa è 'canonicalizzare' il percorso (ridurlo alla forma reale) e verificare che resti dentro i confini consentiti."),
        ],
        sintesi=[
            'Il path traversal usa ../ per uscire dalla cartella prevista e leggere file altrove (LFI).',
            'Se un sito apre file in base a un parametro non controllato, si arriva a /etc/passwd o a segreti.',
            "L'upload non validato accetta qualunque tipo/nome di file: su un server reale può portare a esecuzione di codice.",
            "Non fidarsi mai del nome file scelto dall'utente.",
            'Difesa: whitelist dei file/estensioni, normalizzare i percorsi, permessi minimi del processo web.',
        ],
        glossario=[
            ('Path traversal', 'risalire le cartelle con ../ per uscire dai confini previsti'),
            ('LFI', 'Local File Inclusion: far leggere/includere al sito un file locale'),
            ('Upload non validato', 'accettare file senza controllarne tipo, nome, contenuto'),
            ('Whitelist', "elenco chiuso di ciò che è permesso (l'opposto della blacklist)"),
            ('Webshell', 'un file caricato che permette di eseguire comandi sul server'),
            ('Normalizzazione del percorso', 'ridurre un percorso alla forma reale per verificarlo'),
        ],
        errori=[
            "Costruire percorsi concatenando l'input senza verificare i ../.",
            "Accettare upload senza controllare l'estensione e il tipo reale.",
            'Salvare gli upload in una cartella web con permesso di esecuzione.',
            "Fidarsi del nome file: può contenere ../ o estensioni pericolose.",
        ],
        domande=[
            'Come useresti ../ per leggere un file fuori dalla cartella dei documenti?',
            "Che differenza c'è tra path traversal e LFI?",
            "Perché un upload non validato è pericoloso anche senza esecuzione?",
            "Cos'è una whitelist e perché è meglio di una blacklist?",
            'Come limita i danni un processo web con permessi minimi?',
        ],
        collegamenti=[
            'Lezione 3: i permessi dei file, che qui fanno la differenza.',
            'Lezione 18: il caveau del CTF, raggiunto con path traversal.',
            'Lezione 12-13: altre falle della stessa app (SQLi).',
        ],
    )


    d.h2("Punteggio della Lezione 17")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Path traversal / LFI", "documenti?file=../segreti/lfi.txt", "35"],
        ["Upload non validato", "caricare shell.php su :8096", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 17** · File upload, path traversal e LFI (Blocco 4).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Banca installata (Lezione 12).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire path traversal e LFI attraverso un parametro file non validato.",
        "Capire i rischi dell'upload non validato (tipo/nome).",
        "Collegare alla difesa: whitelist, normalizzazione dei percorsi, minimi permessi.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "LFI: usa l'endpoint `/documenti?file=` della Banca (nessuna sanitizzazione). Il "
        "file riservato con la flag è in `/opt/lab/banca-app/segreti/lfi.txt` (ricreato a "
        "ogni avvio del servizio banca).",
        "Upload: `lab17-upload.service` su :8096 salva i file senza controllare tipo né "
        "nome; se l'estensione è pericolosa, restituisce la flag.",
        "target.sh aggiunge FLAG_UPLOAD a flags.env; FLAG_LFI è già generata dalla "
        "Lezione 12.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env`.")
    d.table(["Passo", "Soluzione", "Variabile flag"], [
        ["1", "curl '.../documenti?file=../segreti/lfi.txt'", "FLAG_LFI"],
        ["2", "curl --data-binary @shell.php '.../upload?nome=shell.php' (:8096)",
         "FLAG_UPLOAD"],
    ], widths=[900, 5626, 2500])
    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["LFI non trova lfi.txt", "riavviare banca (`banca-ctl start`) che ricrea il file; "
         "oppure `lab 17`"],
        ["/etc/passwd non si legge", "verificare i permessi del processo banca (gira come "
         "root nel lab, quindi si legge)"],
        ["upload :8096 giù", "`systemctl status lab17-upload`; rilanciare `lab 17`"],
        ["voglio i valori", "`sudo cat /opt/lab/banca-app/flags.env`"],
    ], widths=[2800, 6226])
    d.h1("Nota di progetto")
    d.p("L'upload usa un servizio dedicato (:8096) con un protocollo semplice (corpo = "
        "contenuto, nome nel parametro) per restare in sola stdlib senza gestire il "
        "multipart. Il concetto (nessuna validazione di tipo/nome) è quello reale. Il "
        "path traversal in scrittura via nome file è citato come approfondimento.")
