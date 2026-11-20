# Mockup Halaman (ASCII, Windows Forms)

Dokumen ini adalah gambaran tata letak setiap layar OmniPOS sebelum dikodekan. Semua gambar memakai kontrol Windows Forms yang bisa dibuat di Visual Studio Designer. Isi field, validasi, dan alur ada di `07-ALUR-PENGGUNA.md`; aturan bisnis di `06-SPESIFIKASI.md`; geometri shell dan tema di `05-UI-SHELL.md`.

Cara pakai:

- Owner halaman memakai mockup sebagai acuan susunan kontrol, bukan sebagai file Designer final. Jarak dan ukuran boleh disesuaikan saat implementasi; field, urutan langkah, dan aturan aktif/nonaktif tidak.
- Bagian yang diberi label **USULAN** belum ada di spec. Itu keputusan desain yang masih bisa diubah owner; daftar lengkapnya ada di §13.
- Mockup tidak berskala piksel. Satu karakter kira-kira 10 px lebar dan 20 px tinggi.
- Kalau mockup dan `06-SPESIFIKASI.md` berbeda soal perilaku, `06` menang dan mockup diperbaiki.

---

## 1. Cara Membaca

| Simbol | Kontrol Windows Forms |
| :--- | :--- |
| `[ teks          ]` | `TextBox`; beberapa baris `[ ]` bertumpuk = `Multiline` |
| `[ teks        v]` | `ComboBox` (`DropDownList`) |
| `[ 10,00      ^v]` | `NumericUpDown` |
| `[ 20/11/2026  v]` | `DateTimePicker` |
| `[x]` / `[ ]` | `CheckBox` tercentang / kosong |
| `(o)` / `( )` | `RadioButton` terpilih / tidak |
| `[ Simpan ]` | `Button` biasa |
| `[[ Bayar ]]` | `Button` utama (biru `#2563EB`) |
| `[- Kembali -]` | `Button` dengan `Enabled = false` |
| `[*Produk*] [ Kategori ]` | `TabControl`; tanda `*` = tab aktif |
| `+----+----+` dengan header | `DataGridView` (`ReadOnly`, `FullRowSelect`) |
| `+- Judul ----+` | `GroupBox` atau `Panel` kartu |
| `> ` di awal baris | baris/menu yang sedang dipilih |
| `*` di label menu | menu hanya tampil jika feature flag aktif |

Aturan umum semua halaman:

- Label selalu terlihat di atas atau di samping input; placeholder bukan pengganti label.
- Tanda `*` pada label = wajib diisi.
- Pesan kesalahan tampil di `Label` dekat field atau `MessageBox`; halaman tidak menutup sendiri saat gagal.
- Uang memakai `decimal` dan `NumericUpDown` dengan `DecimalPlaces = 0`.

---

## 2. Peta Halaman

| Bagian | Layar | Class | Task | Owner | Siapa yang melihat |
| :--- | :--- | :--- | :--- | :--- | :--- |
| §3.1 | Login | `LoginForm` | T-10 | Moreno | Semua |
| §3.2 | Penyiapan awal (4 langkah) | `OnboardingWizardForm` | T-11 | Bagas | Super Admin, saat `is_onboarded = 0` |
| §4.1 | Shell | `MainForm` | T-12 | Moreno | Semua |
| §4.2 | Beranda | `UcBeranda` | T-12 | Moreno | SA, BM, Kasir |
| §5 | Transaksi Kasir + Daftar Nota | `UcKasir` | T-21 | Raymond | SA, BM, Kasir |
| §6 | Shift Kasir | `UcShift` | T-24 | Raymond | SA, BM, Kasir |
| §7 | Pelanggan | `UcPelanggan` | T-15 | Gregorius | SA, BM, Kasir |
| §8 | Antrean Servis | `UcServis` | T-25 | Raymond | SA, BM, Kasir |
| §9.1 | Produk & Kategori | `UcMasterProduk` | T-13 | Rangga | SA, BM |
| §9.2 | Bahan Baku | `UcBahanBaku` | T-14 | Rangga | SA, BM |
| §9.3 | Resep & HPP | `UcResepBOM` | T-14 | Rangga | SA, BM |
| §10 | Inventaris (4 tab) | `UcInventaris` | T-22 | Moreno | SA, BM |
| §11.1 | Laporan | `UcLaporan` | T-32 | Valencia | SA, BM |
| §11.2 | Dashboard Produk Terlaris | `UcDashboard` | T-33 | Valencia | SA, BM |
| §12.1 | Profil Toko | `UcPengaturanToko` | T-18 | Bagas | SA |
| §12.2 | Cabang & Pengguna | `UcPengaturanPengguna` | T-18 | Bagas | SA |

Role dan feature flag tiap menu mengikuti peta di `05-UI-SHELL.md` §3.

---

## 3. Jendela Mandiri

Login dan onboarding adalah `Form` sendiri, bukan `UserControl`, dan tidak berada di dalam shell.

### 3.1 LoginForm (T-10, sudah dibuat)

`FormBorderStyle = FixedSingle`, tanpa tombol maksimalkan/minimalkan, `StartPosition = CenterScreen`, `ClientSize` 440 × 424, `AcceptButton` = tombol Masuk. Gambar di bawah mengikuti `LoginForm.Designer.cs`.

```text
+- OmniPOS - Login --------------------------+
| [O] OmniPOS                                |
|     Masuk dengan akun pengguna             |
+--------------------------------------------+
|                                            |
| Username                                   |
| [                                        ] |
|                                            |
| Password                                   |
| [ ********                               ] |
|                                            |
| [[                Masuk                 ]] |
|                                            |
| Pesan error tampil di sini (teks merah).   |
|                                            |
|                OmniPOS v1.0                |
+--------------------------------------------+
```

- Username kosong atau password kosong, password salah, dan akun nonaktif menampilkan pesan di label merah; password dikosongkan dan fokus kembali ke password.
- Gate setelah login (wizard atau shell) ada di `07-ALUR-PENGGUNA.md` §1.

### 3.2 OnboardingWizardForm (T-11, 4 langkah)

Satu `Form` modal (`ShowDialog`) dengan satu `Panel` per langkah. Indikator langkah, judul, dan tombol di footer ada di Designer; yang berganti hanya panel isi. Tidak ada tulisan database sebelum **Selesai** (`07` §2). Field dan validasi tiap langkah ada di tabel `07` §2; gambar ini hanya susunan kontrolnya.

Footer sama di semua langkah: **Batal** di kiri; **Kembali** dan **Lanjut** di kanan. Di langkah 1 **Kembali** nonaktif; di langkah 4 **Lanjut** menjadi **Selesai**.

**Langkah 1 - Identitas usaha**

```text
+- OnboardingWizardForm - Langkah 1 dari 4 --------------------------------------+
| (1) IDENTITAS --- ( ) Model bisnis --- ( ) Operasional --- ( ) Cabang & akun   |
+--------------------------------------------------------------------------------+
| Identitas usaha                                                                |
| Data ini dipakai di header, struk, dan laporan.                                |
|                                                                                |
| Nama usaha *                                                                   |
| [ Kopi Senja                                                             ]     |
| Alamat *                                                                       |
| [ Jl. Ngagel Jaya Tengah No. 73-77, Surabaya                             ]     |
| [                                                                        ]     |
| Telepon *                                                                      |
| [ 031-5041500                ]  Angka, spasi, + - ( )                          |
|                                                                                |
| Bisa diubah lagi lewat menu Profil Toko.                                       |
+--------------------------------------------------------------------------------+
| [ Batal ]                                           [- Kembali -] [[ Lanjut ]] |
+--------------------------------------------------------------------------------+
```

**Langkah 2 - Model bisnis**

```text
+- OnboardingWizardForm - Langkah 2 dari 4 --------------------------------------+
| (v) Identitas --- (2) MODEL BISNIS --- ( ) Operasional --- ( ) Cabang & akun   |
+--------------------------------------------------------------------------------+
| Model bisnis                                                                   |
| Pilih model yang dijalankan. Menu mengikuti pilihan ini.                       |
|                                                                                |
| +- Model bisnis yang dijalankan -----------------------------------------+     |
| | [x] Retail                                                             |     |
| |     Barang jadi dan barcode. Stok berkurang saat terjual.              |     |
| | [x] F&B                                                                |     |
| |     Menu dan bahan mentah. Stok dipotong lewat resep.                  |     |
| | [ ] Jasa                                                               |     |
| |     Layanan dan antrean kerja. Tidak memotong stok barang.             |     |
| +------------------------------------------------------------------------+     |
|                                                                                |
| Minimal satu model harus dipilih.                                              |
+--------------------------------------------------------------------------------+
| [ Batal ]                                             [ Kembali ] [[ Lanjut ]] |
+--------------------------------------------------------------------------------+
```

