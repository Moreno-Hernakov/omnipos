# Konvensi Kerja Proyek UAS POS

## 1. Branch dan Commit

Nama branch bebas; gunakan nama singkat dan jelas sesuai modul atau task. Prefix `feat/`, `fix/`, atau `docs/` tidak diwajibkan.

Contoh:

```text
kasir-keranjang
T-15-pelanggan
user-guide
```
Aturan:

- Jangan commit langsung ke branch utama.
- Satu branch untuk satu task atau satu perbaikan.
- Tarik perubahan terbaru sebelum mulai dan sebelum merge.
- Commit kecil dan jelas; jangan campur refactor dengan fitur.
- Pesan commit harus singkat dan jelas; prefix seperti `feat:` atau `fix:` tidak diwajibkan.

## 2. Cek Mandiri Sebelum Selesai

- Owner menangani task sampai selesai dan mengecek hasilnya: kesesuaian dengan spec, query parameterized, koneksi `using`, transaksi database, dan penanganan error.
- Jika butuh bantuan atau menyentuh file bersama, koordinasikan dengan anggota terkait sebelum mengubahnya.

## 3. Build dan Uji

```powershell
$msbuild = "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"
& $msbuild "src\OmniPos\OmniPos.csproj" -t:Restore
& $msbuild "src\OmniPos\OmniPos.csproj"
```

- Jalankan perintah dari root repo (`UAS_POS/`), bukan dari folder `VP/`.
- Restore memakai MSBuild, bukan `dotnet restore`.
- Jalankan aplikasi sebagai `.exe` dengan `App.config`; jangan menguji FastReport dari host PowerShell.
- Uji skenario utama task, bukan hanya “form terbuka”.
- Untuk transaksi dan stok, uji juga kasus gagal dan rollback.
- Untuk laporan, uji filter kosong, filter normal, dan total.

## 4. Aturan Coding

- C# 7.3; kode harus mudah dibaca mahasiswa Semester 3.
- Tidak memakai async/await, LINQ berantai panjang, DI, MVVM/MVC, generic/interface/abstract class yang tidak diajarkan.
- Nama class/method PascalCase; variabel lokal camelCase.
- Nama kontrol: `buttonSimpan`, `textBoxNama`, `dataGridViewProduk`, `labelTotal`.
- Uang memakai `decimal`; jangan `double` atau `float`.
- Koneksi, command, dan reader dibungkus `using`.
- Query memakai parameter (`@param`); jangan menyambung nilai input ke SQL.
- UI tidak menulis SQL. Service tidak menyentuh kontrol. Repository tidak menampilkan `MessageBox`.
- Error yang bisa ditampilkan ke pengguna ditangkap di UI; detail teknis tidak ditampilkan mentah-mentah.

### 4.1 Alur Referensi (Vertical Slice)

T-10 (login) dipakai sebagai contoh satu fitur utuh. Fitur lain mengikuti urutan lapisan yang sama.

| Lapisan | Tanggung jawab | Contoh pada T-10 |
| :--- | :--- | :--- |
| UI (`LoginForm`) | Membaca input, memanggil service, menampilkan hasil atau pesan error | Event tombol login memanggil `AuthService` |
| Service (`AuthService`) | Validasi input, hash SHA-256, cek user aktif | Mengembalikan hasil login atau pesan gagal |
| Repository | Query parameterized ke database | `SELECT ... FROM users WHERE username = @username` |
| Database | Menyimpan data | Tabel `users` (`password_hash`, `is_active`) |

Aturan yang dicontohkan:

- Alur satu arah: UI → Service → Repository. Jangan melompati lapisan.
- UI tidak menulis SQL; service tidak menyentuh kontrol WinForms; repository tidak menampilkan `MessageBox`.
- Semua nilai input masuk lewat parameter (`@username`), bukan konkatenasi string.
- Koneksi, command, dan reader dibungkus `using`.
- Pesan error untuk pengguna disiapkan di UI; detail teknis tidak ditampilkan mentah.

### 4.2 UI dan Windows Forms Designer

- Form/UserControl memakai pola biasa: logic di `*.cs`, layout di `*.Designer.cs`. File `.resx` hanya dibuat kalau memakai gambar/ikon/ImageList.
- Layout statis dibuat lewat **View Designer**, bukan `new Button()` di constructor. Kode dinamis hanya untuk item berulang; container dan item tetap dibuat di designer.
- Constructor Form hanya memanggil `InitializeComponent()`; akses database/service ditaruh di `Load` dan dilewati saat design-time.
- Project non-SDK: file baru didaftarkan di `.csproj` (`SubType` + `DependentUpon`). **Add > New Item** di Visual Studio menangani ini otomatis.
- Desain di skala 100%. Jika Visual Studio menampilkan peringatan scaling 200%, klik **Restart Visual Studio with 100% scaling** agar layout tidak bertumpuk.

