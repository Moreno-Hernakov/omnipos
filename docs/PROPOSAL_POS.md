# OMNI-INDUSTRY CONFIGURABLE POS ENGINE: SISTEM POINT OF SALES TERPADU MULTI-SEKTOR BERBASIS DESKTOP C# WINDOWS FORMS DAN BASIS DATA MYSQL

**PROPOSAL PROYEK AKHIR**  
**MATA KULIAH PEMROGRAMAN VISUAL (GASAL 2026/2027)**  

**Disusun oleh:**  
1. BAGAS RIZKY PUTRA WARDANA (NRP: 225310690)  
2. FX THIARNIKA EKA ATUR RANGGA (NRP: 225310691)  
3. GREGORIUS PRIYAGUNG (NRP: 225310692)  
4. MORENO HERNAKOV (NRP: 225310693)  
5. RAYMOND SUGIHARTO (NRP: 225310694)  
6. VALENCIA ANGIE KURNIAWAN (NRP: 225310695)  

**Dosen Pengampu:**  
Hansel Santoso, S.Kom., M.Kom.  

**PROGRAM STUDI S1 INFORMATIKA**  
**FAKULTAS TEKNOLOGI INFORMASI DAN INDUSTRI KREATIF**  
**INSTITUT SAINS DAN TEKNOLOGI TERPADU SURABAYA**  
**2026**  

---

# LEMBAR PENGESAHAN PROPOSAL PROYEK AKHIR

Proposal Proyek Akhir ini telah diajukan dan disetujui untuk dilaksanakan sebagai bagian dari evaluasi Ujian Akhir Semester (UAS) mata kuliah Pemrograman Visual Semester Gasal 2026/2027 di Institut Sains dan Teknologi Terpadu Surabaya.

| Parameter | Keterangan |
| :--- | :--- |
| **Judul Proyek** | Omni-Industry Configurable POS Engine |
| **Mata Kuliah** | Pemrograman Visual (Gasal 2026/2027) |
| **Program Studi** | S1 Informatika |
| **Institusi** | Institut Sains dan Teknologi Terpadu Surabaya |
| **Jumlah Anggota** | 6 (Enam) Orang Mahasiswa |

*Surabaya, 14 November 2026*  

**Menyetujui,**  
Dosen Pengampu Pemrograman Visual: **Hansel Santoso, S.Kom., M.Kom.**  

---

# DAFTAR ISI

- **BAB I PENDAHULUAN**
  - 1.1 Latar Belakang
  - 1.2 Rumusan Masalah
  - 1.3 Tujuan Proyek
  - 1.4 Manfaat Proyek
  - 1.5 Batasan Masalah
- **BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM**
  - 2.1 Konsep & Deskripsi Program
  - 2.2 Onboarding Wizard & Manajemen Konfigurasi Toko
  - 2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)
  - 2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir
  - 2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang
  - 2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)
  - 2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan
- **BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK**
  - 3.1 Alur Kerja & Arsitektur 3-Tier
  - 3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell
  - 3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)
  - 3.4 Alur Logika Bisnis Kritis & Transaksi Atomik
- **BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM**
  - 4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim
  - 4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu
  - 4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)
- **BAB V PENUTUP**
  - 5.1 Kesimpulan
  - 5.2 Harapan Capaian

---

# BAB I PENDAHULUAN

## 1.1 Latar Belakang
Efisiensi operasional pada sektor perdagangan dan jasa mikro, kecil, dan menengah (UMKM) sangat ditentukan oleh keandalan sistem pencatatan transaksi kasir. Sebagian besar perangkat lunak *Point of Sales* (POS) yang beredar di pasaran memiliki desain monolitik dan kaku. Aplikasi ritel murni hanya mengelola transaksi barang jadi berbasis kode *barcode*, sedangkan aplikasi kuliner (*Food and Beverage* / F&B) mengunci fungsionalitasnya pada manajemen pesanan meja dan resep dapur tanpa fleksibilitas penyesuaian multi-cabang. Pelaku usaha yang mengoperasikan model bisnis campuran (*hybrid*), seperti minimarket yang memiliki stan kopi cepat saji atau bengkel motor yang menjual suku cadang fisik sekaligus jasa perbaikan, sering kali terpaksa menggunakan dua hingga tiga aplikasi kasir terpisah yang membingungkan kasir dan menyulitkan rekapitulasi pembukuan.

Tantangan teknis utama pada sektor kuliner terletak pada pemotongan persediaan. Penjualan satu porsi minuman kopi tidak memotong persediaan kopi siap saji di etalase, melainkan mengonsumsi sejumlah takaran bahan baku mentah dapur seperti biji kopi sangrai, susu segar, dan sirup perisa. Ketiadaan formulasi *Bill of Materials* (BOM) pada sistem kasir standar menyebabkan stok bahan baku mentah tidak terdata secara akurat, sehingga selisih fisik dapur sering kali baru terdeteksi pada akhir bulan. Selain itu, kalkulasi Harga Pokok Penjualan (HPP) menjadi tidak akurat karena fluktuasi harga beli bahan baku dari pemasok tidak tercermin secara langsung pada margin laba kotor setiap transaksi.

Kerentanan operasional kasir juga kerap terjadi pada proses pergantian jam kerja (*shift*) kasir. Ketiadaan pencatatan modal awal kas kecil (*petty cash*) dan verifikasi penerimaan uang tunai fisik secara independen membuka celah selisih pembukuan dan kecurangan internal. Di sisi lain, ekspansi usaha ke beberapa lokasi cabang membutuhkan sistem basis data terpusat yang mampu memetakan kepemilikan data per cabang dan mengelola alur mutasi transfer stok antar-cabang secara tertib tanpa menimbulkan kompleksitas arsitektur yang berlebihan bagi pengembang perangkat lunak.

