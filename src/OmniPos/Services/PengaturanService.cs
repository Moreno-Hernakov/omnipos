using System.Collections.Generic;
using OmniPos.Models;
using OmniPos.Repositories;

namespace OmniPos.Services
{
    public class PengaturanService
    {
        private readonly PengaturanRepository pengaturanRepository;

        public PengaturanService()
        {
            pengaturanRepository = new PengaturanRepository();
        }

        // Membaca app_config sekali, lalu menggabungkannya dengan nama cabang pengguna.
        public PengaturanAplikasi Ambil(int? branchId)
        {
            Dictionary<string, string> data = pengaturanRepository.AmbilSemua();
            PengaturanAplikasi hasil = new PengaturanAplikasi();

            hasil.NamaToko = AmbilTeks(data, "business_name", hasil.NamaToko);
            hasil.EnableRetail = AmbilFlag(data, "enable_retail");
            hasil.EnableFnb = AmbilFlag(data, "enable_fnb");
            hasil.EnableRecipeBom = AmbilFlag(data, "enable_recipe_bom");
            hasil.EnableService = AmbilFlag(data, "enable_service");
            hasil.EnableShift = AmbilFlag(data, "enable_shift");
            hasil.EnableMultiBranch = AmbilFlag(data, "enable_multi_branch");

            if (branchId.HasValue)
            {
                string namaCabang = pengaturanRepository.AmbilNamaCabang(branchId.Value);

                if (!string.IsNullOrEmpty(namaCabang))
                {
                    hasil.NamaCabang = namaCabang;
                }
            }

            return hasil;
        }

        private string AmbilTeks(Dictionary<string, string> data, string kunci, string nilaiDefault)
        {
            string nilai;

            if (data.TryGetValue(kunci, out nilai) && !string.IsNullOrEmpty(nilai))
            {
                return nilai;
            }

            return nilaiDefault;
        }

        private bool AmbilFlag(Dictionary<string, string> data, string kunci)
        {
            string nilai;

            if (data.TryGetValue(kunci, out nilai))
            {
                return nilai == "1";
            }

            return true;
        }
    }
}
