# Spesifikasi Teknis & Arsitektur Sistem: Omni-Industry POS Engine

## 1. Pendahuluan

Aplikasi ini dikembangkan sebagai pemenuhan Proyek Akhir (UAS) mata kuliah **Pemrograman Visual (Semester 3)**. Sistem dirancang sebagai *Point of Sales (POS)* dinamis berbasis desktop Windows Forms yang dapat beradaptasi dengan tiga karakteristik industri utama:

1. **Retail**: Mengelola stok barang jadi, kode barcode, dan penjualan langsung.
2. **Food & Beverage (F&B)**: Mengelola menu kuliner, komposisi bahan baku mentah (*Bill of Materials* / BOM), kalkulasi HPP otomatis, serta opsi simpan pesanan berbasis meja (*Hold Bill*).
3. **Jasa / Servis**: Mengelola layanan tanpa pemotongan stok fisik barang dan pelacakan status pengerjaan.

### 1.1 Status Dokumen

- **Versi**: 2.0 (baseline development).
- **Perubahan dari versi 1.0**: penetapan FastReport OpenSource untuk laporan manajemen berformat PDF, pemisahan batas antara laporan PDF dan struk thermal, penambahan tabel pendukung operasional, serta audit kesiapan development.
- **Dokumen acuan**: `docs/PROPOSAL_POS.md` (proposal yang disetujui), `database/schema_pos.sql` (DDL final), dan pengalaman implementasi FastReport pada `W13/`.
- **Aturan sinkronisasi**: setiap perubahan skema wajib dilakukan pada `schema_pos.sql` dan dideskripsikan di dokumen ini. Dokumen ini tidak boleh bertentangan dengan DDL.

### 1.2 Ruang Lingkup Versi 1

Fitur yang masuk ruang lingkup:

- Onboarding Wizard, login, RBAC, dan manajemen cabang.
- Master produk, kategori, bahan baku, resep/BOM, dan kalkulasi HPP.
- Kasir dual-mode: bayar langsung (*Paid*) dan simpan tagihan (*Hold Bill*).
- Pemotongan stok atomik, restock, stock opname, dan transfer antar-cabang.
- Shift kasir: modal awal, rekonsiliasi *blind close*, dan rekap shift.
- Manajemen pelanggan/member dan status pengerjaan jasa.
- Laporan penjualan, laba kotor, mutasi stok, dan dashboard produk terlaris.
- Struk thermal 58 mm melalui `PrintDocument`; laporan manajemen berupa PDF A4 melalui FastReport.

Di luar ruang lingkup versi 1:

- Pembayaran terbelah (*split payment*) dalam satu nota. Versi 1 memakai satu metode bayar per nota (`cash`, `qris`, atau `transfer`).
- Integrasi langsung ke printer thermal merek tertentu, API pajak, dan sinkronisasi cloud.
- Desain template FastReport melalui GUI designer. FastReport OpenSource tidak menyediakan designer.

---

## 2. Arsitektur 3-Tier

1. **Presentation Layer (`UI`)**:
   - `LoginForm`: Autentikasi user dan pengecekan flag `is_onboarded`.
   - `OnboardingWizardForm`: Tampil saat Super Admin login pertama kali.
   - `MainForm`: Single-shell container dengan navigasi dinamis berbasis hak akses dan toggle fitur.
   - `UserControl` per modul: `UcKasir`, `UcMasterProduk`, `UcResepBOM`, `UcInventaris`, `UcShift`, `UcPelanggan`, `UcServis`, `UcLaporan`.
2. **Service / Business Logic Layer (`Services`)**:
   - `OnboardingService`: Baca/tulis `app_config`.
   - `AuthService`: Hashing SHA-256 dan verifikasi hak akses.
   - `RecipeService`: Hitung total HPP menu dari daftar bahan baku mentah.
   - `InventoryService`: Pemotongan stok kondisional, restock, stock opname, dan transfer.
   - `TransactionService`: Pengelolaan transaksi kasir ber-status (*Paid, Hold, Void*) menggunakan `MySqlTransaction`.
   - `ShiftService`: Validasi modal awal dan rekonsiliasi kasir.
   - `ReportService`: Menyusun `DataTable` laporan dari filter, menghitung total, lalu memanggil pembuat PDF.
3. **Repository / Data Access Layer (`Repositories`)**:
   - `KoneksiDB`: Manajemen koneksi terpusat ke MySQL.
   - Kelas static repository berbasis ADO.NET murni dengan parameterized queries (`@param`).
   - `ReportRepository`: Query khusus laporan; tidak boleh mengembalikan koneksi terbuka.

