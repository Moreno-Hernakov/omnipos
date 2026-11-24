namespace OmniPos.Controls
{
    partial class UcBeranda
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel panelKartu;
        private System.Windows.Forms.Label labelSapaan;
        private System.Windows.Forms.Label labelKeterangan;
        private System.Windows.Forms.Panel panelGaris;
        private System.Windows.Forms.Label labelModulJudul;
        private System.Windows.Forms.FlowLayoutPanel panelModul;
        private System.Windows.Forms.Label labelPetunjuk;
        private System.Windows.Forms.Label labelBantuan;

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
            this.panelKartu = new System.Windows.Forms.Panel();
            this.labelBantuan = new System.Windows.Forms.Label();
            this.labelPetunjuk = new System.Windows.Forms.Label();
            this.panelModul = new System.Windows.Forms.FlowLayoutPanel();
            this.labelModulJudul = new System.Windows.Forms.Label();
            this.panelGaris = new System.Windows.Forms.Panel();
            this.labelKeterangan = new System.Windows.Forms.Label();
            this.labelSapaan = new System.Windows.Forms.Label();
            this.panelKartu.SuspendLayout();
            this.SuspendLayout();
            // 
            // panelKartu
            // 
            this.panelKartu.BackColor = System.Drawing.Color.White;
            this.panelKartu.Controls.Add(this.labelBantuan);
            this.panelKartu.Controls.Add(this.labelPetunjuk);
            this.panelKartu.Controls.Add(this.panelModul);
            this.panelKartu.Controls.Add(this.labelModulJudul);
            this.panelKartu.Controls.Add(this.panelGaris);
            this.panelKartu.Controls.Add(this.labelKeterangan);
            this.panelKartu.Controls.Add(this.labelSapaan);
            this.panelKartu.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelKartu.Location = new System.Drawing.Point(0, 0);
            this.panelKartu.Name = "panelKartu";
            this.panelKartu.Size = new System.Drawing.Size(960, 320);
            this.panelKartu.TabIndex = 0;
            this.panelKartu.Paint += new System.Windows.Forms.PaintEventHandler(this.panelKartu_Paint);
            // 
            // labelBantuan
            // 
            this.labelBantuan.AutoSize = true;
            this.labelBantuan.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelBantuan.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelBantuan.Location = new System.Drawing.Point(42, 240);
            this.labelBantuan.Name = "labelBantuan";
            this.labelBantuan.Size = new System.Drawing.Size(302, 15);
            this.labelBantuan.TabIndex = 6;
            this.labelBantuan.Text = "Menu mengikuti peran pengguna dan pengaturan toko.";
            // 
            // labelPetunjuk
            // 
            this.labelPetunjuk.AutoSize = true;
            this.labelPetunjuk.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.labelPetunjuk.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelPetunjuk.Location = new System.Drawing.Point(40, 214);
            this.labelPetunjuk.Name = "labelPetunjuk";
            this.labelPetunjuk.Size = new System.Drawing.Size(275, 19);
            this.labelPetunjuk.TabIndex = 5;
            this.labelPetunjuk.Text = "Pilih menu di panel kiri untuk mulai bekerja.";
            // 
            // panelModul
            // 
            this.panelModul.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panelModul.Location = new System.Drawing.Point(38, 154);
            this.panelModul.Name = "panelModul";
            this.panelModul.Size = new System.Drawing.Size(860, 34);
            this.panelModul.TabIndex = 4;
            this.panelModul.WrapContents = false;
            // 
            // labelModulJudul
            // 
            this.labelModulJudul.AutoSize = true;
            this.labelModulJudul.Font = new System.Drawing.Font("Segoe UI", 8F, System.Drawing.FontStyle.Bold);
            this.labelModulJudul.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelModulJudul.Location = new System.Drawing.Point(40, 132);
            this.labelModulJudul.Name = "labelModulJudul";
            this.labelModulJudul.Size = new System.Drawing.Size(118, 13);
            this.labelModulJudul.TabIndex = 3;
            this.labelModulJudul.Text = "MODUL BISNIS AKTIF";
            // 
            // panelGaris
            // 
            this.panelGaris.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.panelGaris.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(232)))), ((int)(((byte)(240)))));
            this.panelGaris.Location = new System.Drawing.Point(40, 110);
            this.panelGaris.Name = "panelGaris";
            this.panelGaris.Size = new System.Drawing.Size(860, 1);
            this.panelGaris.TabIndex = 2;
            // 
            // labelKeterangan
            // 
            this.labelKeterangan.AutoSize = true;
            this.labelKeterangan.Font = new System.Drawing.Font("Segoe UI", 9.5F);
            this.labelKeterangan.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(71)))), ((int)(((byte)(85)))), ((int)(((byte)(105)))));
            this.labelKeterangan.Location = new System.Drawing.Point(42, 78);
            this.labelKeterangan.Name = "labelKeterangan";
            this.labelKeterangan.Size = new System.Drawing.Size(177, 17);
            this.labelKeterangan.TabIndex = 1;
            this.labelKeterangan.Text = "Peran dan cabang pengguna";
            // 
            // labelSapaan
            // 
            this.labelSapaan.AutoEllipsis = true;
            this.labelSapaan.Font = new System.Drawing.Font("Segoe UI", 20F, System.Drawing.FontStyle.Bold);
            this.labelSapaan.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelSapaan.Location = new System.Drawing.Point(38, 32);
            this.labelSapaan.Name = "labelSapaan";
            this.labelSapaan.Size = new System.Drawing.Size(840, 38);
            this.labelSapaan.TabIndex = 0;
            this.labelSapaan.Text = "Selamat datang";
            // 
            // UcBeranda
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(241)))), ((int)(((byte)(245)))), ((int)(((byte)(249)))));
            this.Controls.Add(this.panelKartu);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.Name = "UcBeranda";
            this.Size = new System.Drawing.Size(960, 640);
            this.panelKartu.ResumeLayout(false);
            this.panelKartu.PerformLayout();
            this.ResumeLayout(false);

        }
    }
}
