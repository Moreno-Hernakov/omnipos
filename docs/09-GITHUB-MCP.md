# Panduan GitHub MCP Server

Panduan memasang, memakai, dan merawat **GitHub MCP Server** di repositori ini. Dokumen ini untuk seluruh anggota tim, bukan hanya pemilik repo.

Repo: `https://github.com/Moreno-Hernakov/omnipos`

---

## 1. Ini Apa dan Untuk Apa

**MCP (Model Context Protocol)** adalah protokol yang menghubungkan asisten AI (Claude Code, omp, Cursor, VS Code Copilot, Codex, dll.) ke layanan luar. **GitHub MCP Server** adalah server resmi GitHub yang membuka repositori, issue, pull request, dan workflow ke asisten AI lewat protokol itu.

Praktisnya, dengan server ini asisten AI bisa membaca kode di GitHub, membuat dan memperbarui issue, membuka pull request, membaca log GitHub Actions, dan mencari kode — tanpa kamu menyalin-tempel manual.

**Yang dipakai di proyek ini:** milestone, issue, pull request, label, dan pembacaan repositori. Lihat bagian 5 soal batasan milestone.

---

## 2. Prasyarat

| Kebutuhan | Keterangan |
| :--- | :--- |
| Windows x64 | Binary yang dipasang adalah `Windows_x86_64` |
| Git | Untuk mengambil token dari kredensial tersimpan (opsional, lihat bagian 4) |
| PowerShell | Sudah ada di Windows; dipakai skrip pemasangan dan milestone |
| Akun GitHub | Punya akses ke repositori `Moreno-Hernakov/omnipos` |
| MCP host | Salah satu: Claude Code, omp, Cursor, VS Code (Copilot), Codex, Windsurf, Zed |

Docker **tidak** dibutuhkan. Proyek ini memakai binary native, bukan container.

---

## 3. Pemasangan

### 3.1 Unduh binary

Binary tidak di-commit karena ukurannya ~30 MB. Jalankan sekali setelah clone:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\install.ps1
```

Skrip akan:
1. Mengunduh `github-mcp-server_Windows_x86_64.zip` versi **2.2.0** dari rilis resmi GitHub.
2. Memverifikasi checksum SHA-256 (`6ecda644...3a850`). Kalau tidak cocok, pemasangan dibatalkan.
3. Mengekstrak `github-mcp-server.exe` ke `tools/github-mcp/`.

Memasang ulang atau memaksa versi terpasang ditimpa:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\install.ps1 -Force
```

Cek hasil:

```powershell
tools\github-mcp\github-mcp-server.exe --version
```

Keluaran yang diharapkan:

```text
GitHub MCP Server
Version: 2.2.0
```

### 3.2 Konfigurasi MCP host

Konfigurasi proyek sudah disiapkan di `.omp/mcp.json` untuk **omp**. Anggota yang memakai host lain menambahkan entri berikut ke file konfigurasi host masing-masing.

Isi `.omp/mcp.json`:

```json
{
  "$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json",
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "tools/github-mcp/github-mcp-server.exe",
      "args": [
        "stdio",
        "--toolsets",
        "context,repos,issues,pull_requests,labels,users"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "!bash tools/github-mcp/get-token.sh"
      }
    }
  }
}
```

Catatan penting soal konfigurasi ini:

- **`command` relatif terhadap root repo.** Server dijalankan dengan direktori kerja root repo, jadi `tools/github-mcp/...` selalu menemukan binary tanpa path absolut per-mesin. Ini yang membuat konfigurasi bisa dibagi ke seluruh tim.
- **Token tidak pernah ditulis di file.** Nilai `env` memakai awalan `!`, yang berarti omp menjalankan sisa baris sebagai perintah shell lalu memakai stdout-nya sebagai nilai. `get-token.sh` mengambil token dari `.omp/github-token`, environment, atau kredensial git. File konfigurasi aman di-commit.
- **Toolset dipersempit.** Hanya `context,repos,issues,pull_requests,labels,users` yang aktif. Ini mengurangi jumlah tool yang masuk ke konteks model dan mempercepat pemilihan tool. Kalau butuh GitHub Actions, tambahkan `actions`; kalau butuh pencarian kode di seluruh organisasi, tambahkan `orgs`.

