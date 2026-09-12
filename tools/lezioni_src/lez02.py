# -*- coding: utf-8 -*-
NUM = 2
SLUG = "allestimento-del-laboratorio"
TITOLO = "Allestimento del laboratorio"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire com'e' fatto il laboratorio (due macchine virtuali su una "
        "rete isolata), come funziona il comando `lab` con cui scaricherai ogni "
        "esercitazione, e verificare che tutto comunichi.",
        "**Al termine sai:** cos'e' una VM e una rete interna, come leggere IP e porte, "
        "come usare `lab NN` in sicurezza, e come diagnosticare la connettivita'.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · La mappa del laboratorio (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Nessun professionista prova gli attacchi sui sistemi veri: userebbe un ambiente "
        "chiuso, una specie di 'poligono di tiro' digitale, dove puo' sbagliare senza fare "
        "danni ne' commettere reati. Il nostro laboratorio e' esattamente questo. Prima di "
        "attaccare qualsiasi cosa, oggi lo montiamo e ci assicuriamo che funzioni.")

    d.h2("Due macchine virtuali su una rete privata")
    d.p("Una macchina virtuale (VM) e' un computer 'finto' che gira dentro il tuo computer "
        "vero. Ne usiamo due, collegate da una rete interna chiamata `labnet` che vive solo "
        "dentro il tuo PC: non tocca internet ne' la rete della scuola.")
    d.table(["Macchina", "Ruolo", "Indirizzo IP", "Cosa contiene"], [
        ["Kali", "attaccante", "10.10.10.5", "gli strumenti e il comando `lab`"],
        ["Bersaglio", "vittima", "10.10.10.20", "Ubuntu con app web vulnerabili (Docker)"],
    ], widths=[1600, 1800, 2100, 3526])
    d.p("Sul bersaglio girano tre applicazioni web, ognuna su una **porta** diversa (la "
        "porta e' come l'interno di un centralino: stesso indirizzo, servizi diversi).")
    d.table(["App", "Indirizzo", "A cosa serve nel corso"], [
        ["Banca della Scuola", "http://10.10.10.20:8080", "app vulnerabile del corso (dalla L12)"],
        ["DVWA", "http://10.10.10.20:8081", "palestra di vulnerabilita' web classica"],
        ["OWASP Juice Shop", "http://10.10.10.20:8082", "app moderna piena di falle didattiche"],
    ], widths=[2400, 3200, 3426])

    d.h2("Come funziona il comando lab")
    d.p("Ogni esercitazione e' uno script conservato sul repository del corso. Non devi "
        "scaricarlo a mano: ci pensa `lab`. Sulle VM c'e' anche un file `/etc/lab-role` che "
        "dice se quella macchina e' 'kali' o 'target', cosi' `lab` scarica lo script giusto "
        "per il suo ruolo.")
    d.cmdref([
        ("`lab`", "Scarica dal repository lo script della lezione indicata per il ruolo "
                  "della macchina, ne mostra un'ANTEPRIMA e chiede conferma, poi lo esegue "
                  "con `sudo`. Esempio: `lab 2` esegue la Lezione 2."),
        ("`sudo`", "Esegue un comando con i poteri di amministratore (root). Serve perche' "
                   "gli script configurano il sistema."),
    ], titolo="Il comando della lezione")
    d.box("verde", "Perche' l'anteprima con conferma", items=[
        "`lab` ti mostra le prime righe dello script PRIMA di eseguirlo e ti chiede 's/N'.",
        "Non e' solo prudenza del corso: e' una regola di sicurezza vera. Non eseguire "
        "MAI uno script che non hai visto ('a scatola chiusa').",
        "Leggere prima cosa fa un comando e' l'abitudine numero uno di chi lavora bene.",
    ])

    d.h1("Parte 2 · Accendere e verificare (pratica, 80 min)")
    d.p("Prima il bersaglio, poi la Kali. L'ordine conta: la Kali, quando fa i controlli, "
        "ha bisogno che il bersaglio sia gia' acceso e coi servizi attivi.")

    d.h2("Passo 1 · Accendi i servizi sul bersaglio (+35)")
    d.p("Sul bersaglio esegui `lab 2`: accende le tre app web e ne mostra lo stato.")
    d.code([
        "lab 2",
        "# leggi la tabella dei servizi: devono risultare tutti 'attivo'",
    ])
    d.p("Se tutto e' attivo, il bersaglio ti consegna la flag `FLAG{bersaglio_online}`.")

    d.h2("Passo 2 · Verifica la rete dalla Kali (+35)")
    d.p("Sulla Kali esegui `lab 2`: controlla il tuo IP, che il bersaglio risponda al ping "
        "e che le tre app rispondano. Se tutto e' verde, ottieni `FLAG{la_rete_e_viva}`.")
    d.code(["lab 2"])
    d.p("Questi sono i comandi che `lab 2` esegue per te; imparali, perche' sono la prima "
        "cosa da fare quando 'qualcosa non va'.")
    d.cmdref([
        ("`ip -4 addr`", "Mostra gli indirizzi IPv4 delle schede di rete. Cerca "
                         "`10.10.10.5`: e' la Kali sulla rete del lab."),
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
    d.box("verde", "L'isolamento e' una difesa", items=[
        "Separare le reti (segmentazione) e' una delle difese piu' efficaci: se una parte "
        "cade, le altre restano al sicuro. Il nostro `labnet` isolato ne e' un esempio.",
        "Il bersaglio ha internet solo al momento del setup, poi resta isolato: meno "
        "esposizione, meno rischi.",
        "L'abitudine di leggere uno script prima di eseguirlo (l'anteprima di `lab`) e' la "
        "stessa che ti salva dal copiare comandi pericolosi trovati online.",
    ])
    d.p("In questa lezione, di solito, si firma anche il patto etico del corso: un impegno "
        "scritto a usare queste competenze solo nel laboratorio e per difendere.")

    d.h2("Punteggio della Lezione 2")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Bersaglio online", "lab 2 sul bersaglio (servizi attivi)", "35"],
        ["La rete e' viva", "lab 2 sulla Kali (tutti i check ok)", "35"],
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
        "Verificare la connettivita' e diagnosticare i problemi tipici di rete.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh (lab 2) riavvia i container (DVWA, Juice Shop, Banca) e stampa lo stato; "
        "a servizi attivi mostra `FLAG{bersaglio_online}`.",
        "kali.sh (lab 2) e' una diagnostica di sola lettura: IP interno, ping al bersaglio, "
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
        ["un'app non risponde", "container giu': sul bersaglio `docker ps`; su ARM DVWA "
         "non parte (atteso, l'aula e' x86)"],
        ["lab dice 'Cannot fork'", "il launcher aveva fine riga CRLF: usare la versione "
         "corrente di `bin/lab` (LF)"],
    ], widths=[2800, 6226])
    d.h1("Nota (x86 vs ARM)")
    d.p("Le immagini di produzione sono x86 e vanno costruite su Windows con VirtualBox. "
        "Su Mac ARM (Parallels) DVWA non parte: e' atteso. Dettagli e checklist di export "
        "nel README di `lezioni/lezione-02/`.")
