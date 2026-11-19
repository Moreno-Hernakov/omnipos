using MySql.Data.MySqlClient;
using OmniPos.Models;

namespace OmniPos.Repositories
{
    public class UserRepository
    {
        public User CariBerdasarkanUsername(string username)
        {
            const string query =
                "SELECT id, branch_id, username, password_hash, nama_lengkap, role, is_active " +
                "FROM users WHERE username = @username LIMIT 1";

            using (MySqlConnection koneksi = KoneksiDB.GetConnection())
            using (MySqlCommand perintah = new MySqlCommand(query, koneksi))
            {
                perintah.Parameters.AddWithValue("@username", username);

                koneksi.Open();

                using (MySqlDataReader pembaca = perintah.ExecuteReader())
                {
                    if (!pembaca.Read())
                    {
                        return null;
                    }

                    User pengguna = new User();
                    pengguna.Id = pembaca.GetInt32("id");
                    pengguna.BranchId = pembaca.IsDBNull(pembaca.GetOrdinal("branch_id"))
                        ? (int?)null
                        : pembaca.GetInt32("branch_id");
                    pengguna.Username = pembaca.GetString("username");
                    pengguna.PasswordHash = pembaca.GetString("password_hash");
                    pengguna.NamaLengkap = pembaca.GetString("nama_lengkap");
                    pengguna.Role = pembaca.GetString("role");
                    pengguna.IsActive = pembaca.GetBoolean("is_active");

                    return pengguna;
                }
            }
        }
    }
}
