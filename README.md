# cybersec_pf · Laboratorio del corso di Sicurezza Informatica

Materiali e automazioni per un corso di **Sicurezza Informatica difensiva e
vulnerability assessment** da 80 ore (40 lezioni da 2 ore), rivolto a una classe
di terza di istituto tecnico. Impostazione fortemente pratica, prospettiva
dell'attaccante per capire la difesa, gamification stile Capture The Flag.

- Ente: Progetto Formazione S.c.r.l. (Brissogne, AO) · Progetto P145 · a.f. 2026/27
- Docente: Michelangelo Chasseur (`chasseurmic`)

> Uso esclusivamente didattico, dentro un laboratorio isolato. Vedi la sezione
> [Uso didattico e legalità](#uso-didattico-e-legalità).

---

## L'idea in una riga

Ogni postazione dell'aula fa girare due macchine virtuali isolate (una Kali
attaccante e un bersaglio Ubuntu). L'immagine si costruisce **una volta sola**;
poi ogni lezione è uno script in questo repository che le VM scaricano ed
eseguono con un solo comando: `lab <numero>`.

---

## Il laboratorio

Due VM per postazione, collegate da una rete interna isolata (in VirtualBox
"Rete interna" di nome `labnet`; su Parallels una Host-Only Network). La rete
vive dentro il singolo PC: i laboratori sono isolati tra loro e non dipendono
dalla rete della scuola.

| VM | Ruolo | IP interno | Contenuto |
|---|---|---|---|
| Kali | attaccante | `10.10.10.5` | strumenti offensivi + launcher `lab` |
| Bersaglio | vittima | `10.10.10.20` | Ubuntu Server headless, app vulnerabili in Docker |

App web sul bersaglio: DVWA su `:8081`, OWASP Juice Shop su `:8082`, la pagina
"Banca della Scuola" su `:8080` (segnaposto fino alla Lezione 12, poi app Flask
vulnerabile a SQLi/XSS).

Requisiti di una postazione: circa **7 GB di RAM liberi** (host circa 3, Kali
circa 2,5, bersaglio circa 1,5, tenendo il bersaglio senza grafica). Con 8 GB si
lavora, con 16 si sta comodi, con 4 no.

---

## Struttura del repository

```
cybersec_pf/
├── README.md                 questo file
├── bin/                      strumenti condivisi da tutte le lezioni
│   ├── lab                   il launcher: scarica ed esegue lo script di una lezione
│   ├── provision-kali.sh     prepara l'immagine base Kali (una volta sola)
│   └── provision-target.sh   prepara l'immagine base bersaglio (una volta sola)
└── lezioni/
    ├── Lezioni/              i documenti Word delle lezioni (materiale d'aula)
    └── lezione-NN/           gli script che le VM eseguono con  lab NN
        ├── kali.sh           parte eseguita sulla Kali (ruolo kali)
        └── target.sh         parte eseguita sul bersaglio (ruolo target)
```

Convenzione dei percorsi: la lezione numero `NN` vive in `lezioni/lezione-NN/`,
con `kali.sh` (lato attaccante) e `target.sh` (lato bersaglio). Il documento
Word della lezione sta in `lezioni/Lezioni/`.

---

## Come funziona il launcher `lab`

Sulle VM è installato `/usr/local/bin/lab` e un file `/etc/lab-role` che vale
`kali` oppure `target`. Il comando

```bash
lab 3
```

