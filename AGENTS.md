# AGENTS.md — Omni-Industry Configurable POS Engine

Aturan khusus untuk folder `UAS_POS/`. Aturan global di `AGENTS.md` root workspace tetap berlaku. Untuk scope `UAS_POS/`, aturan di file ini menang jika ada perbedaan.

---

## 1. Urutan Baca Sebelum Bekerja

1. `AGENTS.md` root workspace.
2. `UAS_POS/AGENTS.md` (file ini).
3. `docs/01-README.md` — peta dokumen dan cara pakai.
4. `docs/02-TASKS.md` — task, owner, dependency, status.
5. `docs/06-SPESIFIKASI.md` — kontrak perilaku fitur.
6. `docs/07-ALUR-PENGGUNA.md` — alur layar, isi field onboarding, field pelanggan, user story.
7. `docs/08-MOCKUP-HALAMAN.md` — tata letak ASCII setiap layar sebelum membuat Form/UserControl.
8. `docs/03-CONVENTIONS.md` — branch, commit, build, ownership, Definition of Done.
9. `docs/04-ARSITEKTUR.md` — sebelum menulis kode.
10. `docs/05-UI-SHELL.md` — sebelum membuat halaman atau menu.
11. `ctx/uas.md` — riwayat keputusan sesi sebelumnya.

Jangan mulai menulis kode sebelum membaca spec dan task yang menjadi tanggung jawabmu.

---

## 2. Source of Truth

| Topik | File |
| :--- | :--- |
| Peta dokumen dan cara pakai | `docs/01-README.md` |
| Perilaku fitur, aturan bisnis, kriteria penerimaan | `docs/06-SPESIFIKASI.md` |
| Alur layar, isi field form/onboarding, user story | `docs/07-ALUR-PENGGUNA.md` |
| Tata letak layar (mockup ASCII), keputusan desain terbuka | `docs/08-MOCKUP-HALAMAN.md` |
| Pembagian tugas, ownership, dan status task | `docs/02-TASKS.md` |
| Branch, commit, build, file ownership, DoD | `docs/03-CONVENTIONS.md` |
| Arsitektur, service/repository, koneksi database | `docs/04-ARSITEKTUR.md` |
| Shell, menu, UserControl, tema | `docs/05-UI-SHELL.md` |
| Skema database final | `database/schema_pos.sql` |
| Riwayat keputusan lintas sesi | `ctx/uas.md` |
| Proposal yang sudah disetujui | `docs/proposal/PROPOSAL_POS.md` |

Proposal yang sudah disetujui **tidak boleh diubah** tanpa persetujuan tim dan dosen. Perubahan teknis setelah approval dicatat di `docs/06-SPESIFIKASI.md`, bukan dengan mengedit proposal secara diam-diam.

---

## 3. Stack dan Batasan

- .NET Framework **4.7.2**, C# **7.3**, Windows Forms.
- MySQL via `MySql.Data` **8.4.0**, ADO.NET murni, parameterized query.
- FastReport OpenSource **2026.2.8** + `Export.PdfSimple` untuk laporan PDF A4; `PrintDocument` untuk struk thermal 58/80 mm.
- Restore paket memakai MSBuild, bukan `dotnet restore`.

Dilarang menambah NuGet, library, atau pola arsitektur baru tanpa persetujuan. Tidak memakai async/await, LINQ berantai panjang, dependency injection, MVVM/MVC, generic/interface/abstract class yang tidak diajarkan, atau reflection untuk produksi. Detail versi dan contoh kode ada di `docs/04-ARSITEKTUR.md`.

---

## 4. Aturan Arsitektur

Alur satu arah: **UI → Service → Repository → Database**.

- UI hanya memanggil Service. UI dilarang menulis SQL atau membuka `MySqlConnection`.
- Service memanggil Repository. Service tidak boleh menyentuh kontrol WinForms.
- Repository hanya mengakses database. Repository tidak menampilkan `MessageBox`.
- Semua koneksi dibungkus `using`; semua input query memakai parameter (`@param`).
- Uang memakai `decimal`.
- Operasi stok, transaksi, dan `stock_movements` wajib satu `MySqlTransaction`.
- Setiap perubahan stok wajib menulis `stock_movements` dengan `stok_sebelum` dan `stok_sesudah`.
- Laporan manajemen memakai FastReport; struk thermal memakai `PrintDocument`. Jangan mencampur keduanya.
- Form/UserControl: logic di `*.cs`, layout di `*.Designer.cs`. Kontrol statis dibuat di Designer; kode dinamis hanya untuk item berulang.