### 2.1 Aturan Dependensi

- UI hanya memanggil Service; UI dilarang menulis SQL atau membuka `MySqlConnection`.
- Service memanggil satu atau beberapa Repository; Service tidak boleh mengakses kontrol WinForms.
- Repository hanya mengakses database; Repository tidak menampilkan `MessageBox`.
- Semua koneksi dibungkus `using`. Semua nilai input masuk query melalui parameter, bukan konkatenasi string.
- Objek uang memakai `decimal`, bukan `double`.

---

## 3. Skema Basis Data

Database: `db_uas_pos` (MySQL 8.x). DDL final ada di `database/schema_pos.sql`.

Jumlah tabel: **16 tabel fisik**, terdiri atas **12 kelompok tabel inti** (tabel `stock_transfers` dan `stock_transfer_details` dihitung satu kelompok) dan **3 tabel pendukung** untuk fitur yang sudah tercantum di proposal: member, kartu stok, dan antrean jasa.

### Tabel Konfigurasi & Autentikasi

1. `app_config` (`id`, `setting_key`, `setting_value`)
2. `branches` (`id`, `nama_cabang`, `alamat`, `no_telp`, `is_pusat`, `created_at`)
3. `users` (`id`, `branch_id`, `username`, `password_hash`, `nama_lengkap`, `role`, `is_active`, `created_at`)

### Tabel Katalog & Resep

4. `categories` (`id`, `nama_kategori`, `tipe_bisnis`)
5. `products` (`id`, `branch_id`, `category_id`, `kode_item`, `nama_produk`, `tipe`, `harga_jual`, `hpp_manual`, `stok`, `is_active`)
6. `raw_materials` (`id`, `nama_bahan`, `satuan`, `harga_beli_satuan`, `stok_minimum`)
7. `branch_materials` (`id`, `branch_id`, `raw_material_id`, `stok`)
8. `product_recipes` (`id`, `product_id`, `raw_material_id`, `takaran`)

### Tabel Kasir & Transaksi

9. `shifts` (`id`, `branch_id`, `user_id`, `waktu_buka`, `waktu_tutup`, `modal_awal`, `uang_sistem`, `uang_fisik`, `selisih`, `status`)
10. `transactions` (`id`, `nomor_nota`, `branch_id`, `user_id`, `customer_id`, `shift_id`, `waktu`, `subtotal`, `diskon`, `pajak`, `total_akhir`, `uang_bayar`, `kembalian`, `tipe_bayar`, `status`, `label_meja_pelanggan`)
11. `transaction_details` (`id`, `transaction_id`, `product_id`, `qty`, `harga_satuan`, `hpp_satuan`, `subtotal`)

### Tabel Mutasi Stok

12. `stock_transfers` (`id`, `nomor_transfer`, `dari_branch_id`, `ke_branch_id`, `user_id`, `tanggal`, `status`)
13. `stock_transfer_details` (`id`, `transfer_id`, `tipe_item`, `item_id`, `qty`)
14. `stock_movements` (`id`, `branch_id`, `tipe_item`, `item_id`, `arah`, `qty`, `stok_sebelum`, `stok_sesudah`, `sumber`, `ref_id`, `nomor_dokumen`, `keterangan`, `user_id`, `waktu`)

### Tabel Pendukung Operasional

15. `customers` (`id`, `branch_id`, `nama`, `no_telp`, `email`, `poin`, `is_active`, `created_at`)
16. `service_jobs` (`id`, `transaction_id`, `branch_id`, `nomor_antrean`, `status`, `teknisi_user_id`, `tanggal_masuk`, `tanggal_selesai`, `catatan`)

### 3.1 Aturan Tabel Pendukung

- `transactions.customer_id` boleh `NULL`; diisi hanya saat kasir memilih member. Relasi memakai `ON DELETE SET NULL`.
- `stock_movements` adalah buku besar stok. Setiap perubahan stok wajib menulis satu baris di tabel ini di dalam transaksi database yang sama dengan perubahan stok.
  - `tipe_item`: `product` atau `material`.
  - `arah`: `in` atau `out`.
  - `sumber`: `sale`, `restock`, `opname`, `transfer_in`, `transfer_out`, atau `void`.
  - `ref_id`: ID transaksi, transfer, atau dokumen sumber; boleh `NULL` untuk restock/opname yang hanya memakai `nomor_dokumen`.
  - `stok_sebelum` dan `stok_sesudah` dipakai untuk kartu stok dan audit.
