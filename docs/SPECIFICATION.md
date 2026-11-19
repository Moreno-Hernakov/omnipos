# Spesifikasi & Panduan Sistem: Omni-Industry POS Engine

**Versi 3.0 — panduan tim.**

Dokumen ini menjelaskan cara kerja aplikasi dan aturan bisnis yang perlu diketahui seluruh anggota. Urusan database dan data contoh dikelola terpusat oleh pemilik database; anggota lain tidak perlu menyiapkannya.

---

## 1. Ringkasan

Omni-Industry POS Engine adalah aplikasi kasir desktop untuk Windows. Satu aplikasi yang sama dapat dipakai oleh tiga jenis usaha:

- **Retail**: minimarket, butik, toko kelontong.
- **Food & Beverage (F&B)**: kafe, kedai kopi, restoran.
- **Jasa**: bengkel, salon, laundry, layanan servis.

Jenis usaha dipilih saat pertama kali aplikasi disiapkan. Menu dan fitur menyesuaikan pilihan tersebut, sehingga pengguna tidak melihat fitur yang tidak dipakai.

Tujuan aplikasi:

- Mempercepat transaksi kasir.
- Menjaga stok tetap akurat.
- Mencatat shift dan uang kas.
- Menyediakan laporan penjualan, laba, dan stok.

---

## 2. Tiga Model Bisnis

| Model | Contoh usaha | Cara stok bekerja |
| :--- | :--- | :--- |
| Retail | Minimarket, butik | Stok barang jadi berkurang setiap penjualan. |
| F&B | Kafe, restoran | Stok bahan mentah berkurang sesuai resep menu yang terjual. |
| Jasa | Bengkel, salon, laundry | Tidak memotong stok barang; status pekerjaan dilacak. |

Satu usaha boleh menggabungkan beberapa model. Contoh: bengkel yang juga menjual oli dan suku cadang.

---

## 3. Alur Pemakaian

1. **Login pertama.** Super Admin masuk dengan akun awal.
2. **Onboarding.** Super Admin mengisi nama toko, alamat, telepon, jenis usaha, pajak, dan cabang pertama.
3. **Siapkan data.** Tambahkan pengguna, cabang, kategori, produk/layanan, bahan baku, dan resep.
4. **Buka shift.** Kasir memasukkan modal awal sebelum mulai melayani.
5. **Transaksi.** Kasir memilih produk, mengisi keranjang, memberi diskon/pajak, lalu memilih bayar langsung atau simpan tagihan.
6. **Stok berubah.** Stok berkurang otomatis. Barang masuk, opname, dan transfer dicatat lewat menu inventaris.
7. **Tutup shift.** Kasir menghitung uang fisik; sistem menampilkan selisih terhadap uang seharusnya.
8. **Laporan.** Pemilik atau manajer mencetak laporan PDF atau melihat dashboard.

---

## 4. Peran Pengguna

| Aksi | Super Admin | Branch Manager | Kasir |
| :--- | :---: | :---: | :---: |
| Onboarding, cabang, pengguna | Ya | Tidak | Tidak |
| Master produk, bahan, resep | Ya | Cabang sendiri | Tidak |
| Kasir dan transaksi | Ya | Cabang sendiri | Ya |
| Stok masuk, opname, transfer | Ya | Cabang sendiri | Tidak |
| Shift kasir | Ya | Cabang sendiri | Shift sendiri |
| Member dan servis | Ya | Cabang sendiri | Ya |
| Laporan penjualan, laba, mutasi | Ya | Cabang sendiri | Tidak |
| Rekap shift | Ya | Cabang sendiri | Shift sendiri |

Menu yang tidak boleh diakses tidak ditampilkan. Pemeriksaan hak akses tetap dilakukan di proses bisnis, bukan hanya di tampilan.

---

## 5. Fitur per Modul

### 5.1 Autentikasi & Konfigurasi