**Langkah 3 - Mesin dan operasional**

```text
+- OnboardingWizardForm - Langkah 3 dari 4 --------------------------------------+
| (v) Identitas --- (v) Model bisnis --- (3) OPERASIONAL --- ( ) Cabang & akun   |
+--------------------------------------------------------------------------------+
| Mesin & operasional                                                            |
| Saklar fitur dan pajak default. Semua bisa diubah lagi nanti.                  |
|                                                                                |
| +- Fitur operasional ----------------------------------------------------+     |
| | [x] Resep & HPP                                                        |     |
| |     Hanya aktif kalau F&B dipilih. HPP dihitung dari takaran bahan.    |     |
| | [x] Wajib buka shift                                                   |     |
| |     Kasir membuka shift dan mengisi modal awal sebelum transaksi.      |     |
| | [x] Multi-cabang                                                       |     |
| |     Menyalakan transfer stok antar-cabang dan filter cabang.           |     |
| +------------------------------------------------------------------------+     |
|                                                                                |
| Pajak default (%)  [ 10,00        ^v]  Nilai awal pajak di kasir.              |
+--------------------------------------------------------------------------------+
| [ Batal ]                                             [ Kembali ] [[ Lanjut ]] |
+--------------------------------------------------------------------------------+
```

**Langkah 4 - Cabang dan akun**

```text
+- OnboardingWizardForm - Langkah 4 dari 4 --------------------------------------+
| (v) Identitas --- (v) Model bisnis --- (v) Operasional --- (4) CABANG & AKUN   |
+--------------------------------------------------------------------------------+
| Cabang & akun                                                                  |
| Selesaikan data cabang pusat dan akun Super Admin pertama.                     |
|                                                                                |
| +- Cabang pusat --------------------+ +- Akun administrator ---------------+   |
| | Nama cabang *                     | | Username *                         |   |
| | [ Kopi Senja - Pusat            ] | | [ admin                          ] |   |
| | Alamat *                          | | Nama lengkap *                     |   |
| | [ Jl. Ngagel Jaya Tengah 73-77  ] | | [ Super Administrator            ] |   |
| | [                               ] | | Password *                         |   |
| | Telepon *                         | | [ ********                       ] |   |
| | [ 031-5041500                   ] | | Konfirmasi password *              |   |
| |                                   | | [ ********                       ] |   |
| | Terisi dari langkah 1,            | |                                    |   |
| | boleh diubah.                     | | Dipakai login setelah penyiapan.   |   |
| |                                   | |                                    |   |
| |                                   | |                                    |   |
| +-----------------------------------+ +------------------------------------+   |
+--------------------------------------------------------------------------------+
| [ Batal ]                                            [ Kembali ] [[ Selesai ]] |
+--------------------------------------------------------------------------------+
```

- Prefill field cabang dilakukan sekali, saat langkah 4 pertama dibuka (`07` §2).
- Kontrol model bisnis dan fitur memakai `CheckBox` biasa; Windows Forms tidak punya kontrol saklar. Satu-satunya ketergantungan: `CheckBox` Resep & HPP `Enabled = false` dan `Checked = false` selama F&B tidak dicentang.
- Password memakai `UseSystemPasswordChar = true`.
- **Selesai** menulis `app_config`, `branches`, `users`, lalu `is_onboarded = 1` dalam satu `MySqlTransaction`; gagal berarti rollback dan form tetap di langkah 4.

---

## 4. Shell dan Beranda

### 4.1 MainForm (T-12, sudah dibuat)

`ClientSize` 1280 × 800, `MinimumSize` 1100 × 700. Sidebar 248 px (`panelSidebar`, `Dock = Left`), header 76 px (`panelHeader`), konten (`panelKonten`, `Padding` 28 px, `Dock = Fill`) hanya memuat satu `UserControl`. Menu dibangun dari kode di `SusunMenu()` berdasarkan peran dan feature flag. Gambar menunjukkan Super Admin dengan semua flag aktif.

```text
+- panelSidebar ---------------+ +- panelHeader + panelKonten -------------------------------------+
| [O] OmniPOS                  | | Beranda                        Super Administrator   [ Keluar ] |
|     Kopi Senja               | | Kopi Senja / Pusat (HQ)                             Super Admin |
+------------------------------+ +-----------------------------------------------------------------+
| > Beranda                    | | +- panelKonten (Padding 28) ------------------------------+     |
|                              | | |                                                         |     |
| KASIR                        | | |                  Satu UserControl aktif                 |     |
|   Transaksi Kasir            | | |             Isi halaman: lihat bagian 5 - 12            |     |
|   Shift Kasir *              | | |                                                         |     |
|   Pelanggan                  | | |                                                         |     |
|   Antrean Servis *           | | |                                                         |     |
|                              | | |                                                         |     |
| MASTER DATA                  | | |                                                         |     |
|   Produk & Kategori          | | |                                                         |     |
|   Bahan Baku *               | | |                                                         |     |
|   Resep & HPP *              | | |                                                         |     |
|                              | | |                                                         |     |
| INVENTARIS                   | | |                                                         |     |
|   Stok Masuk                 | | |                                                         |     |
|   Stok Opname                | | |                                                         |     |
|   Transfer Stok *            | | |                                                         |     |
|   Riwayat Mutasi             | | |                                                         |     |
|                              | | |                                                         |     |
| LAPORAN & ANALITIK           | | |                                                         |     |
|   Laporan                    | | +---------------------------------------------------------+     |
|   Dashboard Produk Terlaris  | |                                                                 |
|                              | |                                                                 |
| PENGATURAN                   | |                                                                 |
|   Profil Toko                | |                                                                 |
|   Cabang & Pengguna          | |                                                                 |
+------------------------------+ |                                                                 |
|         OmniPOS v1.0         | |                                                                 |
+------------------------------+ +-----------------------------------------------------------------+
```

| Peran | Menu yang tampil |
| :--- | :--- |
| Super Admin | Semua grup, termasuk PENGATURAN |
| Branch Manager | Semua grup kecuali PENGATURAN |
| Kasir | Beranda + grup KASIR |

Menu bertanda `*` hilang saat flag-nya `0`: Shift (`enable_shift`), Antrean Servis (`enable_service`), Bahan Baku (`enable_fnb`), Resep & HPP (`enable_recipe_bom`), Transfer Stok (`enable_multi_branch`). Menu diperiksa ulang tiap login.

### 4.2 UcBeranda (T-12, sudah dibuat)

```text
+- UcBeranda --------------------------------------------------------------------------------------+
| +- panelKartu ---------------------------------------------------------------------------+       |
| | Selamat datang, Super Administrator                                                    |       |
| | Super Admin - Pusat (HQ)                                                               |       |
| +----------------------------------------------------------------------------------------+       |
| | MODUL BISNIS AKTIF                                                                     |       |
| | [ Retail ] [ F&B ] [ Jasa ]                                                            |       |
| |                                                                                        |       |
| | Pilih menu di panel kiri untuk mulai bekerja.                                          |       |
| | Menu mengikuti peran pengguna dan pengaturan toko.                                     |       |
| +----------------------------------------------------------------------------------------+       |
+--------------------------------------------------------------------------------------------------+
```

Kartu setinggi 320 px dengan chip modul dari `FlowLayoutPanel`; chip berwarna bergilir biru, kuning, hijau (`Tema.cs`). Area di bawah kartu sengaja kosong.

---

## 5. Transaksi Kasir (`UcKasir`, T-21)

Satu halaman: katalog di kiri, nota di kanan. Field, rumus pajak, dan aturan hold/void ada di `07` §4.1. Gambar menunjukkan mode F&B dengan satu tagihan yang siap dibayar tunai.

