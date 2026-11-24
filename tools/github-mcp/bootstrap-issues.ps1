<#
.SYNOPSIS
    Buat milestone dan issue GitHub dari docs/02-TASKS.md.

.DESCRIPTION
    Membaca papan task di docs/02-TASKS.md lalu menyamakan GitHub dengannya:
    satu milestone bertanggal untuk seluruh papan, satu issue per baris task.

    Fase sengaja BUKAN milestone. Satu issue hanya bisa punya satu milestone, dan
    milestone adalah satu-satunya objek GitHub yang punya tanggal. Karena itu slot
    itu dipakai untuk deadline pengumpulan, bukan untuk pengelompokan kerja. Fase
    tetap tercatat di body setiap issue dan di heading docs/02-TASKS.md.

    Skrip bersifat idempoten: milestone dicocokkan lewat judul, issue lewat awalan
    ID di judul. Yang sudah ada dilewati, bukan diduplikasi. Judul, body, dan
    milestone issue yang menyimpang dari dokumen diperbaiki di tempat.

    Owner dipetakan lewat tabel $OwnerMap. Nama yang belum punya akses GitHub
    dilaporkan di akhir, issue-nya tetap dibuat tanpa assignee.

    Skrip ini hanya membuat dan mengaitkan. Status buka/tutup tidak diubah di
    sini untuk issue yang sudah ada - itu tugas sync-tasks.ps1.

.PARAMETER DryRun
    Tampilkan rencana tanpa memanggil API yang mengubah apa pun.

.PARAMETER Owner
    Pemilik repositori. Default: Moreno-Hernakov.

.PARAMETER Repo
    Nama repositori. Default: omnipos.

.PARAMETER MilestoneTitle
    Judul milestone tunggal. Default: UAS POS - Pengumpulan.

.PARAMETER MilestoneDue
    Tenggat dalam format YYYY-MM-DD. Default: 2026-11-30.

.PARAMETER MilestoneDescription
    Deskripsi milestone. Default memuat catatan kode beku H-1.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1 -DryRun

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1 -MilestoneDue 2026-12-05
#>
param(
    [switch]$DryRun,
    [string]$Owner = 'Moreno-Hernakov',
    [string]$Repo  = 'omnipos',
    [string]$MilestoneTitle = 'UAS POS - Pengumpulan',
    [string]$MilestoneDue   = '2026-11-30',
    [string]$MilestoneDescription = 'Kode beku 29 Nov. 30 Nov hanya pengemasan: zip, screenshot T-42, data demo final T-40.'
)

$ErrorActionPreference = 'Stop'

if ($MilestoneDue -notmatch '^\d{4}-\d{2}-\d{2}$') {
    throw "MilestoneDue harus format YYYY-MM-DD, bukan '$MilestoneDue'."
}

# Nama di kolom Owner -> login GitHub. Tambah baris di sini kalau ada anggota baru.
# $null berarti akunnya belum punya akses ke repo, issue dibuat tanpa assignee.
$OwnerMap = @{
    'Moreno'              = 'Moreno-Hernakov'
    'Bagas'               = 'Bagas-Rizky'
    'Rangga'              = 'FxRangga'
    'Gregorius Priyagung' = 'gpriyagung633'
    'Valencia'            = 'Valencia0902'
    'Raymond'             = $null
}

$repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$docPath  = Join-Path $repoRoot 'docs/02-TASKS.md'
if (-not (Test-Path $docPath)) { throw "File tidak ditemukan: $docPath" }

. "$PSScriptRoot/github-auth.ps1"
$headers = New-GitHubHeaders -Token (Get-GitHubToken)
$api     = "https://api.github.com/repos/$Owner/$Repo"

$DONE = [string][char]0x2705

# --- Baca dokumen ---
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$lines = [System.IO.File]::ReadAllLines($docPath, $utf8NoBom)

$phase = $null
$tasks = @()
foreach ($line in $lines) {
    if ($line -match '^## (Fase \d+ .+)$') { $phase = $Matches[1].Trim(); continue }
    if ($line -notmatch '^\|\s*(T-\d+)\s*\|') { continue }

    $cells = $line.Split('|')
    if ($cells.Count -lt 7) { continue }
    # [0] kosong, [1] ID, [2] Task, [3] Owner, [4] Depends on, [5] Status, [6] Catatan
    $tasks += [pscustomobject]@{
        Id      = $cells[1].Trim()
        Title   = $cells[2].Trim()
        Owner   = $cells[3].Trim()
        Depends = $cells[4].Trim()
        Status  = $cells[5].Trim()
        Note    = $cells[6].Trim()
        Phase   = $phase
    }
}