- Login dengan username dan password.
- Akun nonaktif tidak bisa masuk.
- Onboarding pertama kali: identitas toko, jenis usaha, pajak, dan cabang awal.
- Menu utama menyesuaikan peran pengguna dan fitur yang diaktifkan.
- Manajemen cabang dan pengguna.

Aturan:

- Password tidak disimpan sebagai teks biasa.
- Super Admin dapat mengelola semua cabang; Branch Manager hanya cabangnya sendiri.
- Pengaturan toko dipakai di tampilan, struk, dan laporan.

### 5.2 Master Data & Resep

- Kategori produk dan layanan.
- Produk jadi, menu F&B, dan layanan jasa.
- Bahan baku mentah beserta satuan dan harga beli.
- Resep: daftar bahan dan takaran untuk setiap menu.
- Perhitungan HPP otomatis dari resep.

Aturan:

- Kode item harus unik.
- Produk nonaktif tidak muncul di kasir.
- HPP dihitung dari total takaran dikali harga bahan.
- Produk jasa tidak memiliki resep dan tidak memotong stok.

### 5.3 Kasir & Transaksi

- Pencarian dan katalog produk.
- Keranjang belanja: tambah, kurangi, dan hapus item.
- Diskon dan pajak.
- Bayar langsung (*Paid*).
- Simpan tagihan (*Hold Bill*), misalnya untuk pesanan meja.
- Pembatalan nota (*Void*).
- Cetak struk.

Aturan:

- Satu nota memakai satu metode bayar: tunai, QRIS, atau transfer.
- Transaksi, rincian item, dan perubahan stok harus berhasil semua atau batal semua.
- Hold Bill tidak memotong stok dua kali saat dilunasi.
- Penjualan jasa tidak memotong stok barang.

### 5.4 Inventaris & Stok

- Barang masuk (*restock*).
- Penyesuaian stok (*stock opname*).
- Transfer stok antar-cabang.
- Riwayat mutasi atau kartu stok.
- Peringatan stok menipis.

Aturan:

- Setiap perubahan stok mencatat jumlah sebelum dan sesudah.
- Setiap perubahan stok mencatat sumbernya: penjualan, restock, opname, transfer, atau void.
- Stok dipisahkan per cabang.
- Transfer memiliki status perjalanan dan tidak mengurangi stok dua kali.

### 5.5 Operasional Kasir & Layanan

- Buka dan tutup shift.
- Rekap uang tunai dan non-tunai.
- Data pelanggan/member.
- Antrean dan status pekerjaan jasa.

Aturan:

- Satu kasir hanya memiliki satu shift aktif.
- Tutup shift membandingkan uang sistem dengan uang fisik.
- Member bersifat opsional; transaksi tetap bisa dilakukan tanpa member.
- Satu transaksi servis memiliki satu catatan pekerjaan.

### 5.6 Laporan & Analitik

- Laporan penjualan.
- Laporan laba kotor.
- Laporan mutasi stok.
- Rekap shift kasir.
- Dashboard produk terlaris.

Aturan:

- Laporan manajemen berupa PDF ukuran A4.
- Struk kasir dicetak ke printer thermal 58 mm atau 80 mm.
- Filter tanpa data menampilkan pesan, bukan PDF kosong.
- Hak akses laporan mengikuti peran pengguna.

---

## 6. Aturan Bisnis Utama

- **Uang memakai perhitungan desimal.** Pembulatan hanya dilakukan saat ditampilkan.
- **Transaksi bersifat all-or-nothing.** Jika satu bagian gagal, seluruh transaksi dibatalkan.
- **Stok memiliki jejak audit.** Setiap perubahan stok dapat ditelusuri.
- **Data dipisahkan per cabang.** Pengguna hanya melihat data cabang yang menjadi haknya.
- **Satu nota satu metode bayar.** Pembayaran terbelah belum didukung.
- **Jasa tidak memotong stok barang.**
- **Setiap anggota menguji fiturnya sendiri.** Owner fitur transaksi dan stok juga menguji kasus gagal dan rollback.

