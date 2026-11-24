#!/usr/bin/env bash
# Cetak token GitHub untuk GitHub MCP Server.
# Urutan sumber: .omp/github-token (lokal repo) -> GITHUB_PERSONAL_ACCESS_TOKEN
#                -> GITHUB_TOKEN -> kredensial git tersimpan.
# Dipanggil oleh .omp/mcp.json lewat mekanisme "!command", jadi jangan cetak apa pun selain token.

set -u

# Token khusus repo ini. Tidak di-commit (.gitignore). Menang atas kredensial
# global karena Credential Manager bisa berisi token akun lain (mis. akun kerja).
token_file="$(cd "$(dirname "$0")/../.." && pwd)/.omp/github-token"
if [ -f "$token_file" ]; then
    repo_token=$(tr -d '[:space:]' < "$token_file")
    if [ -n "$repo_token" ]; then
        printf '%s' "$repo_token"
        exit 0
    fi
fi

if [ -n "${GITHUB_PERSONAL_ACCESS_TOKEN:-}" ]; then
    printf '%s' "$GITHUB_PERSONAL_ACCESS_TOKEN"
    exit 0
fi

if [ -n "${GITHUB_TOKEN:-}" ]; then
    printf '%s' "$GITHUB_TOKEN"
    exit 0
fi

token=$(printf 'protocol=https\nhost=github.com\n\n' \
    | git credential fill 2>/dev/null \
    | sed -n 's/^password=//p' \
    | head -n 1)

if [ -z "$token" ]; then
    echo "Token GitHub tidak ditemukan." >&2
    echo "Set GITHUB_PERSONAL_ACCESS_TOKEN, atau simpan kredensial lewat git credential." >&2
    exit 1
fi

printf '%s' "$token"