```text
+- UcKasir ----------------------------------------------------------------------------------------+
| Kasir: Kasir Pusat Satu    Cabang: Pusat (HQ)                            Shift: open sejak 08:00 |
+--------------------------------------------------------------------------------------------------+
| +- Katalog ----------------------------------+ +- Nota ----------------------------------------+ |
| | Cari     [ kode / nama                   ] | | +-------------+-----+---------+----------+    | |
| | Kategori [ Semua kategori               v] | | | Item        | Qty |   Harga | Subtotal |    | |
| |                                            | | +-------------+-----+---------+----------+    | |
| | +---------+-------------+---------+------+ | | | Kopi Susu   |   2 |  25.000 |   50.000 |    | |
| | | Kode    | Nama        |   Harga | Stok | | | | Es Teh      |   1 |   8.000 |    8.000 |    | |
| | +---------+-------------+---------+------+ | | +-------------+-----+---------+----------+    | |
| | | KOP-001 | Kopi Susu   |  25.000 |    - | | |                                               | |
| | | ESH-001 | Es Teh      |   8.000 |    - | | | [ - ] [ + ] [ Hapus item ]                    | |
| | | ROT-001 | Roti Tawar  |  18.000 |   22 | | | Pelanggan   [ Walk-in (tanpa pelanggan)    v] | |
| | | TEH-001 | Teh Botol   |   6.000 |   48 | | |             Poin: -                           | |
| | | OLI-001 | Ganti Oli   |  45.000 |    - | | | Meja/label  [ Meja 5                        ] | |
| | +---------+-------------+---------+------+ | | Diskon (Rp) [ 0            ^v]                | |
| |                                            | | Pajak (%)   [ 10,00        ^v]                | |
| | [ Tambah ke keranjang ]                    | +-----------------------------------------------+ |
| | Klik 2x baris = tambah 1 item.             | | Subtotal                            Rp 58.000 | |
| | '-' = menu F&B atau jasa (tanpa stok).     | | Diskon                                   Rp 0 | |
| |                                            | | Pajak 10%                            Rp 5.800 | |
| |                                            | | TOTAL                               Rp 63.800 | |
| |                                            | +-----------------------------------------------+ |
| |                                            | | Bayar  (o) Tunai  ( ) QRIS  ( ) Transfer      | |
| |                                            | | Uang bayar  [ 100.000      ^v]                | |
| |                                            | | Kembalian                           Rp 36.200 | |
| |                                            | +-----------------------------------------------+ |
| |                                            | | [ Simpan Tagihan ] [[ Bayar ]]                | |
| |                                            | | [ Daftar Nota ] [ Batal Transaksi ]           | |
| +--------------------------------------------+ +-----------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

Perilaku kontrol:

- **Katalog**: `DataGridView` produk aktif di cabang pengguna, difilter oleh kotak Cari (kode atau nama) dan kategori. Klik dua kali atau tombol Tambah memasukkan satu item; item yang sama menaikkan Qty.
- **Keranjang**: baris dipilih lalu `-`, `+`, atau Hapus item. Qty minimal 1. Subtotal tiap baris dan ringkasan di bawahnya dihitung ulang setiap perubahan.
- **Pelanggan**: `ComboBox` dengan `AutoCompleteMode = SuggestAppend` berisi "Walk-in" + pelanggan aktif cabang (nama dan telepon). Default Walk-in. Tidak ada tombol tambah pelanggan di sini (`07` §3).
- **Meja/label**: teks bebas maksimal 100 karakter (`label_meja_pelanggan`).
- **Pajak** prefill dari `tax_percentage`; **Diskon** nominal rupiah, tidak boleh melebihi subtotal.
- **Uang bayar** hanya aktif untuk Tunai dan harus >= total. Untuk QRIS/Transfer kontrol dinonaktifkan; sistem mengisi `uang_bayar = total`, `kembalian = 0`.
- **Bayar** nonaktif saat keranjang kosong. Jika `enable_shift = 1` dan pengguna belum punya shift `open`, Bayar ditolak dengan pesan yang mengarah ke menu Shift Kasir.
- **Simpan Tagihan** membuat nota `hold` dan memotong stok sekali; pelunasan nanti hanya mengganti status (`07` §4.1).
- Transaksi memuat produk jasa membuat satu nomor antrean (`S-001`) yang muncul di §8 setelah bayar atau simpan.
- Semua penulisan (nota, detail, stok, `stock_movements`) diproses `TransactionService` dalam satu transaksi database; halaman hanya memanggil service.

### 5.1 Dialog Daftar Nota (USULAN)

Spec menuntut tagihan hold dapat dipanggil kembali, nota bisa di-void, dan struk bisa dicetak ulang (`06` §5.3, §7.3), tetapi belum menentukan layarnya. Usulan: satu `Form` modal dari tombol **Daftar Nota**.

```text
+- DaftarNotaForm (modal, USULAN) -------------------------------------------------------+
| Status [ hold      v]  Tanggal [ 20/11/2026  v]  [ Muat ]                              |
|                                                                                        |
| +------------------------+-------+-----------+--------------+-----------+--------+     |
| | Nomor nota             | Waktu | Label     | Pelanggan    |     Total | Status |     |
| +------------------------+-------+-----------+--------------+-----------+--------+     |
| | > INV-01-20261120-0007 | 12:41 | Meja 5    | Budi Santoso |    63.800 | hold   |     |
| |   INV-01-20261120-0006 | 12:10 | -         | -            |    25.000 | hold   |     |
| +------------------------+-------+-----------+--------------+-----------+--------+     |
|                                                                                        |
| [[ Buka & Lunasi ]] [ Cetak Ulang ] [ Void ] [ Tutup ]                                 |
+----------------------------------------------------------------------------------------+
```

- **Buka & Lunasi** memuat nota hold ke keranjang untuk pembayaran; stok tidak dipotong lagi.
- **Cetak Ulang** memakai data nota yang sama dan tidak membuat nota baru (`06` §7.3).
- **Void** mengembalikan stok sekali dan mengubah status ke `void`; baris tidak dihapus. Siapa yang boleh void nota yang sudah dibayar belum diputuskan (§13).

---

## 6. Shift Kasir (`UcShift`, T-24)

Menu tampil hanya jika `enable_shift = 1`. Satu halaman dengan empat keadaan; hanya `Panel` yang berganti sesuai status shift pengguna. Aturan buka/tutup dan rumus selisih ada di `07` §4.2.

**Keadaan 1 - belum ada shift aktif**

```text
+- UcShift - keadaan 1 ----------------------------------------------------------------------------+
| +- Buka shift -----------------------------------------------+                                   |
| | Belum ada shift terbuka untuk Kasir Pusat Satu.            |                                   |
| |                                                            |                                   |
| | Cabang          [ Pusat (HQ)                      v]       |                                   |
| | Modal awal (Rp) [ 200.000                        ^v]       |                                   |
| |                                                            |                                   |
| | [[ Buka Shift ]]                                           |                                   |
| +------------------------------------------------------------+                                   |
+--------------------------------------------------------------------------------------------------+
```

Cabang: Super Admin bisa memilih; Branch Manager dan Kasir terkunci ke cabang sendiri (`ComboBox.Enabled = false`). Satu pengguna hanya boleh punya satu shift `open`.

**Keadaan 2 - shift aktif**

```text
+- UcShift - keadaan 2 ----------------------------------------------------------------------------+
| +- Shift aktif ------------------------------------------------------+                           |
| | Kasir                                             Kasir Pusat Satu |                           |
| | Cabang                                                  Pusat (HQ) |                           |
| | Dibuka                                            20/11/2026 08:00 |                           |
| | Modal awal                                              Rp 200.000 |                           |
| | Status                                                        open |                           |
| +--------------------------------------------------------------------+                           |
| | Saldo sistem disembunyikan sampai shift ditutup (blind close).     |                           |
| |                                                                    |                           |
| | [[ Tutup Shift ]]                                                  |                           |
| +--------------------------------------------------------------------+                           |
+--------------------------------------------------------------------------------------------------+
```

**Keadaan 3 - tutup shift (blind close)**

```text
+- UcShift - keadaan 3 ----------------------------------------------------------------------------+
| +- Tutup shift ------------------------------------------------------+                           |
| | Hitung uang tunai fisik di laci, lalu isi nominalnya.              |                           |
| | Saldo sistem baru tampil setelah shift ditutup.                    |                           |
| |                                                                    |                           |
| | Uang fisik (Rp)  [ 1.250.000                ^v]                    |                           |
| |                                                                    |                           |
| | [[ Tutup & Hitung ]] [ Batal ]                                     |                           |
| +--------------------------------------------------------------------+                           |
+--------------------------------------------------------------------------------------------------+
```

**Keadaan 4 - rekap setelah ditutup**

```text
+- UcShift - keadaan 4 ----------------------------------------------------------------------------+
| +- Rekap shift ------------------------------------------------------+                           |
| | Modal awal                                              Rp 200.000 |                           |
| | Total tunai (shift ini)                               Rp 1.100.000 |                           |
| | Uang sistem (modal + tunai)                           Rp 1.300.000 |                           |
| | Uang fisik                                            Rp 1.250.000 |                           |
| | Selisih (fisik - sistem)                     - Rp 50.000 (defisit) |                           |
| | Total non-tunai (QRIS/transfer)                         Rp 430.000 |                           |
| +--------------------------------------------------------------------+                           |
| | [ Cetak Rekap PDF ] [[ Selesai ]]                                  |                           |
| +--------------------------------------------------------------------+                           |
|                                                                                                  |
| Riwayat shift                                                                                    |
| +-------------+-------------+-----------+------------+------------+-----------+--------+         |
| | Buka        | Tutup       |     Modal |     Sistem |      Fisik |   Selisih | Status |         |
| +-------------+-------------+-----------+------------+------------+-----------+--------+         |
| | 20/11 08:00 | 20/11 16:02 |   200.000 |  1.300.000 |  1.250.000 |   -50.000 | closed |         |
| | 19/11 08:01 | 19/11 16:00 |   200.000 |  1.540.000 |  1.540.000 |         0 | closed |         |
| +-------------+-------------+-----------+------------+------------+-----------+--------+         |
+--------------------------------------------------------------------------------------------------+
```

- Selisih negatif = defisit, positif = surplus, 0 = cocok. Pemisahan non-tunai hanya informasi; tidak masuk uang sistem tunai.
- Riwayat shift: Kasir hanya melihat shift sendiri, Branch Manager shift cabangnya, Super Admin semua. Rekap shift untuk Kasir dibuka dari halaman ini, bukan dari menu Laporan (`05` §3).
- **Cetak Rekap PDF** memakai laporan `rekap_shift` (`06` §9.2).

---

## 7. Pelanggan (`UcPelanggan`, T-15)

Satu halaman daftar + form detail (master-detail). Field dan aturan ada di `07` §3. Kasir boleh mengelola pelanggan (`06` §4); hanya Poin yang dikunci untuk Kasir.

```text
+- UcPelanggan ------------------------------------------------------------------------------------+
| Cari [ nama / telepon               ]  [ ] Tampilkan nonaktif                                    |
|                                                                                                  |
| +- Daftar pelanggan -------------------------------------+ +- Detail pelanggan ----------------+ |
| | +-----------------+--------------+-------+----------+  | | Nama *                            | |
| | | Nama            | Telepon      |  Poin | Status   |  | | [ Budi Santoso                  ] | |
| | +-----------------+--------------+-------+----------+  | | Telepon                           | |
| | | > Budi Santoso  | 081234567001 |   120 | aktif    |  | | [ 081234567001                  ] | |
| | |   Siti Aminah   | 081234567002 |    45 | aktif    |  | | Email                             | |
| | |   Dewi Lestari  | 081234567004 |     0 | nonaktif |  | | [ budi@example.com              ] | |
| | +-----------------+--------------+-------+----------+  | | Poin    [ 120                 ^v] | |
| |                                                        | | [x] Aktif                         | |
| |                                                        | | Cabang                            | |
| |                                                        | | [ Pusat (HQ)                   v] | |
| |                                                        | +-----------------------------------+ |
| |                                                        | | [[ Simpan ]] [ Nonaktifkan ]      | |
| |                                                        | | [ Baru ] [ Hapus ]                | |
| |                                                        | |                                   | |
| +--------------------------------------------------------+ +-----------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

