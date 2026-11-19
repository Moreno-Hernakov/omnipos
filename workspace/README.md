# Workspace Proyek UAS POS

Folder ini berisi aturan kerja, pembagian tugas, dan papan status proyek. Isinya bukan kode aplikasi; kode ada di `UAS_POS/src/`.

## Isi Folder

| File | Fungsi |
| :--- | :--- |
| `../AGENTS.md` | Aturan wajib untuk agent dan developer di scope `UAS_POS/`. |
| `TASKS.md` | Roster, modul formal, ownership, ringkasan per anggota, task per fase, dependency, dan status. |
| `CONVENTIONS.md` | Aturan branch, commit, cek mandiri, coding, dan build. |
| `../docs/SPECIFICATION.md` | Panduan fitur, alur kerja, laporan, dan kriteria selesai. |
| `../database/schema_pos.sql` | DDL final database. |

## Cara Pakai

1. Baca `../AGENTS.md` dan `../docs/SPECIFICATION.md` sebelum menerima task.
2. Cek `TASKS.md` untuk task yang menjadi tanggung jawabmu.
3. Baca panduan fitur di `../docs/SPECIFICATION.md`; jangan mengarang aturan sendiri.
4. Implementasi di branch sendiri sesuai `CONVENTIONS.md`.
5. Owner mengerjakan dan mengecek hasil task sendiri sebelum menandai `Done`.
6. Update status di `TASKS.md` dan catatan keputusan di `ctx/uas.md` root.

## Aturan Status

- `Todo` — task belum selesai, baik sedang dikerjakan maupun menunggu dependency/koordinasi. Catat blocker di kolom catatan.
- `Done` — owner sudah memastikan hasil sesuai task, build berhasil, dan skenario utama sudah diuji.

Tidak ada status antara; task yang sedang dikerjakan atau menunggu dependency/koordinasi tetap `Todo`.

Satu task hanya boleh punya satu owner. Jika owner berubah, catat di `TASKS.md`.

## Prinsip Pembagian

- Modul kritikal: checkout, stok, auth, dan laporan PDF dipegang anggota yang mampu menangani integrasi.
- Task pendukung tetap punya deliverable nyata dan tidak boleh memblokir fitur inti.
- Task disusun paralel; dependency hanya untuk hal yang benar-benar menghalangi.
- Setiap anggota menguji fiturnya sendiri; tidak ada task regresi terpusat.
- Setiap anggota tahu owner task dan siapa yang bisa dimintai bantuan bila perlu.
- Perubahan arsitektur dicatat di `docs/SPECIFICATION.md`; perubahan status dicatat di `TASKS.md`; riwayat lintas sesi dicatat di `ctx/uas.md`.