### 4.3 Peta Menu, Halaman, dan Pemiliknya

Shell `MainForm` menampilkan sidebar, header, dan satu halaman (`UserControl`) di `panelKonten`. Peta di bawah adalah kontrak: setiap menu punya halaman, task, dan owner. Menu yang belum punya `UserControl` menampilkan `UcSegeraHadir` sampai pemilik modul menyerahkan halamannya.

| Grup | Menu | Halaman (`UserControl`) | Task | Owner halaman | Role | Feature flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| — | Beranda | `UcBeranda` | T-12 | Moreno | SA, BM, Kasir | — |
| KASIR | Transaksi Kasir | `UcKasir` | T-21 (UI), T-26 (logic) | Gregorius (UI), Raymond (logic) | SA, BM, Kasir | — |
| KASIR | Shift Kasir | `UcShift` | T-24 | Raymond | SA, BM, Kasir | `enable_shift` |
| KASIR | Pelanggan | `UcPelanggan` | T-15 | Gregorius | SA, BM, Kasir | — |
| KASIR | Antrean Servis | `UcServis` | T-17 (UI), T-25 (status) | Gregorius (UI), Raymond (status) | SA, BM, Kasir | `enable_service` |
| MASTER DATA | Produk & Kategori | `UcMasterProduk` | T-13 | Rangga | SA, BM | — |
| MASTER DATA | Bahan Baku | `UcBahanBaku` | T-14 | Rangga | SA, BM | `enable_fnb` |
| MASTER DATA | Resep & HPP | `UcResepBOM` | T-14 | Rangga | SA, BM | `enable_recipe_bom` |
| INVENTARIS | Stok Masuk | `UcInventaris` (tab masuk) | T-22 | Moreno | SA, BM | — |
| INVENTARIS | Stok Opname | `UcInventaris` (tab opname) | T-22 | Moreno | SA, BM | — |
| INVENTARIS | Transfer Stok | `UcInventaris` (tab transfer) | T-22 | Moreno | SA, BM | `enable_multi_branch` |
| INVENTARIS | Riwayat Mutasi | `UcInventaris` (tab mutasi) | T-22 | Moreno | SA, BM | — |
| LAPORAN & ANALITIK | Laporan | `UcLaporan` | T-16 (shell), T-30/T-32 (data) | Gregorius (shell), Valencia (data & PDF) | SA, BM | — |
| LAPORAN & ANALITIK | Dashboard Produk Terlaris | `UcDashboard` | T-33 | Valencia | SA, BM | — |
| PENGATURAN | Profil Toko | `UcPengaturanToko` | T-18 | Bagas | SA | — |
| PENGATURAN | Cabang & Pengguna | `UcPengaturanPengguna` | T-18 | Bagas | SA | — |

Keterangan role: SA = `super_admin`, BM = `branch_manager`, Kasir = `cashier`.

Submenu di dalam halaman (bukan menu sidebar):

- `UcLaporan` memuat empat jenis laporan lewat filter: penjualan, laba kotor, mutasi stok, dan rekap shift.
- `UcInventaris` memuat empat tab: stok masuk, opname, transfer, dan riwayat mutasi. Shell mengirim tab awal lewat method publik, bukan lewat constructor.
- Rekap shift untuk Kasir dibuka dari `UcShift` (shift sendiri), bukan dari menu Laporan.

Aturan shell:

1. Visibilitas menu hanya ditentukan di `MainForm.SusunMenu()` dari role pengguna dan nilai `app_config`. Halaman tidak menyembunyikan menu sendiri.
2. Hak akses tetap diperiksa di service. Menyembunyikan menu bukan pengganti validasi bisnis.
3. Satu `panelKonten` hanya menampung satu halaman. Shell membuang halaman lama sebelum menampilkan yang baru.
4. `MainForm` adalah file milik owner shell. Pemilik modul **tidak mengedit** `MainForm`; serahkan nama class halaman, lalu owner shell menambahkan satu `case` di `BuatHalaman()`.
5. Halaman menerima data lewat method publik setelah `new` (contoh `AturData(...)`), bukan lewat constructor, agar tetap bisa dibuka di View Designer.
6. Menu atau submenu baru wajib memperbarui tabel ini, `SusunMenu()`, dan `workspace/TASKS.md` pada commit yang sama.
7. Label menu ditulis dalam bahasa bisnis dan `UseMnemonic = false`, sehingga karakter `&` tampil apa adanya.

