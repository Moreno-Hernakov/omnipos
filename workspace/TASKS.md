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

| NRP | Anggota | Modul formal | Bagian yang dikerjakan |
| :--- | :--- | :--- | :--- |
| 225310690 | Bagas Rizky Putra Wardana | Modul 1: Autentikasi & Konfigurasi | Onboarding, profil toko, cabang & pengguna |
| 225310691 | FX Thiarnika Eka Atur Rangga | Modul 2: Master Data & Resep BOM | Produk & kategori, bahan baku, resep/BOM & perhitungan HPP |
| 225310692 | Gregorius Priyagung | Modul 3: Kasir & Transaksi | UI katalog/keranjang, pelanggan/member, shell laporan, antrean servis, data demo & panduan |
| 225310693 | Moreno Hernakov | Modul 4: Inventaris & Stok Cabang | Fondasi arsitektur & scaffold, koneksi database, login, shell menu & hak akses, stok masuk/opname/transfer |
| 225310694 | Raymond Sugiharto | Modul 5: Operasional Kasir & Layanan | Transaksi & hold bill, struk, shift kasir, status pekerjaan jasa, alur kasir |
| 225310695 | Valencia Angie Kurniawan | Modul 6: Laporan & Analitik | Data laporan, format PDF, integrasi tampilan laporan, dashboard produk terlaris |

Catatan:

- Setiap anggota menguji fiturnya sendiri sebelum menandai `Done`.
- Fase 0, T-10 (login), dan T-12 (shell menu) dikerjakan lebih dulu sebagai contoh alur. Setelah T-03 selesai, pekerjaan modul lain boleh berjalan paralel; halaman modul tinggal dipasang ke shell sesuai peta menu di `CONVENTIONS.md` §4.3.