Detail teknis, alur koneksi, error handling, dan checklist fitur ada di `docs/04-ARSITEKTUR.md`. Detail shell dan UserControl ada di `docs/05-UI-SHELL.md`. Jangan mengarang isi laporan atau format output sendiri; kontraknya ada di `docs/06-SPESIFIKASI.md` bagian 7 dan lampiran 9.2.

---

## 5. Aturan Kerja Tim

1. **Satu task satu owner.** Owner bertanggung jawab sampai task masuk status `Done` di `docs/02-TASKS.md`.
2. **Owner menangani task sampai selesai.** Cek kesesuaian dengan spec, build, dan skenario utama sebelum menandai `Done`.
3. **Jangan edit file shared tanpa koordinasi.** File shared: `MainForm.cs`, `KoneksiDB.cs`, `.csproj`, `App.config`, `schema_pos.sql`, `docs/06-SPESIFIKASI.md`.
4. **Branch sendiri.** Jangan commit langsung ke branch utama. Lihat `docs/03-CONVENTIONS.md`.
5. **Update task board.** Perbarui `docs/02-TASKS.md` saat task selesai atau catatan blocker/dependency berubah; hanya gunakan `Todo` dan `Done`.
6. **Update konteks.** Setelah keputusan arsitektur atau bug fix, update `ctx/uas.md`.
7. **Jangan menandai task selesai jika build masih error atau belum diuji.**

### 5.1 Aturan Task Pendukung Non-Kritis

- Task tidak boleh berada di jalur kritis checkout, stok, auth, atau laporan PDF.
- Jika task gagal, fitur inti harus tetap bisa didemokan.
- Task tidak boleh mengubah `TransactionService`, `InventoryService`, `RecipeService`, `Laporan.cs`, `KoneksiDB`, atau schema.
- Deliverable harus jelas: form, grid, filter, seed data, atau dokumen.
- Owner task pendukung menyelesaikan deliverable sesuai kontrak; owner modul terkait menangani integrasi kritis bila diperlukan.

Pembagian owner task ada di `docs/02-TASKS.md`.

---

## 6. Alur Kerja per Task

1. Baca task di `docs/02-TASKS.md` dan kontrak di `docs/06-SPESIFIKASI.md`.
2. Cek branch dan tarik perubahan terbaru.
3. Implementasi di branch sendiri.
4. Build dengan MSBuild sampai 0 error.
5. Uji skenario di task.
6. Periksa sendiri hasil implementasi terhadap Definition of Done.
7. Update `docs/02-TASKS.md`.
8. Update `ctx/uas.md` jika ada keputusan atau bug fix.
9. Merge setelah build dan uji lulus.

---

## 7. Definition of Done

Sebuah task dianggap selesai jika:

- [ ] Perilaku sesuai kontrak di `docs/06-SPESIFIKASI.md`.
- [ ] Build MSBuild 0 error.
- [ ] Skenario utama task sudah diuji oleh owner; setiap anggota menguji fiturnya sendiri.
- [ ] Tidak ada SQL di UI, tidak ada koneksi terbuka, tidak ada nilai query hasil konkatenasi.
- [ ] Tidak ada `TODO`, placeholder, atau handler kosong yang menyerupai fitur selesai.
- [ ] File yang diubah sesuai scope task; tidak ada perubahan tak terkait.
- [ ] Owner sudah mengecek sendiri hasil implementasi sebelum menandai `Done`.
- [ ] `docs/02-TASKS.md` diperbarui.
- [ ] `ctx/uas.md` diperbarui bila ada keputusan teknis baru.

---

## 8. Perintah Build

Sesuaikan path MSBuild dengan instalasi Visual Studio di mesin masing-masing. Jalankan dari root repo `UAS_POS/`.

```powershell
$msbuild = "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"
& $msbuild "src\OmniPos\OmniPos.csproj" -t:Restore
& $msbuild "src\OmniPos\OmniPos.csproj"
```

Jangan memakai `dotnet restore` untuk project .NET Framework lama. Error `RuntimeIdentifier 'win'` bukan bug kode.

---

## 9. Larangan Keras

- Jangan mengubah `docs/proposal/` tanpa persetujuan.
- Perubahan schema hanya oleh pemilik database dan wajib disinkronkan ke `database/schema_pos.sql`; dampak fitur dicatat di `docs/06-SPESIFIKASI.md`.
- Jangan menambahkan tabel/kolom yang tidak dipakai fitur.
- Jangan menaruh logic bisnis di event handler UI.
- Jangan memakai `double` untuk uang.
- Jangan menghapus atau menimpa pekerjaan anggota lain.
- Jangan mengklaim task selesai tanpa build dan uji.
