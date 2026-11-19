namespace OmniPos.Controls
{
    partial class UcSegeraHadir
    {
        private System.ComponentModel.IContainer components = null;
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
            this.labelJudul = new System.Windows.Forms.Label();
            this.labelPesan = new System.Windows.Forms.Label();
            this.labelStatus = new System.Windows.Forms.Label();
            this.SuspendLayout();
            //
            // labelJudul
            //
            this.labelJudul.AutoSize = true;
            this.labelJudul.Font = new System.Drawing.Font("Segoe UI", 18F, System.Drawing.FontStyle.Bold);
            this.labelJudul.ForeColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.labelJudul.Location = new System.Drawing.Point(24, 24);
            this.labelJudul.Name = "labelJudul";
            this.labelJudul.Size = new System.Drawing.Size(140, 32);
            this.labelJudul.TabIndex = 0;
            this.labelJudul.Text = "Nama Menu";
            //
            // labelPesan
            //
            this.labelPesan.AutoSize = true;
            this.labelPesan.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.labelPesan.ForeColor = System.Drawing.Color.FromArgb(55, 65, 81);
            this.labelPesan.Location = new System.Drawing.Point(26, 74);
            this.labelPesan.Name = "labelPesan";
            this.labelPesan.Size = new System.Drawing.Size(290, 19);
            this.labelPesan.TabIndex = 1;
            this.labelPesan.Text = "Halaman ini belum tersedia.";
            //
            // labelStatus
            //
            this.labelStatus.AutoSize = true;
            this.labelStatus.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelStatus.ForeColor = System.Drawing.Color.FromArgb(107, 114, 128);
            this.labelStatus.Location = new System.Drawing.Point(26, 104);
            this.labelStatus.Name = "labelStatus";
            this.labelStatus.Size = new System.Drawing.Size(330, 15);
            this.labelStatus.TabIndex = 2;
            this.labelStatus.Text = "Modul sedang dikerjakan sesuai papan task.";
            //
            // UcSegeraHadir
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(248, 250, 252);
            this.Controls.Add(this.labelStatus);
            this.Controls.Add(this.labelPesan);
            this.Controls.Add(this.labelJudul);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.Name = "UcSegeraHadir";
            this.Size = new System.Drawing.Size(900, 600);
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