### 3.3 Konfigurasi untuk host lain

**Claude Code** (`.mcp.json` di root repo):

```json
{
  "mcpServers": {
    "github": {
      "command": "tools/github-mcp/github-mcp-server.exe",
      "args": ["stdio", "--toolsets", "context,repos,issues,pull_requests,labels,users"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<token>" }
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`) — VS Code tidak mendukung `!command`, jadi token harus lewat input:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "github_token",
      "description": "GitHub Personal Access Token",
      "password": true
    }
  ],
  "servers": {
    "github": {
      "type": "stdio",
      "command": "${workspaceFolder}/tools/github-mcp/github-mcp-server.exe",
      "args": ["stdio", "--toolsets", "context,repos,issues,pull_requests,labels,users"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}" }
    }
  }
}
```

**Cursor** (`.cursor/mcp.json`): bentuknya sama dengan Claude Code.

**Tanpa token sama sekali:** server bisa login lewat OAuth dengan membuka browser. Hapus entri `env`, lalu jalankan server; browser akan terbuka dan kamu login seperti biasa. Token hasil OAuth hanya disimpan di memori dan hilang saat proses berhenti, jadi setiap sesi baru butuh login ulang. Untuk pemakaian harian, PAT lebih praktis.

---

## 4. Menyiapkan Token

### 4.1 Buat Personal Access Token

1. Buka <https://github.com/settings/personal-access-tokens/new> (fine-grained) atau <https://github.com/settings/tokens/new> (classic).
2. Untuk **classic**, centang scope `repo`. Itu cukup untuk membaca dan menulis issue, PR, dan milestone di repositori publik maupun privat.
3. Untuk **fine-grained**, pilih repositori `omnipos`, lalu beri izin:
   - **Issues**: Read and write
   - **Pull requests**: Read and write
   - **Contents**: Read and write
   - **Metadata**: Read-only (otomatis)
4. Salin token (`ghp_...` atau `github_pat_...`). Token hanya ditampilkan sekali.

### 4.2 Simpan token

Skrip `get-token.sh` dan `github-auth.ps1` memeriksa berurutan dan memakai yang pertama ditemukan:

1. `.omp/github-token` (file lokal repo, tidak di-commit)
2. `GITHUB_PERSONAL_ACCESS_TOKEN`
3. `GITHUB_TOKEN`
4. kredensial git tersimpan

**Opsi A — file token lokal repo** (paling aman untuk mesin yang dipakai kerja lain):

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\set-token.ps1
```

Skrip meminta token lewat prompt tersembunyi, memvalidasinya, dan **menolak menyimpan** kalau akunnya tidak punya izin tulis pada repo tujuan. Yang ditulis hanya token yang lolos dua syarat: `GET /user` tidak 401, dan `permissions.push` bernilai `true` pada `Moreno-Hernakov/omnipos`. Berkas hasilnya `.omp/github-token` dengan ACL dibatasi ke user Windows saat ini.

Kalau tidak mau lewat prompt:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\set-token.ps1 -Token "ghp_xxxxxxxxxxxx"
```

Dipakai lebih dulu daripada kredensial git karena Windows Credential Manager bisa berisi token akun lain (misalnya akun kantor). Kalau file ini ada, akun di dalamnya yang dipakai MCP dan skrip milestone — bukan akun yang tersimpan di `git:https://github.com`.

**Opsi B — environment variable** (hilang saat terminal ditutup):

```powershell
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_xxxxxxxxxxxx"
```

Untuk permanen di Windows:

```powershell
setx GITHUB_PERSONAL_ACCESS_TOKEN "ghp_xxxxxxxxxxxx"
```

**Opsi C — kredensial git** (disimpan di Windows Credential Manager, dipakai ulang oleh `git push`):

```powershell
git config --global credential.helper manager-core
```

Saat pertama kali `git push` ke GitHub, jendela login muncul. Setelah berhasil, token tersimpan dan `get-token.sh` akan mengambilnya otomatis.

> **Perangkap:** kredensial `git:https://github.com` bersifat global per mesin, bukan per repo. Di mesin yang juga dipakai untuk akun lain, kredensial ini bisa berisi token akun tersebut. Akibatnya issue tercatat atas nama akun yang salah, dan milestone gagal karena akun itu tidak punya izin tulis. Cek dengan `-Action whoami` (§5.2).

