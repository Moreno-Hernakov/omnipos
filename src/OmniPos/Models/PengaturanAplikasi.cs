namespace OmniPos.Models
{
    // Nilai konfigurasi yang dipakai shell: identitas toko dan feature flag.
    public class PengaturanAplikasi
    {
        public string NamaToko { get; set; }
        public string NamaCabang { get; set; }
        public bool EnableRetail { get; set; }
        public bool EnableFnb { get; set; }
        public bool EnableRecipeBom { get; set; }
        public bool EnableService { get; set; }
        public bool EnableShift { get; set; }
        public bool EnableMultiBranch { get; set; }

        public PengaturanAplikasi()
        {
            NamaToko = "OmniPOS";
            NamaCabang = "Semua Cabang";
            EnableRetail = true;
            EnableFnb = true;
            EnableRecipeBom = true;
            EnableService = true;
            EnableShift = true;
            EnableMultiBranch = true;
        }
    }
}
