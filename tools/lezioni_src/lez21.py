# -*- coding: utf-8 -*-
import comune
NUM = 21
SLUG = "crittografia-simmetrica-asimmetrica"
TITOLO = "Cifratura simmetrica e asimmetrica"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire la differenza tra cifratura simmetrica e asimmetrica, e tra "
        "cifrare (reversibile) e fare l'hash (irreversibile), usando openssl.",
        "**Al termine sai:** cifrare e decifrare con una chiave condivisa (AES), generare "
        "una coppia di chiavi RSA e capire a cosa servono chiave pubblica e privata, "
        "compresa la firma digitale.",
        "**Flag in palio:** 2 flag (70 punti). Lezione sulla Kali (offline).",
    ])

    d.h1("Parte 1 · Chiavi e lucchetti (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Quando mandi un messaggio su WhatsApp, paghi online o apri un sito con il "
        "lucchetto, dietro c'è la crittografia. Serve a due cose: tenere segreto un "
        "contenuto e garantire che venga davvero da chi dice. Ci sono due grandi famiglie "
        "di cifratura, e non vanno confuse con l'hash della lezione scorsa.")

    d.h2("Cifrare non è fare l'hash")
    d.table(["", "Hash", "Cifratura"], [
        ["Reversibile?", "no, a senso unico", "si, con la chiave giusta"],
        ["A cosa serve", "verificare integrità, conservare password", "tenere segreto un contenuto"],
        ["Esempi", "MD5, SHA-256", "AES, RSA"],
    ], widths=[2000, 3513, 3513])

    d.h2("Simmetrica: una sola chiave")
    d.p("Nella cifratura simmetrica (per esempio AES) la stessa chiave cifra e decifra. "
        "Veloce e robusta, ma c'è un problema: come consegni la chiave all'altra persona "
        "senza che qualcuno la intercetti?")

    d.h2("Asimmetrica: due chiavi, una coppia")
    d.p("Nella cifratura asimmetrica (per esempio RSA) ogni persona ha due chiavi legate "
        "tra loro: una pubblica (la puoi dare a tutti) e una privata (segretissima). Cio' "
        "che cifri con la pubblica si apre solo con la privata. Così chiunque può "
        "mandarti un messaggio segreto usando la tua chiave pubblica, ma solo tu, con la "
        "privata, lo leggi. E se firmi con la tua privata, tutti verificano con la tua "
        "pubblica che sei stato davvero tu: è la firma digitale.")

    d.h1("Parte 2 · Cifra e decifra con openssl (pratica, 80 min)")
    d.p("Sulla Kali `lab 21` prepara `~/lab/lezione-21` con un messaggio cifrato AES, una "
        "coppia di chiavi RSA e un messaggio cifrato per la chiave pubblica.")

    d.h2("Passo 1 · Simmetrica: apri con la passphrase (+30)")
    d.p("Ti è stata data la passphrase: `chiavesegreta`. Decifra il file AES.")
    d.code([
        "cd ~/lab/lezione-21",
        "openssl enc -d -aes-256-cbc -pbkdf2 -in segreto.enc -pass pass:chiavesegreta",
    ])
    d.p("Dentro trovi la prima flag. Prova anche a cifrare un tuo messaggio con lo stesso "
        "comando (senza `-d`).")

    d.h2("Passo 2 · Asimmetrica: apri con la chiave privata (+40)")
    d.p("Il messaggio è stato cifrato con la chiave pubblica: solo la privata "
        "(`priv.pem`) lo apre.")
    d.code([
        "openssl pkeyutl -decrypt -inkey priv.pem -in messaggio.enc",
    ])
    d.box("blu", "Approfondimento: la firma digitale", intro=(
        "Si firma con la privata, si verifica con la pubblica:"), items=[
        "echo 'io sono io' > f.txt",
        "openssl dgst -sha256 -sign priv.pem -out f.sig f.txt",
        "openssl dgst -sha256 -verify pub.pem -signature f.sig f.txt   (Verified OK)",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "Usare la crittografia bene", items=[
        "Non inventare algoritmi: usare standard collaudati (AES, RSA, curve ellittiche).",
        "La sicurezza sta nella chiave, non nel segreto dell'algoritmo (principio di "
        "Kerckhoffs).",
        "Chiavi lunghe, generate a caso, conservate al sicuro; la chiave privata non si "
        "condivide mai.",
        "In pratica si combinano: asimmetrica per scambiare in sicurezza una chiave "
        "simmetrica, poi simmetrica (veloce) per i dati. È quello che fa HTTPS, prossima "
        "lezione.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Il problema dello scambio della chiave', "La cifratura simmetrica è veloce ma ha un tallone d'Achille: come fai avere la chiave all'altra persona senza che qualcuno la intercetti? La cifratura asimmetrica risolve proprio questo. Un'idea elegante è lo scambio di Diffie-Hellman: due persone riescono a mettersi d'accordo su una chiave segreta comune scambiandosi solo informazioni pubbliche, in modo che chi ascolta non possa ricavarla. Nella pratica si combinano i due mondi: si usa l'asimmetrica (lenta) solo per concordare in sicurezza una chiave, poi si passa alla simmetrica (veloce) per cifrare i dati veri. Sulle dimensioni: una chiave RSA robusta è di 2048 o 4096 bit, mentre le curve ellittiche (ECC) offrono la stessa sicurezza con chiavi molto più corte. È esattamente ciò che fa HTTPS, il tema della prossima lezione."),
        ],
        sintesi=[
            "Cifrare è reversibile con la chiave giusta; l'hash no. Non vanno confusi.",
            'Cifratura simmetrica (AES): una sola chiave cifra e decifra; veloce, ma bisogna scambiare la chiave.',
            "Cifratura asimmetrica (RSA): coppia pubblica/privata; ciò che cifri con la pubblica apre solo con la privata.",
            "La firma digitale: firmi con la privata, tutti verificano con la pubblica (autenticità e non ripudio).",
            "La sicurezza sta nella chiave, non nel segreto dell'algoritmo (principio di Kerckhoffs).",
        ],
        glossario=[
            ('Cifratura simmetrica', 'stessa chiave per cifrare e decifrare (es. AES)'),
            ('Cifratura asimmetrica', 'coppia di chiavi pubblica/privata (es. RSA)'),
            ('Chiave pubblica/privata', "una si distribuisce, l'altra resta segreta"),
            ('Firma digitale', "prova che un messaggio viene da te e non è alterato"),
            ('openssl', 'strumento a riga di comando per crittografia'),
            ('Kerckhoffs', "principio: la sicurezza sta nella chiave, non nell'algoritmo segreto"),
        ],
        errori=[
            'Confondere cifratura (reversibile) e hash (a senso unico).',
            'Condividere la chiave privata: va tenuta segretissima.',
            'Inventare algoritmi propri invece di usare standard collaudati.',
            'Usare chiavi corte o prevedibili.',
        ],
        domande=[
            "Qual è la differenza tra cifrare e fare l'hash?",
            'Vantaggi e limiti della cifratura simmetrica?',
            'Come fa la cifratura asimmetrica a far ricevere segreti senza scambiare una chiave prima?',
            'Come funziona una firma digitale?',
            'Cosa dice il principio di Kerckhoffs?',
        ],
        collegamenti=[
            "Lezione 19: l'hash, da non confondere con la cifratura.",
            'Lezione 22: HTTPS/TLS, che combina simmetrica e asimmetrica.',
            "Lezione 23-24: perché il traffico cifrato non si legge sniffando.",
        ],
    )


    d.h2("Punteggio della Lezione 21")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Decifrare (simmetrico)", "openssl enc -d ... segreto.enc", "30"],
        ["Decifrare (asimmetrico)", "openssl pkeyutl -decrypt ... priv.pem", "40"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 21** · Cifratura simmetrica e asimmetrica (Blocco 5).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali (Lezione 2) con openssl. Nessun bersaglio.",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Distinguere hash e cifratura; simmetrica e asimmetrica.",
        "Usare openssl per AES e RSA e capire chiave pubblica/privata e firma.",
        "Preparare il terreno a HTTPS/TLS (Lezione 22).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh genera in `~/lab/lezione-21/`: `segreto.enc` (AES-256, passphrase "
        "`chiavesegreta`, contiene FLAG{decifrato_simmetrico}), la coppia `priv.pem`/"
        "`pub.pem`, e `messaggio.enc` (cifrato con la pubblica, contiene "
        "FLAG{la_chiave_privata_apre}). I plaintext temporanei vengono cancellati.",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "openssl enc -d -aes-256-cbc -pbkdf2 -in segreto.enc -pass pass:chiavesegreta",
         "FLAG{decifrato_simmetrico}"],
        ["2", "openssl pkeyutl -decrypt -inkey priv.pem -in messaggio.enc",
         "FLAG{la_chiave_privata_apre}"],
    ], widths=[700, 5626, 2700])
    d.p("Passphrase simmetrica: `chiavesegreta`. Le flag sono didattiche e in chiaro nel "
        "codice: qui la competenza è l'operazione di cifratura, non la segretezza del "
        "valore.")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["'bad decrypt'", "passphrase sbagliata: è `chiavesegreta`; serve `-pbkdf2`"],
        ["pkeyutl errore di padding", "usare il file `messaggio.enc` generato da `lab 21`"],
        ["voglio rigenerare tutto", "rilanciare `lab 21` (ricrea chiavi e cifrati)"],
    ], widths=[2600, 6426])
    d.h1("Nota tecnica")
    d.p("Comandi verificati con OpenSSL 3 (Kali). RSA cifra solo messaggi piccoli: la flag "
        "ci sta. Nella pratica reale si cifra una chiave simmetrica, non i dati: il "
        "concetto viene richiamato nella Lezione 22 (HTTPS/TLS).")