**Opsi D — tulis langsung di config host** (paling tidak aman, jangan di-commit):

Ganti nilai `env` di `.omp/mcp.json` dari `"!bash tools/github-mcp/get-token.sh"` menjadi token literal. **Jangan commit perubahan ini.**

### 4.3 Cek token

Cara paling cepat — sekaligus menampilkan izin tulis pada repo:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action whoami
```

Keluaran yang benar:

```text
Akun token : Moreno-Hernakov
Repositori : Moreno-Hernakov/omnipos
Izin       : admin
```

Kalau `Akun token` bukan pemilik repo, atau `Izin` bukan `admin`/`write`, ganti token lewat §4.2 opsi A.

Cek mentah lewat API:

```powershell
curl -s -H "Authorization: Bearer $env:GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

Kalau berhasil, muncul JSON berisi `"login"`. Kalau `401`, token salah atau kedaluwarsa.

---

## 5. Batasan Penting: Milestone

**GitHub MCP Server v2.2.0 tidak punya tool milestone.** Ini bukan salah konfigurasi.

Sudah diperiksa dengan menjalankan server memakai `--toolsets all` (77 tool aktif): tidak ada satu pun tool bernama `*milestone*`. Tool `issue_write` punya parameter `milestone`, tetapi isinya **nomor milestone yang sudah ada** — bukan pembuatan milestone baru. Memanggilnya dengan nomor yang belum ada menghasilkan:

```text
Issue.milestone (invalid)
```

Artinya: milestone harus dibuat lebih dulu lewat REST API, baru nomornya dipakai oleh `issue_write`.

### 5.1 Skrip bantuan milestone

`tools/github-mcp/milestones.ps1` mengisi celah itu memakai token yang sama dengan MCP server.

**Lihat semua milestone:**

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action list
```

**Buat milestone:**

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action create `
  -Title "Nama Milestone" `
  -Description "Ringkasan isi milestone" `
  -DueOn "2026-12-05"
```

> Untuk kebutuhan sehari-hari, jangan pakai perintah ini. Milestone papan sudah dibuat dan dirawat `bootstrap-issues.ps1` (§6.1). `milestones.ps1` dipakai kalau perlu milestone tambahan di luar alur papan.

**Pasang milestone ke issue:**

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action assign -Issue 7 -Milestone 1
```

`-DueOn` memakai format `YYYY-MM-DD`. Parameter `-Owner` dan `-Repo` bisa diubah kalau repositori berpindah.

### 5.2 Izin yang dibutuhkan untuk milestone

Pembuatan milestone **butuh izin tulis (push) pada repositori**. Tanpa itu, REST API membalas `404` — bukan `403`. Ini perilaku GitHub, bukan bug skrip: endpoint yang tidak bisa diakses disembunyikan sebagai "tidak ditemukan".

Bedakan dua kasus yang mirip tetapi berbeda penyebabnya:

| Gejala | Penyebab |
| :--- | :--- |
| `-Action list` gagal `404` | Token tidak punya akses baca ke repo, atau nama owner/repo salah |
| `-Action list` berhasil, `-Action create` gagal `404` | Token punya akses baca tetapi tidak punya izin push |
| Issue bisa dibuat, milestone tidak | Repo publik: siapa pun boleh membuka issue, tetapi milestone tetap butuh push |

**Kasus yang paling sering di proyek ini:** repo `omnipos` bersifat publik, sehingga token akun mana pun bisa membuat dan menutup issue. Itu membuat orang mengira token sudah punya izin tulis. Padahal milestone butuh `push`, dan `push` hanya dimiliki collaborator.

Cek akun pemilik token yang sedang dipakai:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action whoami
curl -s -H "Authorization: Bearer $env:GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
```

`-Action whoami` menampilkan tiga baris: akun token, repositori, dan tingkat izin (`admin`/`maintain`/`write`/`triage`/`read`). Kalau `Izin` bukan `write` atau lebih tinggi, milestone tidak akan bisa dibuat dan issue akan tercatat atas nama akun itu.

Kalau `login` yang muncul **bukan** akun pemilik repo, itu penyebabnya. Token milik akun lain tidak akan pernah bisa membuat milestone di repo ini, seberapa pun scope-nya — scope `repo` hanya berlaku untuk repo yang memang bisa diakses akun tersebut.

**Perbaikan:** buat PAT dari akun pemilik repo (`Moreno-Hernakov`), lalu simpan sebagai token lokal repo:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\set-token.ps1
```

