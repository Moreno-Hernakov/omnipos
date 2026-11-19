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
├── README.md                  # Ringkasan proyek & panduan tim
├── workspace/                 # Aturan kerja, pembagian tugas, dan task board
│   ├── README.md              # Cara pakai workspace
│   ├── TEAM.md                # Roster, ownership, dan task low-impact
│   ├── TASKS.md               # Papan status task per fase
│   └── CONVENTIONS.md         # Branch, commit, cek mandiri, coding, build
├── docs/                      # Dokumen spesifikasi & naskah laporan
│   ├── SPECIFICATION.md       # Spesifikasi arsitektur & alur kerja lengkap
│   └── PROPOSAL_POS.md        # Proposal yang sudah disetujui
├── database/                  # Skrip basis data MySQL
│   └── schema_pos.sql         # Skrip DDL 16 tabel (13 tabel inti + 3 pendukung)
└── src/                       # Kode sumber C# Windows Forms (.sln & .csproj)
```

### Aturan & Pembagian Tugas

- Baca `AGENTS.md` sebelum mengubah kode.
- `workspace/TEAM.md` memuat roster, ownership eksekusi, dan batas task low-impact.
- `workspace/TASKS.md` adalah papan status task. Satu task satu owner.
- `workspace/CONVENTIONS.md` mengatur branch, commit, cek hasil task, build, dan coding.
- Kontrak teknis tetap di `docs/SPECIFICATION.md`; DDL final di `database/schema_pos.sql`.

---

## 🚀 Fitur Unggulan
1. **Configurable Onboarding Wizard**: Setup identitas bisnis dan aktivasi fitur dinamis saat pertama kali login.
2. **Bill of Materials (BOM) & HPP Engine**: Perhitungan otomatis HPP menu F&B dan pemotongan stok bahan mentah dapur.
3. **Dual-Mode Kasir**: Mendukung *Bayar Langsung* (Retail/Minimarket) dan *Simpan Tagihan / Hold Bill* (Dine-in / Servis).
4. **Shift Kasir & Petty Cash**: Pencatatan modal awal dan rekonsiliasi kas saat tutup toko.
5. **Multi-Cabang & Mutasi Stok**: Transfer stok antar-cabang dengan pelacakan status.
6. **Laporan & Analitik**: Laporan penjualan, laba kotor harian/bulanan, kartu stok, dan rekap shift diekspor ke PDF A4 melalui **FastReport OpenSource**. Struk kasir tetap dicetak thermal 58/80 mm melalui `PrintDocument`.
