# -*- coding: utf-8 -*-
import comune
NUM = 22
SLUG = "https-tls-certificati"
TITOLO = "HTTPS e TLS: certificati e attacchi nel lab"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire cosa c'è dietro il lucchetto di HTTPS: il protocollo TLS, "
        "i certificati e le autorità di certificazione (CA), e perché un avviso sul "
        "certificato non va mai ignorato.",
        "**Al termine sai:** leggere un certificato con openssl, capire un certificato "
        "self-signed e la catena di fiducia, e cosa comporta bypassare i controlli.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Il lucchetto spiegato (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Quando digiti la password della banca su un sito, come fai a sapere che nessuno "
        "la sta leggendo per strada e che il sito è davvero quello vero e non un clone? "
        "La risposta è HTTPS: HTTP che viaggia dentro un tunnel cifrato (TLS). Il "
        "lucchetto del browser dice due cose: il traffico è cifrato, e l'identità del "
        "sito è garantita da un certificato.")

    d.h2("Come nasce il tunnel")
    d.p("TLS mette insieme le due cifrature della lezione scorsa: usa quella asimmetrica "
        "(le chiavi del certificato) per accordarsi in sicurezza su una chiave "
        "simmetrica, poi usa quella simmetrica (veloce) per cifrare tutto il traffico. "
        "Così ottiene sicurezza e velocità insieme.")

    d.h2("Il certificato e la catena di fiducia")
    d.p("Il certificato è come una carta d'identità del sito: dice chi è e contiene la "
        "sua chiave pubblica. Ma chi garantisce che sia autentico? Una autorità di "
        "certificazione (CA) lo firma. Il browser si fida di una lista di CA note; se il "
        "certificato è firmato da una di loro, il lucchetto è verde. Se è "
        "'self-signed' (firmato da se stesso, come nel nostro lab) nessuna CA lo "
        "garantisce e il browser avvisa.")

    d.h1("Parte 2 · Guarda dentro il lucchetto (pratica, 80 min)")
    d.p("Sul bersaglio `lab 22` avvia un sito HTTPS con certificato self-signed su :8443.")

    d.h2("Passo 1 · Leggi il certificato (+35)")
    d.p("Con openssl ti colleghi e leggi la carta d'identità del server.")
    d.code([
        "echo | openssl s_client -connect 10.10.10.20:8443 2>/dev/null \\",
        "  | openssl x509 -noout -subject -issuer -dates",
    ])
    d.p("Guarda il campo OU (Organizational Unit) del subject: c'è la prima flag. Nota "
        "anche che issuer e subject coincidono: è il segno di un certificato self-signed.")

    d.h2("Passo 2 · Scarica la pagina (+35)")
    d.p("Prova prima senza ignorare i controlli, poi ignorandoli.")
    d.code([
        "curl https://10.10.10.20:8443/        # errore: certificato non fidato",
        "curl -k https://10.10.10.20:8443/     # -k salta il controllo: ecco la flag",
    ])
    d.box("rosso", "Attenzione al -k", items=[
        "Il primo curl fallisce apposta: sta proteggendoti da un certificato non garantito.",
        "`-k` (o 'accetta il rischio' nel browser) salta il controllo: nel lab è comodo, "
        "nella vita reale espone a un attacco man-in-the-middle (lo vedremo nel Blocco 6).",
        "Un avviso sul certificato NON va mai ignorato su siti veri.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "HTTPS fatto bene", items=[
        "Certificati validi, emessi da una CA (oggi gratis con Let's Encrypt): niente "
        "self-signed su siti pubblici.",
        "Solo versioni recenti di TLS; niente protocolli vecchi e bucati (SSL, TLS 1.0).",
        "HSTS: dire al browser di usare sempre HTTPS, mai HTTP.",
        "Educare gli utenti: un avviso sul certificato è un allarme, non un fastidio da "
        "cliccare via.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ('Il handshake TLS, passo per passo (semplificato)', "Quando apri un sito HTTPS, prima di scambiare qualunque dato avviene una stretta di mano. Il tuo browser dice 'ciao, ecco le versioni di TLS e gli algoritmi che conosco'. Il server risponde scegliendo l'algoritmo e inviando il suo certificato, che contiene la chiave pubblica e l'identità, firmato da una CA. Il browser verifica quella firma risalendo alla catena di CA di cui si fida: se non torna, scatta l'avviso. A quel punto le due parti concordano (usando l'asimmetrica) una chiave simmetrica di sessione e da lì in poi tutto il traffico viaggia cifrato con quella, veloce. Capire questi passaggi spiega perché un certificato self-signed fa avvisare il browser (nessuna CA lo garantisce) e perché ignorare quell'avviso apre la porta a un man-in-the-middle."),
        ],
        sintesi=[
            "HTTPS è HTTP dentro un tunnel cifrato (TLS): riservatezza del traffico e identità del sito.",
            "TLS usa l'asimmetrica per scambiare in sicurezza una chiave simmetrica, poi la simmetrica per i dati.",
            "Il certificato è la carta d'identità del sito, firmata da una CA di cui il browser si fida.",
            "Un certificato self-signed non è garantito da nessuna CA: il browser avvisa (giustamente).",
            "Un avviso sul certificato non va MAI ignorato: è il segnale di un possibile MITM.",
        ],
        glossario=[
            ('TLS/SSL', 'il protocollo che cifra il traffico (la S di HTTPS)'),
            ('Certificato', "documento con l'identità e la chiave pubblica del sito"),
            ('CA', "Certificate Authority: l'ente che firma e garantisce i certificati"),
            ('Self-signed', 'certificato firmato da se stesso, non garantito da una CA'),
            ('Catena di fiducia', 'il browser si fida delle CA, che garantiscono i siti'),
            ('HSTS', 'regola che impone al browser di usare sempre HTTPS'),
        ],
        errori=[
            "Ignorare l'avviso del browser sul certificato ('accetta il rischio').",
            'Usare curl -k su siti reali: salta il controllo del certificato.',
            'Usare certificati self-signed su siti pubblici.',
            'Tenere versioni vecchie e bucate di TLS/SSL.',
        ],
        domande=[
            'Cosa garantisce il lucchetto di HTTPS, oltre alla cifratura?',
            'Come fa TLS a unire i vantaggi di simmetrica e asimmetrica?',
            "Cos'è una CA e cosa cambia con un certificato self-signed?",
            "Perché un avviso sul certificato è un allarme e non un fastidio?",
            "Cosa fa curl -k e perché è pericoloso fuori dal lab?",
        ],
        collegamenti=[
            'Lezione 21: le due cifrature che TLS mette insieme.',
            'Lezione 25-26: il MITM da cui HTTPS (con certificato valido) protegge.',
            "Lezione 29-30: perché controllare dominio e lucchetto sventa il phishing.",
        ],
    )


    d.h2("Punteggio della Lezione 22")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Leggere il certificato", "openssl s_client + x509 (campo OU)", "35"],
        ["Scaricare via HTTPS", "curl -k su :8443", "35"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 22** · HTTPS e TLS, certificati (Blocco 5, chiusura).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** bersaglio acceso; Python3 e openssl (presenti).",
        "**Deliverable studente:** 2 flag (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Capire TLS, certificati, CA e catena di fiducia.",
        "Leggere un certificato con openssl e riconoscere un self-signed.",
        "Capire il rischio di ignorare gli avvisi (ponte verso il MITM del Blocco 6).",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh genera un certificato self-signed con FLAG{certificato_letto} nel campo "
        "OU e avvia `lab22-https.service`: un server HTTPS (stdlib ssl) su :8443 che serve "
        "FLAG{https_ignora_il_lucchetto}.",
        "kali.sh: briefing con i comandi openssl e curl.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "openssl s_client -connect :8443 | openssl x509 -subject (campo OU)",
         "FLAG{certificato_letto}"],
        ["2", "curl -k https://10.10.10.20:8443/", "FLAG{https_ignora_il_lucchetto}"],
    ], widths=[700, 5926, 2400])
    d.p("Le flag sono didattiche e in chiaro (la competenza è leggere il certificato e "
        "capire il -k, non la segretezza).")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["curl senza -k fallisce", "è voluto: certificato self-signed non fidato"],
        [":8443 non risponde", "`systemctl status lab22-https`; rilanciare `lab 22`"],
        ["s_client non mostra l'OU", "aggiungere `| openssl x509 -noout -subject`"],
        ["rigenerare il certificato", "`rm /opt/lab/lab22/cert.pem` e rilanciare `lab 22`"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("Chiude il Blocco 5. Il collegamento con la Lezione 21 è esplicito: TLS usa "
        "asimmetrico per scambiare una chiave simmetrica. L'avviso sul certificato "
        "prepara il tema del man-in-the-middle (Blocco 6).")
