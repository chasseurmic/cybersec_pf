#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera la "Guida al setup del laboratorio" (Word) con lo stesso stile delle
dispense. Uso:  python3 tools/genera_guida_setup.py
Output: lezioni/Lezioni/Guida-Setup-Laboratorio.docx
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docxgen as g


def build():
    d = g.Doc("Guida al setup del laboratorio (VirtualBox)")
    d.titolo = "Guida al setup del laboratorio · VirtualBox"
    d.body = []
    d._intestazione()

    d.box("blu", "A cosa serve questa guida", [
        "**Per chi:** il docente. Spiega come costruire le due macchine virtuali del "
        "corso (Kali attaccante e bersaglio Ubuntu) e come impacchettarle in UN SOLO file "
        "OVA da distribuire agli studenti.",
        "**Risultato:** un file `corso-cyber-lab.ova` che ogni studente importa in "
        "VirtualBox e avvia. Da quel momento le esercitazioni si scaricano col comando "
        "`lab NN`.",
        "**Tempo:** circa 2-3 ore la prima volta (soprattutto per gli aggiornamenti e il "
        "download delle immagini Docker). Si fa UNA VOLTA SOLA.",
    ])

    d.h1("Prima di tutto · Mac o PC? La questione dell'architettura")
    d.p("È la decisione più importante e spesso la fonte di tutti i problemi. Una macchina "
        "virtuale contiene un sistema operativo compilato per una specifica architettura "
        "di CPU. Ci sono due mondi che NON sono compatibili tra loro:")
    d.table(["Architettura", "Dove si trova", "VM che produce"], [
        ["x86-64 (Intel/AMD)", "i PC Windows dell'aula", "immagini x86-64"],
        ["ARM64 (Apple Silicon)", "i Mac con chip M1/M2/M3/M4", "immagini ARM64"],
    ], widths=[2600, 3400, 3026])
    d.box("rosso", "La regola d'oro (leggere due volte)", items=[
        "Un OVA costruito su un Mac Apple Silicon (ARM64) NON si avvia sui PC x86 "
        "dell'aula, e viceversa. L'architettura del guest deve combaciare con quella su "
        "cui girerà.",
        "Quindi: l'OVA da distribuire agli studenti va costruito su una macchina x86-64 "
        "(un PC Windows o Linux, idealmente uno dei PC dell'aula).",
        "Su VirtualBox per Apple Silicon puoi eseguire solo guest ARM: utile per provare "
        "il flusso, non per creare l'immagine finale x86.",
    ])
    d.h2("In pratica, cosa fare")
    d.table(["Hai a disposizione", "Cosa usare", "Note"], [
        ["Un PC Windows/Linux x86", "VirtualBox su quel PC", "PERCORSO CONSIGLIATO: "
         "costruisci qui l'OVA da distribuire"],
        ["Solo un Mac Apple Silicon", "UTM in emulazione x86 (lento) o un PC x86 in "
         "prestito", "il Mac va bene come banco di prova ARM, non per l'immagine finale"],
        ["Aula già x86", "un PC dell'aula per costruire, gli altri per gli studenti",
         "la scelta più semplice e affidabile"],
    ], widths=[2600, 3200, 3226])
    d.p("Il resto della guida assume che tu stia lavorando su una macchina x86-64 con "
        "VirtualBox: è lo scenario dell'aula. Se provi prima sul Mac (ARM) i passi sono "
        "identici, cambiano solo le immagini (ARM invece di x86) e il risultato non è "
        "distribuibile agli studenti x86.")

    d.h1("Prerequisiti")
    d.bullets([
        "**VirtualBox** (ultima versione) installato sulla macchina x86 di costruzione. "
        "Gratuito, da virtualbox.org.",
        "**Extension Pack** di VirtualBox (facoltativo, comodo per USB e altro).",
        "Le **ISO**: Kali Linux (Installer a 64 bit) e Ubuntu Server LTS (64 bit).",
        "Il **repository del corso** (`cybersec_pf`) scaricato o clonato, per avere gli "
        "script `bin/provision-*.sh`, `bin/lab` e `lezioni/lezione-02/costruisci-ova.*`.",
        "**Spazio disco:** circa 30-40 GB durante la costruzione. **RAM della macchina "
        "studente:** circa 7 GB liberi (host 3, Kali 2,5, bersaglio 1,5).",
        "Una **connessione internet** durante il setup (serve per aggiornamenti, "
        "strumenti e immagini Docker). Dopo, il laboratorio funziona offline.",
    ])

    d.h1("La rete del laboratorio (schema)")
    d.p("Ogni VM ha DUE schede di rete. Questo schema è il cuore di tutto: se sbagli qui, "
        "niente funziona.")
    d.table(["Scheda", "Tipo in VirtualBox", "A cosa serve"], [
        ["Scheda 1", "NAT", "dà internet alla VM durante il setup (e alla Kali anche in "
         "aula, per scaricare gli script con `lab`)"],
        ["Scheda 2", "Rete interna (Internal Network), nome `labnet`", "collega Kali e "
         "bersaglio in una rete privata isolata dentro il PC"],
    ], widths=[1600, 3400, 4026])
    d.p("Indirizzi sulla rete interna: **Kali = 10.10.10.5**, **bersaglio = 10.10.10.20**. "
        "Li impostano da soli gli script di provisioning, che rilevano in automatico quale "
        "sia la scheda interna.")

    d.h1("Passo 1 · La VM Kali (attaccante)")
    d.numbered([
        "In VirtualBox: Nuova > nome `kali-studente`, tipo Linux, versione Debian/Kali "
        "(64 bit). Assegna 2-3 GB di RAM e un disco da circa 25 GB.",
        "Sezione Rete: Scheda 1 = NAT. Scheda 2 = Rete interna, nome `labnet`.",
        "Avvia la VM con la ISO di Kali e completa l'installazione (utente `kali`).",
        "Ad installazione finita, apri un terminale nella Kali, porta dentro il "
        "repository del corso (chiavetta o `git clone`) ed esegui il provisioning:",
    ])
    d.code([
        "sudo ./bin/provision-kali.sh studente",
        "sudo install -m 755 bin/lab /usr/local/bin/lab",
        "echo kali | sudo tee /etc/lab-role",
    ])
    d.p("`provision-kali.sh` installa gli strumenti del corso (nmap, wireshark, hydra, "
        "john, hashcat, sqlmap, scapy, ecc.), imposta l'IP interno `10.10.10.5` e prepara "
        "le flag introduttive. `install ... lab` mette il comando `lab`; il file "
        "`/etc/lab-role` dice a `lab` che questa macchina è la 'kali'.")

    d.h1("Passo 2 · La VM bersaglio (Ubuntu Server)")
    d.numbered([
        "In VirtualBox: Nuova > nome `target-ubuntu`, tipo Linux, Ubuntu (64 bit). "
        "Assegna circa 1,5-2 GB di RAM e un disco da circa 15 GB.",
        "Sezione Rete: Scheda 1 = NAT. Scheda 2 = Rete interna, nome `labnet` (identico "
        "alla Kali).",
        "Installa Ubuntu Server SENZA interfaccia grafica (risparmia RAM). Crea un utente "
        "amministratore.",
        "Ad installazione finita, porta dentro il repository ed esegui il provisioning:",
    ])
    d.code([
        "sudo ./bin/provision-target.sh",
        "sudo install -m 755 bin/lab /usr/local/bin/lab",
        "echo target | sudo tee /etc/lab-role",
    ])
    d.p("`provision-target.sh` installa Docker, imposta l'IP interno `10.10.10.20`, scarica "
        "le app web vulnerabili (DVWA, OWASP Juice Shop) e l'immagine nginx per la 'Banca "
        "della Scuola', e le avvia. Il file `/etc/lab-role` qui vale `target`.")
    d.box("blu", "Nota sulle app del Blocco 4", items=[
        "La 'Banca della Scuola' (app vulnerabile del corso, dalla Lezione 12) è in Python "
        "della sola libreria standard e viene installata dallo script della Lezione 12 "
        "(`lab 12`), non dal provisioning: gira offline senza Docker.",
        "DVWA e Juice Shop sono container Docker: su x86 partono, su ARM (Mac) DVWA no. È "
        "un altro motivo per costruire l'immagine finale su x86.",
    ])

    d.h1("Passo 3 · Verifica prima di esportare")
    d.p("Con entrambe le VM accese, controlla che tutto risponda. Se un controllo fallisce, "
        "NON esportare: risolvi prima.")
    d.h2("Sulla Kali")
    d.code([
        "ip -4 addr | grep 10.10.10.5        # deve comparire l'IP interno",
        "cat /etc/lab-role                    # deve dire: kali",
        "ping -c1 10.10.10.20                 # il bersaglio risponde",
        "lab 2                                # deve chiudersi con FLAG{la_rete_e_viva}",
    ])
    d.h2("Sul bersaglio")
    d.code([
        "ip -4 addr | grep 10.10.10.20        # IP interno",
        "cat /etc/lab-role                    # deve dire: target",
        "docker ps                            # dvwa e juiceshop in stato Up",
        "curl -s localhost:8081 | head -n1    # DVWA risponde",
    ])
    d.p("Quando tutto è verde, spegni ENTRAMBE le VM in modo pulito (`sudo poweroff`), "
        "non sospenderle.")

    d.h1("Passo 4 · Esportare in un unico OVA")
    d.p("L'OVA è un singolo file che contiene entrambe le VM: è ciò che distribuirai. Due "
        "modi.")
    d.h2("Modo A · dall'interfaccia di VirtualBox")
    d.numbered([
        "File > Esporta applicazione (Export Appliance).",
        "Seleziona ENTRAMBE le VM (`kali-studente` e `target-ubuntu`).",
        "Formato OVF 2.0, nome file `corso-cyber-lab.ova`, ed esporta.",
    ])
    d.h2("Modo B · con lo script del repository")
    d.p("Dalla cartella del repository, sulla macchina di costruzione:")
    d.code([
        "# Windows (PowerShell):",
        ".\\lezioni\\lezione-02\\costruisci-ova.ps1",
        "# Linux:",
        "./lezioni/lezione-02/costruisci-ova.sh",
    ])
    d.p("Lo script controlla che le due VM esistano e siano spente, poi produce "
        "`corso-cyber-lab.ova`. Se le tue VM hanno nomi diversi da `kali-studente` e "
        "`target-ubuntu`, passali come parametri (vedi l'intestazione dello script).")

    d.h1("Immagine del docente (a parte)")
    d.p("Per avere la cartella con le soluzioni sulla tua Kali personale, rifai il Passo 1 "
        "in una VM separata usando il ruolo `docente`:")
    d.code(["sudo ./bin/provision-kali.sh docente"])
    d.p("Aggiunge `/root/soluzioni`. Questa immagine NON va nell'OVA degli studenti: "
        "esportala a parte e tienila per te.")

    d.h1("Distribuzione e uso in aula")
    d.box("verde", "Istruzioni per gli studenti (da consegnare)", items=[
        "Copia il file `corso-cyber-lab.ova` sul tuo PC.",
        "Apri VirtualBox: File > Importa applicazione, scegli il file .ova, conferma.",
        "Vengono create due VM: `kali-studente` e `target-ubuntu`. Avviale entrambe.",
        "Accedi alla Kali (utente `kali`). Per ogni lezione: prima sul bersaglio "
        "`lab NN`, poi sulla Kali `lab NN` (NN = numero lezione a due cifre).",
        "Se un comando `lab` non trova la lezione, controlla la connessione della Kali "
        "(scheda NAT attiva).",
    ])
    d.p("In aula la Kali tiene la scheda NAT attiva (le serve per scaricare gli script "
        "con `lab`); il bersaglio ha internet solo al momento del setup, poi resta "
        "isolato. Per il blocco malware (Lezioni 31-34) si stacca internet anche dalla "
        "Kali.")

    d.h1("Se qualcosa non funziona (troubleshooting)")
    d.table(["Sintomo", "Causa probabile e rimedio"], [
        ["L'OVA importato non si avvia sui PC dell'aula", "l'OVA è stato costruito su "
         "un'architettura diversa (ARM invece di x86): ricostruiscilo su una macchina x86"],
        ["Le due VM non si vedono in rete", "la Scheda 2 non è 'Rete interna' con lo "
         "stesso nome `labnet` su ENTRAMBE; correggi e riavvia"],
        ["`lab` non scarica gli script", "la Kali non ha internet: attiva la Scheda 1 NAT"],
        ["DVWA non parte sul bersaglio", "se sei su ARM è atteso; su x86 verifica "
         "`docker ps` e `docker logs`"],
        ["`lab` dà errore 'Cannot fork'", "il file `bin/lab` ha fine riga CRLF: usa la "
         "versione del repository (fine riga LF)"],
        ["Poca RAM, le VM sono lente", "tieni il bersaglio senza grafica; chiudi altri "
         "programmi; servono circa 7 GB liberi"],
    ], widths=[3400, 5626])

    d.h1("Riepilogo del flusso")
    d.numbered([
        "Su una macchina x86: crea le due VM con le due schede di rete (NAT + labnet).",
        "Provisiona Kali (`provision-kali.sh studente`) e bersaglio (`provision-target.sh`), "
        "installa `lab`, imposta `/etc/lab-role`.",
        "Verifica con la checklist (Passo 3).",
        "Spegni tutto ed esporta in `corso-cyber-lab.ova`.",
        "Distribuisci l'OVA agli studenti; loro importano e avviano.",
        "Immagine docente a parte con `provision-kali.sh docente`.",
    ])

    d.h1("Appendice · Costruire con UTM sul Mac e portare su Windows")
    d.p("Se hai solo un Mac Apple Silicon, puoi comunque produrre un'immagine x86 usando "
        "UTM, ma con un vincolo preciso e qualche passaggio. In molti casi resta piu' "
        "semplice installare direttamente su un PC Windows x86 (gli script fanno tutto il "
        "lavoro); valuta questa strada solo se non hai un PC x86 a disposizione.")
    d.box("rosso", "La condizione che rende tutto possibile", items=[
        "UTM 'Virtualizza' = solo guest ARM64 (veloce) e NON usabile su Windows x86.",
        "UTM 'Emula' = puo' fare guest x86-64 (lento) e QUESTO gira su Windows.",
        "Quindi in UTM devi creare la VM in modalita' EMULAZIONE, architettura x86_64.",
    ])
    d.h2("Procedura")
    d.numbered([
        "UTM: Crea VM > Emula > Architettura x86_64 > installa Kali/Ubuntu Server da ISO "
        "x86-64.",
        "Firmware: se puoi installa in BIOS/Legacy (combacia col default di VirtualBox); "
        "se usi UEFI, dovrai abilitare EFI in VirtualBox, altrimenti non si avvia.",
        "Consiglio: in UTM fai solo l'installazione base del sistema; il provisioning "
        "(che vuole internet e la seconda scheda) fallo dopo, su VirtualBox in Windows.",
        "Spegni la VM. Trova i dischi nel bundle .utm (tasto destro > Mostra contenuto "
        "pacchetto > Data/*.qcow2).",
        "Converti ogni disco in formato VirtualBox (serve qemu-img: `brew install qemu`):",
    ])
    d.code([
        "qemu-img convert -O vdi Data/disco.qcow2 kali.vdi",
        "# (in alternativa -O vmdk per VMware, -O vhdx per Hyper-V)",
    ])
    d.numbered([
        "Copia i file .vdi sul PC Windows.",
        "VirtualBox (Windows): Nuova VM (Linux 64-bit) > 'Usa un file di disco esistente' "
        "> scegli il .vdi. Ripeti per il bersaglio.",
        "Configura le due schede (Scheda 1 NAT, Scheda 2 Rete interna `labnet`); abilita "
        "EFI se avevi installato in UEFI.",
        "Avvia, esegui provision-*.sh + installa `lab` + `/etc/lab-role` se non fatti, "
        "verifica ed esporta l'OVA da Windows.",
    ])
    d.box("verde", "Insidie da conoscere", items=[
        "L'emulazione x86 in UTM sul Mac e' lenta (installazione da zero emulata).",
        "UTM non esporta in OVA: il disco va convertito a mano con qemu-img.",
        "Il firmware EFI/BIOS deve combaciare tra UTM e VirtualBox, altrimenti non avvia.",
        "Rete e controller disco si riconfigurano comunque in VirtualBox.",
        "Vantaggio: i guest sono Linux, quindi si spostano tra hypervisor molto meglio di "
        "un guest Windows; gli script rilevano da soli la scheda interna, quindi il "
        "cambio di nome interfaccia non e' un problema.",
    ])
    d.p("In sintesi: si puo' fare, ma tra emulazione lenta, conversione del disco e "
        "firmware da far combaciare, spesso conviene costruire l'immagine finale "
        "direttamente su un PC x86. UTM resta ottimo (in ARM, veloce) per provare prima "
        "che gli script funzionino.")

    out = os.path.join(HERE, "..", "lezioni", "Lezioni", "Guida-Setup-Laboratorio.docx")
    d.save(out)
    return out


if __name__ == "__main__":
    p = build()
    print("[OK]", os.path.abspath(p))
