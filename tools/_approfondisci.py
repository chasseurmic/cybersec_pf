#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
One-off: aggiunge a ogni dispensa uno o piu' 'approfondimenti' (paragrafi di
teoria piu' estesa) dentro la chiamata comune.studio(...), cosi' le dispense
diventano veri testi di riferimento. Idempotente: salta se gia' presenti.
Uso:  python3 tools/_approfondisci.py
"""
import os
import re

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lezioni_src")

# DATA[num] = lista di (titolo, testo). Un paragrafo esteso per lezione (a volte due).
DATA = {}

DATA[2] = [(
    "Capire gli indirizzi: cosa vuol dire /24",
    "Gli indirizzi della rete del laboratorio sono scritti come 10.10.10.0/24. Un "
    "indirizzo IPv4 e' fatto di 32 bit, divisi in quattro gruppi (i quattro numeri). Il "
    "numero dopo la barra dice quanti bit, partendo da sinistra, identificano la RETE; i "
    "restanti identificano i singoli computer (host). Con /24 i primi 24 bit (cioe' "
    "10.10.10) sono la rete e restano 8 bit per gli host: da 10.10.10.1 a 10.10.10.254, "
    "cioe' 254 indirizzi utilizzabili. Il .0 e' l'indirizzo della rete e il .255 e' il "
    "broadcast (parla a tutti insieme). Ecco perche' la tua Kali (10.10.10.5) e il "
    "bersaglio (10.10.10.20) si parlano direttamente: hanno gli stessi primi tre gruppi, "
    "quindi stanno nella stessa rete locale e non serve un router in mezzo."
), (
    "Perche' proprio due schede di rete",
    "La doppia scheda non e' un capriccio: separa due mondi. La scheda NAT collega la VM "
    "a internet passando dall'host, e serve solo durante il setup (e alla Kali per "
    "scaricare gli script con lab). La scheda su Rete interna collega le VM tra loro in "
    "una bolla isolata. Questa separazione e' gia' una lezione di sicurezza: il traffico "
    "'pericoloso' degli esercizi resta confinato, senza mai toccare la rete della scuola. "
    "Nel mondo reale si chiama segmentazione, ed e' una delle difese piu' efficaci."
)]

DATA[3] = [(
    "I permessi in dettaglio: dalle lettere ai numeri",
    "Ogni terzina di permessi (utente, gruppo, altri) e' in realta' un numero da 0 a 7, "
    "somma di r=4, w=2, x=1. Cosi' rwx=7, rw-=6, r-x=5, r--=4. Tre terzine diventano tre "
    "cifre: 644 vuol dire proprietario rw- (6), gruppo r-- (4), altri r-- (4). Attenzione "
    "alla x sulle cartelle: li' non significa 'eseguire' ma 'attraversare', cioe' poter "
    "entrare nella cartella. Per questo una cartella tipicamente e' 755: tutti possono "
    "entrarci ed elencarla, ma solo il proprietario puo' crearci dentro. Chi assegna i "
    "permessi ragiona sempre da destra a sinistra: cosa serve davvero ad 'altri'? Quasi "
    "mai la scrittura, spesso nemmeno la lettura."
)]

DATA[4] = [(
    "I tre canali: standard input, output ed errore",
    "Ogni comando ha tre canali. Lo standard input (stdin, canale 0) e' cio' che arriva, "
    "di solito dalla tastiera. Lo standard output (stdout, canale 1) e' il risultato "
    "normale. Lo standard error (stderr, canale 2) e' dove finiscono gli errori, tenuti "
    "separati apposta. La pipe | collega lo stdout di un comando allo stdin del "
    "successivo. Le redirezioni dirottano un canale: > e >> agiscono su stdout, 2> agisce "
    "su stderr, e 2>/dev/null butta via gli errori senza sporcare il risultato. Capire "
    "questa distinzione spiega perche' find /srv 2>/dev/null mostra solo i file trovati e "
    "nasconde la valanga di 'Permission denied': gli errori vanno sul canale 2, che tu "
    "stai scartando."
)]

DATA[5] = [(
    "Cosa succede davvero quando accedi",
    "Quando entri, il sistema avvia per te una shell con una tua identita' (l'UID) e i "
    "tuoi gruppi (i GID). Da quel momento ogni file che apri o processo che lanci porta "
    "quella identita', e il kernel decide cosa puoi fare confrontandola con i permessi. "
    "root (UID 0) e' l'eccezione: salta i controlli. I processi formano un albero: il "
    "primo di tutti e' systemd (PID 1), che avvia e sorveglia i servizi. La differenza "
    "tra un processo e un servizio e' proprio questa: un servizio e' un processo che "
    "systemd fa partire da solo all'avvio e riavvia se cade. Ecco perche', per capire da "
    "dove arriva un processo sospetto, si risale al servizio che lo ha generato."
)]

DATA[6] = [(
    "bash, sh e perche' lo scripting conta",
    "bash e' la shell piu' diffusa su Linux, ma non l'unica: sh (dash su Ubuntu) e' piu' "
    "minimale e NON conosce gli array ne' /dev/tcp. Per questo uno script che usa queste "
    "funzioni deve girare con bash: lanciarlo con sh dara' errori strani. Nello scripting "
    "contano molto i codici di uscita: 0 vuol dire riuscito, diverso da 0 fallito, ed e' "
    "cio' che usano if e gli operatori && (esegui il secondo solo se il primo riesce) e "
    "|| (solo se fallisce). Automatizzare non e' solo comodita': e' il modo in cui sono "
    "nati tutti gli strumenti di sicurezza. Capire come e' fatto uno scanner dentro ti "
    "rende capace di modificarlo e di non dipendere da tool pronti che non controlli."
)]

DATA[7] = [(
    "Footprint aziendale: quanto si scopre senza bucare nulla",
    "La ricognizione di un'organizzazione, prima ancora di toccarne i server, mette "
    "insieme pezzi pubblici: il formato delle email (nome.cognome), i nomi dei dipendenti "
    "dai social e dalla pagina 'chi siamo', i sottodomini, le tecnologie usate, documenti "
    "pubblicati con i metadati dentro. Ognuno e' innocuo da solo, ma insieme disegnano una "
    "mappa: chi attaccare (il neoassunto, il responsabile in ferie), come scrivergli, che "
    "software provare a sfruttare. Nel nostro laboratorio tutto questo e' finto e seminato "
    "apposta, ma la tecnica e' quella reale. Il difensore fa lo stesso esercizio sulla "
    "propria azienda per capire cosa sta regalando all'attaccante e ridurlo."
)]

DATA[8] = [(
    "ARP, MAC e IP: chi e' chi sulla rete locale",
    "Ogni scheda di rete ha due indirizzi: uno fisico e permanente, il MAC (es. "
    "08:00:27:ab:cd:ef), e uno logico e mutevole, l'IP. Sulla rete locale i computer si "
    "trovano tramite il MAC, non l'IP: quando uno vuole parlare con 10.10.10.20, chiede "
    "in broadcast 'chi ha questo IP?' e la scheda giusta risponde col proprio MAC. Questo "
    "e' l'ARP, e la coppia IP-MAC finisce nella cache ARP (ip neigh). E' anche il motivo "
    "per cui l'ARP funziona solo dentro la stessa rete locale: oltre il router si ragiona "
    "solo per IP. Capire questa differenza e' la base sia della scoperta host di oggi sia "
    "degli attacchi di spoofing che vedremo nel blocco di rete."
)]

DATA[9] = [(
    "Le porte in dettaglio: well-known, registrate, dinamiche",
    "Le 65535 porte TCP sono divise in tre fasce. Le well-known (1-1023) sono riservate ai "
    "servizi classici e richiedono privilegi per essere aperte: 22 SSH, 80 HTTP, 443 "
    "HTTPS. Le registrate (1024-49151) sono assegnate ad applicazioni note (3306 MySQL, "
    "8080 web alternativo). Le dinamiche (49152-65535) sono usate al volo dai client per "
    "le connessioni in uscita. Uno scanner distingue una porta aperta (arriva SYN-ACK) da "
    "una chiusa (arriva RST) da una filtrata (nessuna risposta, di solito un firewall). Il "
    "SYN scan (-sS) e' veloce perche' non completa il terzo passo dell'handshake, ma serve "
    "root; il connect scan (-sT) completa la connessione e funziona senza privilegi, ma e' "
    "piu' rumoroso e lento."
)]

DATA[10] = [(
    "Dalla versione alla vulnerabilita': CVE e CVSS",
    "Quando conosci nome e versione di un servizio puoi cercare se ha falle note. Le "
    "vulnerabilita' pubbliche hanno un codice CVE (es. CVE-2021-41773) e un punteggio di "
    "gravita' CVSS da 0 a 10. Esistono database consultabili e strumenti che, data una "
    "versione, elencano le CVE che la riguardano. Ecco perche' un banner che grida "
    "'Apache 2.4.49' e' un regalo: l'attaccante cerca la CVE, trova magari un exploit "
    "gia' pronto e lo prova. Il difensore ragiona al contrario: nasconde o riduce i "
    "banner, ma soprattutto aggiorna, perche' se la versione e' l'ultima le CVE note sono "
    "gia' chiuse e conoscere la versione non aiuta piu' l'attaccante."
)]

DATA[11] = [(
    "Anatomia di una richiesta e di una risposta HTTP",
    "Una richiesta HTTP e' testo in chiaro fatto di: una riga iniziale (metodo, percorso, "
    "versione, es. GET /login HTTP/1.1), una serie di header (Host, User-Agent, Cookie, "
    "Content-Type...), una riga vuota e, solo per POST/PUT, un corpo con i dati. La "
    "risposta ha la stessa forma: riga di stato (HTTP/1.1 200 OK), header (Server, "
    "Set-Cookie, Content-Type) e il corpo (la pagina). Un dettaglio fondamentale: HTTP e' "
    "senza stato (stateless), cioe' ogni richiesta e' indipendente e il server di per se' "
    "non ricorda le precedenti. Per 'ricordarti' dopo il login serve un trucco, il "
    "cookie. Vedere queste parti con curl -v ti fa capire che tutto cio' che il browser "
    "invia lo puoi costruire e modificare tu."
)]

DATA[12] = [(
    "Come funziona un database e perche' nasce la SQL injection",
    "Un database relazionale organizza i dati in tabelle (righe e colonne). Le si "
    "interroga con SQL: SELECT * FROM utenti WHERE username='mario' AND password='x' "
    "chiede le righe che soddisfano la condizione. Il problema nasce quando il programma "
    "costruisce quella frase incollando dentro cio' che scrivi, senza distinguere tra "
    "'dati' e 'comando'. Il database riceve un'unica stringa e la interpreta tutta: se nei "
    "dati infili apici e parole chiave SQL, cambi la logica della query. La soluzione, le "
    "query parametrizzate, separa in modo netto il comando (con dei segnaposto ?) dai dati "
    "(passati a parte): cosi' i tuoi apici restano semplice testo e non possono mai "
    "diventare istruzioni. E' la stessa idea del non mischiare ingredienti crudi e cotti."
)]

DATA[13] = [(
    "Oltre la UNION: SQL injection alla cieca",
    "Non sempre i risultati della query si vedono in pagina. In quei casi si usa la SQL "
    "injection 'blind' (alla cieca): si pongono al database domande a risposta si'/no e si "
    "deduce il dato una lettera alla volta. Nella variante boolean-based si guarda se la "
    "pagina cambia (un risultato in piu' o in meno) quando la condizione e' vera. Nella "
    "variante time-based si chiede al database di 'aspettare' qualche secondo se la "
    "condizione e' vera, e si misura il tempo di risposta. E' lento a mano, ma sqlmap lo "
    "automatizza: per questo uno strumento del genere e' cosi' potente, e per questo va "
    "usato solo dove sei autorizzato."
)]

DATA[14] = [(
    "Le tre facce dell'XSS e la regola dell'origine",
    "L'XSS ha tre forme. Riflessa: il payload e' nella richiesta e torna subito nella "
    "risposta (colpisce chi apre un link preparato). Memorizzata: il payload viene salvato "
    "dal sito (un commento, un messaggio) e servito a tutti i visitatori. DOM-based: il "
    "problema e' nel JavaScript della pagina che manipola l'input senza ripulirlo. Perche' "
    "un XSS e' cosi' potente? Perche' il codice iniettato gira con l'origine del sito "
    "vero: il browser protegge i siti l'uno dall'altro con la 'same-origin policy', ma uno "
    "script iniettato NEL sito e' considerato parte del sito e puo' leggere i suoi cookie, "
    "modificare la pagina, inviare richieste come te. Ecco perche' ruba sessioni e compie "
    "azioni al posto della vittima."
)]

DATA[15] = [(
    "Sessioni lato server e token: come si fa bene",
    "Ci sono due modi corretti per ricordarsi di un utente dopo il login. Il primo: il "
    "server crea una sessione, le da' un identificativo lungo e casuale, lo salva da se' e "
    "mette solo quel codice nel cookie; a ogni richiesta ritrova la sessione e sa chi sei. "
    "Il secondo: rilascia un token firmato (es. JWT) che contiene le informazioni e una "
    "firma che il server verifica, cosi' non deve conservare nulla. In entrambi i casi il "
    "punto e' che il client non deve poter falsificare la propria identita': col cookie "
    "casuale non lo indovina, col token firmato non lo puo' alterare senza rompere la "
    "firma. Il difetto della nostra Banca (il cookie che contiene il nome utente in "
    "chiaro) e' proprio l'errore da non fare."
)]

DATA[16] = [(
    "Attacco online e offline, ed entropia delle password",
    "Ci sono due scenari di attacco alle password. Online: si provano le password "
    "direttamente sul login del sito; e' lento e si puo' fermare con rate limiting e "
    "lockout (la difesa di oggi). Offline: l'attaccante ha gia' rubato gli hash e prova a "
    "casa milioni di tentativi al secondo, senza limiti, contro il proprio computer (lo "
    "vedremo nel cracking). Cio' che rende dura una password e' l'entropia, cioe' quanto "
    "e' imprevedibile: una passphrase lunga di parole casuali (quattro-cinque parole) batte "
    "una password corta piena di simboli, perche' offre molte piu' combinazioni ed e' "
    "anche piu' facile da ricordare. La lunghezza, piu' della complessita', e' l'arma vera."
)]

DATA[17] = [(
    "Perche' upload e path traversal sono cosi' pericolosi",
    "Un upload non validato non e' solo 'un file di troppo': su un server reale puo' "
    "trasformarsi in esecuzione di codice. Se il sito salva un file .php in una cartella "
    "servita dal web server, aprirlo lo esegue: l'attaccante ottiene una 'webshell', cioe' "
    "una porta per lanciare comandi sul server. Per questo non basta guardare l'estensione "
    "(si puo' mascherare) ne' il tipo dichiarato dal browser (si falsifica): serve una "
    "whitelist, rinominare i file e salvarli fuori dalla cartella eseguibile. Il path "
    "traversal e' l'altra faccia: se un percorso si costruisce con l'input dell'utente, i "
    "../ permettono di uscire dalla cartella prevista. La difesa e' 'canonicalizzare' il "
    "percorso (ridurlo alla forma reale) e verificare che resti dentro i confini consentiti."
)]

DATA[18] = [(
    "La OWASP Top 10 in breve",
    "La Top 10 di OWASP e' l'elenco, aggiornato ogni pochi anni, delle categorie di falle "
    "web piu' diffuse e gravi. Tra le principali: Broken Access Control (chi puo' fare "
    "cosa, gestito male), Cryptographic Failures (dati sensibili non protetti), Injection "
    "(SQLi, XSS e simili), Insecure Design (falle di progettazione), Security "
    "Misconfiguration (configurazioni sbagliate), Vulnerable Components (librerie vecchie), "
    "Identification and Authentication Failures (login e sessioni deboli). Non e' una lista "
    "di 'bug' ma di famiglie: serve a ragionare per categorie e a non dimenticare interi "
    "fronti. Il valore del mini CTF di oggi e' vedere come, nella pratica, un attacco "
    "reale ne combina piu' di una in sequenza."
)]

DATA[19] = [(
    "Dentro un hash: collisioni, sale e pepe",
    "Una funzione di hash prende un input di qualsiasi lunghezza e produce un'impronta di "
    "lunghezza fissa, in modo che un minimo cambiamento nell'input stravolga l'output "
    "(effetto valanga). Due input diversi che producono lo stesso hash sono una "
    "'collisione': un buon algoritmo le rende praticamente impossibili, ed e' qui che MD5 "
    "ha fallito nel tempo. Per le password non basta l'algoritmo: si aggiunge un sale "
    "(salt), casuale e diverso per ogni utente, memorizzato accanto all'hash, che rende "
    "unico ogni risultato e inutili le tabelle precalcolate. Alcuni sistemi aggiungono "
    "anche un 'pepe' (pepper), un valore segreto uguale per tutti tenuto separato dal "
    "database: se il DB viene rubato ma il pepe no, gli hash restano piu' difficili da "
    "attaccare."
)]

DATA[20] = [(
    "Il costo del cracking: hashrate, regole e maschere",
    "Craccare significa provare tante ipotesi e confrontarne l'hash con quello rubato. La "
    "velocita' si misura in hash al secondo (hashrate): con MD5 una GPU ne fa miliardi, con "
    "bcrypt solo poche migliaia, ed e' questa lentezza voluta a proteggere. Gli strumenti "
    "non provano solo parole di una lista: applicano regole (aggiungi un numero, "
    "sostituisci a con @, metti la maiuscola) che trasformano ogni parola in decine di "
    "varianti, e maschere per tentare schemi noti (una maiuscola, sei lettere, due cifre). "
    "Cosi' 'Password1!' cade subito anche se non e' identica a una voce del dizionario. La "
    "conseguenza pratica: sono le password lunghe e senza schema prevedibile a resistere."
)]

DATA[21] = [(
    "Il problema dello scambio della chiave",
    "La cifratura simmetrica e' veloce ma ha un tallone d'Achille: come fai avere la "
    "chiave all'altra persona senza che qualcuno la intercetti? La cifratura asimmetrica "
    "risolve proprio questo. Un'idea elegante e' lo scambio di Diffie-Hellman: due persone "
    "riescono a mettersi d'accordo su una chiave segreta comune scambiandosi solo "
    "informazioni pubbliche, in modo che chi ascolta non possa ricavarla. Nella pratica si "
    "combinano i due mondi: si usa l'asimmetrica (lenta) solo per concordare in sicurezza "
    "una chiave, poi si passa alla simmetrica (veloce) per cifrare i dati veri. Sulle "
    "dimensioni: una chiave RSA robusta e' di 2048 o 4096 bit, mentre le curve ellittiche "
    "(ECC) offrono la stessa sicurezza con chiavi molto piu' corte. E' esattamente cio' "
    "che fa HTTPS, il tema della prossima lezione."
)]

DATA[22] = [(
    "Il handshake TLS, passo per passo (semplificato)",
    "Quando apri un sito HTTPS, prima di scambiare qualunque dato avviene una stretta di "
    "mano. Il tuo browser dice 'ciao, ecco le versioni di TLS e gli algoritmi che "
    "conosco'. Il server risponde scegliendo l'algoritmo e inviando il suo certificato, "
    "che contiene la chiave pubblica e l'identita', firmato da una CA. Il browser verifica "
    "quella firma risalendo alla catena di CA di cui si fida: se non torna, scatta "
    "l'avviso. A quel punto le due parti concordano (usando l'asimmetrica) una chiave "
    "simmetrica di sessione e da li' in poi tutto il traffico viaggia cifrato con quella, "
    "veloce. Capire questi passaggi spiega perche' un certificato self-signed fa avvisare "
    "il browser (nessuna CA lo garantisce) e perche' ignorare quell'avviso apre la porta a "
    "un man-in-the-middle."
)]

DATA[23] = [(
    "Incapsulamento: le buste dentro le buste",
    "Quando invii un dato, ogni livello della pila TCP/IP aggiunge la propria 'busta' "
    "(header) attorno a quella del livello sopra. L'applicazione produce il contenuto (es. "
    "una richiesta HTTP); il livello di trasporto (TCP) ci mette davanti le porte di "
    "origine e destinazione; il livello di rete (IP) aggiunge gli indirizzi IP; il livello "
    "di collegamento (Ethernet) aggiunge i MAC. In ricezione si aprono le buste in ordine "
    "inverso. Ecco perche' in Wireshark, cliccando un pacchetto, vedi i livelli uno dentro "
    "l'altro: Ethernet, poi IP, poi TCP, poi i dati. E capisci anche la differenza tra i "
    "tre indirizzi che hai incontrato: il MAC serve nella rete locale, l'IP per arrivare "
    "attraverso i router, la porta per consegnare al servizio giusto sul computer di "
    "destinazione."
)]

DATA[24] = [(
    "Raw socket, modalita' promiscua e switch",
    "Per catturare pacchetti che non sono destinati a te servono due cose. La prima e' un "
    "raw socket, cioe' l'accesso diretto ai pacchetti grezzi: e' un'operazione "
    "privilegiata, per questo scapy e tcpdump vogliono root. La seconda e' la modalita' "
    "promiscua della scheda, che le fa accettare anche il traffico non indirizzato al suo "
    "MAC. C'e' pero' un limite fisico: negli hub (vecchi) tutto il traffico arrivava a "
    "tutti, quindi si sniffava tutto; negli switch moderni il traffico viene inviato solo "
    "alla porta giusta, quindi di norma vedi solo il tuo traffico e i broadcast. Per "
    "sniffare quello altrui su uno switch serve un trucco in piu', per esempio mettersi in "
    "mezzo con l'ARP spoofing: ed e' esattamente il ponte verso la lezione successiva."
)]

DATA[25] = [(
    "Perche' l'ARP e' cosi' facile da ingannare",
    "L'ARP e' stato progettato in un'epoca in cui la rete locale era considerata fidata: "
    "per questo non ha alcuna autenticazione. Chiunque puo' inviare una risposta ARP anche "
    "senza che nessuno l'abbia chiesta (gratuitous ARP), e i computer aggiornano la loro "
    "cache fidandosi dell'ultima risposta ricevuta. L'attaccante ne approfitta mandando in "
    "continuazione risposte false che dicono 'quell'IP ce l'ho io', cosi' il traffico "
    "della vittima verso quell'IP arriva a lui. Per un man-in-the-middle completo si "
    "avvelenano entrambi i lati e si attiva l'inoltro dei pacchetti, in modo che le due "
    "parti continuino a parlarsi senza accorgersi del passaggio in mezzo. Si rileva "
    "notando che uno stesso MAC risponde per piu' IP, o con strumenti come arpwatch."
)]

DATA[26] = [(
    "Come funziona davvero il DNS (e dove si rompe)",
    "Il DNS e' una gerarchia. Quando chiedi un nome, si parte dai server radice, che "
    "indicano i server del dominio di primo livello (.it, .com), che a loro volta indicano "
    "i server autoritativi del dominio specifico, che danno la risposta finale. Per non "
    "rifare tutto ogni volta, le risposte vengono messe in cache per un tempo detto TTL. "
    "Ogni punto di questa catena, e ogni cache lungo la strada, e' un possibile bersaglio: "
    "se un attaccante riesce a inserire una risposta falsa (o controlla il DNS che usi), ti "
    "manda dove vuole lui. La difesa moderna e' DNSSEC, che firma le risposte DNS in modo "
    "che non si possano falsificare, e il DNS cifrato (DoH/DoT), che impedisce di "
    "manometterle o spiarle lungo il percorso."
)]

DATA[27] = [(
    "Firewall, IDS e IPS: chi ferma e chi avvisa",
    "Un firewall decide quali pacchetti passano in base a regole; quelli moderni sono "
    "'stateful', cioe' ricordano le connessioni gia' aperte e lasciano passare le risposte "
    "attese. La strategia migliore e' 'default-deny': si blocca tutto e si aprono solo le "
    "poche cose necessarie, l'opposto di aprire tutto e chiudere qualche buco. Accanto al "
    "firewall ci sono l'IDS, che rileva le attivita' sospette e avvisa, e l'IPS, che le "
    "rileva e le blocca automaticamente. La segmentazione, infine, divide la rete in zone "
    "(VLAN): se un attaccante entra in una zona non raggiunge le altre. Difesa in "
    "profondita' vuol dire proprio questo: piu' strati diversi, cosi' che superarne uno non "
    "basti a vincere."
)]

DATA[28] = [(
    "Il ciclo del social engineering e i casi reali",
    "Un attacco basato sulle persone segue un ciclo: raccolta di informazioni (OSINT), "
    "costruzione di un pretesto credibile, contatto e sfruttamento della fiducia, e infine "
    "l'azione (farsi dare una password, un bonifico, l'accesso a una stanza). I casi reali "
    "sono ovunque: la 'truffa del CEO', in cui una email che sembra del capo ordina "
    "all'ufficio contabilita' un bonifico urgente; il finto tecnico che chiama per "
    "'risolvere un problema' e si fa dettare le credenziali; l'SMS del corriere con il "
    "link al pagamento di due euro. Funzionano perche' sfruttano automatismi umani, non "
    "falle tecniche: ecco perche' nessun firewall li ferma e l'unica difesa e' una persona "
    "informata e la buona abitudine di verificare per un secondo canale."
)]

DATA[29] = [(
    "Anatomia di una campagna di phishing",
    "Dietro una pagina di phishing c'e' quasi sempre una piccola 'macchina': un dominio "
    "somigliante a quello vero (typosquatting, es. banca-scuola-sicurezza.xyz), una copia "
    "fedele del sito bersaglio, un modulo che invia le credenziali all'attaccante e un "
    "redirect al sito autentico per non insospettire. L'email che porta il link usa le "
    "leve del social engineering (urgenza, autorita'). Le campagne piu' mirate, lo "
    "spear phishing, sono cucite su una persona specifica usando l'OSINT. Capire come si "
    "monta questo meccanismo, in laboratorio e contro un finto utente, e' il modo migliore "
    "per imparare a smontarlo: quando saprai riconoscere il dominio finto e il redirect, "
    "difficilmente abboccherai."
)]

DATA[30] = [(
    "La checklist antiphishing, ragionata",
    "Riconoscere un phishing e' un metodo, non un colpo d'occhio. Primo, il mittente: "
    "l'indirizzo vero (non il nome mostrato) e' plausibile? Secondo, il link: dove porta "
    "davvero il dominio, leggendo le ultime due etichette prima della prima barra? Terzo, "
    "il tono: c'e' urgenza, minaccia, un premio troppo bello? Quarto, la richiesta: ti "
    "chiedono credenziali o un pagamento cliccando un link? Nel dubbio non si clicca: si "
    "apre il sito dai preferiti o digitando l'indirizzo. Infine, la rete di sicurezza: con "
    "il 2FA, anche se una volta abbocchi, la password rubata da sola non basta. E le "
    "email sospette si segnalano, perche' proteggere se stessi e proteggere gli altri qui "
    "sono la stessa cosa."
)]

DATA[31] = [(
    "La catena di infezione e perche' il malware cambia forma",
    "Molti attacchi malware seguono una 'kill chain': ricognizione, consegna (email, "
    "chiavetta, download), sfruttamento di una falla per l'esecuzione, installazione con "
    "persistenza, collegamento al server di comando (C2) e infine l'azione sull'obiettivo. "
    "Conoscere le tappe aiuta a spezzarle: basta bloccarne una. Il malware inoltre cambia "
    "continuamente forma per sfuggire agli antivirus: le varianti polimorfe modificano il "
    "proprio codice a ogni copia mantenendo lo stesso comportamento. Per questo la difesa "
    "moderna non guarda solo 'com'e' fatto' un file (le firme), ma 'cosa fa' quando gira "
    "(il comportamento): un principio che ritroverai nell'analisi dinamica."
)]

DATA[32] = [(
    "Cosa c'e' dentro un eseguibile e i limiti dell'analisi",
    "Un programma compilato ha un formato preciso: ELF su Linux, PE su Windows. E' diviso "
    "in sezioni (il codice, i dati, le stringhe) e contiene informazioni che l'analisi "
    "statica sa leggere senza eseguire nulla: che tipo di file e', quali librerie usa, "
    "quali testi contiene (URL, comandi, messaggi), qual e' la sua impronta hash. Tutto "
    "questo si ricava a rischio zero. L'analisi statica ha pero' un limite: un malware puo' "
    "offuscare o cifrare le sue parti pericolose, che compaiono solo quando gira. Per "
    "questo la statica e la dinamica sono complementari: la prima dice cosa un file "
    "potrebbe fare e da' indicatori immediati (l'hash, gli URL), la seconda mostra cosa fa "
    "davvero una volta avviato in una sandbox."
)]

DATA[34] = [(
    "IOC e IOA: gli indizi di una compromissione",
    "Osservando un campione in esecuzione si raccolgono due tipi di indizi. Gli IOC "
    "(Indicator Of Compromise) sono tracce concrete: l'hash di un file, un IP o un dominio "
    "contattato, il nome di un file lasciato, una chiave di persistenza. Sono ottimi per "
    "cercare la stessa minaccia su altri computer e per creare regole di blocco. Gli IOA "
    "(Indicator Of Attack) descrivono invece il comportamento, la tattica: 'un processo "
    "office che lancia PowerShell che scarica un file'. Gli IOC cambiano facilmente (basta "
    "che l'attaccante cambi IP), gli IOA colgono lo schema e reggono meglio nel tempo. Un "
    "buon difensore usa entrambi: gli IOC per il blocco immediato, gli IOA per riconoscere "
    "anche le varianti mai viste prima."
)]

DATA[35] = [(
    "Superficie d'attacco, baseline e minimo privilegio",
    "L'hardening ruota attorno a tre idee. La superficie d'attacco e' la somma di tutti i "
    "punti da cui si potrebbe entrare: ogni servizio acceso, porta aperta, account, "
    "permesso. Ridurla vuol dire spegnere l'inutile: cio' che non esiste non si puo' "
    "bucare. La baseline (o benchmark, come quelli del CIS) e' una lista di controllo "
    "concreta di configurazioni sicure, da verificare voce per voce e, meglio ancora, in "
    "automatico. Il minimo privilegio, infine, dice di dare a ogni utente e ogni processo "
    "solo i permessi indispensabili: se qualcosa viene compromesso, i danni restano "
    "limitati. Insieme, questi principi trasformano la sicurezza da 'sperare che vada "
    "bene' a 'disciplina verificabile'."
)]

DATA[36] = [(
    "Cosa loggare, come correlare, ATT&CK",
    "Un buon monitoraggio non registra tutto a caso: sceglie gli eventi che contano "
    "(accessi, cambi di privilegio, errori, connessioni) e li centralizza in un unico "
    "posto, cosi' da poterli correlare tra fonti diverse. Correlare significa collegare "
    "indizi: un accesso fallito ripetuto, seguito da un accesso riuscito, seguito da un "
    "comando insolito, raccontano una storia che i singoli eventi non mostrano. Per "
    "ragionare in modo sistematico su cosa cercare esiste MITRE ATT&CK, una mappa delle "
    "tattiche e tecniche usate dagli attaccanti: aiuta a chiedersi 'ho visibilita' su "
    "questa mossa?'. E i log servono a poco se non c'e' ritenzione (li si conserva a "
    "sufficienza) e qualcuno o qualcosa che li guardi davvero."
)]

DATA[37] = [(
    "La timeline, la comunicazione e le prove",
    "Durante un incidente due cose contano quanto le azioni tecniche. La prima e' la "
    "timeline: ricostruire in ordine cosa e' successo e quando (dal primo accesso "
    "sospetto alla scoperta), perche' senza timeline non capisci l'estensione del danno ne' "
    "come chiuderla. La seconda e' la comunicazione: chi va avvisato, cosa si dice e "
    "quando, evitando sia il silenzio sia il panico. Se l'incidente potrebbe avere seguiti "
    "legali, si preservano le prove senza alterarle (la 'catena di custodia'): per questo "
    "non si cancella tutto d'impulso. Infine il postmortem, l'analisi finale, deve essere "
    "'senza colpe': non serve trovare un colpevole, serve capire come e' entrato "
    "l'attaccante e migliorare i processi perche' non riaccada."
)]

DATA[38] = [(
    "Un metodo per affrontare un CTF",
    "In un CTF non conta solo sapere le tecniche, conta il metodo. Regola numero uno: "
    "enumerare sempre e a fondo, perche' quasi ogni sfida si sblocca con un'informazione "
    "trovata guardando meglio (una porta, un file, un commento). Regola due: leggere per "
    "intero il testo della sfida, spesso il suggerimento e' li'. Regola tre: tenere "
    "appunti dei comandi e dei tentativi, per non ripetere il lavoro e per riusare cio' "
    "che funziona. Regola quattro: non fissarsi; se una sfida ti blocca, passa a un'altra "
    "e torna dopo con occhi freschi. Regola cinque: partire dalle sfide che danno punti "
    "sicuri prima di lanciarsi su quelle difficili. E' lo stesso metodo, ordinato e "
    "paziente, che serve nel lavoro vero."
)]

DATA[39] = [(
    "Tempo e squadra: come non sprecarli",
    "In gara le due risorse piu' scarse sono il tempo e l'attenzione. Sfruttatele "
    "dividendovi per aree in base ai punti di forza (chi e' bravo sul web, chi sui log, "
    "chi sul cracking) e tenendo un foglio condiviso con le flag trovate e le cose gia' "
    "provate: nulla spreca piu' tempo di due persone che risolvono la stessa sfida senza "
    "saperlo. Comunicate a voce cosa state facendo. Prendete subito i punti facili per "
    "mettere fieno in cascina, poi affrontate insieme le sfide difficili. E ricordate che "
    "una flag consegnata vale solo se e' quella della vostra postazione: le flag sono "
    "generate per macchina, quindi verificate sempre sul bersaglio giusto."
)]

DATA[40] = [(
    "La sicurezza e' un processo, non un prodotto",
    "L'ultima idea da portare a casa e' che la sicurezza non si compra e non si finisce: "
    "e' un processo continuo. I sistemi cambiano, nascono nuove vulnerabilita', gli "
    "attaccanti si aggiornano; per questo difendere significa ripetere per sempre lo "
    "stesso ciclo: ridurre la superficie (hardening), sorvegliare (monitoraggio), reagire "
    "(incident response) e imparare (lezioni apprese), poi ricominciare. Le competenze che "
    "avete costruito in questo corso, pensare come un attaccante per difendere meglio, "
    "sono la base di professioni molto richieste: analista SOC, penetration tester, "
    "incident responder. La differenza tra un professionista e un criminale non e' la "
    "conoscenza, e' l'etica e il permesso: usate cio' che sapete per proteggere."
)]


def inject(num):
    path = os.path.join(SRC, "lez%02d.py" % num)
    src = open(path, encoding="utf-8").read()
    if "approfondimenti=" in src:
        return "gia' presente, salto"
    m = re.search(r'(\n)(    comune\.studio\(\n        d,\n)', src)
    if not m:
        return "chiamata comune.studio non trovata!"
    items = DATA[num]
    blocco = "        approfondimenti=[\n" + "".join(
        "            (%r, %r),\n" % (t, x) for t, x in items) + "        ],\n"
    pos = m.end(2)
    src = src[:pos] + blocco + src[pos:]
    open(path, "w", encoding="utf-8").write(src)
    return "aggiunti %d approfondimenti" % len(items)


if __name__ == "__main__":
    for num in sorted(DATA):
        print("L%02d: %s" % (num, inject(num)))