Untuk menjawab seluruh kebutuhan tersebut, dikembangkan proyek akhir bertajuk Omni-Industry Configurable POS Engine berbasis desktop C# Windows Forms dan basis data relasional MySQL via pustaka ADO.NET. Sistem ini memanfaatkan arsitektur 3-Tier yang memisahkan komponen antarmuka pengguna, logika bisnis, dan repositori basis data secara tegas. Fungsionalitas aplikasi diatur secara adaptif melalui panduan pengaturan awal (*Onboarding Wizard*) dan saklar fitur (*feature flags*), sehingga sistem kasir dapat bertransformasi menjadi sistem ritel murni, kasir restoran terintegrasi dapur, sistem jasa servis, atau gabungan ketiganya tanpa mengubah satu baris pun kode sumber aplikasi.

## 1.2 Rumusan Masalah
Berdasarkan permasalahan operasional dan kebutuhan arsitektur perangkat lunak yang telah dipaparkan, rumusan masalah dalam penelitian dan pengembangan proyek ini dirumuskan sebagai berikut:
1. Bagaimana merancang arsitektur perangkat lunak 3-Tier pada C# Windows Forms yang memisahkan antarmuka *Single-Shell*, logika bisnis layanan, dan akses repositori ADO.NET secara modular?
2. Bagaimana membangun mekanisme *Onboarding Wizard* berbasis saklar fitur (*feature flags*) di tabel konfigurasi untuk mengaktifkan atau menonaktifkan modul ritel, kuliner F&B, jasa, resep dapur, dan shift kasir secara dinamis?
3. Bagaimana mengimplementasikan mesin resep (*Bill of Materials* / BOM) yang mampu menghitung Harga Pokok Penjualan (HPP) menu secara otomatis serta memotong stok bahan baku mentah dapur secara proporsional?
4. Bagaimana menyusun mekanisme transaksi kasir *dual-mode* yang mendukung transaksi bayar langsung (*cash and carry*) maupun penangguhan tagihan (*Hold Bill*) untuk pesanan meja dan antrean pengerjaan jasa?
5. Bagaimana menjamin integritas data multi-tabel saat terjadi transaksi penjualan dan transfer stok antar-cabang menggunakan transaksi atomik basis data (`MySqlTransaction`)?

## 1.3 Tujuan Proyek
Tujuan yang ingin dicapai melalui perancangan dan implementasi proyek akhir ini meliputi:
1. Membangun aplikasi desktop *Point of Sales* modular menggunakan bahasa pemrograman C# pada kerangka kerja .NET Framework 4.7.2 dan basis data MySQL.
2. Menyediakan wizard konfigurasi bisnis awal yang memungkinkan Super Admin menyesuaikan identitas toko, persentase pajak, serta mode industri usaha tanpa rekayasa ulang basis data.
3. Mengintegrasikan modul bahan baku mentah dan relasi resep produk kuliner sehingga stok dapur berkurang secara otomatis dan margin laba kotor tercatat akurat.
4. Menerapkan sistem rekonsiliasi shift kasir dengan pencatatan modal awal dan pelaporan selisih kas fisik melalui metode *blind close* saat penutupan buku toko.
5. Merancang skema basis data relasional 12 tabel dengan partisi data cabang (`branch_id`) dan memvalidasi keutuhan transaksi melalui eksekusi *parameterized query*.

## 1.4 Manfaat Proyek
Penerapan sistem Omni-Industry Configurable POS Engine memberikan manfaat nyata bagi berbagai pihak terkait:
1. **Bagi Pelaku Usaha UMKM**: Memperoleh perangkat lunak kasir multifungsi yang fleksibel tanpa perlu membayar biaya langganan ganda untuk modul ritel, restoran, dan jasa servis terpisah.
2. **Bagi Petugas Kasir dan Supervisor**: Mempercepat proses pelayanan pembayaran pelanggan, mencegah kekeliruan perhitungan kembalian, serta mengamankan rekonsiliasi kas saat pergantian shift.
3. **Bagi Tim Dapur dan Gudang**: Memastikan ketersediaan stok bahan mentah terpantau secara berkala melalui peringatan stok menipis dan mempermudah pelacakan mutasi transfer barang antar-cabang.
4. **Bagi Pengembangan Akademik**: Menjadi percontohan implementasi rekayasa perangkat lunak desktop semester 3 yang taat pada kaidah pemisahan lapisan (*separation of concerns*), keamanan data *parameterized query*, dan transaksi atomik ACID.

## 1.5 Batasan Masalah
Agar ruang lingkup perancangan sistem terarah dan sesuai dengan standar kurikulum mata kuliah Pemrograman Visual Semester 3, batasan masalah proyek ditetapkan sebagai berikut:
1. Aplikasi dibangun sebagai perangkat lunak desktop Windows menggunakan bahasa C# pada lingkungan Microsoft Visual Studio 2022 dengan target .NET Framework 4.7.2.
2. Basis data menggunakan MySQL server lokal (XAMPP / MariaDB) yang diakses melalui pustaka ADO.NET murni (`MySql.Data`) dengan seluruh perintah SQL memanfaatkan *parameterized query* (`@param`) untuk mencegah celah *SQL Injection*.
3. Arsitektur multi-cabang dikelola melalui basis data relasional tunggal terpusat (*single central database*) dengan partisi kepemilikan rekaman data menggunakan kolom foreign key `branch_id`.
4. Pencetakan nota transaksi dan lembar rekapitulasi shift kasir disimulasikan melalui komponen `PrintDocument` Windows Forms dalam format teks struk termal standar lebar 58 mm dan 80 mm.
5. Sistem autentikasi menerapkan enkripsi searah (*hashing*) SHA-256 untuk seluruh kata sandi pengguna tanpa penyimpanan teks mentah di basis data.

