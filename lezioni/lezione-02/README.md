# Lezione 2 · costruzione dell'ambiente e file di supporto

Cartella di lavoro della Lezione 2. Contiene sia gli script che gli studenti
lanciano in aula con `lab 2`, sia gli strumenti che servono al docente per
costruire l'immagine una volta sola ed esportarla in un unico OVA.

## File in questa cartella

| File | A chi serve | Cosa fa |
|---|---|---|
| `kali.sh` | studenti (via `lab 2`) | diagnostica lato Kali: verifica IP, ping e app. Assegna la flag `FLAG{la_rete_e_viva}` |
| `target.sh` | studenti (via `lab 2`) | accende le app vulnerabili sul bersaglio e ne mostra lo stato |
| `costruisci-ova.ps1` | docente (Windows) | esporta le due VM in un unico OVA con VirtualBox |
| `costruisci-ova.sh` | docente (Linux) | come sopra, per un host Linux |

Gli script di **costruzione** dell'immagine base (`provision-kali.sh` e
`provision-target.sh`) stanno nella cartella `bin/` del repository, perche'
sono condivisi da tutte le lezioni e si eseguono una volta sola.

---

## Come si costruisce l'ambiente (una volta sola)

Da fare sulla postazione Windows di produzione (x86), perche' l'aula e' x86 e
alcune app vulnerabili non partono su ARM. Il Mac con Parallels serve solo come
banco di prova del flusso.

### Passo 1 · VM Kali (attaccante)

1. Crea la VM Kali in VirtualBox e installa Kali Linux (o parti dalla
   immagine ufficiale VirtualBox).
2. Configura DUE schede di rete:
   - Scheda 1: NAT (da' internet, serve a scaricare gli script con `lab`)
   - Scheda 2: Rete interna, nome `labnet`
3. Avvia la VM e, con internet attivo, lancia il provisioning:
   ```bash
   sudo ./bin/provision-kali.sh studente
   ```
   Installa gli strumenti, imposta l'IP interno `10.10.10.5`, copia le flag
   introduttive e il launcher.
4. Installa il launcher `lab` (una riga, una volta sola):
   ```bash
   sudo install -m 755 bin/lab /usr/local/bin/lab
   echo kali | sudo tee /etc/lab-role
   ```

### Passo 2 · VM bersaglio (target)

1. Crea la VM Ubuntu Server (senza interfaccia grafica, per risparmiare RAM).
2. Configura DUE schede di rete:
   - Scheda 1: NAT (serve solo ora, per scaricare le immagini Docker)
   - Scheda 2: Rete interna, nome `labnet`
3. Avvia la VM e, con internet attivo, lancia il provisioning:
   ```bash
   sudo ./bin/provision-target.sh
   ```
   Installa Docker, imposta l'IP interno `10.10.10.20`, scarica DVWA, Juice
   Shop e nginx, avvia le app e la pagina "Banca della Scuola".
4. Installa il launcher anche qui:
   ```bash
   sudo install -m 755 bin/lab /usr/local/bin/lab
   echo target | sudo tee /etc/lab-role
   ```

### Passo 3 · verifica prima dell'export

Esegui la checklist qui sotto. Se tutto e' verde, spegni ENTRAMBE le VM
(`sudo poweroff`).

### Passo 4 · export in un unico OVA

Sulla postazione Windows, in PowerShell, dalla cartella del repository:
```powershell
.\lezioni\lezione-02\costruisci-ova.ps1
```
Su Linux:
```bash
./lezioni/lezione-02/costruisci-ova.sh
```
Lo script controlla che le due VM esistano e siano spente, poi produce
`corso-cyber-lab.ova` (contiene entrambe le VM). Se le tue VM hanno nomi
diversi da `kali-studente` e `target-ubuntu`, passali come parametri (vedi
l'intestazione dello script).

> Immagine docente: ripeti il Passo 1 con `provision-kali.sh docente` in una VM
> separata (aggiunge `/root/soluzioni`) ed esportala a parte. Non va nell'OVA
> degli studenti.

---

## Checklist di verifica (prima di esportare)

### Sulla Kali
```bash
ip -4 addr | grep 10.10.10.5        # deve comparire l'IP interno
nmap --version                       # gli strumenti sono installati
id kali | grep wireshark             # utente nel gruppo wireshark
cat /etc/lab-role                    # deve dire: kali
ping -c1 10.10.10.20                 # (col target acceso) il bersaglio risponde
```

### Sul bersaglio
```bash
ip -4 addr | grep 10.10.10.20        # deve comparire l'IP interno
docker ps                            # dvwa, juiceshop e banca in stato "Up"
docker image inspect nginx:alpine >/dev/null && echo "nginx in cache OK"
curl -s localhost:8081 | head -n1    # DVWA risponde
curl -s localhost:8082 | head -n1    # Juice Shop risponde
curl -s localhost:8080 | grep FLAG   # Banca della Scuola risponde
cat /etc/lab-role                    # deve dire: target
```

### Prova incrociata (dalla Kali, col target acceso)
```bash
lab 2                                # deve chiudersi con FLAG{la_rete_e_viva}
```

### Prima dell'export
- [ ] Entrambe le VM spente (`poweroff`, non solo sospese)
- [ ] Kali: scheda 1 NAT + scheda 2 Rete interna `labnet`
- [ ] Bersaglio: scheda 1 NAT + scheda 2 Rete interna `labnet`
- [ ] RAM per postazione: circa 7 GB liberi (host 3, Kali 2,5, target 1,5)

---

## Nota sul repository pubblico

I file Word delle lezioni stanno in `lezioni/Lezioni/` e non vanno pubblicati
sul repo pubblico. Se il repo e' pubblico, aggiungi a `.gitignore`:
```
lezioni/Lezioni/
*.ova
```
Dalle sfide vere in poi, tieni i VALORI delle flag fuori dal repo pubblico
(repo privato o flag generate a runtime).
