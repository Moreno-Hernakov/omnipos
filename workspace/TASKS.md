# Papan Task Proyek UAS POS

Status: `Todo`, `Done`.

Aturan:

- Satu task satu owner.
- Status hanya `Todo` (belum selesai, termasuk sedang dikerjakan atau terhambat) dan `Done` (build dan uji task selesai).
- Catat blocker atau dependency yang menunggu di kolom catatan; status tetap `Todo`.
- Owner memastikan hasil sesuai task, build berhasil, dan skenario utama sudah diuji sebelum menandai `Done`.
- Setiap anggota menguji fiturnya sendiri. Owner fitur transaksi dan stok juga menguji kasus gagal dan rollback. Tidak ada task regresi terpusat.
- Judul task ditulis dalam bahasa bisnis agar mudah dibaca dosen dan pemangku kepentingan. Detail teknis tetap ada di kolom catatan, `docs/SPECIFICATION.md` (perilaku), dan `database/schema_pos.sql`.
- Dependency adalah penghalang teknis, bukan izin untuk mulai. Pekerjaan boleh dimulai paralel selama skema dan kontrak tersedia; integrasi dicek setelah dependency selesai.
- Jika owner berubah, catat di papan ini. Owner baru membaca kontrak di `docs/SPECIFICATION.md` dan memakai branch yang sama; jangan membuat implementasi paralel.

## Ringkasan per Anggota

Modul formal mengikuti proposal. Kolom bagian menunjukkan pengerjaan aktual tiap anggota.

| NRP | Anggota | Modul formal | Bagian yang dikerjakan | Support |
| :--- | :--- | :--- | :--- | :--- |
| 225310690 | Bagas Rizky Putra Wardana | Modul 1: Autentikasi & Konfigurasi | Onboarding, menu utama & hak akses | Moreno |
| 225310691 | FX Thiarnika Eka Atur Rangga | Modul 2: Master Data & Resep BOM | Produk & kategori, bahan baku, resep/BOM & perhitungan HPP | Moreno |
| 225310692 | Gregorius Priyagung | Modul 3: Kasir & Transaksi | UI katalog/keranjang, pelanggan/member, shell laporan, antrean servis, data demo & panduan | Raymond, Valencia |
| 225310693 | Moreno Hernakov | Modul 4: Inventaris & Stok Cabang | Fondasi arsitektur & scaffold, koneksi database, login contoh alur, stok masuk/opname/transfer | Bagas |
| 225310694 | Raymond Sugiharto | Modul 5: Operasional Kasir & Layanan | Transaksi & hold bill, struk, shift kasir, status pekerjaan jasa, alur kasir | Moreno, Gregorius |
| 225310695 | Valencia Angie Kurniawan | Modul 6: Laporan & Analitik | Data laporan, format PDF, integrasi tampilan laporan, dashboard produk terlaris | Gregorius |

Catatan:

- Setiap anggota menguji fiturnya sendiri sebelum menandai `Done`.
- Fase 0 dan T-10 (login) dikerjakan lebih dulu sebagai contoh alur. Setelah T-03 selesai, pekerjaan modul lain boleh berjalan paralel.

## Fase 0 — Fondasi

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-00 | Perancangan arsitektur, model data, dan aturan kerja tim | Moreno | — | Done | Fondasi reusable: `docs/SPECIFICATION.md`, `database/schema_pos.sql`, panduan `workspace/` |
| T-01 | Penyiapan fondasi aplikasi dan lingkungan pengembangan | Moreno | T-00 | Todo | Scaffold `src/OmniPos.sln` (net472), paket FastReport/MySql, restore MSBuild; blocker semua task kode |
| T-02 | Penyiapan data awal dan contoh bisnis | Moreno | T-01 | Todo | Import schema + seed demo; Agung membantu data contoh, schema tetap tanggung jawab Moreno |
| T-03 | Koneksi aplikasi ke basis data | Moreno | T-01 | Todo | `App.config` + `KoneksiDB` + tes koneksi; jangan hardcode credential |