---

# BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM

## 2.1 Konsep & Deskripsi Program
Omni-Industry Configurable POS Engine dirancang sebagai mesin kasir desktop cerdas yang mampu beradaptasi dengan model operasional berbagai sektor bisnis. Kata *omni-industry* merepresentasikan kemampuan adaptasi sistem dalam melayani tiga model operasional utama: ritel barang jadi (minimarket, butik, toko kelontong), operasional kuliner (kafe, kedai kopi, restoran cepat saji), serta penyedia jasa dan servis (bengkel, binatu/laundry, salon kecantikan). Karakteristik ketiga sektor tersebut dipadukan ke dalam satu mesin pemrosesan terintegrasi melalui mekanisme aktivasi saklar fitur.

Kekuatan utama arsitektur ini terletak pada penghapusan redundansi sistem. Ketika pengguna memilih model bisnis ritel murni, antarmuka kasir hanya menampilkan input pemindai barcode, pencarian produk cepat, dan keranjang belanja kasir. Sebaliknya, saat model kuliner F&B diaktifkan, antarmuka menambahkan katalog visual berbasis kategori, opsi penandaan nomor meja pelanggan, dan pengiriman daftar pesanan ke dapur. Jika model jasa diaktifkan, kasir dapat mencatat nama teknisi atau penanggung jawab serta memantau status antrean pekerjaan tanpa memicu pemotongan stok barang fisik.

## 2.2 Onboarding Wizard & Manajemen Konfigurasi Toko
Saat aplikasi pertama kali dijalankan pasca instalasi basis data, sistem mendeteksi nilai parameter `is_onboarded` pada tabel `app_config`. Jika parameter bernilai `0`, proses login Super Admin secara otomatis mengalihkan pengguna ke antarmuka Onboarding Wizard sebelum masuk ke jendela utama aplikasi. Wizard ini memandu pemilik usaha mengonfigurasi profil usaha dan memilih fitur fungsional yang dibutuhkan dalam empat tahapan terstruktur:

| Tahap | Nama Konfigurasi | Parameter Basis Data | Keterangan Operasional |
| :---: | :--- | :--- | :--- |
| **1** | Identitas Usaha | `business_name`, `business_address`, `business_phone` | Mencatat nama toko, alamat operasional, dan nomor telepon kontak yang akan dicetak pada kepala nota struk kasir. |
| **2** | Pemilihan Sektor | `enable_retail`, `enable_fnb`, `enable_service` | Memilih jenis industri yang dijalankan toko untuk memfilter navigasi antarmuka dan jenis produk yang dapat diinput. |
| **3** | Mesin & Operasional | `enable_recipe_bom`, `enable_shift`, `tax_percentage` | Mengaktifkan modul resep dapur, mewajibkan kasir membuka shift petty cash, serta menentukan tarif pajak transaksi (misal: 10,0%). |
| **4** | Cabang & Akun | `branches` (HQ), `users` (Super Admin) | Memverifikasi data cabang utama dan menetapkan kredensial administrator permanen sebelum flag `is_onboarded` diubah menjadi 1. |

Seluruh parameter yang tersimpan di tabel `app_config` bertindak sebagai *feature flags* global. Selama aplikasi berjalan, kelas penyedia layanan membaca konfigurasi ini untuk menentukan apakah tab navigasi resep dapur ditampilkan atau disembunyikan dari antarmuka kasir.

## 2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)
Katalog barang pada sistem dibagi menjadi tiga kelompok entitas yang terhubung: kategori produk (`categories`), master produk dan layanan (`products`), serta master bahan baku mentah dapur (`raw_materials`). Setiap produk memiliki penanda tipe bisnis (*retail*, *fnb*, atau *service*) yang menentukan perilaku pemotongan persediaan saat nota penjualan diterbitkan.

Pada sektor kuliner F&B, produk olahan seperti Kopi Susu Gula Aren tidak memiliki stok fisik langsung di gudang barang jadi. Sebagai gantinya, produk tersebut dikaitkan dengan beberapa bahan baku mentah melalui tabel perantara `product_recipes`. Tabel ini menyimpan relasi banyak-ke-banyak antara produk dan bahan baku mentah lengkap dengan takaran pemakaian per porsi sajian (misalnya: 18,00 gram bubuk kopi, 120,00 ml susu segar cair, dan 25,00 ml sirup gula aren).

Mesin resep menjalankan algoritma kalkulasi Harga Pokok Penjualan (HPP) otomatis secara berkala. Setiap kali harga beli bahan mentah diperbarui pada master `raw_materials`, sistem menjumlahkan hasil kali antara takaran pemakaian resep dengan harga beli satuan terbaru untuk seluruh bahan penyusun menu tersebut. Nilai HPP terhitung kemudian disimpan ke dalam atribut `hpp_manual` pada tabel `products`, sehingga margin laba kotor per item menu dapat dihitung secara real-time tanpa memerlukan rekalkulasi manual oleh supervisor.

