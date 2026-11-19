using System;
using System.Windows.Forms;

namespace OmniPos.Controls
{
    // Halaman sementara untuk menu yang modulnya belum dibuat.
    public partial class UcSegeraHadir : UserControl
    {
        public UcSegeraHadir()
        {
            InitializeComponent();
        }

        public void AturJudul(string judul)
        {
            labelJudul.Text = judul;
        }
    }
}
