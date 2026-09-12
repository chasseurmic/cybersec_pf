# -*- coding: utf-8 -*-
NUM = 20
SLUG = "cracking-dizionario-john-hashcat"
TITOLO = "Cracking a dizionario: john e hashcat"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire come, dagli hash rubati, si ritrovano le password con un "
        "attacco a dizionario, prima con uno strumento scritto da te, poi con john e "
        "hashcat.",
        "**Al termine sai:** cos'e' un attacco a dizionario agli hash, usare un cracker "
        "MD5, e lanciare john e hashcat con una wordlist.",
        "**Flag in palio:** 2 flag (70 punti). Lezione sulla Kali (offline).",
    ])

    d.h1("Parte 1 · Dall'hash alla password (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Un attaccante ruba il database di un sito: trova gli hash, non le password. Ma se "
        "gli hash sono MD5 senza sale (come purtroppo capita ancora), ritrovare le "
        "password e' facilissimo. Non si 'inverte' l'hash: si indovina. Si prova a fare "
        "l'hash di milioni di parole comuni e si confronta. Quando due hash coincidono, "
        "hai trovato la password. E' l'altra faccia della Lezione 19.")

    d.h2("Attacco a dizionario")
    d.p("Invece di provare tutte le combinazioni (troppe), si prova solo una lista di "
        "password probabili. La piu' famosa e' rockyou, 14 milioni di password vere "
        "trapelate anni fa. Con hash veloci come MD5, un PC normale ne prova milioni al "
        "secondo.")
    d.code([
        "# l'idea, in tre righe di pseudocodice:",
        "per ogni parola nella wordlist:",
        "    se md5(parola) == hash_rubato:  ->  password trovata",
    ])

    d.h1("Parte 2 · Rompi gli hash (pratica, 80 min)")
    d.p("Sulla Kali `lab 20` prepara `~/lab/lezione-20` con `hashes.txt`, `wordlist.txt` e "
        "il tuo `cracker.py`.")

    d.h2("Passo 1 · Il tuo cracker (+40)")
    d.p("Leggi e lancia il cracker: prova ogni parola e confronta gli hash.")
    d.code([
        "cd ~/lab/lezione-20",
        "cat cracker.py",
        "python3 cracker.py hashes.txt wordlist.txt",
    ])
    d.p("Tra le password recuperate ce n'e' una 'segreta' (piu' lunga delle altre): "
        "consegnala al verificatore.")
    d.code(["lab20-verifica <password_segreta>"])

    d.h2("Passo 2 · Gli strumenti professionali (+30)")
    d.p("john e hashcat fanno lo stesso, ma molto piu' veloci e con mille opzioni. Ecco "
        "come si rompe lo stesso file.")
    d.code([
        "john --format=raw-md5 --wordlist=wordlist.txt hashes.txt",
        "john --show --format=raw-md5 hashes.txt",
        "",
        "# oppure hashcat (modo 0 = MD5, attacco 0 = dizionario):",
        "hashcat -m 0 -a 0 hashes.txt wordlist.txt --force",
        "hashcat -m 0 hashes.txt --show",
    ])
    d.p("Consegna una delle password recuperate con gli strumenti pro:")
    d.code(["lab20-verifica pro <password_recuperata>"])
    d.box("blu", "La wordlist gigante", intro=(
        "Su Kali c'e' rockyou, con milioni di password vere:"), items=[
        "gunzip -k /usr/share/wordlists/rockyou.txt.gz",
        "poi usala al posto di wordlist.txt (attenzione: e' enorme).",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Perche' certi hash si rompono e altri no", items=[
        "MD5 e SHA senza sale sono velocissimi: milioni di tentativi al secondo, quindi "
        "cadono in fretta.",
        "bcrypt, scrypt e Argon2 sono lenti apposta: lo stesso attacco richiederebbe anni.",
        "Il sale rende inutili le tabelle precalcolate: ogni password va attaccata da sola.",
        "Password lunghe e non comuni non sono nelle wordlist: l'attacco a dizionario le "
        "manca.",
    ])
    d.p("Morale: se scegli una passphrase lunga e il sito usa un hash lento e salato, un "
        "attacco a dizionario diventa impraticabile.")

    d.h2("Punteggio della Lezione 20")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Cracker fatto in casa", "cracker.py + lab20-verifica", "40"],
        ["Strumenti pro", "john/hashcat + lab20-verifica pro", "30"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 20** · Cracking a dizionario, john e hashcat (Blocco 5, con tool).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2) con john e hashcat. Nessun bersaglio.",
        "**Deliverable studente:** 2 flag (70 punti) + un cracker riutilizzabile.",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire l'attacco a dizionario agli hash (complemento della Lezione 19).",
        "Scrivere un cracker MD5 e usare john/hashcat.",
        "Motivare in difesa hash lenti e salati e password robuste.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `~/lab/lezione-20/` con `wordlist.txt`, `hashes.txt` (MD5 di "
        "password, tramonto2011, giardino, qwerty) e `cracker.py`; installa `lab20-verifica`.",
        "Il verificatore ricalcola i md5 attesi: robusto e offline.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "cracker.py; password segreta = tramonto2011 ; lab20-verifica tramonto2011",
         "FLAG{cracker_a_dizionario}"],
        ["2", "john/hashcat; es. giardino ; lab20-verifica pro giardino", "FLAG{john_e_hashcat}"],
    ], widths=[700, 5626, 2700])
    d.p("Hash nel file: md5 di password, tramonto2011, giardino, qwerty. La 'segreta' e' "
        "tramonto2011 (l'unica non banale). Per la parte pro va bene qualsiasi password "
        "recuperata, ma il verificatore 'pro' controlla 'giardino'.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["john dice 'No password hashes loaded'", "specificare `--format=raw-md5`"],
        ["hashcat si lamenta", "aggiungere `--force` (CPU); su VM va bene"],
        ["cracker non trova nulla", "verificare di passare hashes.txt e wordlist.txt "
         "nell'ordine giusto"],
        ["rockyou non c'e'", "e' in /usr/share/wordlists/rockyou.txt.gz: `gunzip -k`"],
    ], widths=[3200, 5826])
    d.h1("Nota tecnica (x86)")
    d.p("john e hashcat funzionano su x86; hashcat su VM usa la CPU (`--force`), piu' "
        "lento ma sufficiente per la wordlist piccola. Da provare sul bersaglio reale x86 "
        "solo se si vuole misurare la velocita' con rockyou completa.")