## 2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir
Modul transaksi kasir menyediakan antarmuka terpadu yang dirancang ergonomis bagi kecepatan kerja petugas kasir. Sistem mendukung dua mode penyelesaian transaksi penjualan yang dapat dipilih secara fleksibel sesuai situasi antrean toko:
1. **Mode Bayar Langsung (*Paid*)**: Diterapkan pada pola transaksi ritel cepat (*cash and carry*). Kasir memasukkan item belanja melalui pemindai barcode atau klik katalog, memilih metode pembayaran (tunai, transfer bank, atau QRIS), memasukkan nominal uang bayar pelanggan, dan sistem langsung menerbitkan struk nota pembayaran lunas.
2. **Mode Simpan Tagihan (*Hold Bill*)**: Diterapkan pada pesanan makan di tempat (*dine-in*) restoran atau antrean unit pada layanan servis. Kasir mencatat pesanan belanja beserta label pengenal berupa nomor meja atau nomor polisi kendaraan. Transaksi disimpan ke basis data dengan status *Hold*. Saat pelanggan selesai bersantap atau servis rampung, kasir memanggil kembali nota gantung tersebut untuk menerima pembayaran dan mengubah status transaksi menjadi *Paid*.

Untuk menjaga akuntabilitas keuangan tunai, sistem mewajibkan pengelolaan shift kasir. Saat memulai jam kerja, kasir harus membuka shift baru dengan memasukkan modal awal kas kecil (*petty cash*) yang diberikan bendahara. Sepanjang shift berlangsung, seluruh transaksi tunai yang berhasil dicatat oleh kasir akan diakumulasikan ke dalam variabel saldo sistem. Saat jam kerja berakhir, kasir melakukan proses penutupan buku kas (*blind close*). Kasir menghitung uang fisik yang ada di laci kasir dan menginput nominal tersebut ke dalam sistem tanpa melihat saldo rekapitulasi sistem terlebih dahulu.

Sistem kemudian membandingkan uang fisik aktual dengan formula saldo akhir sistem: modal awal ditambah total transaksi tunai. Selisih yang terjadi dicatat secara otomatis ke dalam kolom `selisih` pada tabel `shifts`, baik bernilai 0 (cocok), bernilai positif (*surplus*), maupun bernilai negatif (*shortage* / defisit). Laporan penutupan shift dicetak sebagai bukti serah terima kasir kepada pengelola toko.

## 2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang
Manajemen persediaan membedakan penanganan antara stok barang jadi pada sektor ritel dan stok bahan baku mentah pada sektor kuliner F&B. Seluruh stok bahan baku mentah dipartisi per cabang pada tabel `branch_materials`, sehingga ketersediaan persediaan dapur di cabang utama tidak tercampur dengan ketersediaan di cabang pembantu.

Sistem menyediakan tiga fungsi pengendalian persediaan utama:
1. **Restock (Barang Masuk)**: Mencatat penerimaan kiriman barang dari pemasok. Kuantitas stok produk atau bahan mentah di cabang terkait akan bertambah, disertai pembaruan harga beli satuan jika terjadi perubahan tarif pasokan.
2. **Stock Opname (Penyesuaian Fisik)**: Formulir verifikasi berkala untuk mencocokkan jumlah stok tercatat pada sistem dengan stok fisik nyata di gudang atau rak toko. Selisih kerusakan, penyusutan, atau kehilangan dicatat secara transparan dengan riwayat keterangan penyesuaian.
3. **Transfer Stok Antar-Cabang**: Modul pergerakan persediaan antar-lokasi usaha. Pengiriman stok dari cabang asal ke cabang tujuan dicatat pada tabel `stock_transfers` dan `stock_transfer_details` dengan status alur kerja: *Pending* (barang dalam perjalanan) dan *Completed* (barang telah diterima dan diverifikasi di cabang tujuan). Stok di cabang asal berkurang saat transfer diterbitkan, dan stok cabang tujuan bertambah setelah penerimaan dikonfirmasi.

## 2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)
Pengelolaan hak akses menggunakan pendekatan *Role-Based Access Control* (RBAC) dengan tiga tingkatan hierarki peran pengguna. Seluruh kredensial akun diamankan menggunakan algoritma *hashing* SHA-256.

| Tingkatan Peran | Cakupan Hak Akses | Lingkup Otoritas Cabang |
| :--- | :--- | :--- |
| **Super Admin** | Akses penuh ke seluruh menu sistem: Onboarding Wizard, manajemen master data, konfigurasi cabang, resep BOM, pembagian shift, seluruh transaksi kasir, mutasi stok antar-cabang, dan laporan laba rugi analitik. | Seluruh Cabang (Pusat & Cabang Pembantu) |
| **Branch Manager** | Akses ke manajemen master data produk dan bahan cabang, verifikasi stock opname, persetujuan transfer stok masuk/keluar, evaluasi shift kasir harian cabang, dan laporan penjualan cabang. | Terbatas pada Cabang Tempat Bertugas |
| **Cashier (Kasir)** | Akses operasional kasir: Buka/Tutup shift pribadi, input transaksi penjualan (Bayar Langsung & Hold Bill), pencarian katalog, pembatalan item nota sebelum bayar, dan pencetakan struk nota. | Hanya Shift dan Meja Kasir Terdaftar |

