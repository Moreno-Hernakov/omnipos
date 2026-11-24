<#
.SYNOPSIS
    Sinkronkan status task di docs/02-TASKS.md dengan issue GitHub.

.DESCRIPTION
    docs/02-TASKS.md adalah sumber utama yang dibaca manusia; issue GitHub adalah
    sumber kebenaran untuk status. Skrip ini menyamakan keduanya.

    Penanda status di dokumen memakai emoji, bukan checkbox markdown, karena
    checkbox di dalam sel tabel tidak dirender GitHub:
        U+2705  centang hijau  = selesai
        U+2B1C  kotak putih    = belum selesai

    Pencocokan memakai ID task di judul issue, format: [T-22] Judul task.
    Baris tabel dicari lewat kolom ID, lalu penanda di kolom Status diubah.

    Arah sinkronisasi:
      toDoc    — GitHub -> dokumen. Issue closed menjadi centang, open menjadi kotak.
      toGitHub — dokumen -> GitHub. Centang menutup issue, kotak membuka.
      check    — hanya laporkan perbedaan, tidak menulis apa pun.

.PARAMETER Direction
    toDoc (default), toGitHub, atau check.

.PARAMETER Owner
    Pemilik repositori. Default: Moreno-Hernakov.

.PARAMETER Repo
    Nama repositori. Default: omnipos.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1 -Direction check

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1 -Direction toGitHub
#>
param(
    [ValidateSet('toDoc', 'toGitHub', 'check')]
    [string]$Direction = 'toDoc',

    [string]$Owner = 'Moreno-Hernakov',
    [string]$Repo  = 'omnipos'
)

$ErrorActionPreference = 'Stop'

# Ditulis lewat kode karakter supaya berkas skrip ini tidak bergantung pada
# encoding yang dipakai saat menyimpan.
$DONE = [string][char]0x2705   # centang hijau
$TODO = [string][char]0x2B1C   # kotak putih

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$docPath  = Join-Path $repoRoot 'docs/02-TASKS.md'

if (-not (Test-Path $docPath)) {
    throw "File tidak ditemukan: $docPath. Jalankan skrip dari dalam repo UAS_POS."
}

. "$PSScriptRoot/github-auth.ps1"

$headers = New-GitHubHeaders -Token (Get-GitHubToken)

function Get-AllIssues {
    $all = @()
    $page = 1
    while ($true) {
        $batch = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/issues?state=all&per_page=100&page=$page" -Headers $headers
        if (-not $batch) { break }
        $all += $batch
        if ($batch.Count -lt 100) { break }
        $page++
    }
    # Pull request juga muncul di endpoint issues; abaikan.
    return $all | Where-Object { -not $_.pull_request }
}

# --- Baca dokumen: kumpulkan baris task (ID + status) ---
# Dibaca sebagai UTF-8 tanpa BOM supaya emoji tidak rusak.
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$lines = [System.IO.File]::ReadAllLines($docPath, $utf8NoBom)

$docTasks = @{}   # ID -> @{ LineIndex = n; Done = bool }
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\|\s*(T-\d+)\s*\|(.*)$') {
        $id  = $Matches[1]
        $rest = $Matches[2]
        # Kolom Status adalah kolom kelima; cari emoji penanda di baris itu.
        if ($rest.Contains($DONE)) {
            $docTasks[$id] = @{ LineIndex = $i; Done = $true }
        } elseif ($rest.Contains($TODO)) {
            $docTasks[$id] = @{ LineIndex = $i; Done = $false }
        }
    }
}

if ($docTasks.Count -eq 0) {
    throw "Tidak ada baris task dengan penanda emoji di $docPath. Kolom Status harus berisi $DONE atau $TODO."
}

# --- Baca GitHub: petakan ID task ke status issue ---
$issues = Get-AllIssues
$ghTasks = @{}
foreach ($issue in $issues) {
    if ($issue.title -match '^\[(T-\d+)\]') {
        $ghTasks[$Matches[1]] = @{
            Number = $issue.number
            Closed = ($issue.state -eq 'closed')
            Title  = $issue.title
        }
    }
}

# --- Bandingkan ---
$onlyDoc = $docTasks.Keys | Where-Object { -not $ghTasks.ContainsKey($_) } | Sort-Object
$onlyGh  = $ghTasks.Keys | Where-Object { -not $docTasks.ContainsKey($_) } | Sort-Object
$drift   = @()
foreach ($id in ($docTasks.Keys | Sort-Object)) {
    if (-not $ghTasks.ContainsKey($id)) { continue }
    if ($docTasks[$id].Done -ne $ghTasks[$id].Closed) {
        $drift += $id
    }
}

Write-Host "Dokumen : $($docTasks.Count) task"
Write-Host "GitHub  : $($ghTasks.Count) issue bertanda [T-xx]"

if ($onlyDoc) { Write-Host "Belum ada issue di GitHub : $($onlyDoc -join ', ')" }
if ($onlyGh)  { Write-Host "Issue tanpa baris di dokumen: $($onlyGh -join ', ')" }
if ($drift)   { Write-Host "Status berbeda            : $($drift -join ', ')" }
if (-not $drift -and -not $onlyDoc -and -not $onlyGh) { Write-Host 'Semua sinkron.' }

if ($Direction -eq 'check') {
    if ($drift.Count -gt 0) { exit 1 }
    exit 0
}

# --- Terapkan ---
$changed = 0

if ($Direction -eq 'toDoc') {
    foreach ($id in $drift) {
        $idx  = $docTasks[$id].LineIndex
        $want = $ghTasks[$id].Closed
        if ($want) {
            $lines[$idx] = $lines[$idx].Replace($TODO, $DONE)
        } else {
            $lines[$idx] = $lines[$idx].Replace($DONE, $TODO)
        }
        $changed++
        Write-Host "  $id -> $(if ($want) { $DONE } else { $TODO })"
    }
}

if ($Direction -eq 'toGitHub') {
    foreach ($id in $drift) {
        $number = $ghTasks[$id].Number
        $wantClosed = $docTasks[$id].Done
        $body = @{ state = $(if ($wantClosed) { 'closed' } else { 'open' }) } | ConvertTo-Json
        Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo/issues/$number" `
            -Method PATCH -Headers $headers -ContentType 'application/json' -Body $body | Out-Null
        $changed++
        Write-Host "  $id (#$number) -> $(if ($wantClosed) { 'closed' } else { 'open' })"
    }
}

if ($changed -gt 0 -and $Direction -eq 'toDoc') {
    [System.IO.File]::WriteAllLines($docPath, $lines, $utf8NoBom)
    Write-Host ''
    Write-Host "Dokumen diperbarui: $changed baris. Commit docs/02-TASKS.md untuk menyimpan."
} elseif ($changed -gt 0) {
    Write-Host ''
    Write-Host "GitHub diperbarui: $changed issue."
} else {
    Write-Host ''
    Write-Host 'Tidak ada perubahan.'
}