- `service_jobs` dibuat otomatis saat transaksi bertipe jasa disimpan, atau saat kasir menandai pesanan sebagai pekerjaan servis. Satu transaksi servis memiliki maksimal satu `service_jobs`.
- `stock_movements.item_id` bersifat polimorfik (menunjuk `products.id` atau `raw_materials.id`), sehingga tidak memakai foreign key ke salah satu tabel. Validasi dilakukan di `InventoryService`.

---

## 4. Pembagian Modul Tim (6 Anggota)

```text
1. Autentikasi & Konfigurasi
~ Login & Role Access (RBAC)
~ Onboarding Wizard
~ Manajemen Cabang

2. Master Data & Resep
~ Kategori, Produk & Layanan
~ Bahan Baku
~ Resep / BOM
~ Kalkulasi HPP Otomatis

3. Kasir & Transaksi
~ Katalog & Keranjang Belanja
~ Bayar Langsung
~ Simpan Tagihan (Hold Bill / Meja)
~ Hitung Diskon, Pajak & Cetak Struk

4. Inventaris & Stok
~ Stok Masuk (Restock)
~ Stock Opname (Penyesuaian Stok)
~ Transfer Stok Antar-Cabang
~ Peringatan Stok Menipis

5. Operasional Kasir & Layanan
~ Shift Kasir (Modal Awal & Tutup Kasir)
~ Manajemen Pelanggan / Member
~ Status Pengerjaan Jasa / Antrean

6. Laporan & Analitik
~ Laporan Penjualan (Harian, Bulanan, Cabang)
~ Laporan Laba Kotor (Omzet minus HPP)
~ Laporan Mutasi Stok
~ Dashboard Menu Terlaris
```

---

## 5. Arsitektur Pelaporan & Pencetakan

### 5.1 Batas FastReport dan PrintDocument

| Keluaran | Teknologi | Format | Alasan |
| :--- | :--- | :--- | :--- |
| Laporan penjualan | FastReport OpenSource + `PDFSimpleExport` | PDF A4 | Laporan tabel multi-halaman, filter, total, dan arsip digital. |
| Laporan laba kotor | FastReport OpenSource + `PDFSimpleExport` | PDF A4 | Rekap omzet, HPP, dan margin per produk. |
| Laporan mutasi stok | FastReport OpenSource + `PDFSimpleExport` | PDF A4 | Kartu stok berbasis `stock_movements`. |
| Rekap shift kasir | FastReport OpenSource + `PDFSimpleExport` | PDF A4 | Bukti serah terima kasir dan rekonsiliasi kas. |
| Struk nota kasir | `PrintDocument` WinForms | Thermal 58 mm (default) / 80 mm | Kertas thermal, lebar tetap, dicetak langsung ke printer. |
| Salinan nota PDF | Tidak termasuk v1 | — | Bisa ditambahkan kemudian sebagai laporan FastReport A5 bila diminta dosen. |

FastReport **tidak** dipakai untuk struk thermal. `PDFSimpleExport` menghasilkan PDF halaman penuh, bukan perintah cetak thermal. Pemisahan ini menjaga proposal yang sudah disetujui tetap berlaku: struk memakai `PrintDocument`, laporan manajemen memakai FastReport.

Catatan rekonsiliasi proposal: proposal awal menyebut lembar rekapitulasi shift kasir dicetak dengan `PrintDocument` selebar struk. Spesifikasi v2 memindahkan rekap shift ke FastReport A4 karena isinya tabel rekonsiliasi multi-kolom, bukan struk thermal. Ruang lingkup fitur tidak berubah; yang berubah hanya media cetak laporan. Struk nota kasir tetap memakai `PrintDocument`.

### 5.2 Dependensi dan Konfigurasi Proyek

| Komponen | Versi / Konfigurasi |
| :--- | :--- |
| Target framework | .NET Framework **4.7.2** |
| Bahasa | C# 7.3 |
| Database driver | `MySql.Data` **8.4.0** |
| Report engine | `FastReport.OpenSource` **2026.2.8** |
| PDF exporter | `FastReport.OpenSource.Export.PdfSimple` **2026.2.8** |
| Referensi wajib | `Microsoft.CSharp`, `System.Data`, `System.Drawing`, `System.Windows.Forms`, `System.Xml` |
| Binding redirect | `AutoGenerateBindingRedirects` = `true` |
| Restore paket | `MSBuild.exe <project>.csproj -t:Restore` |