## Fase 0 — Fondasi

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-00 | Perancangan arsitektur, model data, dan aturan kerja tim | Moreno | — | Done | Fondasi reusable: `docs/SPECIFICATION.md`, `database/schema_pos.sql`, panduan `workspace/` |
| T-01 | Penyiapan fondasi aplikasi dan lingkungan pengembangan | Moreno | T-00 | Done | `src/OmniPos.sln` (net472, C# 7.3), paket MySql.Data/FastReport, restore+build MSBuild 0 error |
| T-02 | Penyiapan data awal dan contoh bisnis | Moreno | T-01 | Done | `database/seed_demo.sql` + `database/README.md`; 16 tabel, 5 akun demo, seed aman dijalankan ulang |
| T-03 | Koneksi aplikasi ke basis data | Moreno | T-01 | Done | `App.config` + `KoneksiDB`; tes koneksi ke MariaDB 11.4 lulus, kredensial di config bukan di kode |

## Fase 1 — Akses Pengguna, Data Master, dan Tampilan Pendukung

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-10 | Login pengguna dan validasi hak akses | Moreno | T-03 | Done | `LoginForm` + `AuthService` + `UserRepository` SHA-256; lulus uji login benar, password salah, input kosong, akun nonaktif. Login sudah terhubung ke `MainForm` dan kembali ke form login setelah Keluar |
| T-11 | Penyiapan awal toko (onboarding) | Bagas | T-03 | Todo | `OnboardingWizardForm` + `app_config`; empat tahap, set `is_onboarded=1`. Onboarding disisipkan sebelum `MainForm`; shell T-12 sudah siap |
| T-12 | Menu utama dan navigasi sesuai peran | Moreno | T-03 | Done | Dialihkan dari Bagas ke Moreno. `MainForm` shell: sidebar, header, `panelKonten`, role + feature flag dari `app_config`, tombol Keluar. Uji login 3 peran dan logout lulus; halaman modul memakai `UcSegeraHadir` sampai owner menyerahkan `UserControl` |
| T-13 | Pengelolaan produk dan kategori | Rangga | T-03 | Todo | `UcMasterProduk` + `UcKategori`; CRUD sederhana, validasi kode item. Menu: Produk & Kategori |
| T-14 | Pengelolaan bahan baku, resep, dan HPP | Rangga | T-13 | Todo | `UcBahanBaku` + `UcResepBOM` + `RecipeService`; HPP = takaran × harga bahan. Menu: Bahan Baku dan Resep & HPP |
| T-15 | Pengelolaan pelanggan/member | Gregorius Priyagung | T-03 | Todo | `UcPelanggan` CRUD; checkout tetap jalan tanpa member. Menu: Pelanggan |
| T-16 | Tampilan awal laporan (filter dan grid) | Gregorius Priyagung | T-03 | Todo | shell `UcLaporan`; tanpa query dan PDF. Shell sudah siap (T-12); owner shell menambahkan case halaman |
| T-17 | Daftar antrean servis (baca saja) | Gregorius Priyagung | T-03 | Todo | `UcServis` read-only; tanpa update status. Menu: Antrean Servis, tampil jika `enable_service=1` |
| T-18 | Pengelolaan profil toko, cabang, dan pengguna | Bagas | T-12 | Todo | `UcPengaturanToko` + `UcPengaturanPengguna` + service/repository terkait; hanya Super Admin. Menu: Profil Toko dan Cabang & Pengguna |

## Fase 2 — Operasional Kasir, Stok, dan Shift

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-20 | Pemrosesan transaksi penjualan secara utuh | Raymond | T-03 | Todo | `TransactionService` atomik: header, detail, hold, void; `MySqlTransaction` + rollback. Uji dengan produk setelah T-13, resep F&B setelah T-14 |
| T-21 | Tampilan kasir (katalog dan keranjang) | Gregorius Priyagung | T-03 | Todo | `UcKasir` layout, keranjang, tombol; tanpa logic transaksi. Shell sudah siap (T-12); owner shell menambahkan case halaman |
| T-26 | Alur kasir: pilih produk, bayar, simpan tagihan | Raymond | T-20 | Todo | `UcKasir` logic: katalog, keranjang, bayar, hold bill; integrasi event UI setelah T-21 |
| T-22 | Pengelolaan stok: barang masuk, opname, dan transfer | Moreno | T-03 | Todo | `InventoryService` + `stock_movements` untuk restock/opname/transfer; setiap perubahan stok wajib ledger. Pemotongan saat sale diintegrasikan dengan T-20. Satu `UcInventaris` dengan empat tab: Stok Masuk, Stok Opname, Transfer Stok, Riwayat Mutasi. Perlu keputusan desain: stok produk tersimpan per baris `products.branch_id`, sedangkan transfer butuh stok tujuan |
| T-23 | Cetak struk belanja | Raymond | T-03 | Todo | `PrintDocument` thermal 58/80 mm; cetak ulang tidak membuat nota baru. Uji dengan nota setelah T-20 |
| T-24 | Buka dan tutup shift kasir | Raymond | T-03 | Todo | `ShiftService` + `UcShift`: buka, blind close, rekap. Menu: Shift Kasir, tampil jika `enable_shift=1`. Rekap diuji setelah T-20 |
| T-25 | Pelacakan status pekerjaan jasa | Raymond | T-03 | Todo | Status/antrean servis + `service_jobs`; satu job per transaksi servis. Status tampil di halaman Antrean Servis. Uji dengan transaksi servis setelah T-20 |

## Fase 3 — Pelaporan dan Analitik

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-30 | Penyusunan data laporan manajemen | Valencia | T-02 | Todo | `ReportRepository` + `ReportService` (4 laporan); query parameterized, total dihitung di C#. Uji data setelah T-20 dan T-22 |
| T-31 | Pembuatan format laporan PDF | Valencia | T-02 | Todo | Empat template `.frx` + `Laporan.cs`; tanpa designer, ikuti kontrak spec. Isi data mengikuti T-30 |
| T-32 | Integrasi tampilan laporan dengan data | Valencia | T-30, T-31 | Todo | `UcLaporan` ke `ReportService`; empat jenis laporan lewat filter. Shell sudah siap (T-12) |
| T-33 | Dashboard produk terlaris | Valencia | T-02 | Todo | `UcDashboard`: `DataGridView` + grafik batang. Menu: Dashboard Produk Terlaris. Uji setelah T-20 |

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
