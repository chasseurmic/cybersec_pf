# -*- coding: utf-8 -*-
NUM = 32
SLUG = "analisi-statica-sandbox"
TITOLO = "Analisi statica di base in sandbox"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** analizzare un file sospetto SENZA eseguirlo (analisi statica), per "
        "capire cosa fa in modo sicuro, ricavando indicatori utili alla difesa.",
        "**Al termine sai:** usare `file`, `strings`, `sha256sum` e `base64` per esaminare "
        "un campione, trovare URL/comandi nascosti e calcolarne l'impronta (IOC).",
        "**Flag in palio:** 3 flag (80 punti). Sandbox isolata; il campione e' innocuo.",
    ])

    d.h1("Parte 1 · Guardare senza aprire (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Un analista che riceve un file sospetto non lo apre col doppio clic: sarebbe come "
        "aprire un pacco bomba per vedere cosa c'e' dentro. Prima fa l'analisi statica: "
        "guarda il file dall'esterno e legge cio' che contiene senza eseguirlo. Gia' cosi' "
        "si scopre moltissimo: che tipo di file e', quali indirizzi contatta, quali "
        "comandi nasconde. Il campione di oggi e' finto e innocuo, ma le tecniche sono "
        "quelle vere.")

    d.h2("La cassetta degli attrezzi dell'analista")
    d.table(["Comando", "Cosa rivela"], [
        ["`file`", "che tipo di file e' (eseguibile, script, dati...)"],
        ["`strings`", "tutto il testo leggibile dentro il file (URL, comandi, messaggi)"],
        ["`sha256sum`", "l'impronta unica del file, l'indicatore (IOC) per riconoscerlo"],
        ["`base64 -d`", "decodifica le parti offuscate in base64"],
    ], widths=[2200, 6826])
    d.p("Un IOC (Indicator Of Compromise) e' un indizio che permette di riconoscere una "
        "minaccia: l'hash di un file, un IP, un dominio. Gli antivirus e i team di sicurezza "
        "si scambiano gli IOC per proteggere tutti.")

    d.h1("Parte 2 · Smonta il campione (pratica, 80 min)")
    d.p("Sulla Kali `lab 32` crea `~/lab/lezione-32/campione.bin` (innocuo, solo dati).")

    d.h2("Passo 1 · Tipo e stringhe sospette (+30)")
    d.code([
        "cd ~/lab/lezione-32",
        "file campione.bin",
        "strings campione.bin",
        "strings campione.bin | grep FLAG      # una flag e' in chiaro nel file",
    ])
    d.p("Nota anche il C2 (`http://10.66.66.66/...`) e il mutex: indizi tipici del malware.")

    d.h2("Passo 2 · L'impronta del file, l'IOC (+25)")
    d.code([
        "sha256sum campione.bin",
        "lab32-verifica hash <sha256>",
    ])

    d.h2("Passo 3 · Decodifica la parte nascosta (+25)")
    d.p("Una riga e' offuscata in base64. Decodificala per leggere il comando nascosto.")
    d.code([
        "strings campione.bin | grep cfg_base64",
        "echo \"<la-stringa-base64>\" | base64 -d",
        "# dentro c'e' un'altra flag",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "A cosa serve l'analisi statica, per difendere", items=[
        "Ricavare gli IOC (hash, IP, domini) e bloccarli su firewall e antivirus.",
        "Capire cosa farebbe il malware senza correre rischi (nessuna esecuzione).",
        "Condividere gli indicatori con la comunita' per proteggere altri.",
        "Riconoscere l'offuscamento (base64 e simili): un file 'normale' non nasconde "
        "comandi cifrati.",
    ])

    d.h2("Punteggio della Lezione 32")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Stringhe sospette", "strings | grep FLAG", "30"],
        ["Impronta IOC", "sha256sum ; lab32-verifica hash", "25"],
        ["Config offuscata", "base64 -d", "25"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 32** · Analisi statica di base in sandbox (Blocco 8).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2), ambiente isolato senza internet.",
        "**Deliverable studente:** 3 flag (80 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Analisi statica: esaminare un file senza eseguirlo.",
        "Usare file/strings/sha256sum/base64; concetto di IOC.",
        "Riconoscere offuscamento e indicatori (C2, mutex).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `campione.bin`: file di soli dati (NON eseguibile) con stringhe "
        "sospette, un C2 finto, un mutex e una config base64. Installa `lab32-verifica`.",
        "La flag delle stringhe e' in chiaro; quella base64 e' offuscata; l'hash si "
        "verifica ricalcolandolo (robusto).",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "strings campione.bin | grep FLAG", "FLAG{stringhe_rivelatrici}"],
        ["2", "sha256sum campione.bin ; lab32-verifica hash <valore>", "FLAG{impronta_del_file}"],
        ["3", "riga cfg_base64 ; base64 -d", "FLAG{comando_nascosto}"],
    ], widths=[700, 5626, 2700])
    d.p("La config base64 decodifica in: 'esegui il payload alle 03:00 e cifra i file "
        "FLAG{comando_nascosto}'. Su Kali usare `base64 -d`.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["base64 -d da' errore", "assicurarsi di passare SOLO la stringa base64 (senza "
         "'cfg_base64='); su Kali il flag e' `-d`"],
        ["hash non combacia", "usare sha256sum sullo stesso file `campione.bin`"],
        ["strings non c'e'", "e' in binutils; presente su Kali"],
    ], widths=[2800, 6226])
    d.h1("Nota di sicurezza")
    d.p("Il campione e' deliberatamente inerte (dati, non codice): nessun rischio anche se "
        "aperto per sbaglio. E' l'occasione per ribadire che con file REALI non si fa mai "
        "il doppio clic: prima analisi statica, in sandbox.")
