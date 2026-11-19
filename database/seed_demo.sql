-- ========================================================
-- SEED DATA DEMO: OMNI-INDUSTRY CONFIGURABLE POS ENGINE
-- Dijalankan setelah database/schema_pos.sql.
-- Skrip aman dijalankan ulang (idempotent) karena memakai ID tetap.
--
-- Akun demo (password di-hash SHA-256):
--   admin    / admin123     (super_admin, sudah ada di schema)
--   manager1 / manager123   (branch_manager, cabang 1)
--   kasir1   / kasir123     (cashier, cabang 1)
--   kasir2   / kasir123     (cashier, cabang 2)
--   nonaktif / kasir123     (cashier nonaktif, untuk uji login ditolak)
-- ========================================================

USE `db_uas_pos`;

-- --------------------------------------------------------
-- Cabang
-- --------------------------------------------------------
INSERT INTO `branches` (`id`, `nama_cabang`, `alamat`, `no_telp`, `is_pusat`) VALUES
(2, 'Cabang Darmo', 'Jl. Raya Darmo No. 45, Surabaya', '031-5678123', 0)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Pengguna demo
-- --------------------------------------------------------
INSERT INTO `users` (`id`, `branch_id`, `username`, `password_hash`, `nama_lengkap`, `role`, `is_active`) VALUES
(2, 1, 'manager1', '866485796cfa8d7c0cf7111640205b83076433547577511d81f8030ae99ecea5', 'Manajer Cabang Pusat', 'branch_manager', 1),
(3, 1, 'kasir1', 'f02b7c1e519e4fa436147f7e1399974f9510aa9c8e0cb8be29151eb540f9d214', 'Kasir Pusat Satu', 'cashier', 1),
(4, 2, 'kasir2', 'f02b7c1e519e4fa436147f7e1399974f9510aa9c8e0cb8be29151eb540f9d214', 'Kasir Cabang Darmo', 'cashier', 1),
(5, 1, 'nonaktif', 'f02b7c1e519e4fa436147f7e1399974f9510aa9c8e0cb8be29151eb540f9d214', 'Kasir Nonaktif', 'cashier', 0)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Kategori
-- --------------------------------------------------------
INSERT INTO `categories` (`id`, `nama_kategori`, `tipe_bisnis`) VALUES
(1, 'Minuman Kemasan', 'retail'),
(2, 'Makanan Ringan', 'retail'),
(3, 'Kopi', 'fnb'),
(4, 'Makanan Berat', 'fnb'),
(5, 'Servis Kendaraan', 'service'),
(6, 'Laundry', 'service')
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Produk, menu, dan layanan
-- Produk retail memakai stok barang jadi.
-- Menu F&B memakai resep (hpp_manual dibiarkan 0).
-- Layanan jasa tidak memotong stok.
-- --------------------------------------------------------
INSERT INTO `products` (`id`, `branch_id`, `category_id`, `kode_item`, `nama_produk`, `tipe`, `harga_jual`, `hpp_manual`, `stok`, `is_active`) VALUES
(1, 1, 1, 'RTM-001', 'Air Mineral 600 ml', 'retail', 4000.00, 2200.00, 120.00, 1),
(2, 1, 1, 'RTM-002', 'Teh Botol 350 ml', 'retail', 5000.00, 3000.00, 80.00, 1),
(3, 1, 2, 'RTM-003', 'Keripik Kentang 68 g', 'retail', 12000.00, 7500.00, 45.00, 1),
(4, 1, 2, 'RTM-004', 'Cokelat Batang 65 g', 'retail', 15000.00, 9500.00, 30.00, 1),
(5, 1, 3, 'FNB-001', 'Kopi Susu Gula Aren', 'fnb', 22000.00, 0.00, 0.00, 1),
(6, 1, 3, 'FNB-002', 'Americano', 'fnb', 18000.00, 0.00, 0.00, 1),
(7, 1, 4, 'FNB-003', 'Nasi Goreng Spesial', 'fnb', 25000.00, 0.00, 0.00, 1),
(8, 1, 5, 'SVC-001', 'Ganti Oli Mesin', 'service', 60000.00, 25000.00, 0.00, 1),
(9, 1, 6, 'SVC-002', 'Cuci Setrika 3 kg', 'service', 25000.00, 8000.00, 0.00, 1),
(10, 2, 1, 'DRM-001', 'Air Mineral 600 ml', 'retail', 4500.00, 2400.00, 60.00, 1),
(11, 2, 3, 'DRM-002', 'Kopi Susu Gula Aren', 'fnb', 24000.00, 0.00, 0.00, 1)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Bahan baku mentah (harga beli per satuan)
-- --------------------------------------------------------
INSERT INTO `raw_materials` (`id`, `nama_bahan`, `satuan`, `harga_beli_satuan`, `stok_minimum`) VALUES
(1, 'Biji Kopi Arabika', 'gram', 350.00, 1000.00),
(2, 'Susu UHT Full Cream', 'ml', 18.00, 3000.00),
(3, 'Gula Aren Cair', 'ml', 25.00, 1000.00),
(4, 'Beras Premium', 'gram', 12.00, 5000.00),
(5, 'Telur Ayam', 'butir', 2500.00, 24.00),
(6, 'Minyak Goreng', 'ml', 17.00, 2000.00),
(7, 'Sabun Cuci Laundry', 'ml', 30.00, 500.00)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Stok bahan baku per cabang
-- --------------------------------------------------------
INSERT INTO `branch_materials` (`id`, `branch_id`, `raw_material_id`, `stok`) VALUES
(1, 1, 1, 5000.00),
(2, 1, 2, 20000.00),
(3, 1, 3, 5000.00),
(4, 1, 4, 25000.00),
(5, 1, 5, 120.00),
(6, 1, 6, 10000.00),
(7, 1, 7, 3000.00),
(8, 2, 1, 1500.00),
(9, 2, 2, 6000.00),
(10, 2, 3, 1500.00)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Resep / BOM (takaran per satu porsi)
-- --------------------------------------------------------
INSERT INTO `product_recipes` (`id`, `product_id`, `raw_material_id`, `takaran`) VALUES
(1, 5, 1, 18.00),
(2, 5, 2, 150.00),
(3, 5, 3, 20.00),
(4, 6, 1, 18.00),
(5, 7, 4, 150.00),
(6, 7, 5, 1.00),
(7, 7, 6, 20.00),
(8, 11, 1, 18.00),
(9, 11, 2, 150.00),
(10, 11, 3, 20.00)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Pelanggan / member
-- --------------------------------------------------------
INSERT INTO `customers` (`id`, `branch_id`, `nama`, `no_telp`, `email`, `poin`, `is_active`) VALUES
(1, 1, 'Budi Santoso', '081234567001', 'budi@example.com', 120, 1),
(2, 1, 'Siti Aminah', '081234567002', 'siti@example.com', 45, 1),
(3, 2, 'Andi Wijaya', '081234567003', 'andi@example.com', 10, 1)
ON DUPLICATE KEY UPDATE `id` = `id`;