- Kotak Cari menyaring nama atau telepon; pelanggan nonaktif disembunyikan kecuali kotak centang dicentang.
- **Baru** mengosongkan form. **Simpan** menambah (form kosong) atau mengubah (baris terpilih). **Nonaktifkan** menukar `is_active`; pelanggan nonaktif tidak muncul di kasir. **Hapus** meminta konfirmasi dan aman untuk nota lama karena FK `ON DELETE SET NULL`.
- Email divalidasi formatnya hanya kalau diisi. Telepon dan email boleh kosong.
- **Poin** diisi manual oleh Super Admin dan Branch Manager; untuk Kasir `NumericUpDown.Enabled = false`. Poin tidak bertambah otomatis (`07` §3).
- **Cabang**: pilihan untuk Super Admin; untuk Branch Manager dan Kasir terkunci ke cabang sendiri.

---

## 8. Antrean Servis (`UcServis`, T-25)

Menu tampil hanya jika `enable_service = 1`. Daftar pekerjaan di atas, detail pekerjaan terpilih di bawah. Status, nomor antrean, dan aturan pembatalan ada di `07` §4.3.

```text
+- UcServis ---------------------------------------------------------------------------------------+
| Status [ Semua       v]  Tanggal [ 20/11/2026  v]  [ Muat ]                                      |
|                                                                                                  |
| +---------+----------------------+-----------+-------+------------------+------------+           |
| | Antrean | Nota                 | Label     | Masuk | Teknisi          | Status     |           |
| +---------+----------------------+-----------+-------+------------------+------------+           |
| |   S-001 | INV-01-20261120-0009 | B 5521 KL | 09:05 | Kasir Pusat Satu | selesai    |           |
| |   S-002 | INV-01-20261120-0010 | D 7788 AB | 09:40 | -                | antri      |           |
| | > S-003 | INV-01-20261120-0011 | B 1234 XY | 10:20 | Kasir Pusat Satu | dikerjakan |           |
| +---------+----------------------+-----------+-------+------------------+------------+           |
|                                                                                                  |
| +- Pekerjaan terpilih: S-003 --------------------------------------------------------------+     |
| | Nota INV-01-20261120-0011                                               Label: B 1234 XY |     |
| | Status    dikerjakan                                                                     |     |
| | Teknisi   [ Kasir Pusat Satu          v]                                                 |     |
| | Catatan   [ Ganti oli + filter                                       ]                   |     |
| +------------------------------------------------------------------------------------------+     |
| | [- Mulai Dikerjakan -] [[ Selesai ]] [- Diambil -] [ Batalkan Pekerjaan ]                |     |
| | [[ Simpan Teknisi & Catatan ]]                                                           |     |
| +------------------------------------------------------------------------------------------+     |
+--------------------------------------------------------------------------------------------------+
```

Tombol aktif sesuai status pekerjaan:

| Status | Tombol aktif |
| :--- | :--- |
| `antri` | Mulai Dikerjakan, Batalkan Pekerjaan |
| `dikerjakan` | Selesai, Batalkan Pekerjaan |
| `selesai` | Diambil |
| `diambil`, `batal` | Tidak ada (hanya baca) |

- Gambar menunjukkan baris S-003 berstatus `dikerjakan`: Mulai dan Diambil nonaktif.
- Teknisi opsional; pilihannya pengguna aktif di cabang yang sama.
- Membatalkan pekerjaan tidak otomatis mem-void nota; void dilakukan di alur kasir (`07` §4.3).
- Pekerjaan dibuat otomatis dari transaksi kasir; halaman ini tidak punya tombol tambah.

---

## 9. Master Data

Data produk dipisah per cabang (`products.branch_id`). Super Admin memilih cabang di pojok kanan atas tiap halaman; Branch Manager terkunci ke cabangnya.

### 9.1 Produk & Kategori (`UcMasterProduk`, T-13)

Satu menu, satu halaman, dua tab. **USULAN**: Kategori adalah `UcKategori` yang ditanam di `TabPage` kedua `UcMasterProduk`, supaya peta menu tetap satu entri (§13).

**Tab Produk**

```text
+- UcMasterProduk - tab Produk --------------------------------------------------------------------+
| [*Produk*] [ Kategori ]                                            Cabang [ Pusat (HQ)        v] |
+--------------------------------------------------------------------------------------------------+
| Cari [ kode / nama      ]  Kategori [ Semua         v]  Tipe [ Semua   v]  [ ] Nonaktif          |
| +---------+--------------------+--------------+---------+----------+----------+-------+-------+  |
| | Kode    | Nama               | Kategori     | Tipe    |    Harga |      HPP |  Stok | Aktif |  |
| +---------+--------------------+--------------+---------+----------+----------+-------+-------+  |
| | KOP-001 | Kopi Susu          | Minuman Kopi | fnb     |   25.000 |    9.150 |     - | Ya    |  |
| | ROT-001 | Roti Tawar         | Roti         | retail  |   18.000 |   12.000 |    22 | Ya    |  |
| | OLI-001 | Ganti Oli          | Servis       | service |   45.000 |        0 |     - | Ya    |  |
| | TEH-001 | Teh Botol          | Minuman Kopi | retail  |    6.000 |    4.500 |    48 | Tidak |  |
| +---------+--------------------+--------------+---------+----------+----------+-------+-------+  |
+--------------------------------------------------------------------------------------------------+
| Kode *        [ KOP-001                    ]   Tipe            [ fnb                 v]          |
| Nama *        [ Kopi Susu                  ]   Harga jual (Rp) [ 25.000             ^v]          |
| Kategori      [ Minuman Kopi              v]   HPP (Rp)        [ 9.150      ] otomatis           |
| [x] Aktif                                      Stok            - (lewat Inventaris)              |
|                                                                                                  |
| [ Baru ] [[ Simpan ]] [ Nonaktifkan ]                                                            |
+--------------------------------------------------------------------------------------------------+
```