scarica da GitHub lo script `lezioni/lezione-03/<ruolo>.sh` (dove `<ruolo>` è
letto da `/etc/lab-role`), ne mostra un'**anteprima** e chiede **conferma**
prima di eseguirlo con `sudo`. L'anteprima con conferma non è solo prudenza: è
una buona pratica di sicurezza che si insegna in aula ("non eseguire mai uno
script a scatola chiusa").

Il repository sorgente è configurato in testa a `bin/lab`:

```
REPO_RAW="https://raw.githubusercontent.com/chasseurmic/cybersec_pf/main"
```

---

## Preparare l'ambiente (una volta sola)

Le immagini di **produzione** vanno costruite su una postazione **Windows x86**
con VirtualBox (vedi [x86 vs ARM](#nota-x86-vs-arm)). Guida completa,
checklist e script di export in `lezioni/lezione-02/` (`README.md`,
`costruisci-ova.ps1`, `costruisci-ova.sh`). In breve:

1. **VM Kali** con due schede (1: NAT per internet; 2: Rete interna `labnet`):
   ```bash
   sudo ./bin/provision-kali.sh studente     # oppure: docente
   sudo install -m 755 bin/lab /usr/local/bin/lab
   echo kali | sudo tee /etc/lab-role
   ```
2. **VM bersaglio** con due schede (1: NAT; 2: Rete interna `labnet`):
   ```bash
   sudo ./bin/provision-target.sh
   sudo install -m 755 bin/lab /usr/local/bin/lab
   echo target | sudo tee /etc/lab-role
   ```
3. Verifica con la checklist, spegni entrambe le VM ed esporta in un unico OVA:
   ```powershell
   .\lezioni\lezione-02\costruisci-ova.ps1
   ```

I due script di provisioning rilevano da soli l'interfaccia della rete interna e
funzionano su VirtualBox, Parallels e UTM. L'immagine **docente** si ottiene con
`provision-kali.sh docente` (aggiunge `/root/soluzioni`) e va esportata a parte,
non nell'OVA degli studenti.

---

## Svolgere una lezione in aula

Con le VM già importate dall'OVA:

1. Sul **bersaglio**: `lab N` (prepara i bersagli e i file esca della lezione).
2. Sulla **Kali**: `lab N` (prepara gli strumenti e mostra la missione).
3. Gli studenti svolgono l'esercitazione seguendo il Word della lezione, trovano
   le flag e comunicano il punteggio al docente.

Rete durante il corso: la Kali tiene la scheda NAT attiva (le serve per scaricare
gli script); il bersaglio ha internet solo al momento del setup della lezione,
poi resta isolato. Per il blocco malware (Lezioni 31-34) si stacca internet
anche dalla Kali.

---

## Lezioni disponibili

| N | Titolo | Contenuto script |
|---|---|---|
| 01 | Triade CIA e primo accesso | flag di benvenuto su Kali e pagina Banca sul bersaglio |
| 02 | Allestimento del laboratorio | self-check dell'ambiente + strumenti di build ed export OVA |
| 03 | Filesystem e permessi | caccia al tesoro sul bersaglio via SSH (utente ospite `studente`) |

Le lezioni successive vengono aggiunte con la stessa struttura
`lezioni/lezione-NN/`.

---

## Regole e convenzioni

- **Script idempotenti**: ogni `kali.sh` / `target.sh` si può rieseguire senza
  danni. È così che si "rigioca" o si ripristina una lezione.
- **Fine riga LF** e niente CRLF negli script (un CRLF nel launcher causava
  errori "Cannot fork").
- **Valori delle flag**: nelle prime lezioni sono didattici e restano nel repo
  pubblico. Dalle sfide vere in poi vanno tenuti **fuori** dal repo pubblico
  (repo privato o flag generate a runtime).
- **Materiale d'aula fuori dal repo pubblico**: i Word in `lezioni/Lezioni/` e i
  file `.ova` non vanno pubblicati. Sono già in `.gitignore`.

---

## Nota x86 vs ARM

L'aula è composta da PC Windows x86: le immagini di produzione devono essere
x86-64 e vanno costruite su Windows con VirtualBox. Il Mac Apple Silicon con
Parallels e Kali ARM64 va bene solo come banco di prova del flusso, perché su
ARM alcune app vulnerabili (DVWA in particolare) non partono. VirtualBox su Apple
Silicon esegue solo guest ARM; per la suite x86 completa su Mac l'unica strada è
UTM in emulazione (lento).

---

## Uso didattico e legalità

Tutti gli strumenti e le tecniche di questo repository sono pensati **solo** per
il laboratorio isolato del corso. Attaccare, scansionare o provare password su
sistemi esterni al laboratorio è un reato (accesso abusivo a sistema informatico,
art. 615-ter c.p., e articoli collegati). Il patto etico firmato dagli studenti è
parte della Lezione 2.
