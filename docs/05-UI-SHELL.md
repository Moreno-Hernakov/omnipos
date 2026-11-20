# Panduan UI, Shell, dan UserControl

Cara membuat halaman dan menambahkannya ke menu. Aturan arsitektur ada di `04-ARSITEKTUR.md`.

## 1. Form vs UserControl

| Aspek | `Form` | `UserControl` |
| :--- | :--- | :--- |
| Jenis | Jendela mandiri | Kontrol yang ditanam di parent |
| Tampil | `Show()`, `ShowDialog()`, `Application.Run()` | `panel.Controls.Add(uc)` |
| Title bar / taskbar | Ya | Tidak |
| `ShowDialog` / `DialogResult` | Ya | Tidak |
| Message loop sendiri | Ya | Ikut Form induk |
| Nama di proyek | `LoginForm`, `MainForm`, `OnboardingWizardForm` | `UcBeranda`, `UcKasir`, `UcInventaris` |

Aturan:

- **Form** untuk jendela aplikasi dan dialog modal.
- **UserControl** untuk isi menu; satu shell, banyak halaman.
- Jangan menanam Form ke `panelKonten` (trik `TopLevel = false` tidak dipakai).
- Jangan memakai UserControl untuk dialog konfirmasi; pakai `MessageBox` atau Form modal.

## 2. Anatomi Shell

`MainForm` (`src/OmniPos/Forms/MainForm.cs`) terdiri dari:

- **Sidebar** (`panelMenu`) — tombol menu dibuat dari kode, bukan Designer.
- **Header** — judul halaman, breadcrumb toko/cabang, identitas pengguna, tombol Keluar.
- **Konten** (`panelKonten`) — hanya satu `UserControl` aktif.

Alur hidup:

1. `Program` membuat `MainForm`, mengisi `Pengguna`, lalu `Application.Run`.
2. `MainForm_Load` — kalau `Pengguna == null` (dibuka Designer), berhenti.
3. `MuatPengaturan()` — ambil `app_config` lewat `PengaturanService`; gagal → peringatan + pengaturan bawaan.
4. `TampilkanIdentitas()` — nama toko, cabang, nama/role pengguna, inisial avatar.
5. `SusunMenu()` — buat ulang seluruh tombol sidebar dari role + feature flag.
6. `BukaMenu("beranda", ...)` — tampilkan Beranda.
7. Klik menu → `TombolMenu_Click` → `BukaMenu` → `TampilkanHalaman` → `BuatHalaman`.

`TampilkanHalaman` membuang halaman lama (`Remove` + `Dispose`) sebelum menambah halaman baru. Jadi setiap pindah menu, halaman dibuat ulang dari nol.

## 3. Peta Menu

Shell menampilkan sidebar, header, dan satu halaman di `panelKonten`. Tabel ini adalah kontrak: setiap menu punya halaman, task, dan owner. Menu yang belum punya `UserControl` menampilkan `UcSegeraHadir`.

| Grup | Menu | Halaman (`UserControl`) | Task | Owner halaman | Role | Feature flag |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| — | Beranda | `UcBeranda` | T-12 | Moreno | SA, BM, Kasir | — |
| KASIR | Transaksi Kasir | `UcKasir` | T-21 | Raymond | SA, BM, Kasir | — |
| KASIR | Shift Kasir | `UcShift` | T-24 | Raymond | SA, BM, Kasir | `enable_shift` |
| KASIR | Pelanggan | `UcPelanggan` | T-15 | Gregorius | SA, BM, Kasir | — |
| KASIR | Antrean Servis | `UcServis` | T-25 | Raymond | SA, BM, Kasir | `enable_service` |
| MASTER DATA | Produk & Kategori | `UcMasterProduk` | T-13 | Rangga | SA, BM | — |
| MASTER DATA | Bahan Baku | `UcBahanBaku` | T-14 | Rangga | SA, BM | `enable_fnb` |
| MASTER DATA | Resep & HPP | `UcResepBOM` | T-14 | Rangga | SA, BM | `enable_recipe_bom` |
| INVENTARIS | Stok Masuk | `UcInventaris` (tab masuk) | T-22 | Moreno | SA, BM | — |
| INVENTARIS | Stok Opname | `UcInventaris` (tab opname) | T-22 | Moreno | SA, BM | — |
| INVENTARIS | Transfer Stok | `UcInventaris` (tab transfer) | T-22 | Moreno | SA, BM | `enable_multi_branch` |
| INVENTARIS | Riwayat Mutasi | `UcInventaris` (tab mutasi) | T-22 | Moreno | SA, BM | — |
| LAPORAN & ANALITIK | Laporan | `UcLaporan` | T-32 | Valencia | SA, BM | — |
| LAPORAN & ANALITIK | Dashboard Produk Terlaris | `UcDashboard` | T-33 | Valencia | SA, BM | — |
| PENGATURAN | Profil Toko | `UcPengaturanToko` | T-18 | Bagas | SA | — |
| PENGATURAN | Cabang & Pengguna | `UcPengaturanPengguna` | T-18 | Bagas | SA | — |

