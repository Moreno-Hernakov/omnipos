using OmniPos.Repositories;

namespace OmniPos.Services
{
    // Mengecek kesiapan sistem (saat ini koneksi database) agar UI tidak memanggil repository langsung.
    public class SistemService
    {
        public bool CekKoneksi(out string detail)
        {
            return KoneksiDB.TesKoneksi(out detail);
        }
    }
}
