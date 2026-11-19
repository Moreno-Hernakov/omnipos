using System.Configuration;
using MySql.Data.MySqlClient;

namespace OmniPos.Repositories
{
    public static class KoneksiDB
    {
        // Connection string dibaca dari App.config, bukan ditulis di kode.
        private static string AmbilConnectionString()
        {
            ConnectionStringSettings pengaturan = ConfigurationManager.ConnectionStrings["OmniPosDb"];

            if (pengaturan == null)
            {
                throw new ConfigurationErrorsException("Connection string 'OmniPosDb' tidak ditemukan di App.config.");
            }

            return pengaturan.ConnectionString;
        }

        public static MySqlConnection GetConnection()
        {
            return new MySqlConnection(AmbilConnectionString());
        }

        // Dipakai untuk mengecek database saat aplikasi mulai atau saat uji manual.
        public static bool TesKoneksi(out string pesan)
        {
            try
            {
                using (MySqlConnection koneksi = GetConnection())
                {
                    koneksi.Open();
                    pesan = "Koneksi berhasil. Versi server: " + koneksi.ServerVersion;
                    return true;
                }
            }
            catch (MySqlException ex)
            {
                pesan = "Koneksi gagal: " + ex.Message;
                return false;
            }
        }
    }
}