Keterangan role: SA = `super_admin`, BM = `branch_manager`, Kasir = `cashier`.

Submenu di dalam halaman (bukan menu sidebar):

- `UcLaporan` memuat empat jenis laporan lewat filter: penjualan, laba kotor, mutasi stok, dan rekap shift.
- `UcInventaris` memuat empat tab: stok masuk, opname, transfer, dan riwayat mutasi. Shell mengirim tab awal lewat method publik, bukan lewat constructor.
- Rekap shift untuk Kasir dibuka dari `UcShift`, bukan dari menu Laporan.

### Aturan shell

1. Visibilitas menu hanya ditentukan di `MainForm.SusunMenu()` dari role pengguna dan nilai `app_config`. Halaman tidak menyembunyikan menu sendiri.
2. Hak akses tetap diperiksa di service. Menyembunyikan menu bukan pengganti validasi bisnis.
3. Satu `panelKonten` hanya menampung satu halaman. Shell membuang halaman lama sebelum menampilkan yang baru.
4. `MainForm` milik owner shell. Pemilik modul **tidak mengedit** `MainForm`; serahkan nama class halaman, lalu owner shell menambahkan satu `case` di `BuatHalaman()`.
5. Halaman menerima data lewat method publik setelah `new` (contoh `AturData(...)`), bukan lewat constructor, agar tetap bisa dibuka di View Designer.
6. Menu atau submenu baru wajib memperbarui tabel ini, `SusunMenu()`, dan `02-TASKS.md` pada commit yang sama.
7. Label menu ditulis dalam bahasa bisnis dan `UseMnemonic = false`, sehingga karakter `&` tampil apa adanya.

## 4. Membuat UserControl Baru

1. Di Solution Explorer, klik kanan folder **`src/OmniPos/Controls`** (bukan project root).
2. **Add > New Item > User Control (Windows Forms)**.
3. Nama file memakai prefix `Uc`, contoh `UcKasir.cs`. Visual Studio membuat `UcKasir.cs` + `UcKasir.Designer.cs` dan mendaftarkannya ke `.csproj`.
4. Namespace otomatis `OmniPos.Controls` (RootNamespace `OmniPos` + folder `Controls`). Jangan diubah.
5. Susun layout di **View Designer**; logic di `UcKasir.cs`.
6. Build dulu sebelum dipakai di `MainForm`.

Jangan pilih `Form (Windows Forms)` untuk halaman menu. Jangan pilih `Component`; itu bukan kontrol visual.

### Aturan Designer

- Logic di `*.cs`, layout di `*.Designer.cs`. Jangan mengedit `*.Designer.cs` manual.
- File `.resx` hanya dibuat kalau memakai gambar/ikon/ImageList.
- Layout statis dibuat di Designer, bukan `new Button()` di constructor. Kode dinamis hanya untuk item berulang; container tetap dari Designer.
- Constructor `UserControl` hanya `InitializeComponent()`. Akses service/database ditaruh di method publik (`AturData`, `MuatData`) yang dipanggil shell, bukan di constructor.
- Desain di skala 100%. Jika Visual Studio memberi peringatan scaling 200%, pilih **Restart Visual Studio with 100% scaling**.

## 5. Mendaftarkan Halaman ke Shell

Shell memiliki satu titik dispatch: `MainForm.BuatHalaman(string kunci, string judul)`.

Contoh untuk halaman kasir:

```csharp
if (kunci == "kasir")
{
    UcKasir kasir = new UcKasir();
    kasir.AturData(pengguna, pengaturan);
    return kasir;
}
```

Langkah:

1. Pastikan tombol menu sudah ada di `SusunMenu()`. Kalau belum, tambahkan `TambahMenu("Nama Menu", "kunci")` di grup yang tepat.
2. Tambahkan `case`/`if` di `BuatHalaman()` dengan kunci yang sama.
3. Kirim data lewat method publik setelah `new`; jangan lewat constructor.
4. Perbarui tabel peta menu di dokumen ini.
5. Uji dengan login role yang berhak dan role yang tidak berhak.

Kalau bukan owner shell: cukup serahkan nama class dan kunci menu ke Moreno. Jangan edit `MainForm`.

### Menambah menu sidebar baru

Hanya kalau memang menu baru (bukan halaman untuk menu yang sudah ada):

1. Tambahkan baris di tabel peta menu.
2. Tambahkan `TambahMenu(...)` di `SusunMenu()` pada grup yang benar.
3. Tambahkan gate role/feature flag bila perlu (`pengaturan.EnableShift`, dst.).
4. Tambahkan dispatch di `BuatHalaman()`.
5. Perbarui `02-TASKS.md` dan tabel ini pada commit yang sama.

### Mengirim data ke halaman

Gunakan method publik, bukan constructor:

```csharp
public void AturData(User pengguna, PengaturanAplikasi pengaturan)
{
    this.pengguna = pengguna;
    this.pengaturan = pengaturan;

    labelNama.Text = pengguna.NamaLengkap;
}
```

Alasan: halaman tetap bisa dibuka di View Designer (Designer memanggil constructor tanpa argumen) dan shell tetap memegang kendali data.

## 6. Tema Visual

Shell memakai satu tema minimalis agar semua modul terlihat satu aplikasi.

| Token | Nilai | Pemakaian |
| :--- | :--- | :--- |
| Primer | `#2563EB` | tombol utama, menu aktif, avatar |
| Primer gelap | `#1D4ED8` | hover tombol/menu aktif |
| Aksen | `#EA580C` | penanda sekunder (belum dipakai di shell) |
| Latar | `#F8FAFC` | latar form |
| Latar konten | `#F1F5F9` | area kerja di dalam `panelKonten` |
| Kartu | `#FFFFFF` | panel konten, kartu beranda |
| Border | `#E2E8F0` | garis header dan pemisah |
| Teks | `#1E293B` | judul dan teks utama |
| Teks muted | `#475569` | keterangan |
| Teks lembut | `#64748B` | label grup dan metadata |
| Sidebar | `#111827` | latar sidebar |
| Sidebar hover | `#1F2937` | hover menu |
| Sidebar teks | `#D1D5DB` | teks menu tidak aktif |
| Sidebar muted | `#94A3B8` | label grup sidebar |

Aturan:

- Font tunggal `Segoe UI`. Skala: 20 pt sapaan, 13.5 pt judul halaman, 9.5 pt isi, 8.5 pt metadata, 8 pt label grup.
- Jarak mengikuti kelipatan 4/8 px; tombol menu 40 px, tombol utama 40 px, header 76 px, sidebar 248 px.
- Kontras teks minimal 4.5:1. Menu aktif putih di `#2563EB`; menu tidak aktif `#D1D5DB` di `#111827`.
- Ikon memakai bentuk geometris dari `Panel` sampai ada aset ikon resmi. Jangan memakai emoji sebagai ikon.
- `Tema.cs` menyimpan token untuk kontrol yang dibuat dari kode. Designer memakai nilai literal karena `*.Designer.cs` ditulis Visual Studio.
- Halaman modul mengikuti token yang sama; jangan menambah palet atau font baru tanpa memperbarui tabel ini.

## 7. Checklist Uji UI

- Login sebagai Super Admin, Branch Manager, dan Kasir; menu yang muncul sesuai role.
- Matikan feature flag di `app_config`; menu terkait hilang tanpa error.
- Klik semua menu bergantian beberapa kali; tidak ada kontrol menumpuk dan tidak ada error disposal.
- Halaman yang belum dibuat menampilkan `UcSegeraHadir`, bukan crash.
- Tombol Keluar kembali ke login dengan bersih.
- Layout tidak bertumpuk di skala 100%.