## 2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan
Modul pelaporan dirancang untuk menyajikan data operasional bisnis yang akurat dan transparan bagi pemilik usaha. Fitur pelaporan terbagi menjadi empat jenis laporan analitik terstruktur:
1. **Laporan Penjualan Transaksi**: Menampilkan rekapitulasi riwayat transaksi per periode tanggal dengan opsi filter berdasarkan cabang, kasir yang bertugas, status nota (*Paid*, *Hold*, *Void*), serta metode pembayaran (tunai, transfer, QRIS).
2. **Laporan Laba Kotor (*Gross Profit*)**: Menghitung selisih antara nilai omzet penjualan bersih dengan total Harga Pokok Penjualan (HPP) tercatat pada tabel `transaction_details`, sehingga pemilik usaha mengetahui keuntungan riil operasional.
3. **Laporan Kartu Mutasi Stok**: Melacak rekam jejak keluar-masuk setiap item barang atau bahan mentah yang dipicu oleh transaksi kasir, penerimaan restock, penyesuaian stock opname, maupun transfer antar-cabang.
4. **Dashboard Grafik Menu Terlaris**: Menyajikan peringkat sepuluh item produk terlaris berdasarkan kuantitas terjual dan kontribusi nominal terhadap omzet toko.

---

# BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK

## 3.1 Alur Kerja & Arsitektur 3-Tier
Untuk memastikan kemudahan pemeliharaan kode sumber, pengujian logika bisnis, dan kepatuhan terhadap prinsip rekayasa perangkat lunak, sistem Omni-Industry Configurable POS Engine menerapkan arsitektur 3-Tier yang terbagi menjadi tiga lapisan independen:
1. **Presentation Layer (Lapisan Antarmuka)**: Terdiri atas form dialog modal dan `UserControl` dinamis yang bertugas menampilkan elemen visual, menerima input tombol mouse/keyboard, dan memvalidasi kelengkapan teks form. Lapisan ini bebas dari penulisan query SQL maupun koneksi basis data langsung.
2. **Service / Business Logic Layer (Lapisan Logika Bisnis)**: Berisi kelas-kelas layanan yang memproses aturan bisnis, meliputi validasi ketersediaan stok, kalkulasi HPP resep F&B, rekonsiliasi perhitungan selisih kas fisik shift, dan koordinasi pembungkusan transaksi atomik.
3. **Repository / Data Access Layer (Lapisan Akses Data)**: Mengelola komunikasi langsung ke basis data MySQL via ADO.NET. Lapisan ini mengeksekusi perintah SQL terparameter (*parameterized query*) secara eksklusif menggunakan helper koneksi terpusat.

## 3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell
Aplikasi desktop mengadopsi pola antarmuka *Single-Shell Navigation* pada jendela utama `MainForm`. Pola ini memanfaatkan satu form induk tetap yang memuat panel navigasi bilah samping (*sidebar*) dan panel kontainer konten utama (`panelContent`). Saat pengguna mengklik salah satu menu di bilah samping, aplikasi tidak membuka form jendela pop-up baru yang saling bertumpuk di layar monitor kasir. Sebagai gantinya, kontrol antarmuka `UserControl` yang relevan dimuat secara dinamis ke dalam `panelContent`.

Menu navigasi pada bilah samping bersifat adaptif. Komponen bilah samping membaca konfigurasi saklar fitur dan tingkatan peran pengguna saat proses inisialisasi form. Jika Super Admin menonaktifkan fitur kuliner F&B pada Onboarding Wizard, tombol navigasi Resep Dapur dan Bahan Baku otomatis disembunyikan dari antarmuka seluruh pengguna.

## 3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)
Penyimpanan data sistem menggunakan basis data relasional MySQL bernama `db_uas_pos` yang terdiri atas 12 tabel terstruktur. Struktur rinci setiap tabel dijabarkan pada spesifikasi berikut:

### 1. Tabel app_config (Konfigurasi Sistem & Feature Flags)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengenal konfigurasi |
| `setting_key` | VARCHAR(50) | NOT NULL, UNIQUE | Kata kunci konfigurasi (misal: enable_fnb, is_onboarded) |
| `setting_value` | TEXT | NULL | Nilai konfigurasi yang tersimpan dalam format teks atau angka |

### 2. Tabel branches (Data Cabang & Kantor Pusat)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengenal cabang |
| `nama_cabang` | VARCHAR(100) | NOT NULL | Nama identitas cabang toko |
| `alamat` | TEXT | NULL | Alamat fisik lokasi cabang operasional |
| `no_telp` | VARCHAR(20) | NULL | Nomor telepon kontak cabang |
| `is_pusat` | TINYINT(1) | DEFAULT 0 | Penanda cabang utama/kantor pusat (1=Pusat, 0=Cabang) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu pembuatan data cabang |

### 3. Tabel users (Akun Pengguna & Hak Akses RBAC)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengguna |
| `branch_id` | INT | FK -> branches.id, NULL | Cabang tempat pengguna bertugas (NULL untuk Super Admin) |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | Nama login unik untuk autentikasi sistem |
| `password_hash` | VARCHAR(64) | NOT NULL | Hash kata sandi terenkripsi algoritma SHA-256 |
| `nama_lengkap` | VARCHAR(100) | NOT NULL | Nama lengkap petugas atau pengelola |
| `role` | ENUM | 'super_admin','branch_manager','cashier' | Tingkatan hak akses operasional pengguna |
| `is_active` | TINYINT(1) | DEFAULT 1 | Status keaktifan akun pengguna (1=Aktif, 0=Nonaktif) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu pendaftaran akun pengguna |

### 4. Tabel categories (Kategori Kelompok Item)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama kategori |
| `nama_kategori` | VARCHAR(100) | NOT NULL | Nama kelompok produk (misal: Minuman Kopi, Suku Cadang) |
| `tipe_bisnis` | ENUM | 'retail','fnb','service' | Klasifikasi sektor bisnis pemilik kategori |

