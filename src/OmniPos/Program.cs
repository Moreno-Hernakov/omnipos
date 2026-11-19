using System;
using System.Diagnostics;
using System.Windows.Forms;
using OmniPos.Forms;
using OmniPos.Models;
using OmniPos.Services;

namespace OmniPos
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            SistemService sistemService = new SistemService();
            string detailKoneksi;

            if (!sistemService.CekKoneksi(out detailKoneksi))
            {
                Debug.WriteLine("Cek koneksi gagal: " + detailKoneksi);
                MessageBox.Show(
                    "Tidak dapat terhubung ke database. Periksa server MySQL dan pengaturan App.config.",
                    "Koneksi Database",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
                return;
            }

            // Login dan shell berulang agar tombol Keluar mengembalikan pengguna ke halaman login.
            while (true)
            {
                User pengguna;

                using (LoginForm formLogin = new LoginForm())
                {
                    if (formLogin.ShowDialog() != DialogResult.OK)
                    {
                        break;
                    }

                    pengguna = formLogin.PenggunaLogin;
                }

                using (MainForm formUtama = new MainForm())
                {
                    formUtama.Pengguna = pengguna;
                    Application.Run(formUtama);

                    if (!formUtama.KeluarKarenaLogout)
                    {
                        break;
                    }
                }
            }
        }
    }
}