Skrip menolak token yang akunnya tidak punya izin tulis, jadi salah akun langsung ketahuan sebelum tersimpan. Berkas `.omp/github-token` di-ignore `.gitignore` dan dibaca lebih dulu daripada kredensial git, sehingga token kerja yang tersimpan di Windows Credential Manager tidak lagi ikut terpakai. Kalau kamu tetap ingin memakai kredensial git, hapus dulu kredensial lama:

```powershell
cmdkey /delete:LegacyGeneric:target=git:https://github.com
```

Alternatif tanpa mengubah token: minta pemilik repo membuat milestone-nya (bagian 5.3), atau tambahkan akun pemilik token sebagai collaborator dengan akses **Write**.

### 5.3 Alternatif: buat milestone lewat web

Kalau tidak mau mengurus izin token:

1. Buka <https://github.com/Moreno-Hernakov/omnipos/milestones>
2. Klik **New milestone**
3. Isi judul, deskripsi, dan tenggat
4. Catat nomornya (muncul di URL setelah dibuat)
5. Pasang ke issue lewat web, atau lewat `issue_write` dengan parameter `milestone`

---

## 6. Pemakaian Harian

Setelah terpasang dan token tersedia, minta asisten AI melakukan hal seperti:

```text
Buat issue untuk task T-22 di repo Moreno-Hernakov/omnipos dengan judul
"[T-22] Pengelolaan stok: barang masuk, opname, dan transfer", label "inventaris",
dan isi dari docs/02-TASKS.md baris T-22.
```

```text
Tampilkan semua issue yang masih terbuka di omnipos, kelompokkan per milestone.
```

```text
Baca docs/02-TASKS.md dari branch main, lalu buat issue untuk setiap task
yang statusnya "- [ ]".
```

```text
Buka pull request dari branch T-22-inventaris ke main, isi deskripsinya dengan
ringkasan perubahan dan checklist Definition of Done.
```

### 6.1 Membuat milestone dan issue dari papan task

Sekali jalan, seluruh papan bisa dipindahkan ke GitHub:

```powershell
# Lihat rencananya dulu
powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1 -DryRun

# Jalankan
powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1
```

Skrip membaca `docs/02-TASKS.md`, membuat satu milestone untuk seluruh papan, lalu satu issue per baris:

| Isi issue | Sumber |
| :--- | :--- |
| Judul `[T-22] ...` | kolom ID + Task |
| Body: Task, Owner, Depends on, Fase, Catatan | kolom tabel |
| Milestone | `UAS POS - Pengumpulan`, tenggat 30 Nov 2026 |
| Assignee | kolom Owner lewat peta `$OwnerMap` di skrip |

**Satu milestone, bukan satu per fase.** Satu issue hanya bisa punya satu milestone, dan milestone adalah satu-satunya objek GitHub yang punya tanggal. Kalau fase dijadikan milestone, deadline tidak punya tempat tinggal. Fase tetap tercatat di heading `docs/02-TASKS.md` dan di baris `**Fase**:` pada body setiap issue, jadi tidak ada informasi yang hilang.

