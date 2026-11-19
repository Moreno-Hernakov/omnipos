using System.Security.Cryptography;
using System.Text;
using OmniPos.Models;
using OmniPos.Repositories;

namespace OmniPos.Services
{
    public class HasilLogin
    {
        public bool Berhasil { get; set; }
        public string Pesan { get; set; }
        public User Pengguna { get; set; }
    }

    public class AuthService
    {
        private readonly UserRepository userRepository;

        public AuthService()
        {
            userRepository = new UserRepository();
        }

        public HasilLogin Login(string username, string password)
        {
            if (string.IsNullOrEmpty(username) || string.IsNullOrEmpty(password))
            {
                return Gagal("Username dan password wajib diisi.");
            }

            User pengguna = userRepository.CariBerdasarkanUsername(username.Trim());

            if (pengguna == null)
            {
                return Gagal("Username atau password salah.");
            }

            string hashInput = HitungSha256(password);

            if (pengguna.PasswordHash != hashInput)
            {
                return Gagal("Username atau password salah.");
            }

            if (!pengguna.IsActive)
            {
                return Gagal("Akun ini sedang tidak aktif. Hubungi administrator.");
            }

            HasilLogin hasil = new HasilLogin();
            hasil.Berhasil = true;
            hasil.Pesan = "Login berhasil.";
            hasil.Pengguna = pengguna;
            return hasil;
        }

        public static string HitungSha256(string teks)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                byte[] data = sha256.ComputeHash(Encoding.UTF8.GetBytes(teks));
                StringBuilder hasil = new StringBuilder();

                foreach (byte b in data)
                {
                    hasil.Append(b.ToString("x2"));
                }

                return hasil.ToString();
            }
        }

        private HasilLogin Gagal(string pesan)
        {
            HasilLogin hasil = new HasilLogin();
            hasil.Berhasil = false;
            hasil.Pesan = pesan;
            hasil.Pengguna = null;
            return hasil;
        }
    }
}