### 5. Tabel products (Master Produk, Menu Kuliner, & Layanan Jasa)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama produk |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang pemilik kepemilikan item barang |
| `category_id` | INT | FK -> categories.id, NULL | Kategori pengelompokan produk |
| `kode_item` | VARCHAR(50) | NOT NULL | Kode unik barcode atau penomoran inventaris toko |
| `nama_produk` | VARCHAR(150) | NOT NULL | Nama deskriptif barang jadi, menu, atau layanan jasa |
| `tipe` | ENUM | 'retail','fnb','service' | Karakteristik item yang menentukan metode pemotongan stok |
| `harga_jual` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Tarif harga jual resmi yang ditagihkan kepada konsumen |
| `hpp_manual` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga Pokok Penjualan (HPP) modal per satuan item |
| `stok` | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | Kuantitas stok barang jadi (khusus item retail) |
| `is_active` | TINYINT(1) | DEFAULT 1 | Status penjualan produk (1=Dijual, 0=Diarsipkan) |

### 6. Tabel raw_materials (Master Bahan Baku Mentah Dapur F&B)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama bahan baku mentah |
| `nama_bahan` | VARCHAR(100) | NOT NULL | Nama bahan mentah dapur (misal: Biji Kopi, Susu UHT) |
| `satuan` | VARCHAR(20) | NOT NULL | Satuan ukur takaran standar (gram, ml, butir, pcs) |
| `harga_beli_satuan` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga pembelian modal per satuan unit takaran |
| `stok_minimum` | DECIMAL(10,2) | NOT NULL, DEFAULT 5.00 | Ambang batas peringatan stok bahan mentah menipis |

### 7. Tabel branch_materials (Stok Bahan Baku Mentah per Cabang)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama relasi stok cabang |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang lokasi penyimpanan bahan mentah |
| `raw_material_id` | INT | FK -> raw_materials.id | Bahan baku mentah yang disimpan |
| `stok` | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | Jumlah kuantitas stok fisik bahan mentah yang tersedia |

### 8. Tabel product_recipes (Resep & Formulasi Bill of Materials / BOM)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama komponen resep |
| `product_id` | INT | FK -> products.id, NOT NULL | Menu olahan kuliner yang memiliki resep takaran |
| `raw_material_id` | INT | FK -> raw_materials.id | Bahan mentah yang digunakan pada komposisi menu |
| `takaran` | DECIMAL(10,2) | NOT NULL | Besaran volume/berat bahan yang dikonsumsi per porsi menu |

### 9. Tabel shifts (Pencatatan Shift & Rekonsiliasi Kasir)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama sesi shift kasir |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang tempat sesi shift kasir berlangsung |
| `user_id` | INT | FK -> users.id, NOT NULL | Petugas kasir yang bertanggung jawab atas sesi shift |
| `waktu_buka` | DATETIME | NOT NULL | Waktu presisi pembukaan buku laci kasir |
| `waktu_tutup` | DATETIME | NULL | Waktu presisi penutupan buku dan serah terima kasir |
| `modal_awal` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nominal saldo awal kas kecil (petty cash) saat buka shift |
| `uang_sistem` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total akumulasi saldo kasir menurut perhitungan transaksi sistem |
| `uang_fisik` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total nominal uang kertas/logam riil yang dihitung kasir |
| `selisih` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Selisih rekonsiliasi kas (uang_fisik dikurangi uang_sistem) |
| `status` | ENUM | 'open','closed' | Status sesi kerja kasir (open=Berjalan, closed=Selesai) |

### 10. Tabel transactions (Header Nota Penjualan Kasir)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama transaksi penjualan |
| `nomor_nota` | VARCHAR(50) | NOT NULL, UNIQUE | Kode pengenal unik nota struk kasir (misal: TRX-202611-0001) |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang tempat transaksi kasir diterbitkan |
| `user_id` | INT | FK -> users.id, NOT NULL | Petugas kasir yang melayani transaksi penjualan |
| `shift_id` | INT | FK -> shifts.id, NULL | Sesi shift kerja kasir tempat transaksi dibukukan |
| `waktu` | DATETIME | NOT NULL | Waktu penerbitan nota transaksi penjualan |
| `subtotal` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total nilai belanja sebelum potongan diskon dan pajak |
| `diskon` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Besaran potongan promosi atau potongan member |
| `pajak` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nilai pertambahan pajak toko terhitung |
| `total_akhir` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nilai tagihan akhir bersih yang wajib dibayar konsumen |
| `uang_bayar` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Jumlah uang tunai atau nominal transfer yang diterima |
| `kembalian` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Uang kembalian yang diserahkan kembali kepada konsumen |
| `tipe_bayar` | ENUM | 'cash','qris','transfer' | Metode pembayaran transaksi kasir |
| `status` | ENUM | 'paid','hold','void' | Status nota (paid=Lunas, hold=Gantung/Meja, void=Batal) |
| `label_meja_pelanggan` | VARCHAR(100) | NULL | Nomor meja makan (F&B) atau nomor antrean kendaraan (Jasa) |

### 11. Tabel transaction_details (Rincian Item Belanja Transaksi)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama baris detail item transaksi |
| `transaction_id` | INT | FK -> transactions.id | Nota transaksi induk pemilik baris belanja |
| `product_id` | INT | FK -> products.id, NOT NULL | Produk, menu, atau layanan yang dibeli konsumen |
| `qty` | DECIMAL(10,2) | NOT NULL | Banyaknya kuantitas barang yang ditransaksikan |
| `harga_satuan` | DECIMAL(12,2) | NOT NULL | Harga jual satuan produk saat nota dicetak |
| `hpp_satuan` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga Pokok Penjualan (HPP) modal saat nota dicetak |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Total harga baris item (qty dikali harga_satuan) |

