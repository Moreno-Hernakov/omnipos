# UAS Pemrograman Visual: Omni-Industry Configurable POS Engine

Aplikasi desktop **Point of Sales (POS)** modular dan adaptif berbasis **C# Windows Forms (.NET Framework 4.7.2)** dan **MySQL (ADO.NET)** untuk memenuhi kebutuhan operasional kasir, inventaris, dan manajemen cabang pada sektor Retail, F&B, dan Jasa.

---

## 👥 Tim Pengembang (6 Orang)
- **225310690** — BAGAS RIZKY PUTRA WARDANA
- **225310691** — FX THIARNIKA EKA ATUR RANGGA
- **225310692** — GREGORIUS PRIYAGUNG
- **225310693** — MORENO HERNAKOV
- **225310694** — RAYMOND SUGIHARTO
- **225310695** — VALENCIA ANGIE KURNIAWAN

---

## 📁 Struktur Direktori

```text
UAS_POS/
├── AGENTS.md                  # Aturan wajib untuk agent/developer di scope UAS_POS
├── README.md                  # Ringkasan proyek & quick start
├── docs/                      # Seluruh dokumen kerja, dibaca berurutan
│   ├── 01-README.md           # Peta dokumen & cara pakai
│   ├── 02-TASKS.md            # Roster, ownership, task per fase, status
│   ├── 03-CONVENTIONS.md      # Branch, commit, build, file ownership, DoD
│   ├── 04-ARSITEKTUR.md       # Stack, 3 lapis, service/repository, koneksi
│   ├── 05-UI-SHELL.md         # Form vs UserControl, menu, tema
│   ├── 06-SPESIFIKASI.md      # Perilaku fitur & aturan bisnis
│   ├── 07-ALUR-PENGGUNA.md    # Alur layar, field onboarding, user story
│   ├── 08-MOCKUP-HALAMAN.md   # Mockup ASCII setiap layar (Windows Forms)
│   └── proposal/              # Proposal resmi (.md & .docx)
├── database/                  # Skrip basis data MySQL
│   ├── README.md              # Setup server & akun aplikasi
│   ├── schema_pos.sql         # DDL 16 tabel
│   └── seed_demo.sql          # Data contoh
└── src/                       # Kode sumber C# Windows Forms (.sln & .csproj)
```

## 🔧 Tooling Repositori

Proyek memakai **GitHub MCP Server** resmi supaya asisten AI bisa membaca repo, mengelola issue, dan membuka pull request langsung dari GitHub.

Pemasangan sekali setelah clone:

```powershell
powershell -ExecutionPolicy Bypass -File tools\github-mcp\install.ps1
```

Konfigurasi MCP sudah ada di `.omp/mcp.json`; token diambil otomatis dari environment atau kredensial git, jadi tidak ada token yang di-commit. Panduan lengkap (token, host lain seperti VS Code/Cursor/Claude Code, dan cara membuat milestone) ada di `docs/09-GITHUB-MCP.md`.

## 🚀 Mulai di Sini

1. Baca `AGENTS.md` sebelum mengubah kode.
2. Ikuti urutan dokumen di `docs/01-README.md`.
3. Cari task milikmu di `docs/02-TASKS.md`.
4. Siapkan database lokal mengikuti `database/README.md`.
5. Setelah aplikasi jalan, login dengan akun demo `admin` / `admin123`. Daftar akun lain ada di `database/README.md` bagian **Akun demo**.

Aturan penting:

- Satu task satu owner; status ditandai `✅` / `⬜`, dan status asli ada di issue GitHub (sinkron lewat `tools/github-mcp/sync-tasks.ps1`).
- Perilaku fitur mengikuti `docs/06-SPESIFIKASI.md`; jangan mengarang aturan sendiri.
- UI hanya memanggil Service, tidak menulis SQL dan tidak membuka koneksi.
- Menu dan halaman mengikuti peta di `docs/05-UI-SHELL.md`.

---

## 🚀 Fitur Unggulan
1. **Configurable Onboarding Wizard**: Setup identitas bisnis dan aktivasi fitur dinamis saat pertama kali login.
2. **Bill of Materials (BOM) & HPP Engine**: Perhitungan otomatis HPP menu F&B dan pemotongan stok bahan mentah dapur.
3. **Dual-Mode Kasir**: Mendukung *Bayar Langsung* (Retail/Minimarket) dan *Simpan Tagihan / Hold Bill* (Dine-in / Servis).
4. **Shift Kasir & Petty Cash**: Pencatatan modal awal dan rekonsiliasi kas saat tutup toko.
5. **Multi-Cabang & Mutasi Stok**: Transfer stok antar-cabang dengan pelacakan status.
6. **Laporan & Analitik**: Laporan penjualan, laba kotor harian/bulanan, kartu stok, dan rekap shift diekspor ke PDF A4 melalui **FastReport OpenSource**. Struk kasir tetap dicetak thermal 58/80 mm melalui `PrintDocument`.