## Fase 1 — Akses Pengguna, Data Master, dan Tampilan Pendukung

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-10 | Login pengguna dan validasi hak akses | Moreno | T-03 | Todo | `LoginForm` + `AuthService` SHA-256, cek user aktif; uji password salah dan user nonaktif. Dijadikan contoh alur referensi UI → Service → Repository |
| T-11 | Penyiapan awal toko (onboarding) | Bagas | T-03 | Todo | `OnboardingWizardForm` + `app_config`; empat tahap, set `is_onboarded=1`. Integrasi setelah T-10 |
| T-12 | Menu utama dan navigasi sesuai peran | Bagas | T-03 | Todo | `MainForm` shell + role/feature flag; menu yang tidak berhak disembunyikan. Integrasi login setelah T-10 |
| T-13 | Pengelolaan produk dan kategori | Rangga | T-03 | Todo | `UcMasterProduk` + `UcKategori`; CRUD sederhana, validasi kode item |
| T-14 | Pengelolaan bahan baku, resep, dan HPP | Rangga | T-13 | Todo | `UcBahanBaku` + `UcResepBOM` + `RecipeService`; HPP = takaran × harga bahan |
| T-15 | Pengelolaan pelanggan/member | Gregorius Priyagung | T-03 | Todo | `UcPelanggan` CRUD; checkout tetap jalan tanpa member |
| T-16 | Tampilan awal laporan (filter dan grid) | Gregorius Priyagung | T-03 | Todo | shell `UcLaporan`; tanpa query dan PDF. Integrasi ke `MainForm` setelah T-12 |
| T-17 | Daftar antrean servis (baca saja) | Gregorius Priyagung | T-03 | Todo | `UcServis` read-only; tanpa update status |

## Fase 2 — Operasional Kasir, Stok, dan Shift

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-20 | Pemrosesan transaksi penjualan secara utuh | Raymond | T-03 | Todo | `TransactionService` atomik: header, detail, hold, void; `MySqlTransaction` + rollback. Uji dengan produk setelah T-13, resep F&B setelah T-14 |
| T-21 | Tampilan kasir (katalog dan keranjang) | Gregorius Priyagung | T-03 | Todo | `UcKasir` layout, keranjang, tombol; tanpa logic transaksi. Integrasi ke `MainForm` setelah T-12 |
| T-26 | Alur kasir: pilih produk, bayar, simpan tagihan | Raymond | T-20 | Todo | `UcKasir` logic: katalog, keranjang, bayar, hold bill; integrasi event UI setelah T-21 |
| T-22 | Pengelolaan stok: barang masuk, opname, dan transfer | Moreno | T-03 | Todo | `InventoryService` + `stock_movements` untuk restock/opname/transfer; setiap perubahan stok wajib ledger. Pemotongan saat sale diintegrasikan dengan T-20 |
| T-23 | Cetak struk belanja | Raymond | T-03 | Todo | `PrintDocument` thermal 58/80 mm; cetak ulang tidak membuat nota baru. Uji dengan nota setelah T-20 |
| T-24 | Buka dan tutup shift kasir | Raymond | T-03 | Todo | `ShiftService` + `UcShift`: buka, blind close, rekap. Rekap diuji setelah T-20 |
| T-25 | Pelacakan status pekerjaan jasa | Raymond | T-03 | Todo | Status/antrean servis + `service_jobs`; satu job per transaksi servis. Uji dengan transaksi servis setelah T-20 |

## Fase 3 — Pelaporan dan Analitik

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-30 | Penyusunan data laporan manajemen | Valencia | T-02 | Todo | `ReportRepository` + `ReportService` (4 laporan); query parameterized, total dihitung di C#. Uji data setelah T-20 dan T-22 |
| T-31 | Pembuatan format laporan PDF | Valencia | T-02 | Todo | Empat template `.frx` + `Laporan.cs`; tanpa designer, ikuti kontrak spec. Isi data mengikuti T-30 |
| T-32 | Integrasi tampilan laporan dengan data | Valencia | T-30, T-31 | Todo | `UcLaporan` ke `ReportService`; integrasi ke shell setelah T-16 |
| T-33 | Dashboard produk terlaris | Valencia | T-02 | Todo | `DataGridView` + grafik batang. Uji setelah T-20 |

## Fase 4 — Finalisasi dan Demonstrasi

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-40 | Data demo final dan akun contoh | Gregorius Priyagung | T-02 | Todo | seed demo konsisten dengan laporan; perbarui setelah fitur terbentuk |
| T-42 | Panduan pengguna dan tangkapan layar | Gregorius Priyagung | T-00 | Todo | panduan pengguna dan screenshot; ambil screenshot setelah UI siap, dipakai saat demo |

## Fondasi Awal yang Reusable

Bagian ini disiapkan sekali di Fase 0 dan dipakai ulang oleh seluruh modul. Tidak perlu dikerjakan ulang per fitur.

| Aset | Isi | Dipakai oleh |
| :--- | :--- | :--- |
| Arsitektur sistem | Pola 3-Tier (UI, Service, Repository), pembagian modul, dan alur transaksi atomik | Semua modul |
| Model data | Skema 16 tabel, relasi antar-cabang, dan konvensi penamaan | Master data, kasir, stok, laporan |
| Aturan kerja | Branch, commit, status task, dan Definition of Done | Seluruh anggota |
| Alat bantu dokumen | Generator proposal dan template laporan | Dokumen dan laporan akhir |
