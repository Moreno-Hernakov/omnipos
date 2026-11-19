using System;
using System.Collections.Generic;
using System.Configuration;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;
using MySql.Data.MySqlClient;
using OmniPos.Controls;
using OmniPos.Models;
using OmniPos.Services;

namespace OmniPos.Forms
{
    public partial class MainForm : Form
    {
        private User pengguna;
        private PengaturanAplikasi pengaturan = new PengaturanAplikasi();
        private Button tombolMenuAktif;
        private UserControl halamanAktif;

        public bool KeluarKarenaLogout { get; private set; }

        public User Pengguna
        {
            get { return pengguna; }
            set { pengguna = value; }
        }

        public MainForm()
        {
            InitializeComponent();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            // Designer ikut membuat form tanpa pengguna; lewati pemuatan data.
            if (pengguna == null)
            {
                return;
            }

            MuatPengaturan();
            TampilkanIdentitas();
            SusunMenu();
        }

        private void MuatPengaturan()
        {
            PengaturanService pengaturanService = new PengaturanService();

            try
            {
                pengaturan = pengaturanService.Ambil(pengguna.BranchId);
            }
            catch (MySqlException ex)
            {
                Debug.WriteLine("Gagal memuat app_config: " + ex.Message);
                MessageBox.Show(
                    "Pengaturan toko tidak dapat dimuat. Menu ditampilkan dengan pengaturan bawaan.",
                    "Pengaturan Aplikasi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);
            }
            catch (ConfigurationErrorsException ex)
            {
                Debug.WriteLine("Gagal memuat app_config: " + ex.Message);
                MessageBox.Show(
                    "Pengaturan toko tidak dapat dimuat. Menu ditampilkan dengan pengaturan bawaan.",
                    "Pengaturan Aplikasi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);
            }
            catch (ArgumentException ex)
            {
                Debug.WriteLine("Gagal memuat app_config: " + ex.Message);
                MessageBox.Show(
                    "Pengaturan toko tidak dapat dimuat. Menu ditampilkan dengan pengaturan bawaan.",
                    "Pengaturan Aplikasi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);
            }
        }

        private void TampilkanIdentitas()
        {
            string namaPeran = NamaPeran(pengguna.Role);

            Text = "OmniPOS - " + pengaturan.NamaToko;
            labelLogoSub.Text = pengaturan.NamaToko;
            labelJudulHalaman.Text = "Beranda";
            labelJejak.Text = pengaturan.NamaToko + " / " + pengaturan.NamaCabang;
            labelPengguna.Text = pengguna.NamaLengkap;
            labelPeran.Text = namaPeran;
            labelInisial.Text = AmbilInisial(pengguna.NamaLengkap);
        }

        private string AmbilInisial(string nama)
        {
            if (string.IsNullOrWhiteSpace(nama))
            {
                return "?";
            }

            string[] bagian = nama.Split(new char[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);

            if (bagian.Length == 0)
            {
                return "?";
            }

            string inisial = bagian[0].Substring(0, 1);

            if (bagian.Length > 1)
            {
                inisial += bagian[bagian.Length - 1].Substring(0, 1);
            }

            return inisial.ToUpper();
        }

        private void SusunMenu()
        {
            panelMenu.Controls.Clear();
            tombolMenuAktif = null;

            Button tombolBeranda = TambahMenu("Beranda", "beranda");

            if (BolehKasir())
            {
                TambahJudulGrup("KASIR");
                TambahMenu("Transaksi Kasir", "kasir");

                if (pengaturan.EnableShift)
                {
                    TambahMenu("Shift Kasir", "shift");
                }

                TambahMenu("Pelanggan", "pelanggan");

                if (pengaturan.EnableService)
                {
                    TambahMenu("Antrean Servis", "servis");
                }
            }

            if (BolehMasterData())
            {
                TambahJudulGrup("MASTER DATA");
                TambahMenu("Produk & Kategori", "produk");

                if (pengaturan.EnableFnb)
                {
                    TambahMenu("Bahan Baku", "bahan");
                }

                if (pengaturan.EnableRecipeBom)
                {
                    TambahMenu("Resep & HPP", "resep");
                }
            }

            if (BolehInventaris())
            {
                TambahJudulGrup("INVENTARIS");
                TambahMenu("Stok Masuk", "stok-masuk");
                TambahMenu("Stok Opname", "stok-opname");

                if (pengaturan.EnableMultiBranch)
                {
                    TambahMenu("Transfer Stok", "stok-transfer");
                }

                TambahMenu("Riwayat Mutasi", "stok-mutasi");
            }

            if (BolehLaporan())
            {
                TambahJudulGrup("LAPORAN & ANALITIK");
                TambahMenu("Laporan", "laporan");
                TambahMenu("Dashboard Produk Terlaris", "dashboard");
            }

            if (PeranSuperAdmin())
            {
                TambahJudulGrup("PENGATURAN");
                TambahMenu("Profil Toko", "pengaturan-toko");
                TambahMenu("Cabang & Pengguna", "pengaturan-pengguna");
            }

            BukaMenu("beranda", "Beranda", tombolBeranda);
        }

        private void TambahJudulGrup(string judul)
        {
            Label labelGrup = new Label();
            labelGrup.AutoSize = false;
            labelGrup.Width = LebarTombolMenu();
            labelGrup.Height = 32;
            labelGrup.Margin = new Padding(2, 16, 0, 4);
            labelGrup.Font = Tema.FontGrup;
            labelGrup.ForeColor = Tema.SidebarMuted;
            labelGrup.Text = judul;
            labelGrup.TextAlign = ContentAlignment.BottomLeft;

            panelMenu.Controls.Add(labelGrup);
        }

        private Button TambahMenu(string judul, string kunci)
        {
            Button tombol = new Button();
            tombol.Width = LebarTombolMenu();
            tombol.Height = 40;
            tombol.Margin = new Padding(0, 2, 0, 2);
            tombol.FlatStyle = FlatStyle.Flat;
            tombol.FlatAppearance.BorderSize = 0;
            tombol.FlatAppearance.MouseOverBackColor = Tema.SidebarHover;
            tombol.BackColor = Tema.Sidebar;
            tombol.ForeColor = Tema.SidebarTeks;
            tombol.Font = Tema.FontMenu;
            tombol.TextAlign = ContentAlignment.MiddleLeft;
            tombol.Padding = new Padding(14, 0, 0, 0);
            tombol.Cursor = Cursors.Hand;
            tombol.UseMnemonic = false;
            tombol.Text = judul;
            tombol.Tag = kunci;
            tombol.Click += TombolMenu_Click;

            panelMenu.Controls.Add(tombol);
            return tombol;
        }

        private int LebarTombolMenu()
        {
            // Sisakan ruang scrollbar agar tombol tidak terpotong saat menu melebihi tinggi layar.
            int lebar = panelMenu.ClientSize.Width - SystemInformation.VerticalScrollBarWidth
                - panelMenu.Padding.Horizontal - 2;

            if (lebar < 120)
            {
                lebar = 204;
            }

            return lebar;
        }

        private void TombolMenu_Click(object sender, EventArgs e)
        {
            Button tombol = (Button)sender;
            string kunci = tombol.Tag == null ? "" : tombol.Tag.ToString();

            BukaMenu(kunci, tombol.Text, tombol);
        }

        private void BukaMenu(string kunci, string judul, Button tombol)
        {
            TampilkanHalaman(kunci, judul);

            labelJudulHalaman.Text = judul;
            labelJejak.Text = pengaturan.NamaToko + " / " + pengaturan.NamaCabang;

            if (tombolMenuAktif != null)
            {
                tombolMenuAktif.BackColor = Tema.Sidebar;
                tombolMenuAktif.ForeColor = Tema.SidebarTeks;
                tombolMenuAktif.FlatAppearance.MouseOverBackColor = Tema.SidebarHover;
            }

            tombolMenuAktif = tombol;
            tombol.BackColor = Tema.Primer;
            tombol.ForeColor = Color.White;
            tombol.FlatAppearance.MouseOverBackColor = Tema.PrimerGelap;
        }

        private void TampilkanHalaman(string kunci, string judul)
        {
            UserControl halaman = BuatHalaman(kunci, judul);

            panelKonten.SuspendLayout();

            if (halamanAktif != null)
            {
                panelKonten.Controls.Remove(halamanAktif);
                halamanAktif.Dispose();
            }

            halamanAktif = halaman;
            halaman.Dock = DockStyle.Fill;
            panelKonten.Controls.Add(halaman);

            panelKonten.ResumeLayout();
        }

        private UserControl BuatHalaman(string kunci, string judul)
        {
            if (kunci == "beranda")
            {
                UcBeranda beranda = new UcBeranda();
                beranda.AturData(
                    "Selamat datang, " + pengguna.NamaLengkap,
                    NamaPeran(pengguna.Role) + " - " + pengaturan.NamaCabang,
                    AmbilModulAktif());
                return beranda;
            }

            // Modul lain belum memiliki UserControl; shell menampilkan halaman sementara.
            UcSegeraHadir segeraHadir = new UcSegeraHadir();
            segeraHadir.AturJudul(judul);
            return segeraHadir;
        }

        private string[] AmbilModulAktif()
        {
            List<string> modul = new List<string>();

            if (pengaturan.EnableRetail)
            {
                modul.Add("Retail");
            }

            if (pengaturan.EnableFnb)
            {
                modul.Add("F&B");
            }

            if (pengaturan.EnableService)
            {
                modul.Add("Jasa");
            }

            return modul.ToArray();
        }

        private string NamaPeran(string role)
        {
            switch (role)
            {
                case "super_admin":
                    return "Super Admin";
                case "branch_manager":
                    return "Branch Manager";
                case "cashier":
                    return "Kasir";
                default:
                    return role;
            }
        }

        private bool PeranSuperAdmin()
        {
            return pengguna.Role == "super_admin";
        }

        private bool PeranManajer()
        {
            return pengguna.Role == "branch_manager";
        }

        private bool BolehKasir()
        {
            // Semua peran yang berhasil login boleh membuka layar kasir sesuai hak di spesifikasi.
            return PeranSuperAdmin() || PeranManajer() || pengguna.Role == "cashier";
        }

        private bool BolehMasterData()
        {
            return PeranSuperAdmin() || PeranManajer();
        }

        private bool BolehInventaris()
        {
            return PeranSuperAdmin() || PeranManajer();
        }

        private bool BolehLaporan()
        {
            return PeranSuperAdmin() || PeranManajer();
        }

        private void buttonLogout_Click(object sender, EventArgs e)
        {
            DialogResult jawaban = MessageBox.Show(
                "Keluar dari akun " + pengguna.NamaLengkap + "?",
                "Konfirmasi Keluar",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question);

            if (jawaban == DialogResult.Yes)
            {
                KeluarKarenaLogout = true;
                Close();
            }
        }
    }
}
