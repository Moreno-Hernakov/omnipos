# AGENTS.md — Omni-Industry Configurable POS Engine

Aturan khusus untuk folder `UAS_POS/`. Aturan global di `AGENTS.md` root workspace tetap berlaku. Untuk scope `UAS_POS/`, aturan di file ini menang jika ada perbedaan.

---

## 1. Urutan Baca Sebelum Bekerja

1. `AGENTS.md` root workspace.
2. `UAS_POS/AGENTS.md` (file ini).
3. `UAS_POS/workspace/README.md`.
4. `UAS_POS/docs/SPECIFICATION.md`.
5. `UAS_POS/workspace/TASKS.md`.
6. `ctx/uas.md` untuk riwayat keputusan sesi sebelumnya.

Jangan mulai menulis kode sebelum membaca spec dan task yang menjadi tanggung jawabmu.

---

## 2. Source of Truth

| Topik | File |
| :--- | :--- |
| Perilaku fitur, alur kerja, kriteria penerimaan | `docs/SPECIFICATION.md` |
| Skema database final | `database/schema_pos.sql` |
| Pembagian tugas, ownership, dan status task | `workspace/TASKS.md` |
| Aturan coding dan workflow | `workspace/CONVENTIONS.md` |
| Riwayat keputusan lintas sesi | `ctx/uas.md` |
| Proposal yang sudah disetujui | `docs/PROPOSAL_POS.md` |

Proposal yang sudah disetujui **tidak boleh diubah** tanpa persetujuan tim dan dosen. Perubahan teknis setelah approval dicatat di `docs/SPECIFICATION.md`, bukan dengan mengedit proposal secara diam-diam.

---

## 3. Stack dan Batasan

- .NET Framework **4.7.2**, C# **7.3**, Windows Forms.
- MySQL via `MySql.Data` **8.4.0**, ADO.NET murni, parameterized query.
- FastReport OpenSource **2026.2.8** + `FastReport.OpenSource.Export.PdfSimple` **2026.2.8** untuk laporan PDF A4.
- `PrintDocument` untuk struk thermal 58/80 mm.
- Restore paket memakai MSBuild, bukan `dotnet restore`.

Dilarang menambah NuGet, library, atau pola arsitektur baru tanpa persetujuan. Tidak memakai async/await, LINQ berantai panjang, dependency injection, MVVM/MVC, generic/interface/abstract class yang tidak diajarkan, atau reflection untuk keperluan produksi.

---

## 4. Aturan Arsitektur

- UI hanya memanggil Service. UI dilarang menulis SQL atau membuka `MySqlConnection`.
- Service memanggil Repository. Service tidak boleh menyentuh kontrol WinForms.
- Repository hanya mengakses database. Repository tidak menampilkan `MessageBox`.
- Semua koneksi dibungkus `using`.
- Semua input query memakai parameter (`@param`), bukan konkatenasi string.
- Uang memakai `decimal`.
- Operasi yang mengubah stok, transaksi, dan `stock_movements` wajib berada dalam satu `MySqlTransaction`.
- Setiap perubahan stok wajib menulis `stock_movements` dengan `stok_sebelum` dan `stok_sesudah`.
- Laporan manajemen memakai FastReport; struk thermal memakai `PrintDocument`. Jangan mencampur keduanya.
- Template `.frx` dibuat dari kode karena FastReport OpenSource tidak punya designer.
- Form/UserControl memakai pola WinForms biasa: logic di `*.cs`, layout di `*.Designer.cs`. Kontrol statis dibuat di designer; kode dinamis hanya untuk item berulang.

Detail perilaku laporan ada di `docs/SPECIFICATION.md` bagian 7 dan lampiran 11.2. Jangan mengarang isi laporan atau format output sendiri.

---

## 5. Aturan Kerja Tim

