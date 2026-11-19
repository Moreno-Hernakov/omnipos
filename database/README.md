# Database OmniPOS

Basis data MySQL/MariaDB untuk aplikasi OmniPOS. Pemilik: Moreno (225310693).

## Berkas

| Berkas | Isi |
| :--- | :--- |
| `schema_pos.sql` | DDL 16 tabel + konfigurasi awal + akun `admin`. |
| `seed_demo.sql` | Data contoh retail, F&B, dan jasa untuk demonstrasi. Aman dijalankan ulang. |

## Import dari awal

Jalankan dari root repo `UAS_POS/`, dengan klien MySQL/MariaDB di `PATH`:

```powershell
mysql -u root -p < database/schema_pos.sql
mysql -u root -p < database/seed_demo.sql
```

Urutan wajib: `schema_pos.sql` lebih dulu, lalu `seed_demo.sql`. Skrip seed memakai ID tetap dan `ON DUPLICATE KEY UPDATE`, jadi menjalankannya ulang tidak menggandakan data master. Baris saldo awal `stock_movements` dengan nomor dokumen `SEED-AWAL` dihapus lalu ditulis ulang.

Di XAMPP, klien berada di `C:\xampp\mysql\bin\mysql.exe`. Contoh:

```powershell
C:\xampp\mysql\bin\mysql.exe -u root < database\schema_pos.sql
C:\xampp\mysql\bin\mysql.exe -u root < database\seed_demo.sql
```

## Akun demo

| Username | Password | Peran | Cabang | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| `admin` | `admin123` | super_admin | Pusat (HQ) | Dibuat oleh `schema_pos.sql`. |
| `manager1` | `manager123` | branch_manager | Pusat (HQ) | Untuk uji menu manajer. |
| `kasir1` | `kasir123` | cashier | Pusat (HQ) | Untuk uji transaksi. |
| `kasir2` | `kasir123` | cashier | Cabang Darmo | Untuk uji filter cabang. |
| `nonaktif` | `kasir123` | cashier | Pusat (HQ) | `is_active = 0`, login harus ditolak. |

Password disimpan sebagai hash SHA-256 di kolom `users.password_hash`.

## Koneksi aplikasi

Aplikasi membaca connection string dari `src/OmniPos/App.config`. Jangan menaruh SQL atau kredensial di kode C#. Untuk pengembangan lokal, buat user aplikasi agar aplikasi tidak memakai `root`:

```sql
CREATE USER IF NOT EXISTS 'omnipos_app'@'localhost' IDENTIFIED BY 'omnipos_dev';
GRANT SELECT, INSERT, UPDATE, DELETE ON db_uas_pos.* TO 'omnipos_app'@'localhost';
FLUSH PRIVILEGES;
```

Nilai di `App.config` harus sama dengan user yang dibuat di server.