Tenggat diubah lewat parameter, bukan dengan mengedit skrip:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\bootstrap-issues.ps1 -MilestoneDue 2026-12-05
```

Format `-MilestoneDue` wajib `YYYY-MM-DD`; nilai lain ditolak sebelum ada panggilan API. `-MilestoneTitle` dan `-MilestoneDescription` juga bisa diubah dengan cara yang sama.

**Soal tanggal.** `due_on` adalah tanggal, bukan pengingat — GitHub tidak mengirim notifikasi milestone. Yang terjadi adalah UI menandai overdue setelah tanggal lewat. Karena itu tenggat dipasang di hari pengumpulan sebenarnya (30 Nov), sementara buffer ditulis di deskripsi: *kode beku 29 Nov, 30 Nov hanya pengemasan*. Memasang `due_on` lebih awal dari deadline asli membuat semuanya tampak telat padahal belum, dan itu melatih orang mengabaikan warna merah.

**Idempoten.** Aman dijalankan berulang. Milestone dicocokkan lewat judul persis, issue lewat awalan `[T-xx]` di judul. Yang sudah ada tidak diduplikasi: kalau judul, body, milestone, atau tenggatnya berbeda, skrip memperbaikinya. Body yang tidak memuat penanda `Sumber: docs/02-TASKS.md` dianggap tulisan tangan dan tidak pernah ditimpa.

Task yang sudah `✅` di dokumen langsung dibuat dalam keadaan tertutup, jadi hasil pertama langsung sinkron tanpa perlu `sync-tasks.ps1` lebih dulu.

**Peta owner.** Nama di kolom Owner bukan login GitHub, jadi dipetakan di `$OwnerMap`:

| Kolom Owner | Login GitHub |
| :--- | :--- |
| Moreno | Moreno-Hernakov |
| Bagas | Bagas-Rizky |
| Rangga | FxRangga |
| Gregorius Priyagung | gpriyagung633 |
| Valencia | Valencia0902 |
| Raymond | *(belum collaborator)* |

Nama yang belum punya akses ke repo dilaporkan di akhir; issue-nya tetap dibuat tanpa assignee. Setelah akunnya ditambahkan sebagai collaborator, jalankan ulang skrip — assignee terpasang otomatis.

### 6.2 Alur Status: Dokumen vs GitHub

`docs/02-TASKS.md` adalah sumber utama yang dibaca manusia. Issue GitHub adalah tempat kejadiannya. Keduanya disamakan oleh `tools/github-mcp/sync-tasks.ps1`.

**Penanda selesai di GitHub — dua cara, keduanya sah:**

| Cara | Kapan dipakai |
| :--- | :--- |
| Merge PR dengan `Closes #12` di body | Cara utama. Otomatis menutup issue saat merge |
| Klik **Close issue** manual | Kalau tidak lewat PR, atau PR sudah terlanjur merge |

Keduanya menghasilkan state `closed` yang sama, dan `sync-tasks.ps1` memperlakukan keduanya identik. Tidak ada perbedaan.

**Mencocokkan issue dengan baris tabel:** skrip membaca ID di awal judul issue. Format wajib `[T-22] Judul apa pun`. Issue tanpa awalan itu diabaikan, jadi jangan mengubah format judul.

**Perintah:**

```powershell
# Lihat perbedaan tanpa mengubah apa pun. Exit code 1 kalau ada drift.
powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1 -Direction check

# GitHub -> dokumen. Issue closed jadi "✅", open jadi "⬜".
powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1

# Dokumen -> GitHub. Emoji jadi perintah buka/tutup issue.
powershell -ExecutionPolicy Bypass -File tools\github-mcp\sync-tasks.ps1 -Direction toGitHub
```

**Rutinitas yang disarankan — tiga titik, bukan setiap push:**

1. **Sebelum mulai kerja** — `-Direction check` untuk melihat status terbaru.
2. **Setelah merge PR** — `-Direction toDoc`, lalu commit `docs/02-TASKS.md`.
3. **Saat menutup fase** — `-Direction check` memastikan tidak ada drift sebelum demo.

Menjalankan ini di setiap `git push` tidak disarankan: setiap sinkronisasi menulis ulang file dan menambah commit yang mengotori riwayat, sementara status issue jarang berubah di antara push.

### 6.3 Kenapa status memakai emoji, bukan checkbox

Markdown GitHub mendukung task list `- [ ]` / `- [x]`, tetapi **hanya di level blok**. Di dalam sel tabel, penanda itu keluar sebagai teks mentah.

Ini dibuktikan langsung lewat API render resmi GitHub (`POST /markdown`, mode `gfm`):

| Ditulis | Hasil render di dalam sel tabel |
| :--- | :--- |
| `- [x]` | `<td>- [x]</td>` — teks mentah |
| `[x]` | `<td>[x]</td>` — teks mentah |
| `✅` | `<td>✅</td>` — terender |
| `**Done**` | `<td><strong>Done</strong></td>` — terender |

Di luar tabel, `- [x]` tetap jadi kotak centang:

```html
<ul class="contains-task-list">
  <li class="task-list-item"><input type="checkbox" disabled checked> item</li>
```