- Kode item harus unik dan produk nonaktif tidak muncul di kasir (`06` §5.2). Tabel `products` belum punya `UNIQUE` pada `kode_item`, jadi keunikan diperiksa di service sebelum simpan (T-13: validasi kode item). Baris nonaktif diberi warna redup lewat `CellFormatting`.
- **Stok hanya baca di halaman ini.** Setiap perubahan stok wajib menulis `stock_movements` (`AGENTS.md` §4), jadi stok diubah lewat Stok Masuk atau Stok Opname di §10. Stok awal produk baru = 0.
- **HPP**: untuk tipe F&B dengan `enable_recipe_bom = 1`, `TextBox` HPP `ReadOnly` karena nilainya dihitung dari resep (§9.3). Untuk retail dan jasa, HPP diisi manual lewat `NumericUpDown`.
- Tipe `service` tidak punya resep dan tidak memotong stok (`06` §5.2); HPP jasa boleh 0.
- **Nonaktifkan** menukar `is_active`; produk lama tetap ada di nota.

**Tab Kategori**

```text
+- UcMasterProduk - tab Kategori ------------------------------------------------------------------+
| [ Produk ] [*Kategori*]                                            Cabang [ Pusat (HQ)        v] |
+--------------------------------------------------------------------------------------------------+
| +- Daftar kategori ----------------------+ +- Detail kategori ---------------------------------+ |
| | +----------------------+-------------+ | | Nama kategori *                                   | |
| | | Nama kategori        | Tipe bisnis | | | [ Minuman Kopi                         ]          | |
| | +----------------------+-------------+ | | Tipe bisnis                                       | |
| | | > Minuman Kopi       | fnb         | | | [ fnb                                 v]          | |
| | |   Roti               | retail      | | +---------------------------------------------------+ |
| | |   Servis Kendaraan   | service     | | | [[ Simpan ]] [ Hapus ]                            | |
| | +----------------------+-------------+ | | [ Baru ]                                          | |
| |                                        | |                                                   | |
| |                                        | |                                                   | |
| +----------------------------------------+ +---------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

- Kategori global (tanpa `branch_id`) dengan tipe bisnis `retail`, `fnb`, atau `service`.
- Tabel `categories` tidak punya `is_active`, jadi tidak ada Nonaktifkan. **Hapus** meminta konfirmasi; produk di kategori itu menjadi tanpa kategori (FK `ON DELETE SET NULL`).

### 9.2 Bahan Baku (`UcBahanBaku`, T-14)

Menu tampil hanya jika `enable_fnb = 1`. Master bahan global (`raw_materials`); stok per cabang di `branch_materials`.

```text
+- UcBahanBaku ------------------------------------------------------------------------------------+
| Cari [ nama bahan           ]  Cabang [ Pusat (HQ)      v]  [ ] Hanya stok menipis               |
|                                                                                                  |
| +----------------------+--------+------------+-----------+-----------+----------+                |
| | Bahan                | Satuan | Harga beli |      Stok |  Stok min | Status   |                |
| +----------------------+--------+------------+-----------+-----------+----------+                |
| | Bubuk kopi           | gram   |        150 |     2.400 |       500 | OK       |                |
| | > Susu cair          | ml     |         35 |       800 |     1.000 | Menipis  |                |
| | Sirup aren           | ml     |         90 |     3.500 |       500 | OK       |                |
| +----------------------+--------+------------+-----------+-----------+----------+                |
+--------------------------------------------------------------------------------------------------+
| Nama bahan *        [ Susu cair              ] Stok minimum    [ 1.000              ^v]          |
| Satuan              [ ml                    v] Stok saat ini   800 ml                            |
| Harga beli/satuan   [ 35                 ^v]   (diubah lewat Inventaris)                         |
|                                                                                                  |
| [ Baru ] [[ Simpan ]] [ Hapus ]                                                                  |
+--------------------------------------------------------------------------------------------------+
```

- Satuan: `ComboBox` berisi gram, ml, pcs, butir (contoh di `schema_pos.sql`).
- Baris dengan stok <= stok minimum diberi status **Menipis** dan warna peringatan lewat `CellFormatting` (pola yang sama dengan W6). Ini satu-satunya peringatan stok menipis karena hanya `raw_materials` punya `stok_minimum` (§13).
- Mengubah **Harga beli** menghitung ulang HPP semua menu yang memakai bahan itu (proposal §2.3).
- Stok bahan hanya baca di sini; perubahan lewat Inventaris.
- **Hapus**: relasi resep memakai `ON DELETE CASCADE`, jadi menghapus bahan diam-diam menghapus baris resep. **USULAN**: tombol Hapus diblokir dengan pesan jika bahan masih dipakai resep.

### 9.3 Resep & HPP (`UcResepBOM`, T-14)

Menu tampil hanya jika `enable_recipe_bom = 1`. Kiri: menu bertipe F&B. Kanan: resep menu terpilih. Rumus HPP: total takaran x harga beli satuan (`06` §5.2).

```text
+- UcResepBOM -------------------------------------------------------------------------------------+
| +- Menu -----------------------------+ +- Resep: Kopi Susu ------------------------------------+ |
| | +-----------+-----------+--------+ | | +------------+--------+---------+--------+---------+  | |
| | | Kode      | Menu      |    HPP | | | | Bahan      | Satuan | Takaran |  Harga |   Biaya |  | |
| | +-----------+-----------+--------+ | | +------------+--------+---------+--------+---------+  | |
| | | > KOP-001 | Kopi Susu |  9.150 | | | | Bubuk kopi | gram   |      18 |    150 |   2.700 |  | |
| | |   LAT-001 | Latte     | 11.400 | | | | Susu cair  | ml     |     120 |     35 |   4.200 |  | |
| | |   ESH-001 | Es Teh    |  1.800 | | | | Sirup aren | ml     |      25 |     90 |   2.250 |  | |
| | +-----------+-----------+--------+ | | +------------+--------+---------+--------+---------+  | |
| |                                    | |                                                       | |
| | Hanya menu bertipe F&B.            | | Bahan [ Bubuk kopi      v]  Takaran [ 18    ^v]       | |
| |                                    | | [ Tambah ] [ Hapus baris ]                            | |
| |                                    | +-------------------------------------------------------+ |
| |                                    | | Harga jual                                  Rp 25.000 | |
| |                                    | | HPP per porsi                                Rp 9.150 | |
| |                                    | |                                                       | |
| |                                    | | [[ Simpan Resep ]]                                    | |
| +------------------------------------+ +-------------------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

- Satu bahan hanya boleh muncul sekali per resep (unik `product_id` + `raw_material_id`); menambah bahan yang sudah ada mengganti takarannya.
- **Simpan Resep** menulis baris `product_recipes` dan nilai HPP ke `products.hpp_manual` lewat `RecipeService`.
- HPP dan harga jual hanya informasi; harga jual diubah di §9.1.

---

## 10. Inventaris (`UcInventaris`, T-22)

Satu `UserControl` dengan `TabControl` berisi empat tab. Empat menu sidebar (Stok Masuk, Stok Opname, Transfer Stok, Riwayat Mutasi) membuka halaman yang sama; shell memilih tab awal lewat method publik (`05` §3). Tab Transfer Stok hanya ada jika `enable_multi_branch = 1`. Super Admin memilih cabang di pojok kanan atas; Branch Manager terkunci ke cabangnya.

Mutasi karena penjualan, hold, dan void ditulis `TransactionService` (T-20); halaman ini menulis restock, opname, dan transfer lewat `InventoryService`. Semua memakai tabel `stock_movements` yang sama dengan `stok_sebelum` dan `stok_sesudah` (`06` §5.4).

Tab strip dan pilihan Cabang sama di semua gambar; hanya tab aktif yang berubah.

### 10.1 Tab Stok Masuk

