using System.Collections.Generic;
using MySql.Data.MySqlClient;

namespace OmniPos.Repositories
{
    public class PengaturanRepository
    {
        public Dictionary<string, string> AmbilSemua()
        {
            Dictionary<string, string> hasil = new Dictionary<string, string>();
            const string query = "SELECT setting_key, setting_value FROM app_config";

            using (MySqlConnection koneksi = KoneksiDB.GetConnection())
            using (MySqlCommand perintah = new MySqlCommand(query, koneksi))
            {
                koneksi.Open();

                using (MySqlDataReader pembaca = perintah.ExecuteReader())
                {
                    while (pembaca.Read())
                    {
                        string kunci = pembaca.GetString("setting_key");
                        string nilai = pembaca.IsDBNull(pembaca.GetOrdinal("setting_value"))
                            ? ""
                            : pembaca.GetString("setting_value");

                        hasil[kunci] = nilai;
                    }
                }
            }

            return hasil;
        }

        public string AmbilNamaCabang(int branchId)
        {
            const string query = "SELECT nama_cabang FROM branches WHERE id = @id LIMIT 1";

            using (MySqlConnection koneksi = KoneksiDB.GetConnection())
            using (MySqlCommand perintah = new MySqlCommand(query, koneksi))
            {
                perintah.Parameters.AddWithValue("@id", branchId);
                koneksi.Open();

                object hasil = perintah.ExecuteScalar();
                return hasil == null ? "" : hasil.ToString();
            }
        }
    }
}
