# -*- coding: utf-8 -*-
NUM = 40
SLUG = "debrief-valutazione"
TITOLO = "Debrief, valutazione e difese apprese"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 30 min debrief · 60 min sintesi difese · 30 min valutazione.",
        "**Obiettivo:** tirare le somme del corso, commentare il CTF e consolidare la cosa "
        "piu' importante: per ogni attacco imparato, la difesa che lo ferma.",
        "**Al termine sai:** collegare ogni tecnica offensiva alla sua contromisura e "
        "portare a casa buone abitudini digitali.",
        "**Flag in palio:** 2 flag finali (70 punti).",
    ])

    d.h1("Parte 1 · Debrief del CTF (30 min)")
    d.p("Si ripercorrono insieme le sfide del CTF: cosa ha funzionato, dove ci si e' "
        "bloccati, quali trucchi sono serviti. Sbagliare e capire perche' e' il modo "
        "migliore per imparare. Ognuno racconta la sfida di cui va piu' fiero.")

    d.h1("Parte 2 · La mappa attacco-difesa (60 min)")
    d.p("Il filo di tutto il corso e' questo: abbiamo imparato ad attaccare per capire "
        "come si difende. Ecco la sintesi.")
    d.table(["Attacco imparato", "Difesa principale"], [
        ["SQL injection", "query parametrizzate (mai concatenare l'input)"],
        ["XSS", "escape dell'output; cookie HttpOnly; CSP"],
        ["Brute force", "rate limiting, lockout, password forti, 2FA"],
        ["Sniffing di rete", "cifrare tutto (HTTPS, SSH, VPN)"],
        ["ARP/DNS spoofing", "reti segmentate, switch gestiti, HTTPS"],
        ["Phishing", "controllare il dominio, 2FA, non fidarsi dei link"],
        ["Malware", "aggiornamenti, antivirus, backup staccati, minimo privilegio"],
        ["Password deboli/hash", "hash lenti e salati (bcrypt/Argon2), passphrase lunghe"],
        ["Servizi/porte esposti", "hardening: spegnere l'inutile, firewall"],
        ["Compromissione", "log e monitoraggio, incident response, backup"],
    ], widths=[3400, 5626])

    d.h2("Quiz finale: abbina le difese (+50)")
    d.p("Per ciascun attacco (in ordine: SQLi, XSS, brute force, sniffing, phishing) "
        "indica la difesa principale con la parola chiave.")
    d.code([
        "# parole chiave: parametrizzate  escape  ratelimiting  cifratura  dominio",
        "lab40-verifica difese <d1> <d2> <d3> <d4> <d5>",
    ])

    d.h2("Chiudi il corso (+20)")
    d.code(["lab40-verifica fine"])

    d.h1("Parte 3 · Le tue difese di tutti i giorni (30 min)")
    d.box("verde", "Cosa portare a casa", items=[
        "Password lunghe e diverse per ogni sito; usa un password manager.",
        "Attiva l'autenticazione a due fattori dove puoi.",
        "Aggiorna sistema e app: molte falle si chiudono solo cosi'.",
        "Diffida di link e allegati; controlla sempre il dominio.",
        "Fai backup e tienili staccati: e' la difesa contro il ransomware.",
        "Usa le tue nuove competenze solo per proteggere, mai per attaccare sistemi "
        "altrui: sarebbe un reato.",
    ])
    d.p("La sicurezza non e' un prodotto, e' un'abitudine. Avete imparato a pensare come "
        "un attaccante: usatelo per difendere voi stessi e gli altri.")

    d.h2("Punteggio della Lezione 40")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Quiz attacco-difesa", "lab40-verifica difese", "50"],
        ["Corso completato", "lab40-verifica fine", "20"],
    ], widths=[4000, 3526, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 40** · Debrief, valutazione e difese apprese (Blocco 10, chiusura del corso).",
        "**Tempi:** 30 min debrief · 60 min sintesi · 30 min valutazione.",
        "**Prerequisiti:** Kali (Lezione 2). Nessun bersaglio.",
        "**Deliverable studente:** 2 flag finali (70 punti).",
    ])
    d.h1("Obiettivi didattici")
    d.bullets([
        "Consolidare il filo conduttore: attaccare per capire come difendere.",
        "Fissare, per ogni attacco, la contromisura principale.",
        "Chiudere con buone abitudini digitali e un messaggio etico forte.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "kali.sh installa `lab40-verifica` con due comandi: `difese` (quiz di abbinamento) "
        "e `fine` (flag di completamento del corso).",
        "target.sh: nessuna azione.",
    ])
    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["Quiz", "difese: parametrizzate escape ratelimiting cifratura dominio",
         "FLAG{difensore_consapevole}"],
        ["Fine", "lab40-verifica fine", "FLAG{corso_completato}"],
    ], widths=[900, 5626, 2500])
    d.p("Ordine attacchi del quiz: SQLi, XSS, brute force, sniffing, phishing.")
    d.h1("Idee per la valutazione finale")
    d.bullets([
        "Somma dei punteggi CTF (L39) + partecipazione + questa autovalutazione.",
        "Chiedere a ciascuno una difesa che applichera' davvero nella propria vita digitale.",
        "Facoltativo: breve relazione su una sfida del CTF (come l'ha risolta).",
    ])
    d.h1("Chiusura del corso")
    d.p("Ribadire l'uso etico e legale delle competenze acquisite (art. 615-ter c.p. e "
        "collegati). Il patto etico firmato nella Lezione 2 resta valido: queste tecniche "
        "si usano per difendere, non per attaccare.")
