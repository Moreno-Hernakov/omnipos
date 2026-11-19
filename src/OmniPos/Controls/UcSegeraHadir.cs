using System;
using System.Drawing;
using System.Windows.Forms;

namespace OmniPos.Controls
{
    // Halaman sementara untuk menu yang modulnya belum dibuat.
    public partial class UcSegeraHadir : UserControl
    {
        public UcSegeraHadir()
        {
            InitializeComponent();
            AturPosisi();
        }

        public void AturJudul(string judul)
        {
            labelJudul.Text = judul;
        }

        protected override void OnResize(EventArgs e)
        {
            base.OnResize(e);
            AturPosisi();
        }

        private void AturPosisi()
        {
            if (panelIsi == null)
            {
                return;
            }

            int kiri = (ClientSize.Width - panelIsi.Width) / 2;
            int atas = (ClientSize.Height - panelIsi.Height) / 2;

            if (kiri < 0)
            {
                kiri = 0;
            }

            if (atas < 0)
            {
                atas = 0;
            }

            panelIsi.Location = new Point(kiri, atas);
        }
    }
}
