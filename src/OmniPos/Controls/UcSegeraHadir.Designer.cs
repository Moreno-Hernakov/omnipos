namespace OmniPos.Controls
{
    partial class UcSegeraHadir
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel panelIsi;
        private System.Windows.Forms.Panel panelIkon;
        private System.Windows.Forms.Panel panelBar1;
        private System.Windows.Forms.Panel panelBar2;
        private System.Windows.Forms.Panel panelBar3;
        private System.Windows.Forms.Label labelJudul;
        private System.Windows.Forms.Label labelPesan;
        private System.Windows.Forms.Label labelStatus;

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
            this.panelIsi = new System.Windows.Forms.Panel();
            this.panelIkon = new System.Windows.Forms.Panel();
            this.panelBar1 = new System.Windows.Forms.Panel();
            this.panelBar2 = new System.Windows.Forms.Panel();
            this.panelBar3 = new System.Windows.Forms.Panel();
            this.labelJudul = new System.Windows.Forms.Label();
            this.labelPesan = new System.Windows.Forms.Label();
            this.labelStatus = new System.Windows.Forms.Label();
            this.panelIsi.SuspendLayout();
            this.panelIkon.SuspendLayout();
            this.SuspendLayout();
            //
            // panelIsi
            //
            this.panelIsi.Controls.Add(this.panelIkon);
            this.panelIsi.Controls.Add(this.labelJudul);
            this.panelIsi.Controls.Add(this.labelPesan);
            this.panelIsi.Controls.Add(this.labelStatus);
            this.panelIsi.Location = new System.Drawing.Point(250, 180);
            this.panelIsi.Name = "panelIsi";
            this.panelIsi.Size = new System.Drawing.Size(460, 240);
            this.panelIsi.TabIndex = 0;
            //
            // panelIkon
            //
            this.panelIkon.BackColor = System.Drawing.Color.FromArgb(239, 246, 255);
            this.panelIkon.Controls.Add(this.panelBar1);
            this.panelIkon.Controls.Add(this.panelBar2);
            this.panelIkon.Controls.Add(this.panelBar3);
            this.panelIkon.Location = new System.Drawing.Point(198, 0);
            this.panelIkon.Name = "panelIkon";
            this.panelIkon.Size = new System.Drawing.Size(64, 64);
            this.panelIkon.TabIndex = 0;
            //
            // panelBar1
            //
            this.panelBar1.BackColor = System.Drawing.Color.FromArgb(147, 197, 253);
            this.panelBar1.Location = new System.Drawing.Point(18, 22);
            this.panelBar1.Name = "panelBar1";
            this.panelBar1.Size = new System.Drawing.Size(28, 4);
            this.panelBar1.TabIndex = 0;
            //
            // panelBar2
            //
            this.panelBar2.BackColor = System.Drawing.Color.FromArgb(147, 197, 253);
            this.panelBar2.Location = new System.Drawing.Point(18, 32);
            this.panelBar2.Name = "panelBar2";
            this.panelBar2.Size = new System.Drawing.Size(20, 4);
            this.panelBar2.TabIndex = 1;
            //
            // panelBar3
            //
            this.panelBar3.BackColor = System.Drawing.Color.FromArgb(191, 219, 254);
            this.panelBar3.Location = new System.Drawing.Point(18, 42);
            this.panelBar3.Name = "panelBar3";
            this.panelBar3.Size = new System.Drawing.Size(24, 4);
            this.panelBar3.TabIndex = 2;
            //
            // labelJudul
            //
            this.labelJudul.Font = new System.Drawing.Font("Segoe UI", 15F, System.Drawing.FontStyle.Bold);
            this.labelJudul.ForeColor = System.Drawing.Color.FromArgb(30, 41, 59);
            this.labelJudul.Location = new System.Drawing.Point(0, 84);
            this.labelJudul.Name = "labelJudul";
            this.labelJudul.Size = new System.Drawing.Size(460, 30);
            this.labelJudul.TabIndex = 1;
            this.labelJudul.Text = "Nama Menu";
            this.labelJudul.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            //
            // labelPesan
            //
            this.labelPesan.Font = new System.Drawing.Font("Segoe UI", 9.5F);
            this.labelPesan.ForeColor = System.Drawing.Color.FromArgb(71, 85, 105);
            this.labelPesan.Location = new System.Drawing.Point(0, 122);
            this.labelPesan.Name = "labelPesan";
            this.labelPesan.Size = new System.Drawing.Size(460, 38);
            this.labelPesan.TabIndex = 2;
            this.labelPesan.Text = "Halaman ini belum tersedia.\r\nModul sedang dikerjakan sesuai papan task.";
            this.labelPesan.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            //
            // labelStatus
            //
            this.labelStatus.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelStatus.ForeColor = System.Drawing.Color.FromArgb(148, 163, 184);
            this.labelStatus.Location = new System.Drawing.Point(0, 170);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(460, 20);
            this.labelStatus.TabIndex = 3;
            this.labelStatus.Text = "Gunakan menu lain sementara.";
            this.labelStatus.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            //
            // UcSegeraHadir
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.Controls.Add(this.panelIsi);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.Name = "UcSegeraHadir";
            this.Size = new System.Drawing.Size(960, 640);
            this.panelIsi.ResumeLayout(false);
            this.panelIkon.ResumeLayout(false);
            this.ResumeLayout(false);
        }
    }
}
