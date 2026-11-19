namespace OmniPos.Forms
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel panelSidebar;
        private System.Windows.Forms.Panel panelLogo;
        private System.Windows.Forms.Label labelLogo;
        private System.Windows.Forms.Label labelLogoSub;
        private System.Windows.Forms.FlowLayoutPanel panelMenu;
        private System.Windows.Forms.Panel panelFooter;
        private System.Windows.Forms.Label labelVersi;
        private System.Windows.Forms.Panel panelUtama;
        private System.Windows.Forms.Panel panelHeader;
        private System.Windows.Forms.Label labelNamaToko;
        private System.Windows.Forms.Label labelCabang;
        private System.Windows.Forms.Label labelPengguna;
        private System.Windows.Forms.Label labelPeran;
        private System.Windows.Forms.Button buttonLogout;
        private System.Windows.Forms.Panel panelGarisHeader;
        private System.Windows.Forms.Panel panelKonten;

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
            this.panelSidebar = new System.Windows.Forms.Panel();
            this.panelLogo = new System.Windows.Forms.Panel();
            this.labelLogo = new System.Windows.Forms.Label();
            this.labelLogoSub = new System.Windows.Forms.Label();
            this.panelMenu = new System.Windows.Forms.FlowLayoutPanel();
            this.panelFooter = new System.Windows.Forms.Panel();
            this.labelVersi = new System.Windows.Forms.Label();
            this.panelUtama = new System.Windows.Forms.Panel();
            this.panelKonten = new System.Windows.Forms.Panel();
            this.panelHeader = new System.Windows.Forms.Panel();
            this.labelNamaToko = new System.Windows.Forms.Label();
            this.labelCabang = new System.Windows.Forms.Label();
            this.labelPengguna = new System.Windows.Forms.Label();
            this.labelPeran = new System.Windows.Forms.Label();
            this.buttonLogout = new System.Windows.Forms.Button();
            this.panelGarisHeader = new System.Windows.Forms.Panel();
            this.panelSidebar.SuspendLayout();
            this.panelLogo.SuspendLayout();
            this.panelFooter.SuspendLayout();
            this.panelUtama.SuspendLayout();
            this.panelHeader.SuspendLayout();
            this.SuspendLayout();
            //
            // panelSidebar
            //
            this.panelSidebar.BackColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.panelSidebar.Controls.Add(this.panelMenu);
            this.panelSidebar.Controls.Add(this.panelFooter);
            this.panelSidebar.Controls.Add(this.panelLogo);
            this.panelSidebar.Dock = System.Windows.Forms.DockStyle.Left;
            this.panelSidebar.Location = new System.Drawing.Point(0, 0);
            this.panelSidebar.Name = "panelSidebar";
            this.panelSidebar.Size = new System.Drawing.Size(236, 800);
            this.panelSidebar.TabIndex = 0;
            //
            // panelLogo
            //
            this.panelLogo.Controls.Add(this.labelLogo);
            this.panelLogo.Controls.Add(this.labelLogoSub);
            this.panelLogo.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelLogo.Location = new System.Drawing.Point(0, 0);
            this.panelLogo.Name = "panelLogo";
            this.panelLogo.Size = new System.Drawing.Size(236, 88);
            this.panelLogo.TabIndex = 0;
            //
            // labelLogo
            //
            this.labelLogo.AutoSize = true;
            this.labelLogo.Font = new System.Drawing.Font("Segoe UI", 16F, System.Drawing.FontStyle.Bold);
            this.labelLogo.ForeColor = System.Drawing.Color.White;
            this.labelLogo.Location = new System.Drawing.Point(20, 22);
            this.labelLogo.Name = "labelLogo";
            this.labelLogo.Size = new System.Drawing.Size(109, 30);
            this.labelLogo.TabIndex = 0;
            this.labelLogo.Text = "OmniPOS";
            //
            // labelLogoSub
            //
            this.labelLogoSub.AutoSize = true;
            this.labelLogoSub.Font = new System.Drawing.Font("Segoe UI", 8.25F);
            this.labelLogoSub.ForeColor = System.Drawing.Color.FromArgb(156, 163, 175);
            this.labelLogoSub.Location = new System.Drawing.Point(22, 54);
            this.labelLogoSub.Name = "labelLogoSub";
            this.labelLogoSub.Size = new System.Drawing.Size(76, 13);
            this.labelLogoSub.TabIndex = 1;
            this.labelLogoSub.Text = "Point of Sale";
            //
            // panelMenu
            //
            this.panelMenu.AutoScroll = true;
            this.panelMenu.BackColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.panelMenu.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelMenu.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.panelMenu.Location = new System.Drawing.Point(0, 88);
            this.panelMenu.Name = "panelMenu";
            this.panelMenu.Padding = new System.Windows.Forms.Padding(12, 8, 12, 8);
            this.panelMenu.Size = new System.Drawing.Size(236, 664);
            this.panelMenu.TabIndex = 1;
            this.panelMenu.WrapContents = false;
            //
            // panelFooter
            //
            this.panelFooter.Controls.Add(this.labelVersi);
            this.panelFooter.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panelFooter.Location = new System.Drawing.Point(0, 752);
            this.panelFooter.Name = "panelFooter";
            this.panelFooter.Size = new System.Drawing.Size(236, 48);
            this.panelFooter.TabIndex = 2;
            //
            // labelVersi
            //
            this.labelVersi.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelVersi.Font = new System.Drawing.Font("Segoe UI", 8.25F);
            this.labelVersi.ForeColor = System.Drawing.Color.FromArgb(107, 114, 128);
            this.labelVersi.Location = new System.Drawing.Point(0, 0);
            this.labelVersi.Name = "labelVersi";
            this.labelVersi.Size = new System.Drawing.Size(236, 48);
            this.labelVersi.TabIndex = 0;
            this.labelVersi.Text = "OmniPOS v1.0";
            this.labelVersi.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            //
            // panelUtama
            //
            this.panelUtama.BackColor = System.Drawing.Color.FromArgb(241, 245, 249);
            this.panelUtama.Controls.Add(this.panelKonten);
            this.panelUtama.Controls.Add(this.panelHeader);
            this.panelUtama.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelUtama.Location = new System.Drawing.Point(236, 0);
            this.panelUtama.Name = "panelUtama";
            this.panelUtama.Size = new System.Drawing.Size(1044, 800);
            this.panelUtama.TabIndex = 1;
            //
            // panelHeader
            //
            this.panelHeader.BackColor = System.Drawing.Color.White;
            this.panelHeader.Controls.Add(this.labelNamaToko);
            this.panelHeader.Controls.Add(this.labelCabang);
            this.panelHeader.Controls.Add(this.labelPengguna);
            this.panelHeader.Controls.Add(this.labelPeran);
            this.panelHeader.Controls.Add(this.buttonLogout);
            this.panelHeader.Controls.Add(this.panelGarisHeader);
            this.panelHeader.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelHeader.Location = new System.Drawing.Point(0, 0);
            this.panelHeader.Name = "panelHeader";
            this.panelHeader.Size = new System.Drawing.Size(1044, 76);
            this.panelHeader.TabIndex = 0;
            //
            // labelNamaToko
            //
            this.labelNamaToko.AutoEllipsis = true;
            this.labelNamaToko.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold);
            this.labelNamaToko.ForeColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.labelNamaToko.Location = new System.Drawing.Point(24, 14);
            this.labelNamaToko.Name = "labelNamaToko";
            this.labelNamaToko.Size = new System.Drawing.Size(380, 24);
            this.labelNamaToko.TabIndex = 0;
            this.labelNamaToko.Text = "Nama Toko";
            //
            // labelCabang
            //
            this.labelCabang.AutoSize = true;
            this.labelCabang.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelCabang.ForeColor = System.Drawing.Color.FromArgb(107, 114, 128);
            this.labelCabang.Location = new System.Drawing.Point(26, 42);
            this.labelCabang.Name = "labelCabang";
            this.labelCabang.Size = new System.Drawing.Size(92, 15);
            this.labelCabang.TabIndex = 1;
            this.labelCabang.Text = "Cabang: Pusat";
            //
            // labelPengguna
            //
            this.labelPengguna.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.labelPengguna.Font = new System.Drawing.Font("Segoe UI", 9.5F, System.Drawing.FontStyle.Bold);
            this.labelPengguna.ForeColor = System.Drawing.Color.FromArgb(17, 24, 39);
            this.labelPengguna.Location = new System.Drawing.Point(588, 16);
            this.labelPengguna.Name = "labelPengguna";
            this.labelPengguna.Size = new System.Drawing.Size(300, 20);
            this.labelPengguna.TabIndex = 2;
            this.labelPengguna.Text = "Nama Pengguna";
            this.labelPengguna.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            //
            // labelPeran
            //
            this.labelPeran.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.labelPeran.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelPeran.ForeColor = System.Drawing.Color.FromArgb(107, 114, 128);
            this.labelPeran.Location = new System.Drawing.Point(588, 40);
            this.labelPeran.Name = "labelPeran";
            this.labelPeran.Size = new System.Drawing.Size(300, 18);
            this.labelPeran.TabIndex = 3;
            this.labelPeran.Text = "Peran";
            this.labelPeran.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            //
            // buttonLogout
            //
            this.buttonLogout.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonLogout.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(209, 213, 219);
            this.buttonLogout.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonLogout.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.buttonLogout.ForeColor = System.Drawing.Color.FromArgb(55, 65, 81);
            this.buttonLogout.Location = new System.Drawing.Point(908, 22);
            this.buttonLogout.Name = "buttonLogout";
            this.buttonLogout.Size = new System.Drawing.Size(112, 32);
            this.buttonLogout.TabIndex = 4;
            this.buttonLogout.Text = "Keluar";
            this.buttonLogout.UseVisualStyleBackColor = true;
            this.buttonLogout.Click += new System.EventHandler(this.buttonLogout_Click);
            //
            // panelGarisHeader
            //
            this.panelGarisHeader.BackColor = System.Drawing.Color.FromArgb(226, 232, 240);
            this.panelGarisHeader.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panelGarisHeader.Location = new System.Drawing.Point(0, 75);
            this.panelGarisHeader.Name = "panelGarisHeader";
            this.panelGarisHeader.Size = new System.Drawing.Size(1044, 1);
            this.panelGarisHeader.TabIndex = 5;
            //
            // panelKonten
            //
            this.panelKonten.BackColor = System.Drawing.Color.FromArgb(241, 245, 249);
            this.panelKonten.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelKonten.Location = new System.Drawing.Point(0, 76);
            this.panelKonten.Name = "panelKonten";
            this.panelKonten.Padding = new System.Windows.Forms.Padding(24);
            this.panelKonten.Size = new System.Drawing.Size(1044, 724);
            this.panelKonten.TabIndex = 1;
            //
            // MainForm
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(248, 250, 252);
            this.ClientSize = new System.Drawing.Size(1280, 800);
            this.Controls.Add(this.panelUtama);
            this.Controls.Add(this.panelSidebar);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.MinimumSize = new System.Drawing.Size(1100, 700);
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "OmniPOS";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.panelSidebar.ResumeLayout(false);
            this.panelLogo.ResumeLayout(false);
            this.panelLogo.PerformLayout();
            this.panelFooter.ResumeLayout(false);
            this.panelUtama.ResumeLayout(false);
            this.panelHeader.ResumeLayout(false);
            this.panelHeader.PerformLayout();
            this.ResumeLayout(false);
        }
    }
}
