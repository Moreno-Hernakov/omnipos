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

## 5. Aturan Database

- Schema final ada di `database/schema_pos.sql`.
- Perubahan schema wajib disetujui dan disinkronkan ke `docs/SPECIFICATION.md`.
- Jangan menambah tabel/kolom tanpa fitur yang memakainya.
- Operasi multi-tabel memakai `MySqlTransaction`.
- Setiap perubahan stok wajib menulis `stock_movements` dalam transaksi yang sama.
- Jangan menghapus data master yang masih direferensikan; gunakan `is_active` bila tersedia.

## 6. Aturan Laporan

- Laporan manajemen memakai FastReport; struk thermal memakai `PrintDocument`.
- Template `.frx` adalah artefak sumber; jangan mengandalkan designer.
- Nama tabel/kolom `DataTable` mengikuti `docs/SPECIFICATION.md` bagian 5.
- Format uang/tanggal dilakukan di C# sebelum masuk `DataTable`.
- Jangan memakai alias dataset yang bentrok dengan namespace FastReport.
- Uji PDF dengan data seed dan filter kosong.

## 7. File Ownership

| File / Folder | Owner utama | Perlu koordinasi |
| :--- | :--- | :--- |
| `src/OmniPos/Forms/` | Bagas | Ya, untuk `MainForm` |
| `src/OmniPos/Controls/UcMasterProduk*` | Rangga | — |
| `src/OmniPos/Controls/UcKasir*` | Raymond | Agung untuk layout |
| `src/OmniPos/Controls/UcInventaris*` | Moreno | — |
| `src/OmniPos/Controls/UcShift*`, `UcServis*` | Raymond | Agung untuk UI read-only |
| `src/OmniPos/Controls/UcLaporan*` | Valencia | Agung untuk shell UI |
| `src/OmniPos/Controls/UcPelanggan*` | Gregorius Priyagung | Dukungan integrasi Raymond bila perlu |
| `src/OmniPos/Services/TransactionService.cs` | Raymond | Bagas, Moreno |
| `src/OmniPos/Services/InventoryService.cs` | Moreno | Raymond |
| `src/OmniPos/Reports/` | Valencia | Moreno |
| `src/OmniPos/Repositories/KoneksiDB.cs` | Bagas | — |
| `database/schema_pos.sql` | Moreno | Bagas |
| `docs/SPECIFICATION.md` | Moreno | Semua owner modul |

## 8. Komunikasi dan Status

- Update `workspace/TASKS.md` saat task selesai atau catatan blocker/dependency berubah.
- Tulis blocker di kolom catatan, bukan hanya di chat.
- Jika task low-impact tertinggal, pemilik modul terkait membantu bagian minimum agar demo tetap jalan.
- Jika ada perubahan kontrak, catat di `docs/SPECIFICATION.md` dan `ctx/uas.md` sebelum coding.
- Jangan mengandalkan ingatan; tulis keputusan di file.

## 9. Definition of Done

Mengikuti checklist di `UAS_POS/AGENTS.md` bagian 7. Ringkasnya: sesuai spec, build 0 error, skenario utama diuji oleh owner, task board diperbarui, dan konteks diperbarui bila perlu.
