using System;
using System.Windows.Forms;
using OmniPos.Forms;
using OmniPos.Repositories;

namespace OmniPos
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            string pesanKoneksi;
            if (!KoneksiDB.TesKoneksi(out pesanKoneksi))
            {
                MessageBox.Show(pesanKoneksi, "Koneksi Database",
                    MessageBoxButtons.OK, MessageBoxIcon.Error);
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
