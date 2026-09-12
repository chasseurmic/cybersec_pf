# -*- coding: utf-8 -*-
import comune
NUM = 34
SLUG = "analisi-dinamica-ioc"
TITOLO = "Analisi dinamica e indicatori di compromissione"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** osservare il comportamento di un programma sospetto MENTRE gira "
        "(analisi dinamica) in una sandbox isolata, e ricavarne gli indicatori di "
        "compromissione (IOC).",
        "**Al termine sai:** far girare un campione in sandbox e osservarne connessioni e "
        "file con strace, ss e ls, individuando il C2 e gli artefatti su disco.",
        "**Flag in palio:** 2 flag (70 punti). Sandbox isolata; il campione è innocuo.",
    ])

    d.h1("Parte 1 · Guardarlo agire, al sicuro (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("L'analisi statica (lezione scorsa) legge il file senza eseguirlo. Ma alcune cose "
        "si capiscono solo vedendolo in azione: a chi si collega, quali file crea, come "
        "cerca di sopravvivere ai riavvii. Questa è l'analisi dinamica, e si fa in una "
        "sandbox: una macchina isolata e usa-e-getta, senza internet, dove il malware può "
        "sfogarsi senza fare danni veri. Il campione di oggi è finto e innocuo, ma si "
        "comporta come uno vero: lascia un file e chiama un server C2.")

    d.h2("Cosa si osserva e con quali strumenti")
    d.table(["Comportamento", "Strumento", "IOC che ricavi"], [
        ["Connessioni di rete", "strace -e connect, ss, lsof", "IP/porta del C2"],
        ["File creati o modificati", "ls, find, watch", "nomi e percorsi degli artefatti"],
        ["Processi avviati", "ps, top, pstree", "nomi dei processi sospetti"],
        ["Persistenza", "controllo di cron, servizi, avvio", "meccanismo di riavvio"],
    ], widths=[2600, 3226, 3200])

    d.h1("Parte 2 · Osserva il campione (pratica, 80 min)")
    d.p("Sulla Kali `lab 34` installa `~/lab/lezione-34/sample-sim.py` (innocuo). Fallo "
        "girare e osservalo.")

    d.h2("Passo 1 · Chi chiama? Il C2 (+35)")
    d.p("Con strace vedi le chiamate di sistema, comprese le connessioni di rete.")
    d.code([
        "cd ~/lab/lezione-34",
        "strace -f -e trace=connect python3 sample-sim.py",
        "# cerca la riga  connect(... 10.66.66.66 ... 4444 ...)",
        "# in alternativa, mentre gira in un altro terminale:",
        "#   ss -tnp | grep 4444",
        "lab34-verifica c2 <ip:porta>",
    ])

    d.h2("Passo 2 · Cosa lascia su disco? (+35)")
    d.p("Molti malware lasciano tracce: file di configurazione, marcatori, copie di se'.")
    d.code([
        "ls -la /tmp/lab34-sandbox        # compare un file nascosto",
        "lab34-verifica file <nomefile>",
    ])

    d.box("blu", "Static e dinamica insieme", items=[
        "La statica (L32) ti dice cosa POTREBBE fare; la dinamica cosa FA davvero.",
        "Insieme danno gli IOC completi: hash (statica) + IP/file/processi (dinamica).",
        "In una vera analisi si combinano sempre, sempre in sandbox isolata.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Dagli IOC alla difesa (blue team)", items=[
        "Bloccare l'IP/dominio del C2 su firewall e proxy: il malware resta 'muto'.",
        "Cercare gli artefatti (i file lasciati) su tutti i PC: chi ce l'ha è infetto.",
        "Regole di rilevamento (SIEM/EDR) basate su questi IOC per accorgersi subito.",
        "Isolare la macchina compromessa: si ricollega all'incident response (Blocco 9).",
    ])
    d.p("Osservare bene un solo campione produce indicatori che proteggono un'intera rete: "
        "è il ponte verso il lavoro del difensore, il tema del prossimo blocco.")
    comune.studio(
        d,
        approfondimenti=[
            ('IOC e IOA: gli indizi di una compromissione', "Osservando un campione in esecuzione si raccolgono due tipi di indizi. Gli IOC (Indicator Of Compromise) sono tracce concrete: l'hash di un file, un IP o un dominio contattato, il nome di un file lasciato, una chiave di persistenza. Sono ottimi per cercare la stessa minaccia su altri computer e per creare regole di blocco. Gli IOA (Indicator Of Attack) descrivono invece il comportamento, la tattica: 'un processo office che lancia PowerShell che scarica un file'. Gli IOC cambiano facilmente (basta che l'attaccante cambi IP), gli IOA colgono lo schema e reggono meglio nel tempo. Un buon difensore usa entrambi: gli IOC per il blocco immediato, gli IOA per riconoscere anche le varianti mai viste prima."),
        ],
        sintesi=[
            "L'analisi dinamica osserva il comportamento del programma mentre gira, in una sandbox isolata.",
            'Si guardano connessioni (strace, ss), file creati (ls) e processi (ps).',
            "Da qui si ricavano gli IOC concreti: l'IP/porta del C2, gli artefatti su disco.",
            'Statica e dinamica insieme danno il quadro completo: cosa POTREBBE fare e cosa FA.',
            'Difesa: bloccare il C2, cercare gli artefatti su tutti i PC, isolare le macchine compromesse.',
        ],
        glossario=[
            ('Analisi dinamica', 'osservare un programma in esecuzione, in sandbox'),
            ('strace', 'mostra le chiamate di sistema di un processo (incluse le connessioni)'),
            ('ss / lsof', 'mostrano le connessioni di rete aperte'),
            ('Artefatto', 'traccia lasciata dal malware (file, chiave, processo)'),
            ('C2', 'server di comando e controllo che il malware contatta'),
            ('IOC', 'indicatori concreti per riconoscere la minaccia'),
        ],
        errori=[
            'Eseguire un campione fuori da una sandbox isolata.',
            'Guardare solo i file e non le connessioni di rete (o viceversa).',
            "Non annotare gli IOC: sono ciò che poi protegge l'intera rete.",
        ],
        domande=[
            "Cosa aggiunge l'analisi dinamica rispetto alla statica?",
            "Come scopri con chi 'parla' un campione (il C2)?",
            'Quali artefatti cerchi e come?',
            "Perché statica e dinamica vanno usate insieme?",
            "Come si passa dagli IOC alla difesa dell'intera rete?",
        ],
        collegamenti=[
            "Lezione 32: l'analisi statica, il primo passo.",
            'Lezione 27 e 36: usare gli IOC su firewall e sistemi di rilevamento.',
            'Lezione 37: isolare e bonificare una macchina compromessa.',
        ],
    )


    d.h2("Punteggio della Lezione 34")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Individua il C2", "strace/ss ; lab34-verifica c2", "35"],
        ["Trova l'artefatto", "ls /tmp/lab34-sandbox ; lab34-verifica file", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 34** · Analisi dinamica e IOC (Blocco 8, chiusura).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2) con strace; ambiente isolato senza internet.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Analisi dinamica in sandbox: osservare comportamento, non solo contenuto.",
        "Usare strace/ss/ls per ricavare IOC (C2, artefatti).",
        "Collegare gli IOC alla difesa e all'incident response (Blocco 9).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh installa `sample-sim.py`: crea `/tmp/lab34-sandbox/.persistenza` e tenta "
        "15 connessioni a 10.66.66.66:4444 (falliscono, isolato). Innocuo. Installa "
        "`lab34-verifica`.",
        "Osservazione: strace mostra i connect(); ls mostra l'artefatto.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "C2 = 10.66.66.66:4444 ; lab34-verifica c2 10.66.66.66:4444", "FLAG{ho_trovato_il_c2}"],
        ["2", "file = .persistenza ; lab34-verifica file .persistenza", "FLAG{indicatore_su_disco}"],
    ], widths=[700, 5926, 2400])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["strace non c'è", "installarlo (su Kali di norma presente); in alternativa usare "
         "`ss -tnp | grep 4444` mentre il campione gira"],
        ["ss non mostra la connessione", "il tentativo dura 1s: rilanciare e guardare "
         "subito, o usare strace che li mostra tutti"],
        ["il campione non termina", "gira circa 30s (15 tentativi x 2s) poi esce da solo; "
         "Ctrl+C per fermarlo prima"],
    ], widths=[3000, 6026])
    d.h1("Nota sul blocco (Lezione 33 saltata)")
    d.p("Su indicazione del docente, la Lezione 33 (ransomware didattico) non è stata "
        "sviluppata. Il Blocco 8 resta comunque completo nei concetti: tipologie e ciclo "
        "di vita (L31), analisi statica (L32) e analisi dinamica con IOC (L34). Se in "
        "futuro si volesse reintrodurre una simulazione di ransomware, andrebbe fatta solo "
        "su file esca in una cartella sandbox, con cifratura reversibile e chiave nota, "
        "senza mai toccare file reali.")