## 5. Aturan Database

- Schema final ada di `database/schema_pos.sql`.
- Perubahan schema hanya oleh pemilik database dan wajib disinkronkan ke `database/schema_pos.sql`; dampak fitur dicatat di `docs/SPECIFICATION.md`.
- Jangan menambah tabel/kolom tanpa fitur yang memakainya.
- Operasi multi-tabel memakai `MySqlTransaction`.
- Setiap perubahan stok wajib menulis `stock_movements` dalam transaksi yang sama.
- Jangan menghapus data master yang masih direferensikan; gunakan `is_active` bila tersedia.

## 6. Aturan Laporan

- Laporan manajemen memakai FastReport; struk thermal memakai `PrintDocument`.
- Template `.frx` adalah artefak sumber; jangan mengandalkan designer.
- Kontrak data laporan mengikuti `docs/SPECIFICATION.md` lampiran 11.2.
- Format uang/tanggal dilakukan di C# sebelum masuk `DataTable`.
- Jangan memakai alias dataset yang bentrok dengan namespace FastReport.
- Uji PDF dengan data seed dan filter kosong.

## 7. File Ownership

| File / Folder | Owner utama | Perlu koordinasi |
| :--- | :--- | :--- |
| `src/OmniPos/Forms/LoginForm*` | Moreno | Bagas |
| `src/OmniPos/Forms/MainForm*` | Moreno | Bagas |
| `src/OmniPos/Controls/UcBeranda*`, `UcSegeraHadir*` | Moreno | — |
| `src/OmniPos/Forms/OnboardingWizardForm*` | Bagas | Moreno |
| `src/OmniPos/Controls/UcMasterProduk*`, `UcKategori*` | Rangga | — |
| `src/OmniPos/Controls/UcBahanBaku*`, `UcResepBOM*` | Rangga | Moreno (HPP) |
| `src/OmniPos/Controls/UcKasir*` | Gregorius Priyagung | Raymond (logic transaksi) |
| `src/OmniPos/Controls/UcInventaris*` | Moreno | Raymond |
| `src/OmniPos/Controls/UcShift*` | Raymond | Gregorius Priyagung (UI) |
| `src/OmniPos/Controls/UcServis*` | Gregorius Priyagung | Raymond (status pekerjaan) |
| `src/OmniPos/Controls/UcLaporan*` | Valencia | Gregorius Priyagung (shell UI) |
| `src/OmniPos/Controls/UcDashboard*` | Valencia | — |
| `src/OmniPos/Controls/UcPelanggan*` | Gregorius Priyagung | Raymond (integrasi checkout) |
| `src/OmniPos/Controls/UcPengaturanToko*`, `UcPengaturanPengguna*` | Bagas | Moreno |
| `src/OmniPos/Services/TransactionService.cs` | Raymond | Bagas, Moreno |
| `src/OmniPos/Services/InventoryService.cs` | Moreno | Raymond |
| `src/OmniPos/Services/RecipeService.cs` | Rangga | Moreno |
| `src/OmniPos/Reports/` | Valencia | Moreno |
| `src/OmniPos/Repositories/KoneksiDB.cs` | Moreno | Bagas |
| `src/OmniPos/Repositories/PengaturanRepository.cs`, `Services/PengaturanService.cs` | Moreno | Bagas |
| `src/OmniPos/Services/AuthService.cs` | Moreno | Bagas |
| `database/schema_pos.sql` | Moreno | Bagas |
| `docs/SPECIFICATION.md` | Moreno | Semua owner modul |

## 8. Komunikasi dan Status

- Update `workspace/TASKS.md` saat task selesai atau catatan blocker/dependency berubah.
- Tulis blocker di kolom catatan, bukan hanya di chat.
- Jika task pendukung tertinggal, pemilik modul terkait membantu bagian minimum agar demo tetap jalan.
- Jika ada perubahan kontrak, catat di `docs/SPECIFICATION.md` dan `ctx/uas.md` sebelum coding.
- Jangan mengandalkan ingatan; tulis keputusan di file.

## 9. Definition of Done

Mengikuti checklist di `UAS_POS/AGENTS.md` bagian 7. Ringkasnya: sesuai spec, build 0 error, skenario utama diuji oleh owner, task board diperbarui, dan konteks diperbarui bila perlu.
