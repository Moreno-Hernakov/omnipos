<#
.SYNOPSIS
    Fungsi bersama untuk mengambil token GitHub di skrip PowerShell proyek ini.

.DESCRIPTION
    Di-dot-source oleh milestones.ps1 dan sync-tasks.ps1:

        . "$PSScriptRoot/github-auth.ps1"
        $token = Get-GitHubToken

    Urutan sumber: GITHUB_PERSONAL_ACCESS_TOKEN -> GITHUB_TOKEN -> kredensial git.

    Catatan teknis: `git credential fill` membaca stdin sampai baris kosong.
    Pipe PowerShell 5.1 ke proses native tidak menutup baris dengan benar, sehingga
    git melaporkan "refusing to work with credential missing protocol field".
    Karena itu input dikirim lewat file sementara dan redirect cmd.exe, yang terbukti
    mengirim baris utuh. File sementara hanya berisi protocol dan host, tanpa rahasia,
    dan selalu dihapus di blok finally.
#>

function Get-GitHubToken {
    # Token khusus repo ini, tidak di-commit. Menang atas kredensial global
    # karena Credential Manager bisa berisi token akun lain (mis. akun kerja).
    $tokenFile = Join-Path (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)) '.omp/github-token'
    if (Test-Path $tokenFile) {
        $repoToken = (Get-Content -Raw -Path $tokenFile).Trim()
        if ($repoToken) { return $repoToken }
    }

    if ($env:GITHUB_PERSONAL_ACCESS_TOKEN) { return $env:GITHUB_PERSONAL_ACCESS_TOKEN }
    if ($env:GITHUB_TOKEN) { return $env:GITHUB_TOKEN }

    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw 'git tidak ditemukan di PATH. Set GITHUB_PERSONAL_ACCESS_TOKEN sebagai gantinya.'
    }

    $queryFile = [System.IO.Path]::GetTempFileName()
    $outFile   = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllText($queryFile, "protocol=https`nhost=github.com`n`n")

        # Redirect lewat cmd.exe: PowerShell tidak bisa menutup baris terakhir
        # saat mem-pipe ke proses native, dan git menolak input yang tidak utuh.
        $cmdLine = 'git credential fill < "{0}" > "{1}" 2>nul' -f $queryFile, $outFile
        $null = cmd.exe /c $cmdLine

        foreach ($line in [System.IO.File]::ReadAllLines($outFile)) {
            if ($line -like 'password=*') {
                $token = $line.Substring(9).Trim()
                if ($token) { return $token }
            }
        }

        throw 'Kredensial GitHub tidak ditemukan. Set GITHUB_PERSONAL_ACCESS_TOKEN, atau simpan kredensial lewat git (credential.helper manager-core).'
    }
    finally {
        Remove-Item $queryFile -Force -ErrorAction SilentlyContinue
        Remove-Item $outFile -Force -ErrorAction SilentlyContinue
    }
}

function New-GitHubHeaders {
    param([string]$Token)

    return @{
        Authorization          = "Bearer $Token"
        Accept                 = 'application/vnd.github+json'
        'X-GitHub-Api-Version' = '2022-11-28'
    }
}
