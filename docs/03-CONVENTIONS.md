# Konvensi Kerja Proyek UAS POS

Aturan branch, commit, build, ownership, dan penyelesaian task. Aturan teknis ada di `04-ARSITEKTUR.md` dan `05-UI-SHELL.md`.

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
- Pesan commit singkat dan jelas; prefix seperti `feat:` atau `fix:` tidak diwajibkan.

## 2. Cek Mandiri Sebelum Selesai

- Owner menangani task sampai selesai dan mengecek hasilnya: kesesuaian dengan spec, query parameterized, koneksi `using`, transaksi database, dan penanganan error.
- Jika butuh bantuan atau menyentuh file bersama, koordinasikan dengan anggota terkait sebelum mengubahnya.
- Jangan menandai `Done` jika build masih error atau skenario utama belum diuji.

## 3. Build dan Uji

```powershell
$msbuild = "C:\Program Files\Microsoft Visual Studio\18\Community\MSBuild\Current\Bin\MSBuild.exe"
& $msbuild "src\OmniPos\OmniPos.csproj" -t:Restore
& $msbuild "src\OmniPos\OmniPos.csproj"
```

- Jalankan dari root repo (`UAS_POS/`), bukan dari folder `VP/`.
- Restore memakai MSBuild, bukan `dotnet restore`.
- Jalankan aplikasi sebagai `.exe` dengan `App.config`; jangan menguji FastReport dari host PowerShell.
- Uji skenario utama task, bukan hanya "form terbuka".
- Untuk transaksi dan stok, uji juga kasus gagal dan rollback.
- Untuk laporan, uji filter kosong, filter normal, dan total.

## 4. File Ownership

| File / Folder | Owner utama | Perlu koordinasi |
| :--- | :--- | :--- |
| `src/OmniPos/Forms/LoginForm*` | Moreno | Bagas |
| `src/OmniPos/Forms/MainForm*` | Moreno | Bagas |
| `src/OmniPos/Controls/UcBeranda*`, `UcSegeraHadir*` | Moreno | — |
| `src/OmniPos/Tema.cs` | Moreno | Semua owner halaman |
| `src/OmniPos/Forms/OnboardingWizardForm*` | Bagas | Moreno |
| `src/OmniPos/Controls/UcMasterProduk*`, `UcKategori*` | Rangga | — |
| `src/OmniPos/Controls/UcBahanBaku*`, `UcResepBOM*` | Rangga | Moreno (HPP) |
| `src/OmniPos/Controls/UcKasir*` | Raymond | — |
| `src/OmniPos/Controls/UcInventaris*` | Moreno | Raymond |
| `src/OmniPos/Controls/UcShift*` | Raymond | — |
| `src/OmniPos/Controls/UcServis*` | Raymond | — |
| `src/OmniPos/Controls/UcLaporan*` | Valencia | — |
| `src/OmniPos/Controls/UcDashboard*` | Valencia | — |
| `src/OmniPos/Controls/UcPelanggan*`, `Services/PelangganService.cs` | Gregorius Priyagung | Raymond (opsional di kasir) |
| `src/OmniPos/Controls/UcPengaturanToko*`, `UcPengaturanPengguna*` | Bagas | Moreno |
| `src/OmniPos/Services/TransactionService.cs` | Raymond | Bagas, Moreno |
| `src/OmniPos/Services/InventoryService.cs` | Moreno | Raymond |
| `src/OmniPos/Services/RecipeService.cs` | Rangga | Moreno |
| `src/OmniPos/Reports/` | Valencia | Moreno |
| `src/OmniPos/Repositories/KoneksiDB.cs` | Moreno | Bagas |
| `src/OmniPos/Repositories/PengaturanRepository.cs`, `Services/PengaturanService.cs` | Moreno | Bagas |
| `src/OmniPos/Services/AuthService.cs` | Moreno | Bagas |
| `database/schema_pos.sql` | Moreno | Bagas |
| `docs/06-SPESIFIKASI.md` | Moreno | Semua owner modul |
| `docs/04-ARSITEKTUR.md`, `docs/05-UI-SHELL.md` | Moreno | Semua owner modul |
| `docs/02-TASKS.md` | Moreno | Owner task terkait |

File shared yang tidak boleh diubah tanpa koordinasi: `MainForm.cs`, `KoneksiDB.cs`, `.csproj`, `App.config`, `schema_pos.sql`, dan `docs/06-SPESIFIKASI.md`.

## 5. Komunikasi dan Status

- Update `02-TASKS.md` saat task selesai atau catatan blocker/dependency berubah.
- Tulis blocker di kolom catatan, bukan hanya di chat.
- Jika task pendukung tertinggal, pemilik modul terkait membantu bagian minimum agar demo tetap jalan.
- Jika ada perubahan kontrak, catat di `06-SPESIFIKASI.md` dan `ctx/uas.md` sebelum coding.
- Jika menu atau halaman baru, perbarui `05-UI-SHELL.md` pada commit yang sama.
- Jangan mengandalkan ingatan; tulis keputusan di file.

## 6. Definition of Done

Checklist lengkap ada di `../AGENTS.md` bagian 7. Ringkasnya:

- Perilaku sesuai `06-SPESIFIKASI.md`.
- Build MSBuild 0 error.
- Skenario utama sudah diuji owner.
- Tidak ada SQL di UI, koneksi terbuka, atau query hasil konkatenasi.
- `02-TASKS.md` diperbarui; `ctx/uas.md` diperbarui bila ada keputusan teknis.