---

## 7. Laporan & Struk

### 7.1 Laporan PDF

| Laporan | Isi utama | Akses |
| :--- | :--- | :--- |
| Penjualan | Nomor nota, tanggal, cabang, kasir, pelanggan, metode bayar, status, subtotal, diskon, pajak, total | Super Admin, Branch Manager |
| Laba kotor | Produk, kategori, jumlah terjual, omzet, HPP, laba kotor, margin | Super Admin, Branch Manager |
| Mutasi stok | Tanggal, nomor dokumen, item, masuk, keluar, saldo, sumber, petugas | Super Admin, Branch Manager |
| Rekap shift | Cabang, kasir, jam buka/tutup, modal awal, tunai, non-tunai, uang sistem, uang fisik, selisih, status | Super Admin, Branch Manager, Kasir (shift sendiri) |

Ketentuan umum:

- Format PDF A4.
- File otomatis terbuka setelah dibuat.
- Nama file unik agar tidak menimpa laporan sebelumnya.
- Header memuat identitas toko, judul laporan, periode, dan filter.
- Total pada laporan harus sama dengan data yang ditampilkan.

### 7.2 Dashboard Produk Terlaris

Dashboard menampilkan sepuluh produk terlaris berdasarkan jumlah terjual dan omzet. Tampilannya berupa tabel dan grafik batang.

### 7.3 Struk Thermal

- Lebar 58 mm (default) atau 80 mm.
- Berisi identitas toko, nomor nota, waktu, kasir, daftar item, subtotal, diskon, pajak, total, metode bayar, uang bayar, dan kembalian.
- Cetak ulang memakai data nota yang sama; tidak membuat nota baru.

---

## 8. Pembagian Tugas

Roster anggota, modul formal, bagian yang dikerjakan, dan status task ada di `workspace/TASKS.md`. Satu task satu owner.

Setiap anggota bertanggung jawab menguji fiturnya sendiri sebelum menandai task selesai. Tidak ada task regresi terpusat.

---

## 9. Kriteria Selesai

Aplikasi dianggap siap demonstrasi jika:

- Login, onboarding, dan hak akses berjalan.
- Master data dapat ditambah, diubah, dan dinonaktifkan.
- Transaksi dapat disimpan, ditahan, dan dibatalkan.
- Stok berkurang otomatis dan tercatat di riwayat.
- Shift dapat dibuka dan ditutup dengan selisih yang benar.
- Empat laporan PDF dan dashboard tampil sesuai filter.
- Struk thermal tampil rapi.
- Build menghasilkan 0 error.
- Setiap owner sudah menguji fiturnya sendiri.

---

## 10. Ketentuan Teknis untuk Developer

Bagian ini boleh dilewati pembaca non-teknis.

- Aplikasi desktop **Windows Forms**.
- .NET Framework **4.7.2**, C# **7.3**.
- Database **MySQL** diakses lewat ADO.NET.
- Database dan data contoh sudah disiapkan terpusat oleh pemilik database. Anggota lain tidak perlu membuat tabel atau menyiapkan data awal.
- Struktur aplikasi tiga lapis:
  - **Tampilan** menangani form dan kontrol.
  - **Logika bisnis** menangani validasi dan aturan.
  - **Akses data** menangani komunikasi ke database.
- Tampilan tidak mengakses database langsung. Logika bisnis tidak menyentuh kontrol form. Akses data tidak menampilkan pesan ke pengguna.
- Pengambilan data memakai parameter, bukan gabungan teks.
- Koneksi, perintah, dan pembaca data ditutup setelah dipakai.
- Perhitungan uang memakai `decimal`.

Alat dan versi:

| Komponen | Versi |
| :--- | :--- |
| .NET Framework | 4.7.2 |
| C# | 7.3 |
| MySql.Data | 8.4.0 |
| FastReport.OpenSource | 2026.2.8 |
| FastReport.OpenSource.Export.PdfSimple | 2026.2.8 |
| Struk thermal | `PrintDocument` bawaan Windows Forms |

