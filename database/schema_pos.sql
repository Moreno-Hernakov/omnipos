-- ========================================================
-- SKRIP BASIS DATA: OMNI-INDUSTRY CONFIGURABLE POS ENGINE
-- Mata Kuliah : Pemrograman Visual (Semester 3)
-- Target RDBMS: MySQL (XAMPP / MariaDB)
-- 16 tabel fisik: 13 tabel inti (12 kelompok) + 3 tabel pendukung
-- ========================================================

CREATE DATABASE IF NOT EXISTS `db_uas_pos`;
USE `db_uas_pos`;

-- 1. Tabel Konfigurasi Aplikasi (Key-Value / Feature Flags)
CREATE TABLE IF NOT EXISTS `app_config` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `setting_key` VARCHAR(50) NOT NULL UNIQUE,
    `setting_value` TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed default initial config
INSERT INTO `app_config` (`setting_key`, `setting_value`) VALUES
('is_onboarded', '0'),
('business_name', 'Omni POS Store'),
('business_address', 'Jl. Ngagel Jaya Tengah No. 73-77, Surabaya'),
('business_phone', '031-5041500'),
('enable_retail', '1'),
('enable_fnb', '1'),
('enable_recipe_bom', '1'),
('enable_service', '1'),
('enable_multi_branch', '1'),
('enable_shift', '1'),
('tax_percentage', '10')
ON DUPLICATE KEY UPDATE `setting_key` = `setting_key`;

-- 2. Tabel Cabang Usaha
CREATE TABLE IF NOT EXISTS `branches` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama_cabang` VARCHAR(100) NOT NULL,
    `alamat` TEXT NULL,
    `no_telp` VARCHAR(20) NULL,
    `is_pusat` TINYINT(1) DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed default branch (HQ)
INSERT INTO `branches` (`id`, `nama_cabang`, `alamat`, `no_telp`, `is_pusat`) VALUES
(1, 'Pusat (HQ)', 'Jl. Ngagel Jaya Tengah No. 73-77', '031-5041500', 1)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- 3. Tabel Pengguna (RBAC)
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NULL,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(64) NOT NULL, -- SHA-256
    `nama_lengkap` VARCHAR(100) NOT NULL,
    `role` ENUM('super_admin', 'branch_manager', 'cashier') NOT NULL DEFAULT 'cashier',
    `is_active` TINYINT(1) DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_users_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seed default Super Admin (Password: admin123 -> SHA256: 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9)
INSERT INTO `users` (`id`, `branch_id`, `username`, `password_hash`, `nama_lengkap`, `role`) VALUES
(1, 1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Super Administrator', 'super_admin')
ON DUPLICATE KEY UPDATE `id` = `id`;

-- 3A. Tabel Pelanggan / Member (pendukung modul operasional)
CREATE TABLE IF NOT EXISTS `customers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NOT NULL,
    `nama` VARCHAR(100) NOT NULL,
    `no_telp` VARCHAR(20) NULL,
    `email` VARCHAR(100) NULL,
    `poin` INT NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) DEFAULT 1,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_customers_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabel Kategori Item
CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama_kategori` VARCHAR(100) NOT NULL,
    `tipe_bisnis` ENUM('retail', 'fnb', 'service') NOT NULL DEFAULT 'retail'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Tabel Produk / Menu / Layanan
CREATE TABLE IF NOT EXISTS `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NOT NULL,
    `category_id` INT NULL,
    `kode_item` VARCHAR(50) NOT NULL,
    `nama_produk` VARCHAR(150) NOT NULL,
    `tipe` ENUM('retail', 'fnb', 'service') NOT NULL DEFAULT 'retail',
    `harga_jual` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `hpp_manual` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `stok` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    `is_active` TINYINT(1) DEFAULT 1,
    CONSTRAINT `fk_products_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_products_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Tabel Master Bahan Mentah (Khusus F&B)
CREATE TABLE IF NOT EXISTS `raw_materials` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nama_bahan` VARCHAR(100) NOT NULL,
    `satuan` VARCHAR(20) NOT NULL, -- 'gram', 'ml', 'pcs', 'butir'
    `harga_beli_satuan` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `stok_minimum` DECIMAL(10,2) NOT NULL DEFAULT 5.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Tabel Stok Bahan Mentah per Cabang
CREATE TABLE IF NOT EXISTS `branch_materials` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NOT NULL,
    `raw_material_id` INT NOT NULL,
    `stok` DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    UNIQUE KEY `uk_branch_material` (`branch_id`, `raw_material_id`),
    CONSTRAINT `fk_bm_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_bm_material` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_materials` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. Tabel Resep / Bill of Materials (BOM)
CREATE TABLE IF NOT EXISTS `product_recipes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `raw_material_id` INT NOT NULL,
    `takaran` DECIMAL(10,2) NOT NULL, -- jumlah satuan pemakaian
    UNIQUE KEY `uk_recipe_item` (`product_id`, `raw_material_id`),
    CONSTRAINT `fk_recipe_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_recipe_material` FOREIGN KEY (`raw_material_id`) REFERENCES `raw_materials` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. Tabel Shift Kasir
