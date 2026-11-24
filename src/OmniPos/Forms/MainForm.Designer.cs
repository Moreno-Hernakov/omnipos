namespace OmniPos.Forms
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel panelSidebar;
        private System.Windows.Forms.Panel panelLogo;
        private System.Windows.Forms.Panel panelLogoMark;
        private System.Windows.Forms.Label labelLogoMark;
        private System.Windows.Forms.Label labelLogo;
        private System.Windows.Forms.Label labelLogoSub;
        private System.Windows.Forms.FlowLayoutPanel panelMenu;
        private System.Windows.Forms.Panel panelFooter;
        private System.Windows.Forms.Panel panelGarisFooter;
        private System.Windows.Forms.Label labelVersi;
        private System.Windows.Forms.Panel panelUtama;
        private System.Windows.Forms.Panel panelHeader;
        private System.Windows.Forms.Label labelJudulHalaman;
        private System.Windows.Forms.Label labelJejak;
        private System.Windows.Forms.Panel panelAvatar;
        private System.Windows.Forms.Label labelInisial;
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
            this.panelMenu = new System.Windows.Forms.FlowLayoutPanel();
            this.panelFooter = new System.Windows.Forms.Panel();
            this.panelGarisFooter = new System.Windows.Forms.Panel();
            this.labelVersi = new System.Windows.Forms.Label();
            this.panelLogo = new System.Windows.Forms.Panel();
            this.panelLogoMark = new System.Windows.Forms.Panel();
            this.labelLogoMark = new System.Windows.Forms.Label();
            this.labelLogo = new System.Windows.Forms.Label();
            this.labelLogoSub = new System.Windows.Forms.Label();
            this.panelUtama = new System.Windows.Forms.Panel();
            this.panelKonten = new System.Windows.Forms.Panel();
            this.panelHeader = new System.Windows.Forms.Panel();
            this.labelJudulHalaman = new System.Windows.Forms.Label();
            this.labelJejak = new System.Windows.Forms.Label();
            this.panelAvatar = new System.Windows.Forms.Panel();
            this.labelInisial = new System.Windows.Forms.Label();
            this.labelPengguna = new System.Windows.Forms.Label();
            this.labelPeran = new System.Windows.Forms.Label();
            this.buttonLogout = new System.Windows.Forms.Button();
            this.panelGarisHeader = new System.Windows.Forms.Panel();
            this.panelSidebar.SuspendLayout();
            this.panelFooter.SuspendLayout();
            this.panelLogo.SuspendLayout();
            this.panelLogoMark.SuspendLayout();
            this.panelUtama.SuspendLayout();
            this.panelHeader.SuspendLayout();
            this.panelAvatar.SuspendLayout();
            this.SuspendLayout();
            // 
            // panelSidebar
            // 
            this.panelSidebar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(17)))), ((int)(((byte)(24)))), ((int)(((byte)(39)))));
            this.panelSidebar.Controls.Add(this.panelMenu);
            this.panelSidebar.Controls.Add(this.panelFooter);
            this.panelSidebar.Controls.Add(this.panelLogo);
            this.panelSidebar.Dock = System.Windows.Forms.DockStyle.Left;
            this.panelSidebar.Location = new System.Drawing.Point(0, 0);
            this.panelSidebar.Name = "panelSidebar";
            this.panelSidebar.Size = new System.Drawing.Size(248, 800);
            this.panelSidebar.TabIndex = 0;
            // 
            // panelMenu
            // 
            this.panelMenu.AutoScroll = true;
            this.panelMenu.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(17)))), ((int)(((byte)(24)))), ((int)(((byte)(39)))));
            this.panelMenu.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelMenu.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.panelMenu.Location = new System.Drawing.Point(0, 96);
            this.panelMenu.Name = "panelMenu";
            this.panelMenu.Padding = new System.Windows.Forms.Padding(12, 8, 12, 8);
            this.panelMenu.Size = new System.Drawing.Size(248, 652);
            this.panelMenu.TabIndex = 1;
            this.panelMenu.WrapContents = false;
            // 
            // panelFooter
            // 
            this.panelFooter.Controls.Add(this.panelGarisFooter);
            this.panelFooter.Controls.Add(this.labelVersi);
            this.panelFooter.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panelFooter.Location = new System.Drawing.Point(0, 748);
            this.panelFooter.Name = "panelFooter";
            this.panelFooter.Size = new System.Drawing.Size(248, 52);
            this.panelFooter.TabIndex = 2;
            // 
            // panelGarisFooter
            // 
            this.panelGarisFooter.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(31)))), ((int)(((byte)(41)))), ((int)(((byte)(55)))));
            this.panelGarisFooter.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelGarisFooter.Location = new System.Drawing.Point(0, 0);
            this.panelGarisFooter.Name = "panelGarisFooter";
            this.panelGarisFooter.Size = new System.Drawing.Size(248, 1);
            this.panelGarisFooter.TabIndex = 0;
            // 
            // labelVersi
            // 
            this.labelVersi.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelVersi.Font = new System.Drawing.Font("Segoe UI", 8.25F);
            this.labelVersi.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelVersi.Location = new System.Drawing.Point(0, 0);
            this.labelVersi.Name = "labelVersi";
            this.labelVersi.Size = new System.Drawing.Size(248, 52);
            this.labelVersi.TabIndex = 1;
            this.labelVersi.Text = "OmniPOS v1.0";
            this.labelVersi.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // panelLogo
            // 
            this.panelLogo.Controls.Add(this.panelLogoMark);
            this.panelLogo.Controls.Add(this.labelLogo);
            this.panelLogo.Controls.Add(this.labelLogoSub);
            this.panelLogo.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelLogo.Location = new System.Drawing.Point(0, 0);
            this.panelLogo.Name = "panelLogo";
            this.panelLogo.Size = new System.Drawing.Size(248, 96);
            this.panelLogo.TabIndex = 0;
            // 
            // panelLogoMark
            // 
            this.panelLogoMark.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(37)))), ((int)(((byte)(99)))), ((int)(((byte)(235)))));
            this.panelLogoMark.Controls.Add(this.labelLogoMark);
            this.panelLogoMark.Location = new System.Drawing.Point(20, 26);
            this.panelLogoMark.Name = "panelLogoMark";
            this.panelLogoMark.Size = new System.Drawing.Size(30, 30);
            this.panelLogoMark.TabIndex = 0;
            // 
            // labelLogoMark
            // 
            this.labelLogoMark.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelLogoMark.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold);
            this.labelLogoMark.ForeColor = System.Drawing.Color.White;
            this.labelLogoMark.Location = new System.Drawing.Point(0, 0);
            this.labelLogoMark.Name = "labelLogoMark";
            this.labelLogoMark.Size = new System.Drawing.Size(30, 30);
            this.labelLogoMark.TabIndex = 0;
            this.labelLogoMark.Text = "O";
            this.labelLogoMark.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelLogo
            // 
            this.labelLogo.Font = new System.Drawing.Font("Segoe UI", 15F, System.Drawing.FontStyle.Bold);
            this.labelLogo.ForeColor = System.Drawing.Color.White;
            this.labelLogo.Location = new System.Drawing.Point(60, 22);
            this.labelLogo.Name = "labelLogo";
            this.labelLogo.Size = new System.Drawing.Size(168, 26);
            this.labelLogo.TabIndex = 1;
            this.labelLogo.Text = "OmniPOS";
            // 
            // labelLogoSub
            // 
            this.labelLogoSub.AutoEllipsis = true;
            this.labelLogoSub.Font = new System.Drawing.Font("Segoe UI", 8.25F);
            this.labelLogoSub.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(148)))), ((int)(((byte)(163)))), ((int)(((byte)(184)))));
            this.labelLogoSub.Location = new System.Drawing.Point(61, 50);
            this.labelLogoSub.Name = "labelLogoSub";
            this.labelLogoSub.Size = new System.Drawing.Size(166, 17);
            this.labelLogoSub.TabIndex = 2;
            this.labelLogoSub.Text = "Point of Sale";
            // 
            // panelUtama
            // 
            this.panelUtama.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(241)))), ((int)(((byte)(245)))), ((int)(((byte)(249)))));
            this.panelUtama.Controls.Add(this.panelKonten);
            this.panelUtama.Controls.Add(this.panelHeader);
            this.panelUtama.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelUtama.Location = new System.Drawing.Point(248, 0);
            this.panelUtama.Name = "panelUtama";
            this.panelUtama.Size = new System.Drawing.Size(1032, 800);
            this.panelUtama.TabIndex = 1;
            // 
            // panelKonten
            // 
            this.panelKonten.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(241)))), ((int)(((byte)(245)))), ((int)(((byte)(249)))));
            this.panelKonten.Dock = System.Windows.Forms.DockStyle.Fill;
            this.panelKonten.Location = new System.Drawing.Point(0, 76);
            this.panelKonten.Name = "panelKonten";
            this.panelKonten.Padding = new System.Windows.Forms.Padding(28);
            this.panelKonten.Size = new System.Drawing.Size(1032, 724);
            this.panelKonten.TabIndex = 1;
            this.panelKonten.Paint += new System.Windows.Forms.PaintEventHandler(this.panelKonten_Paint);
            // 
            // panelHeader
            // 
            this.panelHeader.BackColor = System.Drawing.Color.White;
            this.panelHeader.Controls.Add(this.labelJudulHalaman);
            this.panelHeader.Controls.Add(this.labelJejak);
            this.panelHeader.Controls.Add(this.panelAvatar);
            this.panelHeader.Controls.Add(this.labelPengguna);
            this.panelHeader.Controls.Add(this.labelPeran);
            this.panelHeader.Controls.Add(this.buttonLogout);
            this.panelHeader.Controls.Add(this.panelGarisHeader);
            this.panelHeader.Dock = System.Windows.Forms.DockStyle.Top;
            this.panelHeader.Location = new System.Drawing.Point(0, 0);
            this.panelHeader.Name = "panelHeader";
            this.panelHeader.Size = new System.Drawing.Size(1032, 76);
            this.panelHeader.TabIndex = 0;
            // 
            // labelJudulHalaman
            // 
            this.labelJudulHalaman.AutoEllipsis = true;
            this.labelJudulHalaman.Font = new System.Drawing.Font("Segoe UI", 13.5F, System.Drawing.FontStyle.Bold);
            this.labelJudulHalaman.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelJudulHalaman.Location = new System.Drawing.Point(28, 14);
            this.labelJudulHalaman.Name = "labelJudulHalaman";
            this.labelJudulHalaman.Size = new System.Drawing.Size(360, 26);
            this.labelJudulHalaman.TabIndex = 0;
            this.labelJudulHalaman.Text = "Beranda";
            // 
            // labelJejak
            // 
            this.labelJejak.AutoEllipsis = true;
            this.labelJejak.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelJejak.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelJejak.Location = new System.Drawing.Point(30, 43);
            this.labelJejak.Name = "labelJejak";
            this.labelJejak.Size = new System.Drawing.Size(360, 18);
            this.labelJejak.TabIndex = 1;
            this.labelJejak.Text = "Nama Toko / Cabang";
            // 
            // panelAvatar
            // 
            this.panelAvatar.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.panelAvatar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(37)))), ((int)(((byte)(99)))), ((int)(((byte)(235)))));
            this.panelAvatar.Controls.Add(this.labelInisial);
            this.panelAvatar.Location = new System.Drawing.Point(824, 20);
            this.panelAvatar.Name = "panelAvatar";
            this.panelAvatar.Size = new System.Drawing.Size(36, 36);
            this.panelAvatar.TabIndex = 2;
            // 
            // labelInisial
            // 
            this.labelInisial.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelInisial.Font = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Bold);
            this.labelInisial.ForeColor = System.Drawing.Color.White;
            this.labelInisial.Location = new System.Drawing.Point(0, 0);
            this.labelInisial.Name = "labelInisial";
            this.labelInisial.Size = new System.Drawing.Size(36, 36);
            this.labelInisial.TabIndex = 0;
            this.labelInisial.Text = "SA";
            this.labelInisial.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelPengguna
            // 
            this.labelPengguna.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.labelPengguna.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold);
            this.labelPengguna.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelPengguna.Location = new System.Drawing.Point(580, 16);
            this.labelPengguna.Name = "labelPengguna";
            this.labelPengguna.Size = new System.Drawing.Size(228, 20);
            this.labelPengguna.TabIndex = 3;
            this.labelPengguna.Text = "Nama Pengguna";
            this.labelPengguna.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // labelPeran
            // 
            this.labelPeran.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.labelPeran.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelPeran.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelPeran.Location = new System.Drawing.Point(580, 40);
            this.labelPeran.Name = "labelPeran";
            this.labelPeran.Size = new System.Drawing.Size(228, 18);
            this.labelPeran.TabIndex = 4;
            this.labelPeran.Text = "Peran";
            this.labelPeran.TextAlign = System.Drawing.ContentAlignment.MiddleRight;
            // 
            // buttonLogout
            // 
            this.buttonLogout.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.buttonLogout.BackColor = System.Drawing.Color.White;
            this.buttonLogout.Cursor = System.Windows.Forms.Cursors.Hand;
            this.buttonLogout.FlatAppearance.BorderColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(232)))), ((int)(((byte)(240)))));
            this.buttonLogout.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(241)))), ((int)(((byte)(245)))), ((int)(((byte)(249)))));
            this.buttonLogout.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonLogout.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.buttonLogout.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(51)))), ((int)(((byte)(65)))), ((int)(((byte)(85)))));
            this.buttonLogout.Location = new System.Drawing.Point(892, 22);
            this.buttonLogout.Name = "buttonLogout";
            this.buttonLogout.Size = new System.Drawing.Size(112, 32);
            this.buttonLogout.TabIndex = 5;
            this.buttonLogout.Text = "Keluar";
            this.buttonLogout.UseVisualStyleBackColor = false;
            this.buttonLogout.Click += new System.EventHandler(this.buttonLogout_Click);
            // 
            // panelGarisHeader
            // 
            this.panelGarisHeader.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(232)))), ((int)(((byte)(240)))));
            this.panelGarisHeader.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.panelGarisHeader.Location = new System.Drawing.Point(0, 75);
            this.panelGarisHeader.Name = "panelGarisHeader";
            this.panelGarisHeader.Size = new System.Drawing.Size(1032, 1);
            this.panelGarisHeader.TabIndex = 6;
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(248)))), ((int)(((byte)(250)))), ((int)(((byte)(252)))));
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
            this.panelFooter.ResumeLayout(false);
            this.panelLogo.ResumeLayout(false);
            this.panelLogoMark.ResumeLayout(false);
            this.panelUtama.ResumeLayout(false);
            this.panelHeader.ResumeLayout(false);
            this.panelAvatar.ResumeLayout(false);
            this.ResumeLayout(false);

        }
    }
}
