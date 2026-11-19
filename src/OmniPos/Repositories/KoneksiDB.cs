using System;
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

        // Mengembalikan status koneksi. Detail teknis hanya untuk log, bukan untuk pengguna.
        public static bool TesKoneksi(out string detail)
        {
            detail = "";

            try
            {
                using (MySqlConnection koneksi = GetConnection())
                {
                    koneksi.Open();
                    detail = "Versi server: " + koneksi.ServerVersion;
                    return true;
                }
            }
            catch (MySqlException ex)
            {
                detail = ex.Message;
                return false;
            }
            catch (ConfigurationErrorsException ex)
            {
                detail = ex.Message;
                return false;
            }
            catch (ArgumentException ex)
            {
                detail = ex.Message;
                return false;
            }
        }
    }
}
