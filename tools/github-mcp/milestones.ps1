<#
.SYNOPSIS
    Kelola milestone repositori lewat GitHub REST API.

.DESCRIPTION
    GitHub MCP Server v2.2.0 tidak menyediakan tool milestone: pencarian pada
    katalog toolnya (77 tool dengan --toolsets all) tidak menemukan satu pun tool
    bernama *milestone*. Tool `issue_write` hanya menerima nomor milestone yang
    sudah ada, jadi pembuatan milestone harus lewat REST API.

    Skrip ini mengisi celah tersebut memakai token yang sama dengan MCP server.
    Urutan sumber token: GITHUB_PERSONAL_ACCESS_TOKEN -> GITHUB_TOKEN ->
    kredensial git tersimpan untuk github.com.

.PARAMETER Action
    list   — tampilkan semua milestone beserta nomor dan jumlah issue.
    create — buat milestone baru (-Title wajib).
    assign — pasang milestone ke issue (-Issue dan -Milestone wajib).

.PARAMETER Owner
    Pemilik repositori. Default: Moreno-Hernakov.

.PARAMETER Repo
    Nama repositori. Default: omnipos.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action list

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action create `
        -Title 'Fase 0 — Fondasi' -Description 'Arsitektur, skema, koneksi' -DueOn '2026-12-05'

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action assign -Issue 7 -Milestone 1
#>
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('list', 'create', 'assign', 'whoami')]
    [string]$Action,

    [string]$Owner = 'Moreno-Hernakov',
    [string]$Repo  = 'omnipos',

    [string]$Title,
    [string]$Description,
    [string]$DueOn,

    [int]$Issue,
    [int]$Milestone
)

$ErrorActionPreference = 'Stop'

. "$PSScriptRoot/github-auth.ps1"

$token   = Get-GitHubToken
$headers = New-GitHubHeaders -Token $token
$base = "https://api.github.com/repos/$Owner/$Repo/milestones"

function Invoke-GitHub {
    param([string]$Uri, [string]$Method = 'GET', [hashtable]$Body)

    $params = @{ Uri = $Uri; Headers = $headers; Method = $Method; ContentType = 'application/json' }
    if ($Body) { $params.Body = ($Body | ConvertTo-Json -Depth 5) }

    try {
        return Invoke-RestMethod @params
    }
    catch {
        $status = $_.Exception.Response.StatusCode.value__
        if ($status -eq 404) {
            throw "404 dari $Uri. Penyebab paling sering: token tidak punya izin tulis (butuh scope 'repo' dan akses push) pada repositori $Owner/$Repo."
        }
        throw
    }
}

switch ($Action) {
    'whoami' {
        # Menampilkan akun pemilik token yang sedang dipakai. Kalau bukan pemilik
        # repo, issue akan tercatat atas nama akun itu dan milestone pasti 404.
        $user = Invoke-RestMethod -Uri 'https://api.github.com/user' -Headers $headers
        $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers
        $perm = $repoInfo.permissions
        $level = if ($perm.admin) { 'admin' } elseif ($perm.maintain) { 'maintain' } elseif ($perm.push) { 'write' } elseif ($perm.triage) { 'triage' } else { 'read' }
        Write-Host "Akun token : $($user.login)"
        Write-Host "Repositori : $($repoInfo.full_name)"
        Write-Host "Izin       : $level"
        if (-not $perm.push) {
            Write-Host ''
            Write-Host 'Izin tulis tidak ada. Akibatnya:'
            Write-Host '  - Issue yang dibuat tercatat atas nama akun ini, bukan pemilik repo.'
            Write-Host '  - Milestone tidak bisa dibuat (REST membalas 404).'
            Write-Host ''
            Write-Host 'Perbaikan: isi .omp/github-token dengan PAT milik Moreno-Hernakov,'
            Write-Host 'atau set GITHUB_PERSONAL_ACCESS_TOKEN dari akun tersebut.'
        }
    }

    'list' {
        $items = Invoke-GitHub -Uri "$base`?state=all&per_page=100"
        if (-not $items) {
            Write-Host "Belum ada milestone di $Owner/$Repo."
            break
        }
        $items |
            Select-Object number, title, state, due_on,
                @{ n = 'open_issues';  e = { $_.open_issues } },
                @{ n = 'closed_issues'; e = { $_.closed_issues } } |
            Format-Table -AutoSize
    }

    'create' {
        if (-not $Title) { throw '-Title wajib untuk -Action create.' }

        $body = @{ title = $Title; state = 'open' }
        if ($Description) { $body.description = $Description }
        if ($DueOn)       { $body.due_on      = $DueOn }

        $created = Invoke-GitHub -Uri $base -Method POST -Body $body
        Write-Host "Milestone dibuat: #$($created.number) $($created.title)"
        Write-Host $created.html_url
    }

    'assign' {
        if (-not $Issue)     { throw '-Issue wajib untuk -Action assign.' }
        if (-not $Milestone) { throw '-Milestone wajib untuk -Action assign.' }

        $body = @{ milestone = $Milestone }
        $updated = Invoke-GitHub -Uri "https://api.github.com/repos/$Owner/$Repo/issues/$Issue" -Method PATCH -Body $body

        # GitHub membalas 200 tetapi diam-diam mengabaikan nomor milestone yang tidak ada,
        # jadi hasilnya harus diperiksa ulang dari respons, bukan dari status HTTP.
        if (-not $updated.milestone -or $updated.milestone.number -ne $Milestone) {
            $ada = (Invoke-GitHub -Uri "$base`?state=all&per_page=100") | ForEach-Object { "#$($_.number) $($_.title)" }
            $daftar = if ($ada) { $ada -join ', ' } else { '(tidak ada)' }
            throw "Milestone #$Milestone tidak terpasang ke issue #$Issue. GitHub mengabaikan nomor yang tidak ada. Milestone yang tersedia: $daftar"
        }

        Write-Host "Issue #$($updated.number) dipasang ke milestone #$Milestone ($($updated.milestone.title))."
        Write-Host $updated.html_url
    }
}