### 12. Tabel stock_transfers & stock_transfer_details (Mutasi Stok Cabang)
| Tabel / Kolom | Tipe Data | Atribut | Keterangan Fungsi Alur Mutasi |
| :--- | :--- | :--- | :--- |
| `stock_transfers.id` | INT | PK, AUTO_INCREMENT | Kunci utama berkas transfer antar-cabang |
| `nomor_transfer` | VARCHAR(50) | NOT NULL, UNIQUE | Kode dokumen jalan mutasi stok (TRF-YYYYMM-XXXX) |
| `dari_branch_id` | INT | FK -> branches.id | Cabang asal pengirim persediaan barang/bahan |
| `ke_branch_id` | INT | FK -> branches.id | Cabang tujuan penerima persediaan barang/bahan |
| `user_id` | INT | FK -> users.id | Petugas penanggung jawab pembuatan dokumen mutasi |
| `tanggal` | DATETIME | NOT NULL | Waktu penerbitan dokumen mutasi stok |
| `status` | ENUM | 'pending','completed' | Status perjalanan kiriman (pending=Jalan, completed=Diterima) |
| `detail.transfer_id` | INT | FK -> stock_transfers.id | Kunci pengait dokumen induk transfer |
| `detail.tipe_item` | ENUM | 'product','material' | Jenis item yang dimutasi (barang retail atau bahan mentah) |
| `detail.item_id` | INT | NOT NULL | ID pengenal item produk atau bahan mentah yang dimutasi |
| `detail.qty` | DECIMAL(10,2) | NOT NULL | Volume/kuantitas persediaan yang dipindahkan |

## 3.4 Alur Logika Bisnis Kritis & Transaksi Atomik
Keandalan perangkat lunak kasir bertumpu pada pencegahan inkonsistensi data ketika sistem memproses transaksi multi-item. Penyimpanan transaksi penjualan diimplementasikan menggunakan blok transaksi atomik `MySqlTransaction`. Saat kasir menekan tombol Simpan atau Bayar, sistem menjalankan urutan operasi basis data berikut di dalam satu transaksi utuh:
1. **Penyimpanan Header Transaksi**: Perintah `INSERT` dieksekusi pada tabel `transactions` untuk menyimpan nomor nota unik, total belanja, potongan harga, metode pembayaran, serta identitas kasir yang bertugas.
2. **Penyimpanan Rincian Item**: Seluruh item belanja pada keranjang kasir di-iterasi dan dimasukkan ke tabel `transaction_details` lengkap dengan nilai `harga_satuan` dan nilai `hpp_satuan` riil saat itu.
3. **Pemotongan Stok Kondisional Atomik**: Untuk setiap item belanja, sistem memeriksa tipe item. Jika item bertipe retail, perintah `UPDATE` memotong kolom stok pada tabel `products` di cabang terkait. Jika item bertipe fnb, sistem membaca formulasi resep pada `product_recipes` dan mengeksekusi `UPDATE` untuk memotong persediaan takaran bahan baku mentah pada `branch_materials` secara proporsional. Jika item bertipe service, proses pemotongan stok dilewati.
4. **Commit atau Rollback**: Jika seluruh perintah eksekusi berhasil tanpa ada kendala kekurangan kuantitas stok atau kendala kegagalan jaringan, transaksi diresmikan via perintah `Commit()`. Sebaliknya, jika salah satu item mengalami galat (error), transaksi langsung di-`Rollback()` secara keseluruhan, sehingga tidak ada data nota separuh jadi yang mengotori basis data.

---

# BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM

## 4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim
Untuk memaksimalkan efektivitas pengerjaan proyek akhir dan memastikan seluruh anggota tim memiliki tanggung jawab kode yang terdistribusi secara adil, tanggung jawab pengembangan dibagi menjadi enam modul independen berbasis pembagian arsitektur 3-Tier:

| NRP | Nama Anggota | Peran / Modul Tanggung Jawab | Ruang Lingkup Pengerjaan Modul |
| :---: | :--- | :--- | :--- |
| **225310690** | Bagas Rizky Putra Wardana | Modul 1: Autentikasi & Konfigurasi | Mengembangkan LoginForm, OnboardingWizardForm, AuthService (hashing SHA-256), OnboardingService, dan manajemen cabang usaha (BranchRepository). |
| **225310691** | FX Thiarnika Eka Atur Rangga | Modul 2: Master Data & Resep BOM | Mengembangkan UcMasterProduk, UcResepBOM, RecipeService, manajemen bahan mentah dapur, dan kalkulasi otomatis Harga Pokok Penjualan (HPP). |
| **225310692** | Gregorius Priyagung | Modul 3: Kasir & Transaksi | Mengembangkan UcKasir, katalog pencarian produk, keranjang belanja, mode Bayar Langsung, mode Hold Bill (pesanan meja), dan cetak struk nota. |
| **225310693** | Moreno Hernakov | Modul 4: Inventaris & Stok Cabang | Mengembangkan UcInventaris, InventoryService, modul restock barang masuk, stock opname fisik, dan transfer stok antar-cabang. |
| **225310694** | Raymond Sugiharto | Modul 5: Operasional Kasir & Layanan | Mengembangkan UcShift, ShiftService (buka modal awal petty cash & tutup kasir blind close), manajemen pelanggan/member, dan status pengerjaan antrean jasa. |
| **225310695** | Valencia Angie Kurniawan | Modul 6: Laporan & Analitik | Mengembangkan UcLaporan, ReportService, visualisasi dashboard produk terlaris, laporan laba kotor harian/bulanan, dan kartu riwayat mutasi stok. |