CREATE TABLE IF NOT EXISTS `shifts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `waktu_buka` DATETIME NOT NULL,
    `waktu_tutup` DATETIME NULL,
    `modal_awal` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `uang_sistem` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `uang_fisik` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `selisih` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `status` ENUM('open', 'closed') NOT NULL DEFAULT 'open',
    CONSTRAINT `fk_shifts_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_shifts_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. Tabel Transaksi Penjualan (Header)
CREATE TABLE IF NOT EXISTS `transactions` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nomor_nota` VARCHAR(50) NOT NULL UNIQUE,
    `branch_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `customer_id` INT NULL,
    `shift_id` INT NULL,
    `waktu` DATETIME NOT NULL,
    `subtotal` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `diskon` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `pajak` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `total_akhir` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `uang_bayar` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `kembalian` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `tipe_bayar` ENUM('cash', 'qris', 'transfer') NOT NULL DEFAULT 'cash',
    `status` ENUM('paid', 'hold', 'void') NOT NULL DEFAULT 'paid',
    `label_meja_pelanggan` VARCHAR(100) NULL,
    CONSTRAINT `fk_trans_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_trans_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_trans_customer` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_trans_shift` FOREIGN KEY (`shift_id`) REFERENCES `shifts` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. Tabel Detail Transaksi Penjualan
CREATE TABLE IF NOT EXISTS `transaction_details` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `transaction_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `qty` DECIMAL(10,2) NOT NULL,
    `harga_satuan` DECIMAL(12,2) NOT NULL,
    `hpp_satuan` DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    `subtotal` DECIMAL(12,2) NOT NULL,
    CONSTRAINT `fk_td_trans` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_td_product` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. Tabel Mutasi & Transfer Stok Antar-Cabang
CREATE TABLE IF NOT EXISTS `stock_transfers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nomor_transfer` VARCHAR(50) NOT NULL UNIQUE,
    `dari_branch_id` INT NOT NULL,
    `ke_branch_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `tanggal` DATETIME NOT NULL,
    `status` ENUM('pending', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
    CONSTRAINT `fk_st_from` FOREIGN KEY (`dari_branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_st_to` FOREIGN KEY (`ke_branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_st_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `stock_transfer_details` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `transfer_id` INT NOT NULL,
    `tipe_item` ENUM('product', 'material') NOT NULL DEFAULT 'product',
    `item_id` INT NOT NULL,
    `qty` DECIMAL(10,2) NOT NULL,
    CONSTRAINT `fk_std_transfer` FOREIGN KEY (`transfer_id`) REFERENCES `stock_transfers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Buku Besar Mutasi Stok (kartu stok & audit)
CREATE TABLE IF NOT EXISTS `stock_movements` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `branch_id` INT NOT NULL,
    `tipe_item` ENUM('product', 'material') NOT NULL,
    `item_id` INT NOT NULL,
    `arah` ENUM('in', 'out') NOT NULL,
    `qty` DECIMAL(10,2) NOT NULL,
    `stok_sebelum` DECIMAL(10,2) NOT NULL,
    `stok_sesudah` DECIMAL(10,2) NOT NULL,
    `sumber` ENUM('sale', 'restock', 'opname', 'transfer_in', 'transfer_out', 'void') NOT NULL,
    `ref_id` INT NULL,
    `nomor_dokumen` VARCHAR(50) NULL,
    `keterangan` VARCHAR(255) NULL,
    `user_id` INT NULL,
    `waktu` DATETIME NOT NULL,
    INDEX `idx_mov_item` (`branch_id`, `tipe_item`, `item_id`, `waktu`),
    INDEX `idx_mov_sumber` (`sumber`, `ref_id`),
    CONSTRAINT `fk_mov_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_mov_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabel Antrean & Status Pengerjaan Jasa
CREATE TABLE IF NOT EXISTS `service_jobs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `transaction_id` INT NOT NULL,
    `branch_id` INT NOT NULL,
    `nomor_antrean` VARCHAR(20) NOT NULL,
    `status` ENUM('antri', 'dikerjakan', 'selesai', 'diambil', 'batal') NOT NULL DEFAULT 'antri',
    `teknisi_user_id` INT NULL,
    `tanggal_masuk` DATETIME NOT NULL,
    `tanggal_selesai` DATETIME NULL,
    `catatan` TEXT NULL,
    UNIQUE KEY `uk_service_transaction` (`transaction_id`),
    CONSTRAINT `fk_service_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `transactions` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_service_branch` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_service_teknisi` FOREIGN KEY (`teknisi_user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
