using System;
using System.Windows.Forms;
using OmniPos.Models;
using OmniPos.Services;

namespace OmniPos.Forms
{
    public partial class LoginForm : Form
    {
        public User PenggunaLogin { get; private set; }

        public LoginForm()
        {
            InitializeComponent();
        }

        private void buttonLogin_Click(object sender, EventArgs e)
        {
            labelPesan.Text = "";

            AuthService authService = new AuthService();
            HasilLogin hasil = authService.Login(textBoxUsername.Text, textBoxPassword.Text);

            if (!hasil.Berhasil)
            {
                labelPesan.Text = hasil.Pesan;
                textBoxPassword.Clear();
                textBoxPassword.Focus();
                return;
            }

            PenggunaLogin = hasil.Pengguna;
            DialogResult = DialogResult.OK;
            Close();
        }
    }
}
