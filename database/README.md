# Database OmniPOS

Basis data MySQL/MariaDB untuk aplikasi OmniPOS. Pemilik: Moreno (225310693).

## Tidak ada database di dalam repo

Repo hanya menyimpan skrip SQL. File data server (folder `data`, `ibdata1`, dan sejenisnya) tidak ikut Git; `bin/`, `obj/`, dan folder data MySQL juga di-ignore. Setiap anggota membuat database sendiri dari dua skrip di bawah, memakai server MySQL/MariaDB yang tersedia di komputernya.

Artinya: clone repo tidak otomatis memberi database. Yang dibagikan adalah **skema + seed**, bukan data server.

## Berkas

| Berkas | Isi |
| :--- | :--- |
| `schema_pos.sql` | DDL 16 tabel + konfigurasi awal + akun `admin`. |
| `seed_demo.sql` | Data contoh retail, F&B, dan jasa untuk demonstrasi. Aman dijalankan ulang. |

## Pilihan server lokal

| Lingkungan | Klien | Port default | Root default |
| :--- | :--- | :--- | :--- |
| XAMPP | `C:\xampp\mysql\bin\mysql.exe` | 3306 | password kosong |
| Laragon | `C:\laragon\bin\mysql\mysql-<versi>-winx64\bin\mysql.exe` | 3306 | password kosong |
| MariaDB portable (acuan pengembangan) | `C:\Users\Reno\AppData\Local\omnipos-db\mariadb-11.4.5-winx64\bin\mysql.exe` | 3306 | `root` |

Semua pilihan memakai MySQL/MariaDB, jadi skrip yang sama dipakai di mana saja.

### XAMPP

1. Buka **XAMPP Control Panel**, klik **Start** pada MySQL.
2. Dari root repo `UAS_POS/`, jalankan:

```powershell
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root < database\schema_pos.sql'
cmd /c '"C:\xampp\mysql\bin\mysql.exe" -u root < database\seed_demo.sql'
```

`cmd /c` dipakai karena PowerShell tidak mendukung operator `<`. Kalau root memakai password, tambahkan `-p` setelah `-u root`.

### Laragon

1. Buka Laragon, klik **Start All**.
2. Sesuaikan versi MySQL dengan folder di `C:\laragon\bin\mysql\`, lalu jalankan dari root repo:

```powershell
cmd /c '"C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe" -u root < database\schema_pos.sql'
cmd /c '"C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe" -u root < database\seed_demo.sql'
```

### MariaDB portable (acuan)

Nyalakan server (biarkan jendela terbuka):

```powershell
& "C:\Users\Reno\AppData\Local\omnipos-db\mariadb-11.4.5-winx64\bin\mariadbd.exe" `
  --basedir="C:\Users\Reno\AppData\Local\omnipos-db\mariadb-11.4.5-winx64" `
  --datadir="C:\Users\Reno\AppData\Local\omnipos-db\data" `
  --port=3306 --bind-address=127.0.0.1 --console
```

Lalu import:

```powershell
$mysql = "C:\Users\Reno\AppData\Local\omnipos-db\mariadb-11.4.5-winx64\bin\mysql.exe"
cmd /c "`"$mysql`" -u root -proot < database\schema_pos.sql"
cmd /c "`"$mysql`" -u root -proot < database\seed_demo.sql"
```

### phpMyAdmin

Bisa dipakai di XAMPP maupun Laragon:

1. Buka `http://localhost/phpmyadmin`.
2. Tab **Import**, pilih `database/schema_pos.sql`, klik **Go**.
3. Ulangi untuk `database/seed_demo.sql`.

Urutan wajib: schema dulu, seed setelahnya.

## Idempotensi

Skrip seed memakai ID tetap dan `ON DUPLICATE KEY UPDATE`, jadi menjalankannya ulang tidak menggandakan data master. Baris saldo awal `stock_movements` dengan nomor dokumen `SEED-AWAL` dihapus lalu ditulis ulang. `schema_pos.sql` memakai `CREATE DATABASE IF NOT EXISTS` dan `CREATE TABLE IF NOT EXISTS`.

## Menyamakan koneksi aplikasi

Aplikasi membaca connection string dari `src/OmniPos/App.config`:

```text
Server=127.0.0.1;Port=3306;Database=db_uas_pos;Uid=omnipos_app;Pwd=omnipos_dev;...
```

Cara paling rapi: buat user yang sama di server lokal masing-masing, sehingga `App.config` tidak perlu diubah dan tidak menimbulkan konflik Git.

```sql
CREATE USER IF NOT EXISTS 'omnipos_app'@'localhost' IDENTIFIED BY 'omnipos_dev';
CREATE USER IF NOT EXISTS 'omnipos_app'@'127.0.0.1' IDENTIFIED BY 'omnipos_dev';
GRANT SELECT, INSERT, UPDATE, DELETE ON db_uas_pos.* TO 'omnipos_app'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON db_uas_pos.* TO 'omnipos_app'@'127.0.0.1';
FLUSH PRIVILEGES;
```

Jalankan setelah schema di-import. Kalau port atau password server berbeda, ubah `App.config` **secara lokal** dan jangan commit kredensial pribadi.

Catatan:

- Jika MySQL portable dan Laragon/XAMPP sama-sama memakai port 3306, jalankan salah satu saja.
- Setelah mengubah `App.config`, build ulang atau sesuaikan `bin\Debug\OmniPos.exe.config`. File config di folder output tidak berubah sendiri.

## Kompatibilitas MySQL 8 dan MariaDB

- Skema hanya memakai DDL standar: `InnoDB`, `utf8mb4`, `ENUM`, foreign key, `ON DUPLICATE KEY UPDATE`. Tidak ada stored procedure, trigger, atau `DELIMITER`.
- Acuan pengembangan: MariaDB 11.4.5. Laragon memakai MySQL 8.0.30; sintaks yang dipakai kompatibel.
- MySQL 8 memakai `caching_sha2_password` sebagai default. `MySql.Data` 8.4 mendukungnya, dan connection string sudah memuat `AllowPublicKeyRetrieval=True` serta `SslMode=None`.
- Peringatan `TINYINT(1)` display width di MySQL 8 tidak memengaruhi data.

## Akun demo

| Username | Password | Peran | Cabang | Catatan |
| :--- | :--- | :--- | :--- | :--- |
| `admin` | `admin123` | super_admin | Pusat (HQ) | Dibuat oleh `schema_pos.sql`. |
| `manager1` | `manager123` | branch_manager | Pusat (HQ) | Untuk uji menu manajer. |
| `kasir1` | `kasir123` | cashier | Pusat (HQ) | Untuk uji transaksi. |
| `kasir2` | `kasir123` | cashier | Cabang Darmo | Untuk uji filter cabang. |
| `nonaktif` | `kasir123` | cashier | Pusat (HQ) | `is_active = 0`, login harus ditolak. |

Password disimpan sebagai hash SHA-256 di kolom `users.password_hash`.