```text
+- UcInventaris - Stok Masuk ----------------------------------------------------------------------+
| [*Stok Masuk*] [ Stok Opname ] [ Transfer Stok ] [ Riwayat Mutasi ]                              |
| Cabang [ Pusat (HQ)        v]                                                                    |
+--------------------------------------------------------------------------------------------------+
| +- Penerimaan barang ----------------------------------------------------------------------+     |
| | Tipe item       (o) Produk   ( ) Bahan baku                                              |     |
| | Item            [ Roti Tawar                          v]                                 |     |
| | Qty masuk       [ 24       ^v]  satuan bahan tampil di sini                              |     |
| | Harga beli baru [ 0        ^v]  khusus bahan baku, opsional                              |     |
| | No. dokumen     [ SJ-2026-118                ]  opsional                                 |     |
| | Keterangan      [ Kiriman supplier                               ]                       |     |
| |                                                                                          |     |
| | [[ Simpan Stok Masuk ]]                                                                  |     |
| +------------------------------------------------------------------------------------------+     |
|                                                                                                  |
| Penerimaan terakhir (sumber restock)                                                             |
| +-------------+------------------+--------+----------+----------+----------------+               |
| | Waktu       | Item             |    Qty |  Sebelum |  Sesudah | Dokumen        |               |
| +-------------+------------------+--------+----------+----------+----------------+               |
| | 20/11 09:12 | Roti Tawar       |     24 |        0 |       24 | SJ-2026-118    |               |
| +-------------+------------------+--------+----------+----------+----------------+               |
+--------------------------------------------------------------------------------------------------+
```

- Qty harus > 0. Stok item di cabang terpilih bertambah dan satu baris `stock_movements` (`sumber = restock`) ditulis dalam satu transaksi.
- **Harga beli baru** hanya aktif untuk Bahan baku (produk tidak punya kolom harga beli). Kalau diisi dan berbeda, `raw_materials.harga_beli_satuan` diperbarui dan HPP menu terkait dihitung ulang (proposal §2.5).
- No. dokumen bebas diketik (mis. nomor surat jalan); formatnya tidak diatur sistem.

### 10.2 Tab Stok Opname

```text
+- UcInventaris - Stok Opname ---------------------------------------------------------------------+
| [ Stok Masuk ] [*Stok Opname*] [ Transfer Stok ] [ Riwayat Mutasi ]                              |
| Cabang [ Pusat (HQ)        v]                                                                    |
+--------------------------------------------------------------------------------------------------+
| +- Penyesuaian stok -----------------------------------------------------------------------+     |
| | Tipe item       (o) Produk   ( ) Bahan baku                                              |     |
| | Item            [ Roti Tawar                          v]                                 |     |
| | Stok sistem     22                                                                       |     |
| | Stok fisik      [ 20       ^v]                                                           |     |
| | Selisih         -2  (kurang dari sistem)                                                 |     |
| | Keterangan *    [ Rusak 2 pcs                                    ]                       |     |
| |                                                                                          |     |
| | [[ Simpan Penyesuaian ]]                                                                 |     |
| +------------------------------------------------------------------------------------------+     |
|                                                                                                  |
| Penyesuaian terakhir (sumber opname)                                                             |
| +-------------+------------------+---------+---------+---------+--------------------------+      |
| | Waktu       | Item             |  Sistem |   Fisik | Selisih | Keterangan               |      |
| +-------------+------------------+---------+---------+---------+--------------------------+      |
| | 20/11 17:45 | Roti Tawar       |      22 |      20 |      -2 | Rusak 2 pcs              |      |
| +-------------+------------------+---------+---------+---------+--------------------------+      |
+--------------------------------------------------------------------------------------------------+
```

- Selisih dihitung sistem (`fisik - sistem`) dan tidak bisa diketik. Keterangan wajib bila selisih tidak 0 supaya penyusutan tercatat transparan (proposal §2.5).
- Kalau selisih 0, tidak ada perubahan stok dan tidak ada baris mutasi.

### 10.3 Tab Transfer Stok

> **Belum final (T-22):** `products` menyimpan stok per baris `products.branch_id`, jadi produk di cabang tujuan mungkin belum punya baris. Aturannya (buat baris otomatis, atau hanya produk dengan kode yang sama) belum diputuskan. Susunan layar di bawah mengikuti alur proposal §2.5 dan tidak bergantung pada keputusan itu.

```text
+- UcInventaris - Transfer Stok -------------------------------------------------------------------+
| [ Stok Masuk ] [ Stok Opname ] [*Transfer Stok*] [ Riwayat Mutasi ]                              |
| Cabang [ Pusat (HQ)        v]                                                                    |
+--------------------------------------------------------------------------------------------------+
| +- Buat transfer --------------------------------------------------------------------------+     |
| | Dari cabang     [ Pusat (HQ)          v]   Ke cabang [ Cabang Darmo        v]            |     |
| | Tipe item       (o) Produk   ( ) Bahan baku                                              |     |
| | Item            [ Roti Tawar                v]  Qty [ 6    ^v] [ Tambah ]                |     |
| |                                                                                          |     |
| | +----------+----------------------+--------+-----------+                                 |     |
| | | Tipe     | Item                 |    Qty | Stok asal |                                 |     |
| | +----------+----------------------+--------+-----------+                                 |     |
| | | product  | Roti Tawar           |      6 |        20 |                                 |     |
| | +----------+----------------------+--------+-----------+                                 |     |
| |                                                                                          |     |
| | [[ Kirim Transfer ]]                                                                     |     |
| +------------------------------------------------------------------------------------------+     |
|                                                                                                  |
| Daftar transfer                                                                                  |
| +--------------------+--------------+----------------+-------------+-----------+                 |
| | Nomor              | Dari         | Ke             | Tanggal     | Status    |                 |
| +--------------------+--------------+----------------+-------------+-----------+                 |
| | > TRF-20261120-001 | Pusat (HQ)   | Cabang Darmo   | 20/11 10:05 | pending   |                 |
| |   TRF-20261119-001 | Pusat (HQ)   | Cabang Darmo   | 19/11 14:20 | completed |                 |
| +--------------------+--------------+----------------+-------------+-----------+                 |
|                                                                                                  |
| [[ Terima Transfer ]]                                                                            |
+--------------------------------------------------------------------------------------------------+
```

- **Kirim Transfer** membuat `stock_transfers` berstatus `pending` dan mengurangi stok cabang asal (mutasi `transfer_out`). Stok cabang tujuan belum berubah.
- **Terima Transfer** hanya aktif untuk pengguna cabang tujuan pada transfer `pending`; mengubah status ke `completed` dan menambah stok tujuan (mutasi `transfer_in`). Stok tidak pernah dikurangi dua kali (`06` §5.4).
- Cabang asal dan tujuan tidak boleh sama. Qty tidak boleh melebihi stok asal.
- Nomor transfer pada gambar hanya contoh; formatnya belum ditetapkan (§13). Skema punya status `cancelled`, tetapi spec belum menjelaskan pengembalian stok, jadi tombol Batalkan tidak digambar.

### 10.4 Tab Riwayat Mutasi (kartu stok)

```text
+- UcInventaris - Riwayat Mutasi ------------------------------------------------------------------+
| [ Stok Masuk ] [ Stok Opname ] [ Transfer Stok ] [*Riwayat Mutasi*]                              |
| Cabang [ Pusat (HQ)        v]                                                                    |
+--------------------------------------------------------------------------------------------------+
| Tipe [ Semua   v]  Item [ Roti Tawar          v]  Sumber [ Semua     v]                          |
| Dari [ 01/11/2026  v]  Sampai [ 20/11/2026  v]  [[ Tampilkan ]]                                  |
|                                                                                                  |
| +-------------+----------------------+------------+-------+--------+-------+----------+--------+ |
| | Waktu       | Dokumen              | Item       | Masuk | Keluar | Saldo | Sumber   | User   | |
| +-------------+----------------------+------------+-------+--------+-------+----------+--------+ |
| | 20/11 09:12 | SJ-2026-118          | Roti Tawar |    24 |        |    24 | restock  | admin  | |
| | 20/11 12:41 | INV-01-20261120-0004 | Roti Tawar |       |      2 |    22 | sale     | kasir1 | |
| | 20/11 17:45 |                      | Roti Tawar |       |      2 |    20 | opname   | admin  | |
| +-------------+----------------------+------------+-------+--------+-------+----------+--------+ |
|                                                                                                  |
| Kolom Keterangan dan nama petugas lengkap tersedia dengan geser horizontal.                      |
+--------------------------------------------------------------------------------------------------+
```

- Read-only. Filter Item bergantung pada Tipe; pilihan `Semua` menampilkan semua item.
- Sumber mengikuti nilai `stock_movements.sumber`: `sale`, `restock`, `opname`, `transfer_in`, `transfer_out`, `void`.
- Kolom dan data yang sama dipakai laporan Mutasi Stok (§11.1) dengan kontrak `06` §9.2.

---

## 11. Laporan dan Dashboard

### 11.1 Laporan (`UcLaporan`, T-32)

Satu halaman untuk empat jenis laporan; jenis dipilih di `ComboBox`, bukan tab (`05` §3). Kolom grid dan parameter total mengikuti kontrak `06` §9.2, dan total di footer harus sama dengan data di grid (`06` §7.1). Gambar menunjukkan jenis Penjualan.

