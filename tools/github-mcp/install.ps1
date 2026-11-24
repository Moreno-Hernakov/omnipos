<#
.SYNOPSIS
    Unduh dan pasang GitHub MCP Server (binary Windows x64) ke tools/github-mcp/.

.DESCRIPTION
    Binary tidak di-commit ke Git karena ukurannya ~30 MB. Setiap anggota tim
    menjalankan skrip ini sekali setelah clone.

    Versi dipatok dan checksum SHA-256 diverifikasi sebelum file diekstrak.
    Kalau checksum tidak cocok, skrip berhenti dan tidak memasang apa pun.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\install.ps1

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\github-mcp\install.ps1 -Force
#>
param(
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# --- Versi dan checksum dipatok (lihat rilis: https://github.com/github/github-mcp-server/releases) ---
$Version  = '2.2.0'
$Archive  = 'github-mcp-server_Windows_x86_64.zip'
$Sha256   = '6ecda644e8ea54b26acbc76e80379f4afb6ac1a4c2521366584f2a7f23e3a850'
$ExeName  = 'github-mcp-server.exe'
$BaseUrl  = "https://github.com/github/github-mcp-server/releases/download/v$Version"

$ToolDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ExePath = Join-Path $ToolDir $ExeName

if ((Test-Path $ExePath) -and -not $Force) {
    $current = (& $ExePath --version 2>&1) -join ' '
    Write-Host "Sudah terpasang: $current"
    Write-Host "Pakai -Force untuk memasang ulang."
    exit 0
}

$zipPath = Join-Path $env:TEMP $Archive
Write-Host "Mengunduh GitHub MCP Server v$Version ..."
Invoke-WebRequest -Uri "$BaseUrl/$Archive" -OutFile $zipPath -UseBasicParsing

$actual = (Get-FileHash -Path $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($actual -ne $Sha256) {
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    throw "Checksum tidak cocok. Diharapkan $Sha256, didapat $actual. Unduhan dibatalkan."
}
Write-Host 'Checksum SHA-256 cocok.'

Write-Host 'Mengekstrak ...'
Expand-Archive -Path $zipPath -DestinationPath $ToolDir -Force
Remove-Item $zipPath -Force -ErrorAction SilentlyContinue

if (-not (Test-Path $ExePath)) {
    throw "Ekstraksi selesai tetapi $ExeName tidak ditemukan di $ToolDir."
}

Write-Host ''
& $ExePath --version
Write-Host ''
Write-Host "Terpasang di: $ExePath"
Write-Host 'Langkah berikutnya: baca docs/09-GITHUB-MCP.md bagian "Menyiapkan token".'
