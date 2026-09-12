# -*- coding: utf-8 -*-
import comune
NUM = 2
SLUG = "allestimento-del-laboratorio"
TITOLO = "Allestimento del laboratorio"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire com'è fatto il laboratorio (due macchine virtuali su una "
        "rete isolata), come funziona il comando `lab` con cui scaricherai ogni "
        "esercitazione, e verificare che tutto comunichi.",
        "**Al termine sai:** cos'è una VM e una rete interna, come leggere IP e porte, "
        "come usare `lab NN` in sicurezza, e come diagnosticare la connettività.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · La mappa del laboratorio (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Nessun professionista prova gli attacchi sui sistemi veri: userebbe un ambiente "
        "chiuso, una specie di 'poligono di tiro' digitale, dove può sbagliare senza fare "
        "danni né commettere reati. Il nostro laboratorio è esattamente questo. Prima di "
        "attaccare qualsiasi cosa, oggi lo montiamo e ci assicuriamo che funzioni.")

    d.h2("Due macchine virtuali su una rete privata")
    d.p("Una macchina virtuale (VM) è un computer 'finto' che gira dentro il tuo computer "
        "vero. Ne usiamo due, collegate da una rete interna chiamata `labnet` che vive solo "
        "dentro il tuo PC: non tocca internet né la rete della scuola.")
    d.table(["Macchina", "Ruolo", "Indirizzo IP", "Cosa contiene"], [
        ["Kali", "attaccante", "10.10.10.5", "gli strumenti e il comando `lab`"],
        ["Bersaglio", "vittima", "10.10.10.20", "Ubuntu con app web vulnerabili (Docker)"],
    ], widths=[1600, 1800, 2100, 3526])
    d.p("Sul bersaglio girano tre applicazioni web, ognuna su una **porta** diversa (la "
        "porta è come l'interno di un centralino: stesso indirizzo, servizi diversi).")
    d.table(["App", "Indirizzo", "A cosa serve nel corso"], [
        ["Banca della Scuola", "http://10.10.10.20:8080", "app vulnerabile del corso (dalla L12)"],
        ["DVWA", "http://10.10.10.20:8081", "palestra di vulnerabilità web classica"],
        ["OWASP Juice Shop", "http://10.10.10.20:8082", "app moderna piena di falle didattiche"],
    ], widths=[2400, 3200, 3426])

    d.h2("Come funziona il comando lab")
    d.p("Ogni esercitazione è uno script conservato sul repository del corso. Non devi "
        "scaricarlo a mano: ci pensa `lab`. Sulle VM c'è anche un file `/etc/lab-role` che "
        "dice se quella macchina è 'kali' o 'target', così `lab` scarica lo script giusto "
        "per il suo ruolo.")
    d.cmdref([
        ("`lab`", "Scarica dal repository lo script della lezione indicata per il ruolo "
                  "della macchina, ne mostra un'ANTEPRIMA e chiede conferma, poi lo esegue "
                  "con `sudo`. Esempio: `lab 2` esegue la Lezione 2."),
        ("`sudo`", "Esegue un comando con i poteri di amministratore (root). Serve perché "
                   "gli script configurano il sistema."),
    ], titolo="Il comando della lezione")
    d.box("verde", "Perché l'anteprima con conferma", items=[
        "`lab` ti mostra le prime righe dello script PRIMA di eseguirlo e ti chiede 's/N'.",
        "Non è solo prudenza del corso: è una regola di sicurezza vera. Non eseguire "
        "MAI uno script che non hai visto ('a scatola chiusa').",
        "Leggere prima cosa fa un comando è l'abitudine numero uno di chi lavora bene.",
    ])

    d.h1("Parte 2 · Accendere e verificare (pratica, 80 min)")
    d.p("Prima il bersaglio, poi la Kali. L'ordine conta: la Kali, quando fa i controlli, "
        "ha bisogno che il bersaglio sia già acceso e coi servizi attivi.")

    d.h2("Passo 1 · Accendi i servizi sul bersaglio (+35)")
    d.p("Sul bersaglio esegui `lab 2`: accende le tre app web e ne mostra lo stato.")
    d.code([
        "lab 2",
        "# leggi la tabella dei servizi: devono risultare tutti 'attivo'",
    ])
    d.p("Se tutto è attivo, il bersaglio ti consegna la flag `FLAG{bersaglio_online}`.")

    d.h2("Passo 2 · Verifica la rete dalla Kali (+35)")
    d.p("Sulla Kali esegui `lab 2`: controlla il tuo IP, che il bersaglio risponda al ping "
        "e che le tre app rispondano. Se tutto è verde, ottieni `FLAG{la_rete_e_viva}`.")
    d.code(["lab 2"])
    d.p("Questi sono i comandi che `lab 2` esegue per te; imparali, perché sono la prima "
        "cosa da fare quando 'qualcosa non va'.")
    d.cmdref([
        ("`ip -4 addr`", "Mostra gli indirizzi IPv4 delle schede di rete. Cerca "
                         "`10.10.10.5`: è la Kali sulla rete del lab."),
        ("`ping`", "Verifica che un host risponda in rete. `-c N` invia N pacchetti, "
                   "`-W N` aspetta al massimo N secondi la risposta."),
        ("`curl`", "Contatta un servizio web. `-s` silenzioso, `-o /dev/null` butta via il "
                   "contenuto (ci interessa solo se risponde), `-m N` timeout di N secondi."),
    ])
    d.code([
        "ip -4 addr | grep 10.10.10.5",
        "ping -c 1 10.10.10.20",
        "curl -s -o /dev/null -m 4 http://10.10.10.20:8081 && echo 'DVWA risponde'",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "L'isolamento è una difesa", items=[
        "Separare le reti (segmentazione) è una delle difese più efficaci: se una parte "
        "cade, le altre restano al sicuro. Il nostro `labnet` isolato ne è un esempio.",
        "Il bersaglio ha internet solo al momento del setup, poi resta isolato: meno "
        "esposizione, meno rischi.",
        "L'abitudine di leggere uno script prima di eseguirlo (l'anteprima di `lab`) è la "
        "stessa che ti salva dal copiare comandi pericolosi trovati online.",
    ])
    d.p("In questa lezione, di solito, si firma anche il patto etico del corso: un impegno "
        "scritto a usare queste competenze solo nel laboratorio e per difendere.")
    comune.studio(
        d,
        approfondimenti=[
            ('Capire gli indirizzi: cosa vuol dire /24', "Gli indirizzi della rete del laboratorio sono scritti come 10.10.10.0/24. Un indirizzo IPv4 è fatto di 32 bit, divisi in quattro gruppi (i quattro numeri). Il numero dopo la barra dice quanti bit, partendo da sinistra, identificano la RETE; i restanti identificano i singoli computer (host). Con /24 i primi 24 bit (cioè 10.10.10) sono la rete e restano 8 bit per gli host: da 10.10.10.1 a 10.10.10.254, cioè 254 indirizzi utilizzabili. Il .0 è l'indirizzo della rete e il .255 è il broadcast (parla a tutti insieme). Ecco perché la tua Kali (10.10.10.5) e il bersaglio (10.10.10.20) si parlano direttamente: hanno gli stessi primi tre gruppi, quindi stanno nella stessa rete locale e non serve un router in mezzo."),
            ("Perché proprio due schede di rete", "La doppia scheda non è un capriccio: separa due mondi. La scheda NAT collega la VM a internet passando dall'host, e serve solo durante il setup (e alla Kali per scaricare gli script con lab). La scheda su Rete interna collega le VM tra loro in una bolla isolata. Questa separazione è già una lezione di sicurezza: il traffico 'pericoloso' degli esercizi resta confinato, senza mai toccare la rete della scuola. Nel mondo reale si chiama segmentazione, ed è una delle difese più efficaci."),
        ],
        sintesi=[
            'Il laboratorio sono due VM (Kali attaccante 10.10.10.5, bersaglio 10.10.10.20) su una rete interna isolata chiamata labnet.',
            'Ogni VM ha due schede: NAT (internet) e Rete interna (labnet). Se sbagli qui, niente comunica.',
            "Il comando lab NN scarica lo script della lezione per il ruolo della macchina, ne mostra un'anteprima e chiede conferma.",
            "Ordine di accensione: prima il bersaglio, poi la Kali. L'isolamento della rete è già una forma di difesa (segmentazione).",
        ],
        glossario=[
            ('Macchina virtuale (VM)', 'un computer simulato che gira dentro il tuo PC'),
            ('ISO', 'il file immagine di un disco di installazione (di Kali o Ubuntu)'),
            ('OVA', "un unico file che impacchetta una o più VM pronte da importare"),
            ('NAT', "modalità di rete che dà internet alla VM condividendo l'IP dell'host"),
            ('Rete interna (labnet)', 'rete privata tra le VM, isolata da internet e dalla scuola'),
            ('Porta', 'numero che identifica un servizio su un IP (es. 8080 = web)'),
            ('Container Docker', "app impacchettata con tutto ciò che le serve, avviabile in un istante"),
            ('/etc/lab-role', "file che dice a lab se la macchina è 'kali' o 'target'"),
        ],
        errori=[
            'Mettere la seconda scheda su reti interne con NOMI diversi tra le due VM: non si vedranno.',
            'Accendere la Kali prima del bersaglio e poi stupirsi che i controlli falliscano.',
            "Eseguire uno script senza leggerne l'anteprima: pessima abitudine di sicurezza.",
            'Distribuire un OVA costruito su Mac ARM per PC x86 (non si avvia).',
        ],
        domande=[
            'A cosa servono le due schede di rete di ogni VM?',
            "Perché lab mostra un'anteprima e chiede conferma prima di eseguire?",
            "Cos'è una porta e come fa un solo IP a offrire più servizi?",
            "Che differenza c'è tra NAT e Rete interna?",
            'Con quali comandi verifichi che la Kali veda il bersaglio?',
        ],
        collegamenti=[
            'Lezione 1: i primi comandi che qui usi per la diagnostica.',
            'Lezione 8: scoprire gli host della rete labnet con nmap.',
            "Lezione 12: la 'Banca della Scuola' su :8080 diventa il bersaglio del blocco web.",
        ],
    )


    d.h2("Punteggio della Lezione 2")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Bersaglio online", "lab 2 sul bersaglio (servizi attivi)", "35"],
        ["La rete è viva", "lab 2 sulla Kali (tutti i check ok)", "35"],
    ], widths=[3800, 3726, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 2** · Allestimento del laboratorio (Blocco 1).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** OVA importato; le due VM avviate con la scheda 'Rete interna "
        "labnet' attiva.",
        "**Deliverable studente:** 2 flag (70 punti) + patto etico firmato.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire architettura del lab (VM, rete interna, IP, porte) e il meccanismo `lab`.",
        "Instillare l'abitudine dell'anteprima-prima-di-eseguire.",
        "Verificare la connettività e diagnosticare i problemi tipici di rete.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh (lab 2) riavvia i container (DVWA, Juice Shop, Banca) e stampa lo stato; "
        "a servizi attivi mostra `FLAG{bersaglio_online}`.",
        "kali.sh (lab 2) è una diagnostica di sola lettura: IP interno, ping al bersaglio, "
        "risposta delle tre app; se tutto ok mostra `FLAG{la_rete_e_viva}`.",
        "In `lezioni/lezione-02/` ci sono anche gli script del docente per costruire ed "
        "esportare l'OVA (README, costruisci-ova.ps1/.sh).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "lab 2 sul bersaglio (tutti i servizi attivi)", "FLAG{bersaglio_online}"],
        ["2", "lab 2 sulla Kali (IP, ping, 3 app ok)", "FLAG{la_rete_e_viva}"],
    ], widths=[700, 5626, 2700])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["la Kali non ha 10.10.10.5", "scheda 'Rete interna labnet' non attiva su Kali; "
         "controllare le due schede (NAT + labnet)"],
        ["il bersaglio non risponde al ping", "VM spenta o non su labnet; accenderla e "
         "verificare la scheda 2"],
        ["un'app non risponde", "container giù: sul bersaglio `docker ps`; su ARM DVWA "
         "non parte (atteso, l'aula è x86)"],
        ["lab dice 'Cannot fork'", "il launcher aveva fine riga CRLF: usare la versione "
         "corrente di `bin/lab` (LF)"],
    ], widths=[2800, 6226])
    d.h1("Nota (x86 vs ARM)")
    d.p("Le immagini di produzione sono x86 e vanno costruite su Windows con VirtualBox. "
        "Su Mac ARM (Parallels) DVWA non parte: è atteso. Dettagli e checklist di export "
        "nel README di `lezioni/lezione-02/`.")
