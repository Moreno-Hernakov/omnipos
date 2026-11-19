namespace OmniPos.Controls
{
    partial class UcBeranda
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Label labelSapaan;
        private System.Windows.Forms.Label labelKeterangan;
        private System.Windows.Forms.Label labelModulAktif;
        private System.Windows.Forms.Label labelPetunjuk;
        private System.Windows.Forms.Panel panelGaris;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.labelSapaan = new System.Windows.Forms.Label();
            this.labelKeterangan = new System.Windows.Forms.Label();
            this.labelModulAktif = new System.Windows.Forms.Label();
            this.labelPetunjuk = new System.Windows.Forms.Label();
            this.panelGaris = new System.Windows.Forms.Panel();
            this.SuspendLayout();
            //
            // labelSapaan
            //
            this.labelSapaan.AutoSize = true;
            this.labelSapaan.Font = new System.Drawing.Font("Segoe UI", 18F, System.Drawing.FontStyle.Bold);
            this.labelSapaan.ForeColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.labelSapaan.Location = new System.Drawing.Point(32, 28);
            this.labelSapaan.Name = "labelSapaan";
            this.labelSapaan.Size = new System.Drawing.Size(198, 32);
            this.labelSapaan.TabIndex = 0;
            this.labelSapaan.Text = "Selamat datang";
            //
            // labelKeterangan
            //
            this.labelKeterangan.AutoSize = true;
            this.labelKeterangan.Font = new System.Drawing.Font("Segoe UI", 9.5F);
            this.labelKeterangan.ForeColor = System.Drawing.Color.FromArgb(75, 85, 99);
            this.labelKeterangan.Location = new System.Drawing.Point(34, 70);
            this.labelKeterangan.Name = "labelKeterangan";
            this.labelKeterangan.Size = new System.Drawing.Size(180, 17);
            this.labelKeterangan.TabIndex = 1;
            this.labelKeterangan.Text = "Peran dan cabang pengguna";
            //
            // panelGaris
            //
            this.panelGaris.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panelGaris.BackColor = System.Drawing.Color.FromArgb(226, 232, 240);
            this.panelGaris.Location = new System.Drawing.Point(32, 112);
            this.panelGaris.Name = "panelGaris";
            this.panelGaris.Size = new System.Drawing.Size(720, 1);
            this.panelGaris.TabIndex = 2;
            //
            // labelPetunjuk
            //
            this.labelPetunjuk.AutoSize = true;
            this.labelPetunjuk.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.labelPetunjuk.ForeColor = System.Drawing.Color.FromArgb(31, 41, 55);
            this.labelPetunjuk.Location = new System.Drawing.Point(32, 136);
            this.labelPetunjuk.Name = "labelPetunjuk";
            this.labelPetunjuk.Size = new System.Drawing.Size(330, 19);
            this.labelPetunjuk.TabIndex = 3;
            this.labelPetunjuk.Text = "Pilih menu di panel kiri untuk mulai bekerja.";
            //
            // labelModulAktif
            //
            this.labelModulAktif.AutoSize = true;
            this.labelModulAktif.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelModulAktif.ForeColor = System.Drawing.Color.FromArgb(107, 114, 128);
            this.labelModulAktif.Location = new System.Drawing.Point(34, 170);
            this.labelModulAktif.Name = "labelModulAktif";
            this.labelModulAktif.Size = new System.Drawing.Size(120, 15);
            this.labelModulAktif.TabIndex = 4;
            this.labelModulAktif.Text = "Modul aktif";
            //
            // UcBeranda
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(248, 250, 252);
            this.Controls.Add(this.labelModulAktif);
            this.Controls.Add(this.labelPetunjuk);
            this.Controls.Add(this.panelGaris);
            this.Controls.Add(this.labelKeterangan);
            this.Controls.Add(this.labelSapaan);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.Name = "UcBeranda";
            this.Size = new System.Drawing.Size(900, 600);
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