1. **Satu task satu owner.** Owner bertanggung jawab sampai task masuk status `Done` di `workspace/TASKS.md`.
2. **Owner menangani task sampai selesai.** Cek kesesuaian dengan spec, build, dan skenario utama sebelum menandai `Done`.
3. **Jangan edit file shared tanpa koordinasi.** File shared: `MainForm.cs`, `KoneksiDB.cs`, `.csproj`, `App.config`, `schema_pos.sql`, `docs/SPECIFICATION.md`.
4. **Branch sendiri.** Jangan commit langsung ke branch utama. Nama branch bebas dan deskriptif; lihat `workspace/CONVENTIONS.md`.
5. **Update task board.** Perbarui `workspace/TASKS.md` saat task selesai atau catatan blocker/dependency berubah; hanya gunakan `Todo` dan `Done`. Biarkan status `Todo` saat dikerjakan atau menunggu, serta tulis blocker di kolom catatan.
6. **Update konteks.** Setelah keputusan arsitektur atau bug fix, update `ctx/uas.md`.
7. **Jangan menandai task selesai jika build masih error atau belum diuji.**

### 5.1 Aturan Task Pendukung Non-Kritis

Task pendukung yang tidak berada di jalur kritis tetap punya deliverable nyata. Aturannya:

- Task tidak boleh berada di jalur kritis checkout, stok, auth, atau laporan PDF.
- Jika task gagal, fitur inti harus tetap bisa didemokan.
- Task tidak boleh mengubah `TransactionService`, `InventoryService`, `RecipeService`, `Laporan.cs`, `KoneksiDB`, atau schema.
- Deliverable harus jelas: form, grid, filter, seed data, atau dokumen.
- Owner task pendukung menyelesaikan deliverable sesuai kontrak; owner modul terkait menangani integrasi kritis bila diperlukan.

Pembagian owner task ada di `workspace/TASKS.md`.

---

## 6. Alur Kerja per Task

1. Baca task di `workspace/TASKS.md` dan kontrak di `docs/SPECIFICATION.md`.
2. Cek branch dan tarik perubahan terbaru.
3. Implementasi di branch sendiri.
4. Build dengan MSBuild sampai 0 error.
5. Uji skenario di task.
6. Periksa sendiri hasil implementasi terhadap Definition of Done.
7. Update `workspace/TASKS.md`.
8. Update `ctx/uas.md` jika ada keputusan atau bug fix.
9. Merge setelah build dan uji lulus.

---

## 7. Definition of Done

Sebuah task dianggap selesai jika:

- [ ] Perilaku sesuai kontrak di `docs/SPECIFICATION.md`.
- [ ] Build MSBuild 0 error.
- [ ] Skenario utama task sudah diuji oleh owner; setiap anggota menguji fiturnya sendiri.
- [ ] Tidak ada SQL di UI, tidak ada koneksi terbuka, tidak ada nilai query hasil konkatenasi.
- [ ] Tidak ada `TODO`, placeholder, atau handler kosong yang menyerupai fitur selesai.
- [ ] File yang diubah sesuai scope task; tidak ada perubahan tak terkait.
- [ ] Owner sudah mengecek sendiri hasil implementasi sebelum menandai `Done`.
- [ ] `workspace/TASKS.md` diperbarui.
- [ ] `ctx/uas.md` diperbarui bila ada keputusan teknis baru.

---

## 8. Perintah Build

Sesuaikan path MSBuild dengan instalasi Visual Studio di mesin masing-masing.

```powershell
$msbuild = "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"
& $msbuild "UAS_POS\src\OmniPos\OmniPos.csproj" -t:Restore
& $msbuild "UAS_POS\src\OmniPos\OmniPos.csproj"
```

Jangan memakai `dotnet restore` untuk project .NET Framework lama. Error `RuntimeIdentifier 'win'` bukan bug kode.

---

## 9. Larangan Keras

- Jangan mengubah `docs/PROPOSAL_POS.md` atau `PROPOSAL POS.docx` tanpa persetujuan.
- Perubahan schema hanya oleh pemilik database dan wajib disinkronkan ke `database/schema_pos.sql`; dampak fitur dicatat di `docs/SPECIFICATION.md`.
- Jangan menambahkan tabel/kolom yang tidak dipakai fitur.
- Jangan menaruh logic bisnis di event handler UI.
- Jangan memakai `double` untuk uang.
- Jangan menghapus atau menimpa pekerjaan anggota lain.
- Jangan mengklaim task selesai tanpa build dan uji.
