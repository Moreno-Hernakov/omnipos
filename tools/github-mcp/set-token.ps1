<#
.SYNOPSIS
    Simpan Personal Access Token GitHub ke .omp/github-token setelah divalidasi.

.DESCRIPTION
    Token disimpan hanya kalau lolos dua pemeriksaan:
      1. Token valid (GET /user tidak membalas 401).
      2. Akun pemilik token punya izin tulis (push) pada repositori tujuan.

    Tanpa izin tulis, issue tetap bisa dibuat di repo publik tetapi tercatat atas
    nama akun yang salah, dan milestone selalu gagal 404. Karena itu token tanpa
    push access ditolak, bukan disimpan.

    Berkas hasil: .omp/github-token (di-ignore .gitignore). Dibaca lebih dulu oleh
    get-token.sh dan github-auth.ps1, di atas environment variable dan kredensial
    git tersimpan.

.PARAMETER Token
    PAT yang akan disimpan. Kalau kosong, diminta lewat prompt tersembunyi.

.PARAMETER Owner
    Pemilik repositori. Default: Moreno-Hernakov.

.PARAMETER Repo
    Nama repositori. Default: omnipos.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\set-token.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\set-token.ps1 -Token "ghp_xxxxxxxxxxxx"
#>
param(
    [string]$Token,
    [string]$Owner = 'Moreno-Hernakov',
    [string]$Repo  = 'omnipos'
)

$ErrorActionPreference = 'Stop'

$repoRoot  = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$tokenPath = Join-Path $repoRoot '.omp/github-token'

if (-not $Token) {
    $secure = Read-Host -Prompt 'Tempel PAT GitHub (tidak ditampilkan)' -AsSecureString
    $bstr   = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try   { $Token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
}

$Token = $Token.Trim()
if (-not $Token) { throw 'Token kosong. Tidak ada yang disimpan.' }

. "$PSScriptRoot/github-auth.ps1"
$headers = New-GitHubHeaders -Token $Token

# --- 1. Token valid? ---
try {
    $user = Invoke-RestMethod -Uri 'https://api.github.com/user' -Headers $headers
}
catch {
    $status = $_.Exception.Response.StatusCode.value__
    if ($status -eq 401) { throw 'Token ditolak GitHub (401). Salah ketik, sudah dicabut, atau kedaluwarsa.' }
    throw
}

# --- 2. Punya izin tulis di repo tujuan? ---
try {
    $repoInfo = Invoke-RestMethod -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers
}
catch {
    $status = $_.Exception.Response.StatusCode.value__
    if ($status -eq 404) {
        throw "Token milik '$($user.login)' tidak bisa melihat $Owner/$Repo. Repo privat, atau nama owner/repo salah."
    }
    throw
}

$perm = $repoInfo.permissions
if (-not $perm.push) {
    throw @"
Token milik '$($user.login)' hanya punya akses BACA ke $Owner/$Repo.
Tanpa izin tulis: issue tercatat atas nama akun itu, dan milestone gagal 404.
Token tidak disimpan.

Buat PAT dari akun pemilik repo ($Owner), scope 'repo' untuk classic
atau Issues+Contents+Pull requests read/write untuk fine-grained.
"@
}

# --- 3. Simpan ---
$dir = Split-Path -Parent $tokenPath
if (-not (Test-Path $dir)) { $null = New-Item -ItemType Directory -Path $dir -Force }

[System.IO.File]::WriteAllText($tokenPath, $Token, (New-Object System.Text.UTF8Encoding($false)))

# Batasi akses berkas ke user saat ini saja. Gagal di sini tidak membatalkan penyimpanan.
try {
    $me = "$env:USERDOMAIN\$env:USERNAME"
    $null = icacls $tokenPath /inheritance:r /grant:r "${me}:F" 2>&1
}
catch { }

$level = if ($perm.admin) { 'admin' } elseif ($perm.maintain) { 'maintain' } else { 'write' }
Write-Host "Tersimpan : $tokenPath"
Write-Host "Akun      : $($user.login)"
Write-Host "Repositori: $($repoInfo.full_name)"
Write-Host "Izin      : $level"

if ($user.login -ne $Owner) {
    Write-Host ''
    Write-Host "Peringatan: akun token bukan pemilik repo ($Owner)."
    Write-Host 'Issue akan tercatat atas nama akun ini meski punya izin tulis.'
}

Write-Host ''
Write-Host 'Restart sesi omp agar MCP memuat token baru (token dibaca saat server di-spawn).'
Write-Host 'Verifikasi: powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action whoami'
