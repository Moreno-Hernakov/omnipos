using System;
using System.Drawing;
using System.Windows.Forms;

namespace OmniPos.Controls
{
    public partial class UcBeranda : UserControl
    {
        public UcBeranda()
        {
            InitializeComponent();
        }

        public void AturData(string sapaan, string keterangan, string[] modul)
        {
            labelSapaan.Text = sapaan;
            labelKeterangan.Text = keterangan;
            panelModul.Controls.Clear();

            if (modul == null || modul.Length == 0)
            {
                panelModul.Controls.Add(BuatChip("Belum ada modul aktif", Tema.TeksLembut, Tema.LatarKonten));
                return;
            }

            for (int i = 0; i < modul.Length; i++)
            {
                if (i % 3 == 0)
                {
                    panelModul.Controls.Add(BuatChip(modul[i], Tema.InfoTeks, Tema.InfoLatar));
                }
                else if (i % 3 == 1)
                {
                    panelModul.Controls.Add(BuatChip(modul[i], Tema.PeringatanTeks, Tema.PeringatanLatar));
                }
                else
                {
                    panelModul.Controls.Add(BuatChip(modul[i], Tema.SuksesTeks, Tema.SuksesLatar));
                }
            }
        }

        private Label BuatChip(string teks, Color warnaTeks, Color warnaLatar)
        {
            Label chip = new Label();
            Size ukuranTeks = TextRenderer.MeasureText(teks, Tema.FontChip);

            chip.AutoSize = false;
            chip.Height = 28;
            chip.Width = ukuranTeks.Width + 24;
            chip.Margin = new Padding(0, 0, 8, 0);
            chip.Padding = new Padding(12, 0, 12, 0);
            chip.BackColor = warnaLatar;
            chip.ForeColor = warnaTeks;
            chip.Font = Tema.FontChip;
            chip.Text = teks;
            chip.TextAlign = ContentAlignment.MiddleCenter;

            return chip;
        }

        private void panelKartu_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
