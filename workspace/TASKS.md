# Papan Task Proyek UAS POS

Status: `Todo`, `Done`.

Aturan:

- Satu task satu owner.
- Status hanya `Todo` (belum selesai, termasuk sedang dikerjakan atau terhambat) dan `Done` (build dan uji task selesai).
- Catat blocker atau dependency yang menunggu di kolom catatan; status tetap `Todo`.
- Owner memastikan hasil sesuai task, build berhasil, dan skenario utama sudah diuji sebelum menandai `Done`.
- Task low-impact ditandai `[LOW]`; detail batasannya ada di `TEAM.md`.

## Fase 0 — Fondasi

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-00 | Spec v2, DDL 16 tabel, aturan workspace | Moreno | — | Done | `docs/SPECIFICATION.md`, `database/schema_pos.sql` |
| T-01 | Scaffold `src/OmniPos.sln` (net472), paket FastReport/MySql, restore MSBuild | Bagas | T-00 | Todo | Blocker semua task kode |
| T-02 | Import schema + seed demo awal | Moreno | T-01 | Todo | Agung membantu data contoh; schema tetap menjadi tanggung jawab Moreno |
| T-03 | `App.config` + `KoneksiDB` + tes koneksi | Bagas | T-01 | Todo | Jangan hardcode credential di kode |

## Fase 1 — Auth, Master Data, dan UI Pendukung

| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-10 | LoginForm + AuthService SHA-256 + validasi user aktif | Bagas | T-03 | Todo | Uji password salah dan user nonaktif |
| T-11 | OnboardingWizardForm + baca/tulis `app_config` | Bagas | T-10 | Todo | Empat tahap; set `is_onboarded=1` |
| T-12 | MainForm shell + navigasi berbasis role dan feature flag | Bagas | T-10 | Todo | Menu tidak berhak disembunyikan |
| T-13 | UcMasterProduk + UcKategori | Rangga | T-03 | Todo | CRUD sederhana, validasi kode item |
| T-14 | UcBahanBaku + UcResepBOM + RecipeService/HPP | Rangga | T-13 | Todo | HPP dihitung dari takaran × harga bahan |
| T-15 | UcPelanggan CRUD member | Gregorius Priyagung | T-03 | Todo | `[LOW]`; checkout tetap jalan tanpa member |
| T-16 | Shell UcLaporan: filter, grid, tombol | Gregorius Priyagung | T-12 | Todo | `[LOW]`; tanpa query/PDF |
| T-17 | UcServis read-only daftar antrean | Gregorius Priyagung | T-03 | Todo | `[LOW]`; tanpa update status |

## Fase 2 — Kasir, Stok, Shift
| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-20 | TransactionService atomik: header, detail, hold, void | Raymond | T-03, T-13, T-14 | Todo | `MySqlTransaction`; rollback saat gagal |
| T-21 | UcKasir UI: layout katalog, keranjang, tombol | Gregorius Priyagung | T-12 | Todo | `[LOW]`; tanpa logic transaksi |
| T-26 | UcKasir logic: katalog, keranjang, bayar, hold bill | Raymond | T-20, T-21 | Todo | Owner logic menyambungkan event UI |
| T-22 | InventoryService + `stock_movements` untuk sale/restock/opname/transfer | Moreno | T-20 | Todo | Setiap perubahan stok wajib ledger |
| T-23 | Struk thermal `PrintDocument` 58/80 mm | Raymond | T-20 | Todo | Cetak ulang tidak membuat nota baru |
| T-24 | ShiftService + UcShift: buka, blind close, rekap | Raymond | T-20 | Todo | Uji selisih kas |
| T-25 | Status/antrean servis + `service_jobs` | Raymond | T-20 | Todo | Satu job per transaksi servis |

## Fase 3 — Laporan
| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-30 | ReportRepository + ReportService (4 laporan) | Valencia | T-13, T-20, T-22 | Todo | Query parameterized, hitung total di C# |
| T-31 | Empat template `.frx` + `Laporan.cs` | Valencia | T-30 | Todo | Tanpa designer; ikuti kontrak spec |
| T-32 | Integrasi UcLaporan ke ReportService | Valencia | T-16, T-30, T-31 | Todo | Agung hanya menyediakan shell UI |
| T-33 | Dashboard produk terlaris | Valencia | T-30 | Todo | `DataGridView` + grafik batang |

## Fase 4 — Finalisasi
| ID | Task | Owner | Depends on | Status | Catatan |
| :--- | :--- | :--- | :--- | :--- | :--- |
| T-40 | Seed demo final + akun demo | Gregorius Priyagung | T-14, T-20, T-22 | Todo | `[LOW]`; data harus konsisten dengan laporan |
| T-41 | Checklist uji manual + uji rollback | Gregorius Priyagung | T-20, T-22 | Todo | `[LOW]`; gunakan skenario rollback yang disepakati |
| T-42 | User guide + screenshot | Gregorius Priyagung | T-32 | Todo | `[LOW]`; dipakai saat demo |
| T-43 | Regression akhir + latihan demo | Bagas | Semua | Todo | Semua anggota menjalankan skenario; Bagas koordinator |

## Ringkasan Beban Low-Impact

Task `[LOW]` untuk Gregorius Priyagung: T-15, T-16, T-17, T-21, T-40, T-41, T-42. Kerjakan berurutan; jangan ambil task lain sebelum T-15 dan T-16 selesai.