-- --------------------------------------------------------
-- Saldo awal stok masuk ke buku besar (audit trail)
-- Dihapus dulu agar skrip aman dijalankan ulang.
-- --------------------------------------------------------
DELETE FROM `stock_movements` WHERE `sumber` = 'opname' AND `nomor_dokumen` = 'SEED-AWAL';

INSERT INTO `stock_movements`
(`branch_id`, `tipe_item`, `item_id`, `arah`, `qty`, `stok_sebelum`, `stok_sesudah`, `sumber`, `ref_id`, `nomor_dokumen`, `keterangan`, `user_id`, `waktu`) VALUES
(1, 'product', 1, 'in', 120.00, 0.00, 120.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'product', 2, 'in', 80.00, 0.00, 80.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'product', 3, 'in', 45.00, 0.00, 45.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'product', 4, 'in', 30.00, 0.00, 30.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 1, 'in', 5000.00, 0.00, 5000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 2, 'in', 20000.00, 0.00, 20000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 3, 'in', 5000.00, 0.00, 5000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 4, 'in', 25000.00, 0.00, 25000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 5, 'in', 120.00, 0.00, 120.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 6, 'in', 10000.00, 0.00, 10000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(1, 'material', 7, 'in', 3000.00, 0.00, 3000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(2, 'product', 10, 'in', 60.00, 0.00, 60.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(2, 'material', 1, 'in', 1500.00, 0.00, 1500.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(2, 'material', 2, 'in', 6000.00, 0.00, 6000.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00'),
(2, 'material', 3, 'in', 1500.00, 0.00, 1500.00, 'opname', NULL, 'SEED-AWAL', 'Saldo awal seed demo', 1, '2026-11-01 08:00:00');
