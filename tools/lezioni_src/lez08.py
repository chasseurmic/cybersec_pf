# -*- coding: utf-8 -*-
import comune
NUM = 8
SLUG = "scoperta-host-rete-locale"
TITOLO = "Scoperta host e rete locale (ping sweep, ARP)"


def dispensa(d):
    d.box("blu", "In breve", [
        "**Durata:** 2 ore.  Struttura: 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Obiettivo:** scoprire chi è collegato alla rete locale, con gli strumenti "
        "veri (nmap) e capendo il meccanismo dell'ARP, il protocollo che lega gli "
        "indirizzi IP alle schede di rete.",
        "**Al termine sai:** fare host discovery con `nmap -sn`, leggere la cache ARP con "
        "`ip neigh`, e capire perché l'ARP scopre host anche quando il ping viene "
        "ignorato.",
        "**Flag in palio:** 3 flag (70 punti).",
    ])

    d.h1("Parte 1 · Chi c'è sulla rete (teoria, 25 min)")

    d.h2("Il caso reale")
    d.p("Un attaccante che entra in una rete aziendale (una presa di rete lasciata "
        "libera, una wifi violata) per prima cosa vuole la mappa: quanti computer ci "
        "sono, che indirizzi hanno, chi è un server e chi un PC. Questa mappa è la base "
        "di tutto quello che viene dopo. Nella Lezione 6 ci siamo costruiti uno scanner a "
        "mano; oggi usiamo lo strumento professionale, nmap, e capiamo cosa succede sotto.")

    d.h2("Due modi di scoprire un host")
    d.table(["Metodo", "Come funziona", "Limite"], [
        ["Ping (ICMP)", "chiedo 'ci sei?' a un IP e aspetto la risposta",
         "un host può ignorare il ping (firewall)"],
        ["ARP", "sulla rete locale chiedo 'chi ha questo IP?' e la scheda risponde col MAC",
         "funziona solo nella stessa rete locale (non oltre il router)"],
    ], widths=[1600, 4926, 2500])
    d.p("L'ARP è più affidabile del ping in una rete locale: un computer può decidere "
        "di non rispondere al ping, ma se vuole comunicare deve rispondere all'ARP, "
        "altrimenti nessuno riesce a parlargli. Per questo, sulla rete locale, nmap usa "
        "l'ARP in automatico quando lo lanci come root.")

    d.h2("Cos'è l'ARP, in una riga")
    d.p("Ogni scheda di rete ha un indirizzo fisico unico, il MAC (per esempio "
        "`08:00:27:ab:cd:ef`). Gli IP cambiano, il MAC no. L'ARP (Address Resolution "
        "Protocol) traduce un IP nel MAC corrispondente, e il computer tiene una piccola "
        "rubrica di queste traduzioni: la cache ARP, che leggi con `ip neigh`.")

    d.h1("Parte 2 · Mappa la rete del laboratorio (pratica, 80 min)")
    d.p("La rete interna è `10.10.10.0/24` (gli indirizzi da `10.10.10.1` a "
        "`10.10.10.254`). Sul bersaglio `lab 8` garantisce che sia raggiungibile; sulla "
        "Kali `lab 8` installa il verificatore e mostra la missione.")

    d.h2("Passo 1 · Scoperta host con nmap (+20)")
    d.p("Il flag `-sn` dice a nmap: scopri chi è vivo, senza scansionare le porte.")
    d.code([
        "sudo nmap -sn 10.10.10.0/24",
        "lab08-verifica scoperta",
    ])
    d.p("Nell'output vedrai gli host up con il loro MAC. Dovresti trovare la tua Kali "
        "(`.5`) e il bersaglio (`.20`).")

    d.h2("Passo 2 · Il MAC del bersaglio via ARP (+30)")
    d.p("Pinga una volta il bersaglio per popolare la cache ARP, poi leggila.")
    d.code([
        "ping -c1 10.10.10.20",
        "ip neigh show 10.10.10.20        # riga con lladdr <MAC>",
        "lab08-verifica mac <il-MAC-che-hai-letto>",
    ])

    d.h2("Passo 3 · Quanti host vivi? (+20)")
    d.p("Conta gli host up. Un modo veloce: filtra le righe di report di nmap.")
    d.code([
        "sudo nmap -sn 10.10.10.0/24 | grep -c 'Nmap scan report'",
        "lab08-verifica conta <numero>",
    ])

    d.h1("Parte 3 · Ribaltamento difensivo (15 min)")
    d.p("La scoperta host è rumorosa: un solo indirizzo che in due secondi tocca "
        "centinaia di IP è un segnale chiaro. Chi difende lo nota e reagisce.")
    d.box("verde", "Difendersi dalla mappatura", items=[
        "Monitorare la rete: un IP che fa ARP o ping verso tutta la sottorete è sospetto.",
        "Ignorare il ping abbassa un po' la visibilità, ma l'ARP resta: la vera difesa è "
        "la segmentazione (dividere la rete in parti isolate).",
        "Sistemi di rilevamento (IDS) e switch gestiti possono accorgersi di scansioni e "
        "di ARP anomali; lo vedremo nel blocco sulle difese di rete.",
    ])
    comune.studio(
        d,
        approfondimenti=[
            ("ARP, MAC e IP: chi è chi sulla rete locale", "Ogni scheda di rete ha due indirizzi: uno fisico e permanente, il MAC (es. 08:00:27:ab:cd:ef), e uno logico e mutevole, l'IP. Sulla rete locale i computer si trovano tramite il MAC, non l'IP: quando uno vuole parlare con 10.10.10.20, chiede in broadcast 'chi ha questo IP?' e la scheda giusta risponde col proprio MAC. Questo è l'ARP, e la coppia IP-MAC finisce nella cache ARP (ip neigh). È anche il motivo per cui l'ARP funziona solo dentro la stessa rete locale: oltre il router si ragiona solo per IP. Capire questa differenza è la base sia della scoperta host di oggi sia degli attacchi di spoofing che vedremo nel blocco di rete."),
        ],
        sintesi=[
            "La scoperta host mappa chi è vivo in una rete; è la base di tutto ciò che segue.",
            "Due metodi: ping (ICMP), che un host può ignorare, e ARP, che sulla rete locale è più affidabile.",
            'nmap -sn fa host discovery; sulla rete locale, da root, usa ARP e mostra anche i MAC.',
            "L'ARP lega IP e MAC; la cache si legge con ip neigh dopo un ping.",
            "Una scansione è rumorosa: un IP che tocca centinaia di indirizzi salta all'occhio.",
        ],
        glossario=[
            ('Host discovery', 'scoprire quali indirizzi sono attivi in una rete'),
            ('ICMP / ping', "protocollo e comando per verificare la raggiungibilità"),
            ('ARP', 'protocollo che traduce un IP nel MAC corrispondente sulla LAN'),
            ('Indirizzo MAC', 'identificativo fisico e unico di una scheda di rete'),
            ('Cache ARP', "la 'rubrica' IP-MAC del sistema (ip neigh)"),
            ('/24', 'notazione CIDR: 24 bit di rete, 254 host utilizzabili (10.10.10.1-254)'),
            ('nmap -sn', 'scansione di sola scoperta host, senza scansione delle porte'),
        ],
        errori=[
            'Lanciare nmap -sn senza sudo e non ottenere i MAC (niente ARP).',
            "Leggere ip neigh senza aver prima pingato l'host (cache vuota).",
            "Pensare che ignorare il ping renda un host invisibile: l'ARP lo scopre lo stesso.",
            'Copiare male il MAC (scambiare 0 e O, aggiungere spazi).',
        ],
        domande=[
            "Perché l'ARP è più affidabile del ping sulla rete locale?",
            'Cosa significa /24 e quanti host utilizzabili contiene?',
            'Come leggi il MAC di un host dalla tua macchina?',
            "Perché nmap -sn richiede i privilegi di root per usare l'ARP?",
            'Come contrasta un difensore la mappatura della rete?',
        ],
        collegamenti=[
            'Lezione 6: il ping sweep artigianale in bash, qui fatto con nmap.',
            'Lezione 9: dopo gli host, la scoperta delle porte.',
            "Lezione 25: l'ARP sfruttato in modo offensivo (spoofing e MITM).",
        ],
    )


    d.h2("Punteggio della Lezione 8")
    d.table(["Obiettivo", "Come", "Punti"], [
        ["Scoperta host", "nmap -sn ; lab08-verifica scoperta", "20"],
        ["MAC via ARP", "ip neigh ; lab08-verifica mac", "30"],
        ["Conteggio host", "nmap -sn | grep -c ; lab08-verifica conta", "20"],
    ], widths=[3400, 4126, 1500])


