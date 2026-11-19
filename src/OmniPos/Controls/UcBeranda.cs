using System;
using System.Windows.Forms;

namespace OmniPos.Controls
{
    public partial class UcBeranda : UserControl
    {
        public UcBeranda()
        {
            InitializeComponent();
        }

        public void AturData(string sapaan, string keterangan, string modulAktif)
        {
            labelSapaan.Text = sapaan;
            labelKeterangan.Text = keterangan;
            labelModulAktif.Text = modulAktif;
        }
    }
}
