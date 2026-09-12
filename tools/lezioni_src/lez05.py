# -*- coding: utf-8 -*-
NUM = 5
SLUG = "utenti-gruppi-processi-servizi"
TITOLO = "Utenti, gruppi, processi e servizi"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** capire chi comanda su una macchina Linux (utenti e gruppi), cosa "
        "sta girando (processi) e cosa è esposto (servizi e porte), imparando a "
        "enumerare come fa un attaccante appena ottenuto un accesso.",
        "**Al termine sai:** leggere `/etc/passwd`, usare `id`, `ps`, `ss`, `systemctl` e "
        "`sudo -l`, e riconoscere le tre debolezze classiche: utenti di troppo, "
        "credenziali nei processi, servizi dimenticati.",
        "**Flag in palio:** 4 flag (70 punti).",
    ])

    d.h1("Parte 1 · Chi comanda qui (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Un attaccante ottiene una shell su un server con un account qualunque. La prima "
        "cosa che fa non è attaccare: è guardarsi intorno. Chi sono io? Chi altri esiste "
        "su questa macchina? Cosa sta girando adesso? Cosa è in ascolto sulla rete? "
        "Questa fase si chiama enumerazione, ed è quella che decide tutto: quasi sempre "
        "la strada per diventare amministratore è già lì, in un servizio dimenticato, "
        "in una password scritta male, in una regola di sistema troppo generosa.")

    d.h2("Utenti e gruppi")
    d.p("Ogni utente ha un numero (UID). L'amministratore, root, ha UID 0: può fare "
        "tutto. Gli altri utenti hanno permessi limitati. I gruppi servono a dare gli "
        "stessi permessi a più persone insieme.")
    d.code([
        "whoami          # il tuo nome utente",
        "id              # UID, GID e gruppi a cui appartieni",
        "cat /etc/passwd # elenco di TUTTI gli utenti del sistema",
    ])
    d.p("Ogni riga di `/etc/passwd` ha 7 campi separati da `:` (nome, x, UID, GID, "
        "commento, home, shell). Le password vere non sono qui: stanno in `/etc/shadow`, "
        "leggibile solo da root. Un dettaglio che tradisce: un utente di servizio "
        "dovrebbe avere shell `/usr/sbin/nologin`; se ne ha una di login (`/bin/bash`), "
        "è un campanello d'allarme.")
    d.cmdref([
        ("`whoami`", "Il nome dell'utente con cui sei collegato."),
        ("`id`", "UID, GID e gruppi a cui appartieni (quanti poteri hai)."),
        ("`cat /etc/passwd`", "Elenco di tutti gli utenti (7 campi separati da `:`)."),
        ("`getent passwd`", "Come sopra, ma include anche utenti da fonti esterne; comodo "
                            "con i filtri, es. `getent passwd | grep -v nologin`."),
    ])

    d.h2("Processi")
    d.p("Un processo è un programma in esecuzione, con un numero (PID). `ps aux` li "
        "elenca tutti, con l'intera riga di comando che li ha avviati. E qui c'è una "
        "trappola classica: se un programma viene lanciato con la password scritta tra "
        "gli argomenti, chiunque può leggerla con `ps`.")
    d.code([
        "ps aux              # tutti i processi, con la riga di comando completa",
        "ps aux | grep -i pass   # cerca eventuali password negli argomenti",
        "top                 # processi in tempo reale (q per uscire)",
    ])
    d.cmdref([
        ("`ps aux`", "Elenca tutti i processi (`a` tutti gli utenti, `u` formato "
                     "leggibile, `x` anche quelli senza terminale). La 2a colonna è il PID."),
        ("`top`", "Processi in tempo reale, ordinati per uso di CPU. `q` per uscire."),
        ("`pgrep`", "Trova il PID di un processo dal nome. `-f` cerca nell'intera riga di "
                    "comando, es. `pgrep -f finto-daemon`."),
    ])

    d.h2("Servizi e porte")
    d.p("Un servizio è un programma che parte da solo e resta in ascolto (per esempio "
        "un server web). `systemctl` gestisce i servizi; `ss` mostra le porte aperte. Una "
        "porta aperta che nessuno ricorda è una porta d'ingresso in più per chi attacca.")
    d.code([
        "systemctl status ssh     # stato di un servizio",
        "ss -tlnp                 # porte TCP in ascolto e chi le tiene",
        "sudo -l                  # cosa posso eseguire come root",
    ])
    d.cmdref([
        ("`systemctl`", "Gestisce i servizi. `systemctl status <nome>` mostra lo stato; "
                        "accetta anche un PID: `systemctl status <PID>` dice a quale "
                        "servizio appartiene un processo."),
        ("`ss`", "Mostra le connessioni di rete. `-t` TCP, `-l` in ascolto, `-n` numeri "
                 "(niente risoluzione dei nomi), `-p` il processo che tiene la porta. "
                 "Insieme: `ss -tlnp`."),
        ("`sudo -l`", "Elenca cosa il tuo utente può eseguire come root: una regola troppo "
                      "larga qui è una via per l'escalation dei privilegi."),
    ])

    d.h1("Parte 2 · Enumerazione sul bersaglio (pratica, 80 min)")
    d.p("Il docente lancia `lab 5` sul bersaglio, poi sulla Kali `lab 5` mostra la "
        "missione. Entra nel bersaglio via SSH e vai a caccia delle quattro debolezze.")
    d.code(["ssh studente@10.10.10.20        # password: studente"])

    d.h2("Passo 1 · L'utente di troppo (+15)")
    d.p("Elenca gli utenti e cerca quello che non dovrebbe avere una shell di login. Il "
        "suo campo commento nasconde la flag.")
    d.code([
        "cat /etc/passwd | column -t -s:",
        "grep bash /etc/passwd            # chi ha /bin/bash",
        "grep backup /etc/passwd          # guarda il campo commento",
    ])
    d.cmdref([
        ("`column`", "Incolonna un testo per renderlo leggibile. `-t` crea la tabella, "
                     "`-s:` usa i due punti come separatore (utile per /etc/passwd)."),
        ("`grep`", "Filtra le righe che contengono una parola. `-i` ignora maiuscole, "
                   "`-v` mostra le righe che NON la contengono."),
    ])

    d.h2("Passo 2 · La password nel processo (+20)")
    d.p("Un finto demone è stato avviato con la password tra gli argomenti. Prima "
        "trovala; poi risali dal processo al servizio che lo ha avviato.")
    d.code([
        "ps aux | grep -i pass          # trovi il processo e il suo PID (2a colonna)",
    ])
    d.p("`ps` ti mostra il programma (`/usr/local/bin/finto-daemon`) e il suo PID, ma non "
        "il nome del servizio. Per arrivarci il percorso è: processo, poi PID, poi unità "
        "systemd.")
    d.code([
        "systemctl status <PID>         # systemctl risale all'unità partendo dal PID",
        "# scorciatoia (trova il PID da solo):",
        "systemctl status \"$(pgrep -f finto-daemon | head -1)\"",
    ])
    d.p("In alternativa, cerca chi lo lancia nei file dei servizi: chi avvia un programma "
        "lo nomina nel proprio `ExecStart`.")
    d.code([
        "grep -rl finto-daemon /etc/systemd/system/    # ti indica lab05-daemon.service",
        "systemctl status lab05-daemon                 # ora sai il nome",
    ])
    d.box("blu", "Dal processo al servizio", intro=(
        "Tre modi per sapere quale unità systemd ha avviato un processo:"), items=[
        "`systemctl status <PID>`: systemctl conosce l'unità di ogni processo che ha avviato.",
        "`grep -rl <programma> /etc/systemd/system/`: trova il file del servizio che lo lancia.",
        "`cat /proc/<PID>/cgroup`: contiene il percorso ...system.slice/<servizio>.service.",
    ])

    d.h2("Passo 3 · La porta dimenticata (+15)")
    d.p("Cerca le porte in ascolto: una ha un numero strano (31337). Interrogala.")
    d.code([
        "ss -tlnp | grep 31337",
        "curl http://localhost:31337",
    ])

    d.h2("Passo 4 · Il sudo troppo generoso (+20)")
    d.p("Chiedi al sistema cosa puoi eseguire come root senza password. Poi fallo.")
    d.code([
        "sudo -l",
        "sudo /usr/local/bin/lab05-flag",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("Ogni flag di oggi era un errore di configurazione, non un exploit. Il difensore "
        "chiude proprio queste porte.")
    d.box("verde", "Le contromisure", items=[
        "Utenti di servizio con shell `nologin`; niente account dimenticati con "
        "password deboli.",
        "Mai passare password come argomenti: usare file protetti, variabili d'ambiente "
        "o segreti gestiti dal sistema.",
        "Spegnere i servizi che non servono e chiudere le porte inutili (`systemctl "
        "disable`, firewall).",
        "Regole sudo minime e specifiche: `sudo -l` non deve mai regalare troppo.",
    ])
    d.code([
        "# dal lato difensore: cosa è esposto e chi può diventare root",
        "ss -tlnp                       # porte aperte, da rivedere una a una",
        "getent passwd | grep -v nologin | grep -v false   # chi può fare login",
        "find / -perm -4000 -type f 2>/dev/null             # programmi SUID (poteri di root)",
    ])

    d.h2("Punteggio della Lezione 5")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Utente di troppo", "/etc/passwd, campo commento", "15"],
        ["Password nel processo", "ps aux | grep", "20"],
        ["Porta dimenticata", "ss -tlnp ; curl :31337", "15"],
        ["Sudo troppo generoso", "sudo -l ; sudo lab05-flag", "20"],
    ], widths=[3800, 3726, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 5** · Utenti, gruppi, processi e servizi (Blocco 2).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** ambiente Lezione 2 attivo; accesso ospite SSH (ricreato dal lab).",
        "**Deliverable studente:** 4 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Introdurre l'enumerazione post-accesso: utenti, processi, servizi, privilegi.",
        "Riconoscere tre errori reali: account di troppo, credenziali nei processi, "
        "servizi/porte dimenticati, più una regola sudo troppo larga.",
        "Usare systemctl e ss come strumenti sia offensivi sia difensivi.",
    ])

    d.h1("Come funziona il lab")
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Ricrea l'utente ospite `studente` e SSH a password.",
        "Crea `webadmin` (nologin, esca innocua) e `backup_old` (shell bash + flag nel "
        "campo commento GECOS).",
        "Installa `/usr/local/bin/finto-daemon` e il servizio `lab05-daemon.service`, "
        "avviato con `--password=FLAG{...}` (visibile con ps aux).",
        "Avvia `lab05-porta.service`: un `python3 -m http.server` sulla porta 31337 che "
        "serve la flag 3.",
        "Installa `/usr/local/bin/lab05-flag` e la regola `/etc/sudoers.d/lab05` "
        "(validata con `visudo -cf`) che consente allo studente di eseguirlo come root.",
    ])
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Briefing di sola lettura: comandi di autoconoscenza e missione; verifica SSH.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Comando risolutivo", "Flag"], [
        ["1", "grep backup /etc/passwd (leggere il campo commento)", "FLAG{utente_di_troppo}"],
        ["2", "ps aux | grep -i pass ; poi systemctl status <PID> (o grep -rl finto-daemon "
         "/etc/systemd/system/) per risalire a lab05-daemon", "FLAG{la_password_e_nel_processo}"],
        ["3", "ss -tlnp | grep 31337 ; curl localhost:31337", "FLAG{una_porta_dimenticata}"],
        ["4", "sudo -l ; sudo /usr/local/bin/lab05-flag", "FLAG{sudo_apre_le_porte}"],
    ], widths=[900, 5626, 2500])

    d.h1("Mappa di cosa è seminato dove")
    d.table(["Elemento", "Dettaglio"], [
        ["utente backup_old", "shell /bin/bash, GECOS con la flag 1, password backup_old"],
        ["utente webadmin", "nologin, distrattore innocuo"],
        ["lab05-daemon.service", "ExecStart con --password=FLAG{...} (flag 2)"],
        ["lab05-porta.service", "http.server su :31337, /opt/lab/porta/index.html (flag 3)"],
        ["/etc/sudoers.d/lab05", "NOPASSWD su /usr/local/bin/lab05-flag (flag 4)"],
    ], widths=[2800, 6226])

    d.h1("Rigiocare e resettare")
    d.bullets([
        "Rilanciare `lab 5` sul bersaglio: ricrea utenti, servizi e regola sudo (idempotente).",
        "Per fermare tutto a fine blocco: `systemctl disable --now lab05-daemon "
        "lab05-porta` e `rm -f /etc/sudoers.d/lab05`.",
    ])

    d.h1("Troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["`ss` non c'è", "installare `iproute2` (di norma presente); in alternativa "
         "`netstat -tlnp`"],
        ["porta 31337 non risponde", "`systemctl status lab05-porta`; se fallisce, "
         "verificare che python3 sia presente (lo è su Ubuntu Server)"],
        ["`sudo -l` non mostra la regola", "controllare `/etc/sudoers.d/lab05` e che "
         "`visudo -cf` la validi; rilanciare `lab 5`"],
        ["ps non mostra il demone", "`systemctl restart lab05-daemon`"],
    ], widths=[2800, 6226])

    d.h1("Nota di sicurezza")
    d.p("La regola sudo è volutamente insicura ma limitata a un solo comando innocuo "
        "(stampa una flag). Resta confinata al bersaglio isolato. A fine corso conviene "
        "rimuoverla come mostrato sopra.")