```text
+- UcLaporan --------------------------------------------------------------------------------------+
| Jenis [ Penjualan   v]  Dari [ 01/11/2026  v]  Sampai [ 20/11/2026  v]                           |
| Cabang [ Semua cabang  v]  Kasir [ Semua       v]  Status [ Semua   v]                           |
| Metode bayar [ Semua     v]   [ Tampilkan ] [[ Cetak PDF ]]                                      |
+--------------------------------------------------------------------------------------------------+
| +----------------------+-------------+------------------+--------------+----------+------------+ |
| | Nomor nota           | Waktu       | Kasir            | Pelanggan    | Bayar    |      Total | |
| +----------------------+-------------+------------------+--------------+----------+------------+ |
| | INV-01-20261120-0004 | 20/11 12:41 | Kasir Pusat Satu | Umum         | cash     |     39.600 | |
| | INV-01-20261120-0005 | 20/11 13:05 | Kasir Pusat Satu | Budi Santoso | qris     |     63.800 | |
| | INV-01-20261120-0006 | 20/11 14:20 | Kasir Pusat Satu | Umum         | cash     |     27.500 | |
| +----------------------+-------------+------------------+--------------+----------+------------+ |
| Kolom lain (cabang, status, subtotal, diskon, pajak): geser horizontal.                          |
+--------------------------------------------------------------------------------------------------+
| Jumlah nota 3 | Subtotal 119.000 | Diskon 0 | Pajak 11.900 | Total 130.900                       |
+--------------------------------------------------------------------------------------------------+
```

Filter yang tampil per jenis laporan. Hanya Penjualan yang filternya disebut proposal (§2.7); filter jenis lain adalah **USULAN**.

| Jenis | Filter yang tampil | Total di footer (`06` §9.2) |
| :--- | :--- | :--- |
| Penjualan | Periode, Cabang, Kasir, Status (Paid/Hold/Void), Metode bayar | `jumlah_nota`, `total_subtotal`, `total_diskon`, `total_pajak`, `total_akhir` |
| Laba kotor | Periode, Cabang | `total_omzet`, `total_hpp`, `total_laba_kotor`, `margin_total_persen` |
| Mutasi stok | Periode, Cabang, Tipe item, Sumber | `total_masuk`, `total_keluar` |
| Rekap shift | Periode, Cabang, Kasir | `total_modal_awal`, `total_uang_sistem`, `total_uang_fisik`, `total_selisih` |

- Branch Manager terkunci ke cabangnya; filter Cabang hanya aktif untuk Super Admin dan hanya bila `enable_multi_branch = 1`.
- **Tampilkan** mengisi grid dan footer. **Cetak PDF** membuat PDF A4 lewat FastReport dari data yang sama, memakai nama file unik, lalu membukanya otomatis.
- **Empty state**: kalau filter tidak menghasilkan data, grid diganti pesan "Tidak ada data untuk filter ini.", **Cetak PDF** nonaktif, dan tidak ada PDF kosong yang dibuat (`06` §5.6).
- Kasir tidak melihat halaman ini; rekap shift Kasir ada di §6.

### 11.2 Dashboard Produk Terlaris (`UcDashboard`, T-33)

Sepuluh produk terlaris menurut jumlah terjual atau omzet, ditampilkan sebagai tabel dan grafik batang (`06` §7.2). Periode dan pilihan urutan di bawah adalah **USULAN**; spec hanya menentukan sepuluh produk, tabel, dan grafik batang.

```text
+- UcDashboard ------------------------------------------------------------------------------------+
| Dari [ 01/11/2026  v]  Sampai [ 20/11/2026  v]  Cabang [ Semua cabang  v]                        |
| Urutkan (o) Jumlah terjual  ( ) Omzet   [ Tampilkan ]                                            |
|                                                                                                  |
| +- Tabel ------------------------------------+ +- Grafik batang (jumlah terjual) --------------+ |
| | +----+--------------+-------+------------+ | | Kopi Susu  |######################## 184      | |
| | |  # | Produk       |   Qty |      Omzet | | | Es Teh     |####################     150      | |
| | +----+--------------+-------+------------+ | | Teh Botol  |##################       140      | |
| | |  1 | Kopi Susu    |   184 |  4.600.000 | | | Air Mineral|################         120      | |
| | |  2 | Es Teh       |   150 |  1.200.000 | | | Mie Instan |##############           110      | |
| | |  3 | Teh Botol    |   140 |    840.000 | | | Roti Tawar |#############            96       | |
| | |  4 | Air Mineral  |   120 |    480.000 | | | Latte      |#########                72       | |
| | |  5 | Mie Instan   |   110 |    385.000 | | | Americano  |#########                66       | |
| | |  6 | Roti Tawar   |    96 |  1.728.000 | | | Ganti Oli  |#####                    40       | |
| | |  7 | Latte        |    72 |  2.016.000 | | | Croissant  |#####                    35       | |
| | |  8 | Americano    |    66 |  1.320.000 | | |                                               | |
| | |  9 | Ganti Oli    |    40 |  1.800.000 | | | Skala: 24 # = 184 terjual                     | |
| | | 10 | Croissant    |    35 |    770.000 | | |                                               | |
| | +----+--------------+-------+------------+ | |                                               | |
| |                                            | |                                               | |
| +--------------------------------------------+ +-----------------------------------------------+ |
+--------------------------------------------------------------------------------------------------+
```

- Pilihan **Omzet** mengurutkan tabel dan grafik berdasarkan omzet; selain itu isi layar sama.
- **USULAN**: hanya transaksi berstatus `paid` yang dihitung; `hold` dan `void` tidak. Spec belum menyebut status mana yang masuk.
- Filter Cabang aktif untuk Super Admin dan bila `enable_multi_branch = 1`; Branch Manager terkunci ke cabangnya.
- Grafik batang: dua pilihan teknis, belum diputuskan (§13): kontrol `Chart` bawaan .NET Framework (`System.Windows.Forms.DataVisualization`, perlu `<Reference>` di `.csproj` yang file shared) atau digambar sendiri dengan GDI+ di `Panel`.

---

## 12. Pengaturan (hanya Super Admin, T-18)

### 12.1 Profil Toko (`UcPengaturanToko`)

Mengubah nilai `app_config` yang sama dengan onboarding (`06` §9.1), kecuali `is_onboarded`. Validasi field sama dengan `07` §2.

```text
+- UcPengaturanToko -------------------------------------------------------------------------------+
| +- Identitas toko -------------------------------------------------------------------------+     |
| | Nama usaha *    [ Kopi Senja                                               ]             |     |
| | Alamat *        [ Jl. Ngagel Jaya Tengah No. 73-77, Surabaya               ]             |     |
| | Telepon *       [ 031-5041500                ]                                           |     |
| +------------------------------------------------------------------------------------------+     |
| +- Fitur dan operasional ------------------------------------------------------------------+     |
| | [x] Retail                                  [x] Resep & HPP                              |     |
| | [x] F&B                                     [x] Wajib buka shift                         |     |
| | [ ] Jasa                                    [x] Multi-cabang                             |     |
| |                                                                                          |     |
| | Pajak default (%)  [ 10,00        ^v]                                                    |     |
| +------------------------------------------------------------------------------------------+     |
|                                                                                                  |
| [[ Simpan Perubahan ]] [ Batalkan ]                                                              |
+--------------------------------------------------------------------------------------------------+
```

- Minimal satu dari Retail, F&B, Jasa harus dicentang. `CheckBox` Resep & HPP `Enabled = false` dan `Checked = false` bila F&B tidak dicentang (aturan yang sama dengan onboarding).
- Mematikan fitur hanya menyembunyikan menu; data tidak dihapus. Perubahan berlaku pada login berikutnya karena menu disusun ulang saat login (US-08).
- Tombol **Batalkan** mengembalikan nilai dari database.

### 12.2 Cabang & Pengguna (`UcPengaturanPengguna`)

Satu menu, dua tab: Cabang dan Pengguna.

**Tab Cabang**

```text
+- UcPengaturanPengguna - tab Cabang --------------------------------------------------------------+
| [*Cabang*] [ Pengguna ]                                                                          |
+--------------------------------------------------------------------------------------------------+
| +------------------+------------------------------+---------------+-------+                      |
| | Cabang           | Alamat                       | Telepon       | Pusat |                      |
| +------------------+------------------------------+---------------+-------+                      |
| | Pusat (HQ)       | Jl. Ngagel Jaya Tengah 73-77 | 031-5041500   | Ya    |                      |
| | > Cabang Darmo   | Jl. Darmo 10, Surabaya       | 031-5550100   | Tidak |                      |
| +------------------+------------------------------+---------------+-------+                      |
|                                                                                                  |
| +- Detail cabang ----------------------------------------------------+                           |
| | Nama cabang *   [ Cabang Darmo               ]                     |                           |
| | Alamat          [ Jl. Darmo 10, Surabaya     ]                     |                           |
| | Telepon         [ 031-5550100                ]                     |                           |
| |                 [ ] Cabang pusat (hanya satu)                      |                           |
| |                                                                    |                           |
| | [ Baru ] [[ Simpan ]]                                              |                           |
| +--------------------------------------------------------------------+                           |
+--------------------------------------------------------------------------------------------------+
```