if ($tasks.Count -eq 0) { throw "Tidak ada baris task di $docPath" }

$phases = @($tasks | ForEach-Object { $_.Phase } | Where-Object { $_ } | Select-Object -Unique)
Write-Host "Dokumen  : $($tasks.Count) task, $($phases.Count) fase"
if ($DryRun) { Write-Host 'MODE     : DryRun, tidak ada perubahan' }
Write-Host ''

function Get-PagedList {
    param([string]$Uri)
    $all  = @()
    $page = 1
    while ($true) {
        $sep   = if ($Uri.Contains('?')) { '&' } else { '?' }
        $batch = Invoke-RestMethod -Uri "$Uri${sep}per_page=100&page=$page" -Headers $headers
        if (-not $batch) { break }
        $all += $batch
        if ($batch.Count -lt 100) { break }
        $page++
    }
    return $all
}

# PowerShell 5.1 mengirim -Body string sebagai Latin-1, sehingga karakter non-ASCII
# (em dash, emoji) rusak jadi tanda lain atau memicu "Problems parsing JSON".
# Solusi: escape setiap karakter > 127 menjadi \uXXXX supaya JSON murni ASCII,
# lalu kirim sebagai byte ASCII. Tidak ada lagi ambiguitas charset.
function ConvertTo-AsciiJson {
    param($Object)
    $json = $Object | ConvertTo-Json -Depth 5 -Compress
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $json.ToCharArray()) {
        if ([int]$ch -gt 127) { $null = $sb.AppendFormat('\u{0:x4}', [int]$ch) }
        else                  { $null = $sb.Append($ch) }
    }
    return $sb.ToString()
}

function Invoke-GitHubJson {
    param(
        [string]$Uri,
        [string]$Method,
        [hashtable]$Payload
    )
    $bytes = [System.Text.Encoding]::ASCII.GetBytes((ConvertTo-AsciiJson -Object $Payload))
    return Invoke-RestMethod -Uri $Uri -Method $Method -Headers $headers `
        -ContentType 'application/json' -Body $bytes
}

# --- Milestone ---
# Satu milestone bertanggal untuk seluruh papan. Fase bukan milestone: fase
# adalah pengelompokan kerja tanpa tenggat, sementara milestone adalah satu-satunya
# tempat di GitHub yang punya tanggal. Satu issue hanya bisa punya satu milestone,
# jadi slot itu dipakai untuk deadline, bukan untuk fase. Fase tetap tercatat di
# body setiap issue dan di heading docs/02-TASKS.md.
$existingMs = Get-PagedList -Uri "$api/milestones?state=all"

$targetMs = $existingMs | Where-Object { $_.title -eq $MilestoneTitle } | Select-Object -First 1
$wantDue  = $MilestoneDue

if ($targetMs) {
    $patch = @{}
    $currentDue = if ($targetMs.due_on) { ([datetime]$targetMs.due_on).ToString('yyyy-MM-dd') } else { $null }
    if ($currentDue -ne $MilestoneDue) { $patch.due_on = "${MilestoneDue}T23:59:59Z" }
    if ($MilestoneDescription -and $targetMs.description -ne $MilestoneDescription) {
        $patch.description = $MilestoneDescription
    }

    if ($patch.Count -gt 0) {
        if ($DryRun) {
            Write-Host "milestone  PERBAIKI: '$MilestoneTitle' (#$($targetMs.number)) $($patch.Keys -join ', ')"
        }
        else {
            $targetMs = Invoke-GitHubJson -Uri "$api/milestones/$($targetMs.number)" -Method PATCH -Payload $patch
            Write-Host "milestone  perbaiki: '$MilestoneTitle' (#$($targetMs.number)) $($patch.Keys -join ', ')"
        }
    }
    else {
        Write-Host "milestone  ada    : '$MilestoneTitle' (#$($targetMs.number))"
    }
}
elseif ($DryRun) {
    Write-Host "milestone  BUAT   : '$MilestoneTitle' due $MilestoneDue"
    # Sentinel -1: truthy supaya loop issue tetap melaporkan pemindahan, tapi
    # tidak pernah dipakai karena DryRun tidak memanggil API.
    $targetMs = [pscustomobject]@{ number = -1 }
}
else {
    $payload = @{
        title = $MilestoneTitle
        state = 'open'
        due_on = "${MilestoneDue}T23:59:59Z"
    }
    if ($MilestoneDescription) { $payload.description = $MilestoneDescription }
    $targetMs = Invoke-GitHubJson -Uri "$api/milestones" -Method POST -Payload $payload
    Write-Host "milestone  dibuat : '$MilestoneTitle' (#$($targetMs.number)) due $MilestoneDue"
}

$wantMs = if ($targetMs) { $targetMs.number } else { $null }

# --- Issue ---
$existingIssues = Get-PagedList -Uri "$api/issues?state=all"
$issueById = @{}
foreach ($i in $existingIssues) {
    if ($i.pull_request) { continue }
    if ($i.title -match '^\[(T-\d+)\]') { $issueById[$Matches[1]] = $i.number }
}

$created  = 0
$skipped  = 0
$repaired = 0
$unassigned = @()

# Penanda bahwa body sebuah issue dibuat oleh skrip ini. Body yang tidak punya
# penanda ini dianggap tulisan tangan dan tidak pernah ditimpa.
$bodyMarker = 'Sumber: `docs/02-TASKS.md`'

function New-IssueBody {
    param($Task)
    $lines = @(
        "**Task**: $($Task.Title)"
        "**Owner**: $($Task.Owner)"
        "**Depends on**: $($Task.Depends)"
        "**Fase**: $($Task.Phase)"
        ''
        $Task.Note
        ''
        '---'
        $bodyMarker
    )
    return $lines -join "`n"
}