Karena papan task berbentuk tabel, penanda status memakai emoji:

| Emoji | Arti |
| :--- | :--- |
| `✅` | selesai |
| `⬜` | belum selesai |

Konsekuensi praktis: **tidak ada yang bisa diklik**, baik di GitHub maupun di editor. Status diubah lewat `sync-tasks.ps1`, atau dengan mengedit baris lalu commit. Sumber kebenaran tetap issue GitHub.

Kalau suatu saat papan task diubah dari tabel menjadi daftar bertingkat, checkbox markdown bisa dipakai lagi dan akan jadi kotak centang sungguhan. Selama bentuknya tabel, emoji adalah satu-satunya pilihan yang terender.

### 6.4 Milestone dan progress

Papan ini memakai **satu** milestone: `UAS POS - Pengumpulan`, tenggat `2026-11-30`. Dibuat dan dirawat oleh `bootstrap-issues.ps1` (§6.1); tidak perlu dibuat manual.

Alasannya: satu issue hanya bisa punya satu milestone, dan milestone adalah satu-satunya objek GitHub yang punya tanggal. Memakai slot itu untuk fase berarti deadline tidak punya tempat. Fase tetap ada di dokumen dan di body issue.

Progress milestone dihitung GitHub dari rasio issue tertutup, bukan dari perkiraan waktu. Tidak ada time tracking di GitHub — lihat §5 soal batasan milestone.

Kalau suatu saat butuh milestone tambahan (misal fase terpisah karena diminta dosen), buat lewat `milestones.ps1`:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action create `
  -Title "Milestone Tambahan" -Description "Ringkasan isi"
```

Hati-hati: memindahkan issue ke milestone baru berarti melepasnya dari milestone pengumpulan. Jangan dilakukan sebelum deadline lewat.

### Toolset yang tersedia

Konfigurasi proyek mengaktifkan toolset berikut:

| Toolset | Isi |
| :--- | :--- |
| `context` | Identitas pengguna dan konteks GitHub saat ini |
| `repos` | Baca/tulis file, branch, commit, rilis, pencarian kode |
| `issues` | Baca, buat, perbarui issue dan komentar |
| `pull_requests` | Baca, buat, merge PR, review, komentar |
| `labels` | Baca dan kelola label |
| `users` | Informasi pengguna GitHub |

Menambah toolset lain dilakukan dengan mengedit argumen `--toolsets` di `.omp/mcp.json`. Pilihan yang tersedia: `actions`, `code_security`, `dependabot`, `discussions`, `gists`, `git`, `notifications`, `orgs`, `projects`, `secret_protection`, `security_advisories`, `stargazers`. Daftar lengkap dengan deskripsi ada di `tools/github-mcp/README.md` bagian *Available Toolsets*.

Membatasi toolset bukan hanya soal keamanan: setiap tool menambah teks ke prompt, dan model yang kebanyakan pilihan tool lebih mudah salah pilih.

---

## 7. Pemecahan Masalah

### Server tidak muncul di daftar MCP host

1. Pastikan binary ada: `ls tools\github-mcp\github-mcp-server.exe`
2. Pastikan konfigurasi terbaca. Untuk omp, jalankan `/mcp list` di dalam sesi; entri `github` harus muncul dengan sumber `.omp/mcp.json`.
3. Pastikan host dijalankan dari **root repo** (`UAS_POS/`), bukan dari folder lain. `command` memakai path relatif, jadi direktori kerja menentukan apakah binary ditemukan.

### Server muncul tetapi setiap panggilan gagal `401`

Token tidak terbaca. Uji langsung:

```powershell
bash tools/github-mcp/get-token.sh
```

Kalau keluar pesan "Token GitHub tidak ditemukan", berarti environment variable kosong **dan** tidak ada kredensial git tersimpan. Ikuti bagian 4.2.

### `bash: command not found` saat memuat konfigurasi

`get-token.sh` butuh `bash`. Di Windows, Git for Windows menyediakannya di `C:\Program Files\Git\bin\bash.exe`. Kalau tidak ada di `PATH`, ganti nilai `env` di `.omp/mcp.json` menjadi token literal (bagian 4.2 opsi D) atau pakai host lain yang mendukung environment variable langsung.

