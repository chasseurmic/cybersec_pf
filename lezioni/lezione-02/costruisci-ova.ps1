# costruisci-ova.ps1
# Esporta le DUE VM del laboratorio (Kali + bersaglio) in un UNICO file OVA.
# Da eseguire sulla postazione Windows con VirtualBox, in PowerShell:
#   .\costruisci-ova.ps1
# Parametri opzionali:
#   -Kali   <nome>   nome della VM Kali        (default: kali-studente)
#   -Target <nome>   nome della VM bersaglio   (default: target-ubuntu)
#   -Output <path>   percorso del file .ova     (default: .\corso-cyber-lab.ova)

param(
  [string]$Kali   = "kali-studente",
  [string]$Target = "target-ubuntu",
  [string]$Output = "$PSScriptRoot\corso-cyber-lab.ova"
)
$ErrorActionPreference = "Stop"

# 1) Trova VBoxManage.exe
$vbm = Join-Path $Env:ProgramFiles "Oracle\VirtualBox\VBoxManage.exe"
if (-not (Test-Path $vbm)) {
  $cmd = Get-Command VBoxManage.exe -ErrorAction SilentlyContinue
  if ($cmd) { $vbm = $cmd.Source }
  else { throw "VBoxManage.exe non trovato. Installa VirtualBox o correggi il percorso nello script." }
}

function Get-VMState([string]$name) {
  $info = & $vbm showvminfo $name --machinereadable 2>$null
  if (-not $info) { return $null }
  $riga = $info | Select-String '^VMState='
  if (-not $riga) { return $null }
  return $riga.ToString().Split('=')[1].Trim('"')
}

# 2) Controlli preliminari: le VM esistono e sono spente
foreach ($vm in @($Kali, $Target)) {
  $state = Get-VMState $vm
  if ($null -eq $state) {
    throw "La VM '$vm' non esiste in VirtualBox. Elenca i nomi con:  VBoxManage list vms"
  }
  if ($state -notin @("poweroff", "saved", "aborted")) {
    throw "La VM '$vm' non e' spenta (stato: $state). Spegnila prima di esportare."
  }
  Write-Host "[OK] VM '$vm' presente e spenta (stato: $state)."
}

# 3) Se l'OVA esiste gia', lo sovrascrivo
if (Test-Path $Output) {
  Write-Host "[i] Esiste gia' $Output : lo sovrascrivo."
  Remove-Item $Output -Force
}

# 4) Export delle due VM in un unico OVA
Write-Host "[*] Esporto '$Kali' e '$Target' in un unico file:"
Write-Host "    $Output"
Write-Host "    (l'operazione puo' richiedere diversi minuti)"
& $vbm export $Kali $Target --output $Output --ovf20 --manifest
if ($LASTEXITCODE -ne 0) { throw "Export fallito (codice $LASTEXITCODE)." }

# 5) Verifica finale
if (Test-Path $Output) {
  $mb = [math]::Round((Get-Item $Output).Length / 1MB, 1)
  Write-Host ""
  Write-Host "[OK] Creato l'OVA: $Output  ($mb MB)."
  Write-Host "    Copialo sulle postazioni e importalo con:"
  Write-Host "    VirtualBox > File > Importa applicazione virtuale."
} else {
  throw "Il file OVA non risulta creato."
}