foreach ($t in $tasks) {
    $login = if ($OwnerMap.ContainsKey($t.Owner)) { $OwnerMap[$t.Owner] } else { $null }
    if (-not $login) { $unassigned += "$($t.Id) - $($t.Owner)" }

    $wantTitle = "[$($t.Id)] $($t.Title)"
    $wantBody  = New-IssueBody -Task $t

    if ($issueById.ContainsKey($t.Id)) {
        $num     = $issueById[$t.Id]
        $current = $existingIssues | Where-Object { $_.number -eq $num } | Select-Object -First 1
        $patch   = @{}

        if ($current.title -ne $wantTitle) { $patch.title = $wantTitle }

        # Body hanya disentuh kalau skrip ini yang menulisnya lebih dulu.
        if ($current.body -and $current.body.Contains($bodyMarker) -and $current.body -ne $wantBody) {
            $patch.body = $wantBody
        }

        if ($wantMs -and (-not $current.milestone -or $current.milestone.number -ne $wantMs)) {
            $patch.milestone = $wantMs
        }

        if ($patch.Count -gt 0) {
            if ($DryRun) {
                Write-Host "issue      PERBAIKI: $($t.Id) (#$num) $($patch.Keys -join ', ')"
            }
            else {
                $null = Invoke-GitHubJson -Uri "$api/issues/$num" -Method PATCH -Payload $patch
                Write-Host "issue      perbaiki: $($t.Id) (#$num) $($patch.Keys -join ', ')"
            }
            $repaired++
        }
        else {
            Write-Host "issue      ada    : $($t.Id) (#$num)"
        }
        $skipped++
        continue
    }

    if ($DryRun) {
        $mark = if ($login) { "-> $login" } else { '(tanpa assignee)' }
        Write-Host "issue      BUAT   : $($t.Id) $($t.Title) $mark"
        $created++
        continue
    }

    $payload = @{
        title = $wantTitle
        body  = $wantBody
    }
    if ($wantMs) { $payload.milestone = $wantMs }
    if ($login) { $payload.assignees = @($login) }

    $new = Invoke-GitHubJson -Uri "$api/issues" -Method POST -Payload $payload

    # Task yang sudah selesai di dokumen langsung ditutup agar tidak jadi drift.
    if ($t.Status -eq $DONE) {
        $null = Invoke-GitHubJson -Uri "$api/issues/$($new.number)" -Method PATCH -Payload @{ state = 'closed' }
    }

    $mark = if ($login) { "-> $login" } else { '(tanpa assignee)' }
    Write-Host "issue      dibuat : $($t.Id) (#$($new.number)) $mark"
    $created++
}

Write-Host ''
Write-Host "Ringkasan: $created dibuat, $repaired diperbaiki, $($skipped - $repaired) sudah benar."

if ($unassigned.Count -gt 0) {
    Write-Host ''
    Write-Host 'Tanpa assignee, akunnya belum punya akses ke repo:'
    $unassigned | ForEach-Object { Write-Host "  $_" }
    Write-Host ''
    Write-Host 'Tambahkan sebagai collaborator, lalu jalankan ulang skrip ini.'
}

if (-not $DryRun -and $created -gt 0) {
    Write-Host ''
    Write-Host 'Verifikasi: powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1 -Direction check'
}