def manuale(d):
    d.box("blu", "Scheda docente", [
        "**Lezione 8** · Scoperta host e rete locale (Blocco 3, Reconnaissance).",
        "**Tempi:** 25 min teoria · 80 min pratica · 15 min difesa.",
        "**Prerequisiti:** Kali e bersaglio sulla stessa rete interna `labnet`.",
        "**Deliverable studente:** 3 flag (70 punti).",
    ])

    d.h1("Obiettivi didattici")
    d.bullets([
        "Passare dallo scanner artigianale (L6) allo strumento professionale nmap.",
        "Capire ARP e la differenza tra scoperta L3 (ping) e L2 (ARP).",
        "Leggere la cache ARP e collegarla al concetto di MAC.",
    ])

    d.h1("Come funziona il lab")
    d.h2("kali.sh (sulla Kali)")
    d.bullets([
        "Installa `/usr/local/bin/lab08-verifica` con tre sottocomandi (scoperta, mac, "
        "conta). Non richiede root: usa `ping` e `ip neigh`, così funziona anche se lo "
        "studente lo lancia senza sudo.",
        "Mostra la missione (nmap -sn, ip neigh, conteggio).",
    ])
    d.h2("target.sh (sul bersaglio)")
    d.bullets([
        "Lezione lato Kali: il target garantisce solo di rispondere in rete (ping/ARP) e "
        "stampa il proprio IP e MAC per riferimento del docente.",
    ])

    d.h1("Soluzioni e valori delle flag")
    d.table(["Passo", "Soluzione", "Flag"], [
        ["1", "sudo nmap -sn 10.10.10.0/24 ; lab08-verifica scoperta", "FLAG{host_vivo_trovato}"],
        ["2", "ping -c1 10.10.10.20 ; ip neigh show 10.10.10.20 ; lab08-verifica mac <MAC>",
         "FLAG{arp_rivela_il_mac}"],
        ["3", "conteggio host up (di norma 2) ; lab08-verifica conta 2", "FLAG{quanti_siamo_in_rete}"],
    ], widths=[900, 5626, 2500])
    d.p("Nota: sulla `labnet` con due VM il conteggio corretto è 2 (Kali + bersaglio). "
        "Se il docente aggiunge altre VM alla rete interna, il verificatore ricalcola da "
        "solo il numero atteso (fa un ping sweep interno), quindi resta coerente.")

    d.h1("Rigiocare, resettare, troubleshooting")
    d.table(["Sintomo", "Causa e rimedio"], [
        ["nmap -sn non trova il target", "bersaglio spento o non sulla stessa rete "
         "interna; verificare la scheda 2 'Rete interna labnet' su entrambe le VM"],
        ["ip neigh vuoto per il target", "pingare prima il target: `ping -c1 10.10.10.20`"],
        ["lab08-verifica mac dice non coincide", "spesso è un MAC copiato male; "
         "rileggerlo con `ip neigh show 10.10.10.20`"],
        ["nmap -sn senza MAC", "lanciarlo con sudo: l'ARP richiede i privilegi di root"],
    ], widths=[3200, 5826])

    d.h1("Nota didattica")
    d.p("Il verificatore usa ping e ip neigh (non nmap) per non dipendere dai privilegi "
        "di root nel momento della verifica: così funziona sempre, mentre in aula si "
        "mostra comunque nmap -sn per l'esperienza reale (con sudo).")