Build memakai MSBuild. Jangan memakai `dotnet restore` untuk project .NET Framework lama.

---

## 11. Lampiran Teknis

Bagian ini khusus pengembang dan boleh dilewati.

### 11.1 Pengaturan Aplikasi

| Pengaturan | Nilai | Efek |
| :--- | :--- | :--- |
| `is_onboarded` | `0` / `1` | Menentukan apakah wizard onboarding wajib tampil |
| `business_name` | teks | Nama toko pada tampilan, struk, dan laporan |
| `business_address` | teks | Alamat toko |
| `business_phone` | teks | Telepon toko |
| `enable_retail` | `0` / `1` | Mengaktifkan fitur retail |
| `enable_fnb` | `0` / `1` | Mengaktifkan fitur F&B |
| `enable_recipe_bom` | `0` / `1` | Mengaktifkan resep dan pemotongan bahan |
| `enable_service` | `0` / `1` | Mengaktifkan layanan dan antrean servis |
| `enable_shift` | `0` / `1` | Mewajibkan buka shift sebelum transaksi |
| `enable_multi_branch` | `0` / `1` | Mengaktifkan transfer stok dan filter cabang |
| `tax_percentage` | angka | Tarif pajak default |

### 11.2 Kontrak Data Laporan

Nama tabel dan kolom data laporan harus konsisten antara pengambilan data, `DataTable`, dan template.

| Laporan | Nama data | Kolom |
| :--- | :--- | :--- |
| Penjualan | `penjualan` | `nomor_nota`, `waktu`, `nama_cabang`, `nama_kasir`, `nama_pelanggan`, `tipe_bayar`, `status`, `subtotal`, `diskon`, `pajak`, `total_akhir` |
| Laba kotor | `laba_kotor` | `nama_produk`, `nama_kategori`, `qty_terjual`, `omzet`, `hpp`, `laba_kotor`, `margin_persen` |
| Mutasi stok | `mutasi_stok` | `waktu`, `nomor_dokumen`, `nama_item`, `tipe_item`, `satuan`, `masuk`, `keluar`, `saldo`, `sumber`, `keterangan`, `nama_user` |
| Rekap shift | `rekap_shift` | `nama_cabang`, `nama_kasir`, `waktu_buka`, `waktu_tutup`, `modal_awal`, `total_tunai`, `total_non_tunai`, `uang_sistem`, `uang_fisik`, `selisih`, `status` |

Parameter total:

- Penjualan: `total_subtotal`, `total_diskon`, `total_pajak`, `total_akhir`, `jumlah_nota`.
- Laba kotor: `total_omzet`, `total_hpp`, `total_laba_kotor`, `margin_total_persen`.
- Mutasi stok: `total_masuk`, `total_keluar`.
- Rekap shift: `total_modal_awal`, `total_uang_sistem`, `total_uang_fisik`, `total_selisih`.

### 11.3 Catatan FastReport

- FastReport OpenSource tidak memiliki desain grafis laporan. Template `.frx` dibuat dari kode.
- Ekspor PDF memakai `PDFSimpleExport`. Hasilnya berupa gambar per halaman, sehingga teks tidak bisa diselect. Ini batasan paket dan sudah diterima.
- Panggil `RegisterData` tanpa alias agar tidak bentrok dengan namespace FastReport.
- Sebelum `Prepare()`, pastikan assembly `Microsoft.CSharp` dan `System.Linq` sudah termuat.
- Struk thermal tidak memakai FastReport; gunakan `PrintDocument`.

---

## 12. Referensi

- Proposal resmi: `docs/PROPOSAL_POS.md`.
- Skema database: `database/schema_pos.sql`.
- Papan task dan pembagian anggota: `workspace/TASKS.md`.
- Aturan kerja: `workspace/CONVENTIONS.md`.
- Riwayat keputusan: `ctx/uas.md`.