- Cabang pusat tidak bisa diganti statusnya dari sini, dan tidak ada tombol **Hapus**. Alasannya skema: `branches` tidak punya `is_active` dan semua tabel anak (produk, transaksi, shift, stok) memakai `ON DELETE CASCADE`, sehingga menghapus cabang akan ikut menghapus datanya.
- **USULAN**: tombol Baru/Simpan untuk cabang tambahan nonaktif saat `enable_multi_branch = 0`.

**Tab Pengguna**

```text
+- UcPengaturanPengguna - tab Pengguna ------------------------------------------------------------+
| [ Cabang ] [*Pengguna*]                                                                          |
+--------------------------------------------------------------------------------------------------+
| +------------+------------------------+-----------------+--------------+-------+                 |
| | Username   | Nama lengkap           | Peran           | Cabang       | Aktif |                 |
| +------------+------------------------+-----------------+--------------+-------+                 |
| | admin      | Super Administrator    | super_admin     | Pusat (HQ)   | Ya    |                 |
| | manager1   | Manajer Cabang Pusat   | branch_manager  | Pusat (HQ)   | Ya    |                 |
| | > kasir1   | Kasir Pusat Satu       | cashier         | Pusat (HQ)   | Ya    |                 |
| | nonaktif   | Kasir Nonaktif         | cashier         | Pusat (HQ)   | Tidak |                 |
| +------------+------------------------+-----------------+--------------+-------+                 |
+--------------------------------------------------------------------------------------------------+
| Username *        [ kasir1                 ]   Password              [                    ]      |
| Nama lengkap *    [ Kasir Pusat Satu       ]   Konfirmasi password   [                    ]      |
| Peran *           [ cashier               v]   Kosong saat edit = password                       |
| Cabang *          [ Pusat (HQ)            v]   tidak diubah.                                     |
|                                                [x] Aktif                                         |
|                                                                                                  |
| [ Baru ] [[ Simpan ]] [ Nonaktifkan ]                                                            |
+--------------------------------------------------------------------------------------------------+
```

- Username unik dan hanya bisa diisi saat membuat pengguna; saat edit, `TextBox` Username `ReadOnly`. Password disimpan SHA-256, minimal 6 karakter, `UseSystemPasswordChar = true`.
- Peran: `ComboBox` berisi `super_admin`, `branch_manager`, `cashier`. Cabang wajib untuk Branch Manager dan Kasir.
- Tidak ada tombol **Hapus** pengguna: `transactions.user_id` memakai `ON DELETE CASCADE`, jadi menghapus pengguna ikut menghapus nota miliknya. Pengguna dinonaktifkan; akun nonaktif tidak bisa login (`06` §5.1).
- **USULAN**: sistem menolak menonaktifkan atau menurunkan peran akun yang sedang login, dan menolak kondisi tanpa Super Admin aktif.

---

## 13. Keputusan Terbuka

Hal-hal berikut belum ditetapkan di spec atau schema. Mockup di atas memakai usulan yang tertulis di kolom ketiga supaya layarnya bisa digambar; owner boleh mengubahnya. Setelah diputuskan, catat di `06-SPESIFIKASI.md` atau `07-ALUR-PENGGUNA.md` dan hapus baris yang bersangkutan dari tabel ini.

| No | Halaman | Pertanyaan | Usulan di mockup | Task / Owner |
| :---: | :--- | :--- | :--- | :--- |
| 1 | §9.1 Produk & Kategori | Kategori tab atau halaman terpisah? | `UcKategori` ditanam di `TabPage` kedua `UcMasterProduk`; menu tetap satu entri | T-13 / Rangga |
| 2 | §10.3 Transfer Stok | Aturan stok produk di cabang tujuan yang belum punya baris `products` | Belum digambar; layar tidak bergantung pada aturan ini | T-22 / Moreno |
| 3 | §10.3 Transfer Stok | Format nomor transfer; perilaku status `cancelled` | Nomor `TRF-yyyyMMdd-urut` hanya contoh; tombol Batalkan tidak digambar | T-22 / Moreno |
| 4 | §5.1 Daftar Nota | Siapa boleh void nota yang sudah `paid`? | Hold: semua peran; paid: Super Admin dan Branch Manager | T-21 / Raymond |
| 5 | §5.1 Daftar Nota | Layar pemanggilan hold, void, dan cetak ulang | Satu dialog `DaftarNotaForm` dari tombol Daftar Nota | T-21, T-23 / Raymond |
| 6 | §11.1 Laporan | Filter selain Penjualan | Tabel filter per jenis di §11.1 | T-32 / Valencia |
| 7 | §11.2 Dashboard | Periode, urutan, status transaksi yang dihitung | Dari/Sampai, Jumlah atau Omzet, hanya `paid` | T-33 / Valencia |
| 8 | §11.2 Dashboard | Kontrol grafik batang | Pilih `Chart` bawaan (butuh `<Reference>` di `.csproj`, file shared) atau GDI+ | T-33 / Valencia, koordinasi Moreno |
| 9 | §9.2 Bahan Baku | Hapus bahan yang dipakai resep | Diblokir dengan pesan | T-14 / Rangga |
| 10 | §9.2 Bahan Baku | Peringatan stok menipis untuk produk | Hanya bahan baku, karena hanya `raw_materials` punya `stok_minimum` | T-14 / Rangga |
| 11 | §12.2 Cabang & Pengguna | Penghapusan cabang dan pengguna | Tidak ada tombol Hapus; pengguna dinonaktifkan, cabang tidak dihapus | T-18 / Bagas |
| 12 | §12.2 Cabang & Pengguna | Tambah cabang saat `enable_multi_branch = 0`; guard akun sendiri dan Super Admin terakhir | Tambah cabang nonaktif; guard diterapkan di service | T-18 / Bagas |

---

## 14. Catatan Implementasi Windows Forms

Mengikuti `05-UI-SHELL.md` §4 dan `04-ARSITEKTUR.md`:

- Satu halaman = satu `UserControl` di `src/OmniPos/Controls`; layout di `*.Designer.cs`, logic di `*.cs`. Constructor hanya `InitializeComponent()`; data masuk lewat method publik seperti `AturData(...)` atau `MuatData()`.
- Susun layar dengan `TableLayoutPanel`/`SplitContainer`/`Dock` dan `Anchor` supaya tetap rapi di `MinimumSize` 1100 × 700, bukan posisi piksel tetap. Panel kiri-kanan di mockup (katalog/nota, daftar/detail) cocok memakai `SplitContainer` atau `TableLayoutPanel` dua kolom.
- Daftar memakai `DataGridView` dengan `ReadOnly = true`, `SelectionMode = FullRowSelect`, `AllowUserToAddRows = false`, `AutoSizeColumnsMode = Fill`; kolom angka `Alignment = MiddleRight`. Format uang `N0`.
- Pilihan tetap (peran, status, tipe) memakai `ComboBox` dengan `DropDownStyle = DropDownList`; pelanggan di kasir memakai `DropDown` + `AutoCompleteMode`.
- Angka uang dan qty memakai `NumericUpDown` dengan `DecimalPlaces`, `Minimum`, dan `Maximum` yang masuk akal; nilainya diambil sebagai `decimal`, tidak pernah `double`.
- Tab dan grup memakai `TabControl`/`TabPage` dan `GroupBox`; tombol `Flat` dengan warna `Tema.cs` (primer biru untuk tombol utama).
- Atur `TabIndex` berurutan sesuai alur isian dan set `AcceptButton` pada form modal (Login, Daftar Nota) agar Enter bekerja.
- Dialog konfirmasi (hapus, void, batal) memakai `MessageBox`; dialog yang punya field (Daftar Nota, Onboarding) memakai `Form` modal, bukan `UserControl`.
- Validasi input dilakukan di service; halaman hanya menampilkan pesannya. Halaman tidak menulis SQL dan tidak membuka koneksi.
- Warna, font, dan jarak mengikuti tema `05-UI-SHELL.md` §6 (Segoe UI, primer `#2563EB`). Jangan memakai emoji sebagai ikon.
