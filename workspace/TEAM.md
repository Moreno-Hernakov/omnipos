# Pembagian Tugas Tim

Dokumen ini adalah pembagian kerja **internal**. Tabel modul formal tetap mengikuti proposal yang sudah disetujui; tabel eksekusi menunjukkan owner task dan support bila diperlukan.

## 1. Roster

| NRP | Nama | Modul formal (proposal) |
| :--- | :--- | :--- |
| 225310690 | Bagas Rizky Putra Wardana | Modul 1: Autentikasi & Konfigurasi |
| 225310691 | FX Thiarnika Eka Atur Rangga | Modul 2: Master Data & Resep BOM |
| 225310692 | Gregorius Priyagung | Modul 3: Kasir & Transaksi |
| 225310693 | Moreno Hernakov | Modul 4: Inventaris & Stok Cabang |
| 225310694 | Raymond Sugiharto | Modul 5: Operasional Kasir & Layanan |
| 225310695 | Valencia Angie Kurniawan | Modul 6: Laporan & Analitik |

## 2. Ownership Eksekusi

| Area | Owner | Support |
| :--- | :--- | :--- |
| Scaffold solution, `KoneksiDB`, `App.config` | Bagas | Moreno |
| Auth, onboarding, `MainForm`, RBAC | Bagas | — |
| Master produk, kategori, bahan baku | Rangga | — |
| Resep/BOM dan kalkulasi HPP | Rangga | Moreno |
| UI katalog/keranjang kasir | Gregorius Priyagung | Raymond |
| Logic checkout, hold bill, struk thermal | Raymond | Moreno (kontrak stok) |
| `InventoryService`, restock, opname, transfer | Moreno | — |
| `stock_movements` dan konsistensi stok | Moreno | Raymond |
| Shift kasir dan blind close | Raymond | — |
| Member/pelanggan | Gregorius Priyagung | Raymond |
| Status/antrean servis | Raymond | Gregorius Priyagung (UI read-only) |
| `ReportService`, `ReportRepository`, `Laporan.cs` | Valencia | — |
| Shell UI laporan dan filter | Gregorius Priyagung | Valencia |
| Seed demo, user guide, checklist uji manual | Gregorius Priyagung | Moreno |

Owner mengerjakan task dari awal sampai selesai dan memastikan hasilnya sesuai sebelum menandai `Done`. Support adalah anggota yang bisa dimintai bantuan bila diperlukan.

## 3. Pembagian Khusus Gregorius Priyagung (225310692)

Posisi formal di proposal tetap Modul 3. Scope eksekusinya dipersempit ke task **low-coupling** agar tidak menjadi jalur kritis. Urutan prioritas:

| Prioritas | Task | Deliverable | Dampak jika gagal |
| :---: | :--- | :--- | :--- |
| 1 | CRUD member/pelanggan | `UcPelanggan.cs` + `CustomerRepository.cs`: tambah, edit, nonaktifkan, grid, validasi nama | Checkout tetap jalan dengan `customer_id = NULL` |
| 2 | UI katalog/keranjang kasir | `UcKasir.cs`: layout katalog, keranjang, tombol; tanpa logic transaksi | Logic checkout tetap dipegang Raymond |
| 3 | Shell UI laporan | `UcLaporan.cs`: filter tanggal/cabang/status, grid kosong, tombol Tampilkan/Cetak | Query dan PDF tetap dipegang Valencia |
| 4 | Dokumentasi dan seed demo | `database/seed_demo.sql`, `docs/USER_GUIDE.md`, screenshot | Aplikasi tetap berjalan; demo memakai data manual |
| 5 | Daftar antrean servis read-only | `UcServis.cs`: grid dan filter status, tanpa aksi kritis | Transaksi jasa tetap tersimpan; update status dipegang Raymond |

Aturan untuk task di atas:

- Tidak boleh mengubah `TransactionService`, `InventoryService`, `RecipeService`, `Laporan.cs`, `KoneksiDB`, `MainForm`, `.csproj`, atau schema.
- Nama kontrol dan nama kolom harus mengikuti kontrak di `docs/SPECIFICATION.md`.
- Owner task UI menghubungkan event ke service sesuai kontrak; minta bantuan pemilik modul bila integrasi memerlukan koordinasi.
- Jika task tidak selesai sampai deadline, pemilik modul terkait membantu menyelesaikan bagian minimum agar demo tetap jalan.

## 4. Yang Tidak Diberikan ke Task Low-Impact

- Perhitungan dan penyimpanan transaksi.
- Pemotongan stok, BOM, HPP, dan `stock_movements`.
- Autentikasi, hashing, dan RBAC.
- Tutup shift dan rekonsiliasi kas.
- Query laporan dan template FastReport.
- Perubahan schema dan file shared.

## 5. Aturan Pergantian Owner

1. Perubahan owner dicatat di `TASKS.md` dan bagian ini.
2. Owner baru membaca kontrak di `docs/SPECIFICATION.md` dan current branch.
3. Task yang berpindah tetap memakai branch yang sama; jangan membuat implementasi paralel.
4. Jika task low-impact tertinggal, pemilik modul terkait membantu bagian minimum agar demo tetap jalan.
