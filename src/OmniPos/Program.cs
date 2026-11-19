using System;
using System.Diagnostics;
using System.Windows.Forms;
using OmniPos.Forms;
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

            using (LoginForm formLogin = new LoginForm())
            {
                if (formLogin.ShowDialog() == DialogResult.OK)
                {
                    // T-12 (Bagas) akan mengganti pesan ini dengan MainForm.
                    MessageBox.Show(
                        "Login berhasil sebagai " + formLogin.PenggunaLogin.NamaLengkap +
                        " (" + formLogin.PenggunaLogin.Role + "). Menu utama belum tersedia.",
                        "Login Berhasil",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);
                }
            }
        }
    }
}