Catatan lingkungan:

- `dotnet restore` gagal pada project .NET Framework lama dengan error `RuntimeIdentifier 'win'`. Gunakan MSBuild.
- FastReport tetap kompatibel dengan .NET Framework 4.7.2 karena assembly paket menargetkan `net462`.
- Project harus dijalankan sebagai `.exe` dengan `App.config` yang ikut tersalin, bukan dihosting PowerShell, agar binding redirect assembly berjalan.

### 5.3 Struktur Class Pelaporan

```text
Services/
  ReportService.cs          # filter, query, hitung total, panggil Laporan
Repositories/
  ReportRepository.cs       # query laporan (parameterized)
Reports/
  Laporan.cs                # mesin FastReport, template, export PDF
  Templates/
    laporan_penjualan.frx
    laporan_laba_kotor.frx
    laporan_mutasi_stok.frx
    laporan_shift.frx
```

Tanggung jawab:

- `ReportRepository` hanya menjalankan query dan mengembalikan `DataTable`.
- `ReportService` memvalidasi filter (tanggal awal ≤ tanggal akhir, cabang wajib untuk manajer), memformat nilai uang/tanggal, menghitung total, lalu memanggil method `Laporan`.
- `Laporan` tidak mengenal kontrol UI. Input-nya `DataTable`, parameter teks, dan nama file output.
- `UcLaporan` hanya menampilkan filter, `DataGridView` pratinjau, tombol **Tampilkan** dan **Cetak PDF**.

### 5.4 Daftar Laporan dan Kontrak Data

Semua nama tabel `DataTable` dan nama kolom ditulis huruf kecil. Nama tabel harus sama dengan nama datasource di template `.frx`.

#### A. Laporan Penjualan

- Template: `laporan_penjualan.frx`
- Nama tabel: `penjualan`
- Filter: rentang tanggal, cabang, kasir, status nota (`paid`/`hold`/`void`), metode bayar (`cash`/`qris`/`transfer`).
- Akses: Super Admin (semua cabang), Branch Manager (cabang sendiri).
- Kolom:

| Kolom | Isi |
| :--- | :--- |
| `nomor_nota` | Nomor nota |
| `waktu` | Tanggal dan jam, format `dd/MM/yyyy HH:mm` |
| `nama_cabang` | Nama cabang |
| `nama_kasir` | Nama lengkap kasir |
| `nama_pelanggan` | Nama member atau `-` |
| `tipe_bayar` | `Tunai`, `QRIS`, atau `Transfer` |
| `status` | `Lunas`, `Gantung`, atau `Batal` |
| `subtotal` | Rupiah terformat |
| `diskon` | Rupiah terformat |
| `pajak` | Rupiah terformat |
| `total_akhir` | Rupiah terformat |

Total yang dikirim sebagai parameter: `total_subtotal`, `total_diskon`, `total_pajak`, `total_akhir`, dan `jumlah_nota`.

#### B. Laporan Laba Kotor

- Template: `laporan_laba_kotor.frx`
- Nama tabel: `laba_kotor`
- Filter: rentang tanggal, cabang, kategori.
- Akses: Super Admin (semua cabang), Branch Manager (cabang sendiri).
- Kolom:

| Kolom | Isi |
| :--- | :--- |
| `nama_produk` | Nama produk/menu/layanan |
| `nama_kategori` | Nama kategori atau `-` |
| `qty_terjual` | Jumlah kuantitas, format `N2` |
| `omzet` | Rupiah terformat |
| `hpp` | Rupiah terformat |
| `laba_kotor` | Rupiah terformat |
| `margin_persen` | Persentase laba, format `N2` + `%` |

Total parameter: `total_omzet`, `total_hpp`, `total_laba_kotor`, `margin_total_persen`.

#### C. Laporan Mutasi Stok

- Template: `laporan_mutasi_stok.frx`
- Nama tabel: `mutasi_stok`
- Filter: rentang tanggal, cabang, tipe item (`product`/`material`), item tertentu (opsional).
- Akses: Super Admin (semua cabang), Branch Manager (cabang sendiri).
- Kolom:

| Kolom | Isi |
| :--- | :--- |
| `waktu` | Tanggal dan jam, format `dd/MM/yyyy HH:mm` |
| `nomor_dokumen` | Nomor nota/transfer/dokumen restock/opname |
| `nama_item` | Nama produk atau bahan mentah |
| `tipe_item` | `Produk` atau `Bahan` |
| `satuan` | Satuan item (`pcs`, `gram`, `ml`, dan seterusnya) |
| `masuk` | Qty masuk, format `N2` |
| `keluar` | Qty keluar, format `N2` |
| `saldo` | Stok setelah mutasi, format `N2` |
| `sumber` | `Penjualan`, `Restock`, `Opname`, `Transfer Masuk`, `Transfer Keluar`, `Void` |
| `keterangan` | Keterangan tambahan atau `-` |
| `nama_user` | Petugas yang mencatat |

Total parameter: `total_masuk`, `total_keluar`.

#### D. Rekap Shift Kasir

- Template: `laporan_shift.frx`
- Nama tabel: `rekap_shift`
- Filter: shift tertentu, atau rentang tanggal + cabang + kasir.
- Akses: Super Admin (semua), Branch Manager (cabang sendiri), Cashier (hanya shift miliknya).
- Kolom:

| Kolom | Isi |
| :--- | :--- |
| `nama_cabang` | Nama cabang |
| `nama_kasir` | Nama kasir |
| `waktu_buka` | Tanggal dan jam, format `dd/MM/yyyy HH:mm` |
| `waktu_tutup` | Tanggal dan jam atau `-` bila masih open |
| `modal_awal` | Rupiah terformat |
| `total_tunai` | Total transaksi tunai `paid` selama shift |
| `total_non_tunai` | Total QRIS/transfer `paid` selama shift |
| `uang_sistem` | Rupiah terformat |
| `uang_fisik` | Rupiah terformat |
| `selisih` | Rupiah terformat; negatif diawali `-` |
| `status` | `Buka` atau `Tutup` |

Total parameter: `total_modal_awal`, `total_uang_sistem`, `total_uang_fisik`, `total_selisih`.

#### E. Dashboard Produk Terlaris

Dashboard bukan PDF. `UcLaporan` menampilkan `DataGridView` dan grafik batang (kontrol WinForms) dari query:

```sql
SELECT p.nama_produk, SUM(td.qty) AS qty_terjual, SUM(td.subtotal) AS omzet
FROM transaction_details td
JOIN transactions t ON t.id = td.transaction_id
JOIN products p ON p.id = td.product_id
WHERE t.status = 'paid'
  AND t.waktu BETWEEN @awal AND @akhir
  AND (@branch_id IS NULL OR t.branch_id = @branch_id)
GROUP BY p.id, p.nama_produk
ORDER BY qty_terjual DESC
LIMIT 10;
```

### 5.5 Kontrak Template FastReport

Setiap template memakai struktur band berikut:

| Band | Fungsi |
| :--- | :--- |
| `ReportTitleBand` | Nama toko, alamat, telepon, dan judul laporan |
| `PageHeaderBand` | Label kolom tabel |
| `DataBand` bernama `Data1` | Baris data dari `DataTable` |
| `ReportSummaryBand` | Total dan catatan |
| `PageFooterBand` | “Halaman [Page#] dari [TotalPages#]”, waktu cetak, nama pencetak |

Aturan teknis:

- Kertas A4 portrait: `PaperWidth = 210` mm, `PaperHeight = 297` mm, margin 15 mm. Lebar konten maksimum 180 mm.
- Posisi dan ukuran objek memakai pixel 96 dpi. Konversi wajib: `mm / 25.4f * 96f`. Jangan mencampur satuan mm dan pixel.
- `DataHeaderBand` tidak boleh menjadi anak langsung `ReportPage`; gunakan `PageHeaderBand`, atau letakkan `DataHeaderBand` di dalam `DataBand`.
- Ekspresi data memakai `[penjualan.nomor_nota]`, `[laba_kotor.omzet]`, dan seterusnya. Nama tabel harus sama dengan `DataTable.TableName`.
- Nilai uang dan tanggal diformat di C# sebelum masuk `DataTable`. Template hanya menampilkan string, sehingga hasil tidak bergantung pada locale mesin.
- Parameter laporan diisi dengan `report.SetParameterValue(nama, nilai)` setelah `Load()` dan sebelum `Prepare()`. Method ini membuat parameter bila belum ada.
- Jangan memakai alias dataset yang bentrok dengan namespace FastReport. Panggil `report.RegisterData(ds)` tanpa alias, bukan `RegisterData(ds, "Data")`.
- Panggil `report.Dictionary.Connections.Clear()` setelah `Load()` agar koneksi desainer yang tidak ada tidak ikut diproses.
- Aktifkan datasource tabel (`report.GetDataSource(namaTabel).Enabled = true`) dan hubungkan `Data1` ke datasource tersebut.

### 5.6 Alur Cetak PDF

```text
UcLaporan (filter)
   -> ReportService.AmbilLaporan...()
   -> ReportRepository (query parameterized)
   -> DataTable + total + parameter teks
   -> Laporan.Cetak...()
   -> Report.Load(template .frx)
   -> Dictionary.Connections.Clear()
   -> RegisterData(ds)
   -> SetParameterValue(...)
   -> Prepare()
   -> PDFSimpleExport.Export(report, path)
   -> Process.Start(path)
```

Langkah wajib di `Laporan`:

1. Pastikan folder output ada (`Directory.CreateDirectory`).
2. Pastikan file template ada. Bila hilang, panggil `PastikanTemplate()` untuk membuat ulang dari kode.
3. Sebelum `Prepare()`, sentuh `typeof(Microsoft.CSharp.RuntimeBinder.Binder).Assembly` dan `typeof(System.Linq.Enumerable).Assembly` untuk mencegah error `CS0006: Metadata file 'Microsoft.CSharp' could not be found`.
4. Bungkus `Report` dengan `try/finally` dan panggil `Dispose()`.
5. Simpan PDF dengan nama unik, lalu buka memakai `Process.Start(path)`.
6. Bila `DataTable.Rows.Count == 0`, tampilkan `MessageBox` “Tidak ada data pada filter ini” dan jangan membuat PDF kosong.

### 5.7 Lokasi dan Nama File Output

- Folder: `Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments)\OmniPOS\Laporan`.
- Nama file:
  - `LaporanPenjualan_yyyyMMdd_HHmmss.pdf`
  - `LaporanLabaKotor_yyyyMMdd_HHmmss.pdf`
  - `LaporanMutasiStok_yyyyMMdd_HHmmss.pdf`
  - `RekapShift_yyyyMMdd_HHmmss.pdf`
- Format waktu memakai `CultureInfo.InvariantCulture` agar nama file konsisten.
- File lama tidak dihapus otomatis. Pembersihan manual dilakukan pengguna.

### 5.8 Penanganan Error dan Batasan Paket

- `CS0006: Metadata file 'Microsoft.CSharp' could not be found`: tambahkan `<Reference Include="Microsoft.CSharp" />` dan sentuh assembly sebelum `Prepare()`.
- `CS0234 ... does not exist in the namespace 'FastReport.Data'`: jangan memakai alias dataset yang sama dengan namespace FastReport.
- PDF hasil `PDFSimpleExport` berbentuk raster (satu JPEG per halaman). Teks tidak dapat diselect atau dicari. Ini batasan paket, bukan bug aplikasi dan sudah diterima untuk laporan UAS.
- FastReport OpenSource tidak memiliki report designer. Template `.frx` dibuat dari kode dan disimpan sebagai artefak sumber; jangan mengandalkan GUI designer.
- Bila `Prepare()` gagal karena binding redirect, pastikan aplikasi dijalankan sebagai `.exe` dengan `App.config`, bukan dari host PowerShell.

### 5.9 Struk Thermal

- Struk memakai `PrintDocument` dengan `PrintPage` yang menggambar teks dan garis.
- Lebar default 58 mm; opsi 80 mm disediakan lewat pengaturan printer, bukan template FastReport.
- Isi struk: nama toko/alamat/telepon dari `app_config`, nomor nota, waktu, kasir, daftar item (nama, qty, harga, subtotal), subtotal, diskon, pajak, total, metode bayar, uang bayar, kembalian, dan ucapan terima kasih.
- Data struk diambil dari `transactions` + `transaction_details` setelah transaksi `Commit()`.
- Cetak ulang struk memakai data yang sama; tidak membuat transaksi baru.

---

## 6. Struktur Proyek dan Konvensi

### 6.1 Struktur Solution

```text
UAS_POS/
├── src/
│   ├── OmniPos.sln
│   └── OmniPos/
│       ├── OmniPos.csproj
│       ├── App.config
│       ├── Program.cs
│       ├── Forms/
│       │   ├── LoginForm.cs
│       │   ├── OnboardingWizardForm.cs
│       │   └── MainForm.cs
│       ├── Controls/
│       │   ├── UcKasir.cs
│       │   ├── UcMasterProduk.cs
│       │   ├── UcResepBOM.cs
│       │   ├── UcInventaris.cs
│       │   ├── UcShift.cs
│       │   ├── UcPelanggan.cs
│       │   ├── UcServis.cs
│       │   └── UcLaporan.cs
│       ├── Services/
│       ├── Repositories/
│       ├── Models/
│       └── Reports/
│           ├── Laporan.cs
│           └── Templates/*.frx
├── database/schema_pos.sql
└── docs/
```

### 6.2 Konvensi Kode

- C# 7.3. Tidak memakai async/await, LINQ berantai panjang, generic/interface/abstract class, dependency injection, atau library di luar yang disetujui.
- Nama class dan method: PascalCase. Variabel lokal dan parameter: camelCase.
- Nama kontrol mengikuti pola `buttonSimpan`, `textBoxNama`, `dataGridViewProduk`, `labelTotal`.
- Identifier domain boleh Bahasa Indonesia (`namaProduk`, `totalAkhir`) selama konsisten dalam satu class.
- Setiap event handler UI memiliki `try/catch` yang menampilkan pesan error singkat dan tidak menelan exception tanpa jejak.
- Service melakukan validasi input dan melempar `ArgumentException`/`InvalidOperationException` dengan pesan yang bisa ditampilkan UI.
- Repository memakai `using` untuk koneksi, command, dan reader.
- Nominal uang disimpan dan dihitung sebagai `decimal`; pembulatan dilakukan saat format tampilan.
- Password disimpan sebagai hash SHA-256 hex lowercase sesuai proposal. Password plaintext tidak boleh dicatat di log atau pesan error.

### 6.3 RBAC dan Navigasi

| Menu / Aksi | Super Admin | Branch Manager | Cashier |
| :--- | :---: | :---: | :---: |
| Onboarding & manajemen cabang | Ya | Tidak | Tidak |
| Master produk, bahan, resep/BOM | Ya | Ya (cabang sendiri) | Tidak |
| Kasir & transaksi | Ya | Ya (cabang sendiri) | Ya |
| Restock, opname, transfer | Ya | Ya (cabang sendiri) | Tidak |
| Shift | Ya | Ya (cabang sendiri) | Ya (shift sendiri) |
| Member & servis | Ya | Ya (cabang sendiri) | Ya |
| Laporan penjualan & laba kotor | Ya | Ya (cabang sendiri) | Tidak |
| Laporan mutasi stok | Ya | Ya (cabang sendiri) | Tidak |
| Rekap shift | Ya | Ya (cabang sendiri) | Hanya shift sendiri |
| Pengaturan pengguna | Ya | Tidak | Tidak |

Aturan tambahan:

- `MainForm` menyusun menu dari role dan feature flag. Menu yang tidak berhak tidak ditampilkan, bukan hanya dinonaktifkan.
- Service tetap memeriksa role dan `branch_id`; menyembunyikan menu bukan kontrol keamanan.
- `enable_multi_branch = 0` menyembunyikan menu transfer dan filter cabang; semua data memakai cabang pusat.

### 6.4 Feature Flag

Nilai awal ada di `app_config`:

| Key | Nilai | Efek |
| :--- | :--- | :--- |
| `is_onboarded` | `0` / `1` | Menentukan apakah wizard wajib tampil |
| `business_name` | teks | Nama toko pada UI, struk, dan laporan |
| `business_address` | teks | Alamat pada struk dan laporan |
| `business_phone` | teks | Telepon pada struk dan laporan |
| `enable_retail` | `0` / `1` | Menampilkan kategori dan produk retail |
| `enable_fnb` | `0` / `1` | Menampilkan menu, bahan baku, dan resep |
| `enable_recipe_bom` | `0` / `1` | Mengaktifkan kalkulasi HPP dan pemotongan bahan |
| `enable_service` | `0` / `1` | Menampilkan layanan, antrean, dan status servis |
| `enable_shift` | `0` / `1` | Mewajibkan buka shift sebelum transaksi |
| `enable_multi_branch` | `0` / `1` | Menampilkan transfer stok dan filter cabang |
| `tax_percentage` | angka | Tarif pajak default transaksi |

---

## 7. Kesiapan Development

### 7.1 Yang Sudah Siap

- Arsitektur 3-tier, aturan dependensi, dan pembagian modul.
- Dependensi dan versi paket yang sudah diverifikasi pada W13.
- Skema inti dan tabel pendukung untuk member, kartu stok, dan antrean jasa.
- Alur transaksi atomik, pemotongan stok kondisional, dan aturan `stock_movements`.
- Kontrak data setiap laporan, nama template, parameter, dan format output.
- Matriks RBAC dan feature flag.
- Kriteria penerimaan laporan dan struk.

### 7.2 Yang Belum Siap dan Menjadi Blocker Implementasi

| Area | Status | Tindakan sebelum coding |
| :--- | :--- | :--- |
| Scaffold solution `src/OmniPos.sln` | Belum ada | Buat project .NET Framework 4.7.2, pasang paket, restore via MSBuild, build 0 error. |
| Template `.frx` | Belum dibuat | Buat 4 template dari kode, uji dengan data contoh, commit file `.frx`. |
| Data seed demo | Belum ada | Tambahkan seed 2 cabang, 3 user, 5 produk, 3 resep, 1 shift, dan 5 transaksi contoh. |
| Mockup UI | Belum ada | Setujui layout `MainForm`, `UcKasir`, `UcLaporan`, dan form dialog. |
| Query laporan | Baru kontrak | Implementasikan `ReportRepository` dan uji total terhadap data seed. |
| Struk thermal | Baru kontrak | Tetapkan 58 mm sebagai default dan uji `PrintPreviewDialog`. |
| Pengujian | Baru kriteria | Siapkan skenario uji per modul dan data uji rollback. |

### 7.3 Definition of Ready per Fase

**Fase 1 — Fondasi (bisa dimulai sekarang):**
- Setup solution, `KoneksiDB`, `App.config`, dan struktur folder.
- Login, onboarding, master data, dan RBAC.
- Build 0 error dan koneksi database berhasil.

**Fase 2 — Kasir & Stok:**
- `TransactionService` atomik, `stock_movements`, struk thermal.
- Uji rollback saat stok kurang.
- Uji pemotongan produk retail, bahan F&B, dan layanan jasa.

**Fase 3 — Laporan:**
- Empat template `.frx` dan empat method `Laporan`.
- `ReportService` + `ReportRepository`.
- Uji PDF dengan data seed dan filter kosong.

**Fase 4 — Finalisasi:**
- Uji RBAC, multi-cabang, dan feature flag.
- Uji regresi transaksi dan laporan.
- Susun naskah akhir dan data demo.

---

## 8. Kriteria Penerimaan

### 8.1 Laporan PDF

1. Build MSBuild menghasilkan 0 error dan paket FastReport termuat.
2. Setiap laporan menghasilkan PDF di folder output dan otomatis terbuka.
3. Header PDF memuat nama toko, alamat, telepon, judul, periode, dan info filter.
4. Jumlah baris dan total pada PDF sama dengan hasil query dan `DataGridView`.
5. Filter tanggal, cabang, kasir, status, dan metode bayar bekerja sesuai kontrak.
6. Filter tanpa data menampilkan pesan “Tidak ada data pada filter ini” tanpa crash.
7. PDF multi-halaman memiliki nomor halaman dan header kolom berulang.
8. Branch Manager tidak dapat mencetak data cabang lain; Cashier tidak dapat membuka laporan manajemen.
9. Nama file unik dan tidak menimpa file sebelumnya.

### 8.2 Struk Thermal

1. `PrintPreviewDialog` menampilkan struk 58 mm dengan teks tidak terpotong.
2. Item, qty, harga, subtotal, diskon, pajak, total, bayar, dan kembalian benar.
3. Cetak ulang tidak membuat nota baru.
4. Struk tetap dapat dicetak saat fitur FastReport gagal dimuat.

### 8.3 Transaksi dan Stok

1. Transaksi gagal karena stok kurang tidak menyisakan header, detail, atau mutasi stok.
2. Setiap perubahan stok menghasilkan satu baris `stock_movements` dengan `stok_sebelum` dan `stok_sesudah` yang benar.
3. Transfer `pending` mengurangi stok asal; transfer `completed` menambah stok tujuan; pembatalan mengembalikan stok asal.
4. Penjualan jasa tidak memotong stok produk atau bahan.
5. Hold Bill dapat dilunasi tanpa menduplikasi detail atau memotong stok dua kali.

---

## 9. Referensi Implementasi

- FastReport W13: `W13/225310693 - Moreno Hernakov - tugas/week13_vp/Laporan.cs`.
- Catatan teknis FastReport: `ctx/w13.md`.
- DDL: `UAS_POS/database/schema_pos.sql`.
- Proposal: `UAS_POS/docs/PROPOSAL_POS.md`.
