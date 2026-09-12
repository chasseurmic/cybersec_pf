# -*- coding: utf-8 -*-
NUM = 22
SLUG = "https-tls-certificati"
TITOLO = "HTTPS e TLS: certificati e attacchi nel lab"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire cosa c'e' dietro il lucchetto di HTTPS: il protocollo TLS, "
        "i certificati e le autorita' di certificazione (CA), e perche' un avviso sul "
        "certificato non va mai ignorato.",
        "**Al termine sai:** leggere un certificato con openssl, capire un certificato "
        "self-signed e la catena di fiducia, e cosa comporta bypassare i controlli.",
        "**Flag in palio:** 2 flag (70 punti).",
    ])

    d.h1("Parte 1 · Il lucchetto spiegato (teoria, 25 min)")
    d.h2("Il caso reale")
    d.p("Quando digiti la password della banca su un sito, come fai a sapere che nessuno "
        "la sta leggendo per strada e che il sito e' davvero quello vero e non un clone? "
        "La risposta e' HTTPS: HTTP che viaggia dentro un tunnel cifrato (TLS). Il "
        "lucchetto del browser dice due cose: il traffico e' cifrato, e l'identita' del "
        "sito e' garantita da un certificato.")

    d.h2("Come nasce il tunnel")
    d.p("TLS mette insieme le due cifrature della lezione scorsa: usa quella asimmetrica "
        "(le chiavi del certificato) per accordarsi in sicurezza su una chiave "
        "simmetrica, poi usa quella simmetrica (veloce) per cifrare tutto il traffico. "
        "Cosi' ottiene sicurezza e velocita' insieme.")

    d.h2("Il certificato e la catena di fiducia")
    d.p("Il certificato e' come una carta d'identita' del sito: dice chi e' e contiene la "
        "sua chiave pubblica. Ma chi garantisce che sia autentico? Una autorita' di "
        "certificazione (CA) lo firma. Il browser si fida di una lista di CA note; se il "
        "certificato e' firmato da una di loro, il lucchetto e' verde. Se e' "
        "'self-signed' (firmato da se stesso, come nel nostro lab) nessuna CA lo "
        "garantisce e il browser avvisa.")

    d.h1("Parte 2 · Guarda dentro il lucchetto (pratica, 80 min)")
    d.p("Sul bersaglio `lab 22` avvia un sito HTTPS con certificato self-signed su :8443.")

    d.h2("Passo 1 · Leggi il certificato (+35)")
    d.p("Con openssl ti colleghi e leggi la carta d'identita' del server.")
    d.code([
        "echo | openssl s_client -connect 10.10.10.20:8443 2>/dev/null \\",
        "  | openssl x509 -noout -subject -issuer -dates",
    ])
    d.p("Guarda il campo OU (Organizational Unit) del subject: c'e' la prima flag. Nota "
        "anche che issuer e subject coincidono: e' il segno di un certificato self-signed.")

    d.h2("Passo 2 · Scarica la pagina (+35)")
    d.p("Prova prima senza ignorare i controlli, poi ignorandoli.")
    d.code([
        "curl https://10.10.10.20:8443/        # errore: certificato non fidato",
        "curl -k https://10.10.10.20:8443/     # -k salta il controllo: ecco la flag",
    ])
    d.box("rosso", "Attenzione al -k", items=[
        "Il primo curl fallisce apposta: sta proteggendoti da un certificato non garantito.",
        "`-k` (o 'accetta il rischio' nel browser) salta il controllo: nel lab e' comodo, "
        "nella vita reale espone a un attacco man-in-the-middle (lo vedremo nel Blocco 6).",
        "Un avviso sul certificato NON va mai ignorato su siti veri.",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.box("verde", "HTTPS fatto bene", items=[
        "Certificati validi, emessi da una CA (oggi gratis con Let's Encrypt): niente "
        "self-signed su siti pubblici.",
        "Solo versioni recenti di TLS; niente protocolli vecchi e bucati (SSL, TLS 1.0).",
        "HSTS: dire al browser di usare sempre HTTPS, mai HTTP.",
        "Educare gli utenti: un avviso sul certificato e' un allarme, non un fastidio da "
        "cliccare via.",
    ])

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
    d.p("Le flag sono didattiche e in chiaro (la competenza e' leggere il certificato e "
        "capire il -k, non la segretezza).")
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["curl senza -k fallisce", "e' voluto: certificato self-signed non fidato"],
        [":8443 non risponde", "`systemctl status lab22-https`; rilanciare `lab 22`"],
        ["s_client non mostra l'OU", "aggiungere `| openssl x509 -noout -subject`"],
        ["rigenerare il certificato", "`rm /opt/lab/lab22/cert.pem` e rilanciare `lab 22`"],
    ], widths=[2800, 6226])
    d.h1("Nota didattica")
    d.p("Chiude il Blocco 5. Il collegamento con la Lezione 21 e' esplicito: TLS usa "
        "asimmetrico per scambiare una chiave simmetrica. L'avviso sul certificato "
        "prepara il tema del man-in-the-middle (Blocco 6).")