### Issue tercatat atas nama akun lain

Gejala: issue yang kamu buat muncul sebagai `by <akun-lain>`, bukan `Moreno-Hernakov`. Repo publik membuat siapa pun bisa membuka issue, jadi ini tidak terlihat seperti kesalahan sampai kamu sadar akunnya salah.

Penyebab: token yang dipakai MCP berasal dari kredensial git global (`LegacyGeneric:target=git:https://github.com`) yang berisi PAT akun lain — biasanya akun kantor yang pernah dipakai `git push` di mesin yang sama.

Periksa:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\milestones.ps1 -Action whoami
```

Kalau `Akun token` bukan `Moreno-Hernakov`, simpan PAT pemilik repo lewat `set-token.ps1` (bagian 4.2 opsi A). Skrip itu menolak token tanpa izin tulis, jadi salah akun tidak akan tersimpan. File `.omp/github-token` dibaca lebih dulu daripada kredensial git, jadi kredensial kerja tidak perlu dihapus. Setelah itu restart sesi omp agar MCP memuat token baru.

### `-Action create` mengembalikan `404`

Token tidak punya izin tulis. Lihat bagian 5.2.

### `Issue.milestone (invalid)`

Nomor milestone belum ada. Buat dulu lewat `milestones.ps1 -Action create` atau lewat web, lalu pakai nomor yang benar.

Catatan perilaku GitHub: `PATCH /issues/{n}` dengan nomor milestone yang tidak ada tetap membalas **200 OK**, tetapi milestone-nya diam-diam tidak terpasang. Karena itu `milestones.ps1 -Action assign` membaca ulang respons dan membandingkan `milestone.number`. Kalau tidak cocok, skrip berhenti dengan pesan berisi daftar milestone yang benar-benar ada. Jangan percaya kode status HTTP saja saat memanggil API GitHub langsung.

### Ingin mematikan server untuk sementara

Tambahkan nama server ke `disabledServers` di `~/.omp/agent/mcp.json`:

```json
{ "disabledServers": ["github"] }
```

---

## 8. Berkas Terkait

| Berkas | Isi |
| :--- | :--- |
| `.omp/mcp.json` | Konfigurasi MCP untuk omp; dibagi ke seluruh tim |
| `.omp/github-token` | Token lokal per-mesin (**tidak di-commit**); dibaca pertama oleh kedua skrip token |
| `tools/github-mcp/install.ps1` | Pengunduh binary dengan verifikasi checksum |
| `tools/github-mcp/get-token.sh` | Pengambil token dari environment atau kredensial git |
| `tools/github-mcp/set-token.ps1` | Penyimpan token lokal repo; menolak token tanpa izin tulis |
| `tools/github-mcp/github-auth.ps1` | Helper token untuk skrip PowerShell; dipakai `milestones.ps1` dan `sync-tasks.ps1` |
| `tools/github-mcp/milestones.ps1` | Pengelola milestone lewat REST API; `-Action whoami` untuk cek akun token |
| `tools/github-mcp/bootstrap-issues.ps1` | Membuat/menyamakan milestone + issue dari `docs/02-TASKS.md`; idempoten |
| `tools/github-mcp/README.md` | Dokumentasi resmi GitHub MCP Server v2.2.0 |
| `tools/github-mcp/github-mcp-server.exe` | Binary; **tidak di-commit** (lihat `.gitignore`) |

---

## 9. Catatan Versi

Versi dipatok di dua tempat dan harus selalu sama:

- `tools/github-mcp/install.ps1` — variabel `$Version` dan `$Sha256`
- Dokumen ini — bagian 3.1 dan 9

Saat memperbarui versi:

1. Buka <https://github.com/github/github-mcp-server/releases/latest> dan catat tag serta checksum `Windows_x86_64.zip`.
2. Perbarui `$Version` dan `$Sha256` di `install.ps1`.
3. Jalankan `install.ps1 -Force` dan pastikan `--version` menampilkan versi baru.
4. Perbarui tabel di bawah dan bagian 3.1.

| Versi | Tanggal pasang | Catatan |
| :--- | :--- | :--- |
| 2.2.0 | 23 Nov 2026 | Versi awal. 77 tool dengan `--toolsets all`; tidak ada tool milestone. |
