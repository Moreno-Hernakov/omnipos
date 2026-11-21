# Dokumentasi Proyek UAS POS

Satu folder untuk seluruh dokumen kerja proyek. Kode ada di `../src/`, skrip database di `../database/`, dan aturan wajib untuk agent/developer di `../AGENTS.md`.

## Urutan Baca

1. **`01-README.md`** (file ini) — peta dokumen dan cara pakai.
2. **`02-TASKS.md`** — cari task milikmu, owner, dependency, dan status.
3. **`06-SPESIFIKASI.md`** — kontrak perilaku fitur dan aturan bisnis.
4. **`07-ALUR-PENGGUNA.md`** — alur layar, isi field onboarding, field pelanggan, dan user story.
5. **`08-MOCKUP-HALAMAN.md`** — tata letak ASCII setiap layar (Windows Forms) dan keputusan desain yang masih terbuka.
6. **`03-CONVENTIONS.md`** — branch, commit, build, ownership, dan Definition of Done.
7. **`04-ARSITEKTUR.md`** — lapisan aplikasi dan koneksi database. Baca sebelum menyentuh kode.
8. **`05-UI-SHELL.md`** — shell, menu, dan UserControl. Baca sebelum membuat halaman.

Riwayat keputusan lintas sesi ada di `ctx/uas.md` (di luar repo).

## Peta Dokumen

| File | Isi | Kapan dibaca | Yang mengubah |
| :--- | :--- | :--- | :--- |
| `01-README.md` | Peta dokumen dan cara pakai | Pertama kali | Moreno |
| `02-TASKS.md` | Roster, ownership, task per fase, dependency, status | Setiap mengambil/menutup task | Owner task |
| `03-CONVENTIONS.md` | Branch, commit, cek mandiri, build, file ownership, DoD | Sebelum mulai kerja | Moreno |
| `04-ARSITEKTUR.md` | Stack, 3 lapis, service/repository, koneksi, error, transaksi, gaya kode | Sebelum menulis kode | Moreno + owner modul |
| `05-UI-SHELL.md` | Form vs UserControl, peta menu, cara tambah menu/UC, tema | Sebelum membuat UI | Moreno + owner halaman |
| `06-SPESIFIKASI.md` | Perilaku fitur, aturan bisnis, laporan, kriteria selesai | Sebelum menerima task | Moreno + semua owner modul |
| `07-ALUR-PENGGUNA.md` | Alur layar, isi field onboarding per halaman, field pelanggan, user story | Sebelum membuat Form/UserControl | Moreno + owner halaman |
| `08-MOCKUP-HALAMAN.md` | Mockup ASCII per layar, susunan kontrol Windows Forms, keputusan terbuka | Sebelum membuat Form/UserControl | Moreno + owner halaman |
| `proposal/` | Proposal resmi `.md` dan `.docx` | Saat butuh naskah akademik | Tidak boleh diubah tanpa persetujuan |

## Cara Pakai

1. Baca `../AGENTS.md` dan `06-SPESIFIKASI.md` sebelum menerima task.
2. Cek `02-TASKS.md` untuk task yang menjadi tanggung jawabmu.
3. Baca `04-ARSITEKTUR.md`; kalau task membuat halaman, baca juga `05-UI-SHELL.md`.
4. Implementasi di branch sendiri sesuai `03-CONVENTIONS.md`.
5. Uji sendiri skenario utama task sebelum menandai `Done`.
6. Update status di `02-TASKS.md`, dan catat keputusan di `ctx/uas.md`.

Saat pertama kali menjalankan aplikasi, login memakai akun demo `admin` / `admin123`. Akun peran lain ada di `../database/README.md` bagian **Akun demo**.

Aturan status dan prinsip pembagian ada di `02-TASKS.md`.

## Aturan Dokumen

- **Satu topik satu tempat.** Perilaku fitur dan aturan bisnis hanya di `06-SPESIFIKASI.md`; alur layar, isi field form, dan user story hanya di `07-ALUR-PENGGUNA.md`; tata letak layar (mockup ASCII) hanya di `08-MOCKUP-HALAMAN.md`; cara teknis hanya di `04-ARSITEKTUR.md` dan `05-UI-SHELL.md`; status hanya di `02-TASKS.md`. Jangan menyalin isi yang sama ke dua file.
- **Perubahan menyentuh beberapa file.** Kalau kontrak fitur berubah, perbarui `06-SPESIFIKASI.md` dan `02-TASKS.md` pada commit yang sama. Kalau menu baru, perbarui `05-UI-SHELL.md` juga.
- **Proposal beku.** `proposal/` adalah artefak akademik yang sudah disetujui. Perubahan teknis setelah approval dicatat di `06-SPESIFIKASI.md`, bukan dengan mengedit proposal diam-diam.
- **Path relatif.** Dokumen di folder ini saling menunjuk dengan nama file, bukan path absolut.
- **Bahasa.** Istilah bisnis untuk judul task dan dokumen; istilah teknis hanya di bagian teknis.
