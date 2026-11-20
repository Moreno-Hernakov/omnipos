# Arsitektur Aplikasi OmniPOS

Panduan teknis untuk developer. Perilaku fitur ada di `06-SPESIFIKASI.md`; aturan kerja tim ada di `03-CONVENTIONS.md`.

## 1. Stack dan Versi

| Komponen | Versi / Pilihan |
| :--- | :--- |
| Bahasa | C# 7.3 |
| Framework | .NET Framework 4.7.2, Windows Forms |
| Database | MySQL/MariaDB via ADO.NET (`MySql.Data` 8.4.0) |
| Laporan PDF | FastReport OpenSource 2026.2.8 + `Export.PdfSimple` |
| Struk thermal | `PrintDocument` bawaan Windows Forms |
| Build | MSBuild (bukan `dotnet restore`) |

Jangan menambah NuGet, library, atau pola arsitektur baru tanpa persetujuan. Larangan pola: async/await, LINQ berantai panjang, dependency injection, MVVM/MVC, generic/interface/abstract class yang tidak diajarkan, dan reflection untuk produksi.

## 2. Struktur Source

```text
src/OmniPos/
├── Forms/           # Jendela: LoginForm, MainForm, OnboardingWizardForm
├── Controls/        # Halaman UserControl: UcBeranda, UcKasir, UcInventaris, ...
├── Services/        # Logika bisnis: AuthService, PengaturanService, TransactionService, ...
├── Repositories/    # Akses database: KoneksiDB, UserRepository, ...
├── Models/          # Kelas data: User, PengaturanAplikasi, ...
├── Reports/         # Template dan kode laporan FastReport
├── Tema.cs          # Token warna/font untuk kontrol yang dibuat dari kode
├── App.config       # Connection string `OmniPosDb`
└── OmniPos.csproj
```

Project non-SDK: file baru harus terdaftar di `.csproj` (`Compile Include`, `SubType`, `DependentUpon`). **Add > New Item** di Visual Studio menangani ini otomatis.

## 3. Tiga Lapis

Alur satu arah: **UI → Service → Repository → Database**. Jangan melompati lapisan.

| Lapisan | Tanggung jawab | Boleh | Tidak boleh |
| :--- | :--- | :--- | :--- |
| UI (`Forms`, `Controls`) | Baca input, panggil service, tampilkan hasil/error | `MessageBox`, validasi format input | SQL, `MySqlConnection`, aturan bisnis |
| Service (`Services`) | Validasi, aturan bisnis, orkestrasi repository | Lempar/ubah error menjadi hasil yang bisa ditampilkan | Menyentuh kontrol WinForms, SQL mentah |
| Repository (`Repositories`) | Query parameterized, mapping ke model | `MySqlConnection`, `MySqlCommand`, transaksi | `MessageBox`, keputusan bisnis |
| Database | Menyimpan data | — | — |

## 4. Alur Nyata

### 4.1 Startup

`Program.Main` (`src/OmniPos/Program.cs`):

1. `SistemService.CekKoneksi` → `KoneksiDB.TesKoneksi`. Gagal → `MessageBox` lalu aplikasi berhenti.
2. `LoginForm.ShowDialog()`. Batal → keluar.
3. `MainForm.Pengguna = pengguna`, lalu `Application.Run`.
4. Tombol Keluar menutup `MainForm`; loop kembali ke login.

### 4.2 Login (contoh vertical slice)

| Lapisan | File | Tanggung jawab |
| :--- | :--- | :--- |
| UI | `Forms/LoginForm.cs` | Ambil username/password, panggil `AuthService.Login`, tampilkan `HasilLogin.Pesan` |
| Service | `Services/AuthService.cs` | Validasi input, hash SHA-256, cek user aktif, ubah error DB menjadi pesan umum |
| Repository | `Repositories/UserRepository.cs` | `SELECT ... FROM users WHERE username = @username LIMIT 1` |
| Database | `users` | `username`, `password_hash`, `role`, `is_active` |

### 4.3 Memuat Halaman

`MainForm_Load` memuat `app_config` lewat `PengaturanService`, menampilkan identitas, menyusun menu, lalu membuka Beranda. Setiap klik menu membuat `UserControl` baru lewat `BuatHalaman()`, membuang halaman lama, dan memasang halaman baru di `panelKonten`. Detail shell ada di `05-UI-SHELL.md`.

## 5. Koneksi Database

Connection string **hanya** ada di `src/OmniPos/App.config`, dengan nama `OmniPosDb`:

```text
Server=127.0.0.1;Port=3306;Database=db_uas_pos;Uid=omnipos_app;Pwd=omnipos_dev;...
```

`Repositories/KoneksiDB.cs` membungkus pembacaan config:

```csharp
public static MySqlConnection GetConnection()
{
    return new MySqlConnection(AmbilConnectionString());
}
```

Aturan:

- `GetConnection()` dipanggil **di setiap method repository** yang butuh database, dibungkus `using`.
- `TesKoneksi()` hanya dipanggil sekali saat startup (`SistemService`); bukan pengecekan berkala.
- Connection string tidak boleh ditulis di kode C# atau form.
- Repository tidak menyimpan koneksi sebagai field static; buka dan tutup per operasi.
- Tambah repository baru dengan pola yang sama:

```csharp
public List<Produk> AmbilSemua()
{
    List<Produk> hasil = new List<Produk>();
    const string query = "SELECT id, kode, nama FROM products WHERE is_active = 1";

    using (MySqlConnection koneksi = KoneksiDB.GetConnection())
    using (MySqlCommand perintah = new MySqlCommand(query, koneksi))
    {
        koneksi.Open();

        using (MySqlDataReader pembaca = perintah.ExecuteReader())
        {
            while (pembaca.Read())
            {
                // mapping kolom ke model
            }
        }
    }

    return hasil;
}
```

Setup database lokal dan akun `omnipos_app` ada di `../database/README.md`.

## 6. Penanganan Error

- Repository membiarkan `MySqlException` naik; jangan menangkap untuk menampilkan pesan.
- Service menangkap error teknis, menulis detail ke `Debug.WriteLine`, lalu mengembalikan pesan yang aman untuk pengguna (`HasilLogin`, `bool` + `out string`, atau exception bisnis).
- UI menampilkan pesan dari service. Detail SQL/config tidak boleh muncul di `MessageBox`.
- Error yang tidak bisa dipulihkan (config hilang, koneksi gagal saat startup) ditangani di `Program` atau form pemanggil.

Contoh pola service: `AuthService.Login` mengembalikan `HasilLogin` dengan `Berhasil`, `Pesan`, dan `Pengguna`. `MainForm.MuatPengaturan` menangkap `MySqlException`, `ConfigurationErrorsException`, dan `ArgumentException`, menulis log, lalu menampilkan peringatan dan memakai pengaturan bawaan.

## 7. Transaksi dan Stok

- Operasi multi-tabel wajib `MySqlTransaction` dan `rollback` saat gagal.
- Transaksi penjualan membungkus header nota, detail nota, dan pemotongan stok dalam satu transaksi.
- Setiap perubahan stok wajib menulis `stock_movements` dengan `stok_sebelum` dan `stok_sesudah` pada transaksi yang sama.
- Sumber mutasi harus jelas: penjualan, restock, opname, transfer, atau void.
- Uji kasus sukses dan kasus gagal/rollback.

## 8. Gaya Kode

- Kode harus mudah dibaca mahasiswa Semester 3; utamakan kejelasan.
- Class/method PascalCase; variabel lokal camelCase.
- Nama kontrol: `buttonSimpan`, `textBoxNama`, `dataGridViewProduk`, `labelTotal`.
- Uang memakai `decimal`; jangan `double` atau `float`.
- Koneksi, command, dan reader dibungkus `using`.
- Query memakai parameter (`@param`); jangan menyambung input ke SQL.
- Komentar singkat hanya untuk logika yang tidak obvious.

## 9. Aturan Database

- Schema final ada di `../database/schema_pos.sql`.
- Perubahan schema hanya oleh pemilik database dan wajib disinkronkan ke file itu; dampak fitur dicatat di `06-SPESIFIKASI.md`.
- Jangan menambah tabel/kolom tanpa fitur yang memakainya.
- Jangan menghapus data master yang masih direferensikan; gunakan `is_active` bila tersedia.
- Stok dipisahkan per cabang; transfer tidak boleh mengurangi stok dua kali.

## 10. Laporan Teknis

- Laporan manajemen memakai FastReport; struk thermal memakai `PrintDocument`. Jangan mencampur keduanya.
- Template `.frx` adalah artefak sumber dan dibuat dari kode; FastReport OpenSource tidak punya designer.
- `PDFSimpleExport` meraster halaman menjadi gambar, jadi teks PDF tidak bisa diselect. Ini batasan paket yang sudah diterima.
- Panggil `RegisterData` tanpa alias agar tidak bentrok dengan namespace FastReport.
- Sebelum `Prepare()`, pastikan assembly `Microsoft.CSharp` dan `System.Linq` sudah termuat.
- Format uang/tanggal dilakukan di C# sebelum masuk `DataTable`.
- Kontrak nama tabel/kolom dan parameter total ada di `06-SPESIFIKASI.md` lampiran 9.2.
- Uji PDF dengan data seed dan filter kosong.

## 11. Checklist Fitur Baru

1. Tentukan model di `Models/` bila data belum punya kelas.
2. Buat method repository dengan query parameterized dan `using`.
3. Buat service yang memvalidasi aturan bisnis dan memanggil repository.
4. Buat `UserControl` di `Controls/` (lihat `05-UI-SHELL.md`).
5. Daftarkan halaman di `MainForm.BuatHalaman()` lewat owner shell.
6. Uji skenario utama, input kosong, dan error database.
7. Build MSBuild 0 error, lalu perbarui `02-TASKS.md`.

## 12. Larangan Keras

- SQL atau `MySqlConnection` di Form/UserControl.
- Connection string di kode C#.
- `MessageBox` di repository.
- Logika bisnis di event handler UI.
- `double` untuk uang.
- Query dengan konkatenasi string.
- Menambah tabel/kolom yang tidak dipakai fitur.
- Mengklaim task selesai tanpa build dan uji.