## 4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu
Kolaborasi teknis tim dijalankan dengan menerapkan standar rekayasa perangkat lunak yang ketat:
1. **Standar Antarmuka 3-Tier**: Setiap anggota tim wajib mematuhi pemisahan lapisan. Kode pada UserControl dilarang menulis perintah SQL mentah (seperti `SELECT` atau `INSERT`). Seluruh pemanggilan basis data harus didelegasikan ke kelas Service dan Repository.
2. **Pemeriksaan Kode (*Code Review*)**: Integrasi modul ke dalam solusi proyek utama (`MainForm`) dilakukan bersama oleh seluruh anggota tim guna memverifikasi penamaan variabel, penanganan eksepsi (*try-catch*), dan ketiadaan kebocoran koneksi basis data (seluruh koneksi wajib dibungkus blok `using`).
3. **Pengujian Transaksi Basis Data**: Pengujian fungsi transaksi kasir dan mutasi persediaan wajib diverifikasi menggunakan kasus uji transaksi gagal untuk membuktikan keandalan fitur *Rollback* pada `MySqlTransaction`.

## 4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)
Rencana pengerjaan proyek akhir terbagi ke dalam enam tahapan mingguan terukur hingga pelaksanaan demonstrasi evaluasi UAS:

| Minggu | Tahapan Pengerjaan | Fokus Aktivitas Utama | Target Luaran / Deliverables |
| :---: | :--- | :--- | :--- |
| **Minggu 1** | Analisis & Skema Basis Data | Penyusunan proposal, spesifikasi arsitektur sistem, dan pembuatan skrip DDL SQL 12 tabel. | Dokumen proposal resmi & skrip basis data MySQL. |
| **Minggu 2** | Infrastruktur & Modul 1-2 | Setup project Visual Studio 2022 (.NET 4.7.2), DbHelper ADO.NET, LoginForm, Onboarding Wizard, dan Master Data. | Pondasi arsitektur 3-tier, form autentikasi, dan katalog master data. |
| **Minggu 3** | Modul Resep BOM & Kasir | Implementasi relasi product_recipes, kalkulasi HPP otomatis, form kasir dual-mode, dan cetak nota struk. | Mesin HPP berjalan dan transaksi kasir dapat menyimpan nota. |
| **Minggu 4** | Inventaris & Shift Kasir | Implementasi restock bahan, stock opname fisik, mutasi antar-cabang, dan alur kerja shift kasir blind close. | Pemotongan stok dapur otomatis dan rekonsiliasi kasir. |
| **Minggu 5** | Pelaporan & Dashboard | Pengembangan modul analitik omzet, laporan laba kotor (omzet minus HPP), kartu stok, dan antrean jasa. | Laporan keuangan lengkap dan dashboard visual. |
| **Minggu 6** | Uji Coba & Finalisasi | Pengujian integrasi menyeluruh, pembersihan bug, uji coba transaksi atomik, dan penyusunan laporan akhir UAS. | Aplikasi siap demonstrasi dan naskah laporan lengkap. |

---

# BAB V PENUTUP

## 5.1 Kesimpulan
Omni-Industry Configurable POS Engine dihadirkan sebagai jawaban atas tantangan operasional kasir dan manajemen inventaris pada bisnis multi-sektor yang membutuhkan fleksibilitas tinggi tanpa mengorbankan kesederhanaan arsitektur sistem. Dengan memanfaatkan arsitektur 3-Tier yang kokoh pada platform C# Windows Forms dan basis data MySQL terpusat, sistem mampu memisahkan antarmuka pengguna, logika bisnis, dan akses data secara tertib. Keberadaan Onboarding Wizard berbasis saklar konfigurasi (*feature flags*) memungkinkan aplikasi bertransformasi secara instan memenuhi kebutuhan spesifik sektor ritel, restoran kuliner F&B, dan layanan jasa tanpa memerlukan perubahan struktur kode.

Inovasi formulasi *Bill of Materials* (BOM) pada modul kuliner berhasil menghubungkan menu sajian dengan persediaan bahan baku mentah dapur secara proporsional sekaligus menghitung Harga Pokok Penjualan (HPP) secara otomatis. Ditambah dengan dukungan transaksi atomik `MySqlTransaction` pada alur transaksi kasir *dual-mode* dan transfer stok antar-cabang, serta akuntabilitas rekonsiliasi shift kasir melalui metode *blind close*, perangkat lunak ini dirancang untuk memberikan keandalan data transaksi bisnis yang tinggi.

## 5.2 Harapan Capaian
Melalui penyusunan proposal dan pelaksanaan proyek akhir ini, tim pengembang berharap dapat menghasilkan aplikasi Point of Sales desktop yang fungsional, andal, dan siap dioperasikan dalam lingkungan kerja nyata. Implementasi proyek ini diharapkan dapat menjadi tolak ukur pemahaman praktis mahasiswa dalam menerapkan konsep pemrograman visual berbasis event, arsitektur perangkat lunak 3-Tier, keamanan basis data *parameterized query*, dan kerja sama tim yang terstruktur sesuai dengan standar kompetensi akademik Program Studi S1 Informatika di Institut Sains dan Teknologi Terpadu Surabaya.
