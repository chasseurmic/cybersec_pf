# -*- coding: utf-8 -*-
NUM = 19
SLUG = "password-hash-salt"
TITOLO = "Come sono conservate le password (hash e salt)"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire come un sito serio conserva le password (non in chiaro!) "
        "usando gli hash, e perche' serve il sale (salt) per non farsi rubare tutto in "
        "caso di fuga di dati.",
        "**Al termine sai:** calcolare hash MD5 e SHA-256, capire che sono a senso unico, "
        "riconoscere il pericolo degli hash senza sale e come il sale lo risolve.",
        "**Flag in palio:** 3 flag (70 punti). Lezione sulla Kali (offline).",
    ])

    d.h1("Parte 1 · Non salvare mai le password in chiaro (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Ogni tanto un sito viene bucato e finisce online il suo database di utenti. Se le "
        "password erano salvate in chiaro, e' un disastro immediato: gli attaccanti le "
        "provano su email, social, banche (perche' la gente riusa le password). Per "
        "questo le password non vanno mai salvate cosi' come sono. La soluzione si chiama "
        "hash.")

    d.h2("L'hash: un tritacarne a senso unico")
    d.p("Un hash trasforma un testo in una stringa di lunghezza fissa, in modo che: dallo "
        "stesso testo esca sempre lo stesso hash; da testi diversi escano hash diversi; e "
        "dall'hash NON si possa tornare indietro al testo. E' come tritare la carne: "
        "facile fare l'hamburger, impossibile ricostruire la bistecca.")
    d.code([
        "printf '%s' password | md5sum       # sempre lo stesso risultato",
        "printf '%s' password | sha256sum    # hash piu' robusto e lungo",
        "printf '%s' Password | sha256sum    # una lettera diversa, hash completamente diverso",
    ])
    d.p("Al login il sito non confronta le password: calcola l'hash di quella che scrivi e "
        "lo confronta con quello salvato. Cosi' la password vera non e' scritta da nessuna "
        "parte.")

    d.h2("Il problema: stessa password, stesso hash")
    d.p("Se due utenti scelgono la stessa password e il sito salva l'hash 'nudo', i due "
        "hash sono identici. Un attaccante che vede due hash uguali sa che quelle persone "
        "hanno la stessa password, e con delle tabelle precalcolate (rainbow table) "
        "risale in fretta alle password piu' comuni.")

    d.h2("La soluzione: il sale (salt)")
    d.p("Il sale e' una stringa casuale diversa per ogni utente, che si aggiunge alla "
        "password prima di calcolare l'hash. Cosi' due persone con la stessa password "
        "hanno hash diversi, e le rainbow table non funzionano piu'.")
    d.code([
        "# senza sale: stessa password -> stesso hash",
        "printf '%s' 'primavera' | sha256sum",
        "# con sale (diverso per utente): hash diverso",
        "printf '%s' 's4leprimavera' | sha256sum",
    ])

    d.h1("Parte 2 · Le mani nell'impasto (pratica, 80 min)")
    d.p("Sulla Kali `lab 19` prepara un finto dump di password e il verificatore. Tutto "
        "in `~/lab/lezione-19`, senza rete.")

    d.h2("Passo 1 · Trova i due con la stessa password (+25)")
    d.p("Nel dump ci sono utenti e i loro hash MD5 senza sale. Due hanno lo stesso hash.")
    d.code([
        "cat ~/lab/lezione-19/dump.txt",
        "sort -t: -k2 ~/lab/lezione-19/dump.txt      # gli hash uguali finiscono vicini",
        "lab19-verifica coppia <utente1> <utente2>",
    ])

    d.h2("Passo 2 · Calcola un hash a senso unico (+20)")
    d.code([
        "printf '%s' 'hash a senso unico' | sha256sum",
        "lab19-verifica sha256 <hash>",
    ])

    d.h2("Passo 3 · Aggiungi il sale (+25)")
    d.p("Calcola l'hash della password 'primavera' con il sale 's4le' davanti.")
    d.code([
        "printf '%s' 's4leprimavera' | sha256sum",
        "lab19-verifica sale <hash>",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Come si conservano le password, sul serio", items=[
        "Mai in chiaro. Mai con MD5 o SHA 'nudi': sono troppo veloci da forzare.",
        "Usare funzioni pensate apposta e lente: bcrypt, scrypt, Argon2. La lentezza qui "
        "e' una difesa (rende il brute force costoso).",
        "Sempre con un sale casuale e diverso per ogni utente.",
        "Non reimporre limiti assurdi che spingono a password deboli; incoraggiare "
        "passphrase lunghe e il 2FA.",
    ])
    d.p("Nella prossima lezione vediamo l'altra faccia: quanto e' facile, con un hash "
        "veloce e senza sale, ritrovare le password con un dizionario.")

    d.h2("Punteggio della Lezione 19")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Stessa password", "trovare la coppia con hash uguale", "25"],
        ["Hash a senso unico", "sha256 di una frase", "20"],
        ["Il sale", "sha256 di sale+password", "25"],
    ], widths=[3600, 3926, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 19** · Hash e salt (Blocco 5, apertura password e crittografia).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2). Nessun bersaglio necessario.",
        "**Deliverable studente:** 3 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire hashing (a senso unico) e la differenza con la cifratura (Lezione 21).",
        "Vedere il pericolo degli hash senza sale (password uguali, rainbow table).",
        "Capire il ruolo del sale e, in difesa, delle funzioni lente (bcrypt/Argon2).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh crea `~/lab/lezione-19/dump.txt` (utente:md5) con alice e dave che "
        "condividono md5(password), e installa `lab19-verifica`.",
        "Il verificatore ricalcola da solo i valori attesi con sha256sum/md5sum: robusto e "
        "offline.",
        "target.sh: nessuna azione (lezione lato Kali).",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "coppia: alice dave (stesso md5 di 'password')", "FLAG{stesso_hash_stessa_password}"],
        ["2", "sha256 di 'hash a senso unico'", "FLAG{hash_a_senso_unico}"],
        ["3", "sha256 di 's4leprimavera'", "FLAG{il_sale_cambia_tutto}"],
    ], widths=[700, 5626, 2700])
    d.p("Password nel dump: alice=dave=password, bob=qwerty, carla=letmein, erik=sole. "
        "Utili anche per la Lezione 20 (cracking).")
    d.h1("Rigiocare e troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["hash non combacia", "attenzione a `printf '%s'` (niente a-capo finale); non "
         "usare `echo` che aggiunge \\n"],
        ["la coppia non passa", "sono alice e dave; l'ordine non conta"],
        ["voglio rigiocare", "rilanciare `lab 19` (ricrea dump e verificatore)"],
    ], widths=[2600, 6426])
    d.h1("Nota didattica")
    d.p("Il dettaglio piu' importante da far notare: `echo` aggiunge un a-capo e cambia "
        "l'hash. Usare sempre `printf '%s'`. E' un errore classico e un'ottima occasione "
        "per parlare di precisione.")
