namespace OmniPos.Forms
{
    partial class LoginForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel panelLogoMark;
        private System.Windows.Forms.Label labelLogoMark;
        private System.Windows.Forms.Label labelJudul;
        private System.Windows.Forms.Label labelSubjudul;
        private System.Windows.Forms.Panel panelGaris;
        private System.Windows.Forms.Label labelUsername;
        private System.Windows.Forms.TextBox textBoxUsername;
        private System.Windows.Forms.Label labelPassword;
        private System.Windows.Forms.TextBox textBoxPassword;
        private System.Windows.Forms.Button buttonLogin;
        private System.Windows.Forms.Label labelPesan;
        private System.Windows.Forms.Label labelFooter;

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
            this.panelLogoMark = new System.Windows.Forms.Panel();
            this.labelLogoMark = new System.Windows.Forms.Label();
            this.labelJudul = new System.Windows.Forms.Label();
            this.labelSubjudul = new System.Windows.Forms.Label();
            this.panelGaris = new System.Windows.Forms.Panel();
            this.labelUsername = new System.Windows.Forms.Label();
            this.textBoxUsername = new System.Windows.Forms.TextBox();
            this.labelPassword = new System.Windows.Forms.Label();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.buttonLogin = new System.Windows.Forms.Button();
            this.labelPesan = new System.Windows.Forms.Label();
            this.labelFooter = new System.Windows.Forms.Label();
            this.panelLogoMark.SuspendLayout();
            this.SuspendLayout();
            // 
            // panelLogoMark
            // 
            this.panelLogoMark.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(37)))), ((int)(((byte)(99)))), ((int)(((byte)(235)))));
            this.panelLogoMark.Controls.Add(this.labelLogoMark);
            this.panelLogoMark.Location = new System.Drawing.Point(36, 34);
            this.panelLogoMark.Name = "panelLogoMark";
            this.panelLogoMark.Size = new System.Drawing.Size(34, 34);
            this.panelLogoMark.TabIndex = 0;
            // 
            // labelLogoMark
            // 
            this.labelLogoMark.Dock = System.Windows.Forms.DockStyle.Fill;
            this.labelLogoMark.Font = new System.Drawing.Font("Segoe UI", 12F, System.Drawing.FontStyle.Bold);
            this.labelLogoMark.ForeColor = System.Drawing.Color.White;
            this.labelLogoMark.Location = new System.Drawing.Point(0, 0);
            this.labelLogoMark.Name = "labelLogoMark";
            this.labelLogoMark.Size = new System.Drawing.Size(34, 34);
            this.labelLogoMark.TabIndex = 0;
            this.labelLogoMark.Text = "O";
            this.labelLogoMark.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // labelJudul
            // 
            this.labelJudul.AutoSize = true;
            this.labelJudul.Font = new System.Drawing.Font("Segoe UI", 16F, System.Drawing.FontStyle.Bold);
            this.labelJudul.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelJudul.Location = new System.Drawing.Point(82, 32);
            this.labelJudul.Name = "labelJudul";
            this.labelJudul.Size = new System.Drawing.Size(112, 30);
            this.labelJudul.TabIndex = 1;
            this.labelJudul.Text = "OmniPOS";
            // 
            // labelSubjudul
            // 
            this.labelSubjudul.AutoSize = true;
            this.labelSubjudul.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelSubjudul.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(100)))), ((int)(((byte)(116)))), ((int)(((byte)(139)))));
            this.labelSubjudul.Location = new System.Drawing.Point(84, 62);
            this.labelSubjudul.Name = "labelSubjudul";
            this.labelSubjudul.Size = new System.Drawing.Size(171, 15);
            this.labelSubjudul.TabIndex = 2;
            this.labelSubjudul.Text = "Masuk dengan akun pengguna";
            // 
            // panelGaris
            // 
            this.panelGaris.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(226)))), ((int)(((byte)(232)))), ((int)(((byte)(240)))));
            this.panelGaris.Location = new System.Drawing.Point(36, 102);
            this.panelGaris.Name = "panelGaris";
            this.panelGaris.Size = new System.Drawing.Size(368, 1);
            this.panelGaris.TabIndex = 3;
            // 
            // labelUsername
            // 
            this.labelUsername.AutoSize = true;
            this.labelUsername.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelUsername.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelUsername.Location = new System.Drawing.Point(36, 126);
            this.labelUsername.Name = "labelUsername";
            this.labelUsername.Size = new System.Drawing.Size(60, 15);
            this.labelUsername.TabIndex = 4;
            this.labelUsername.Text = "Username";
            // 
            // textBoxUsername
            // 
            this.textBoxUsername.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxUsername.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.textBoxUsername.Location = new System.Drawing.Point(38, 146);
            this.textBoxUsername.Name = "textBoxUsername";
            this.textBoxUsername.Size = new System.Drawing.Size(362, 25);
            this.textBoxUsername.TabIndex = 5;
            // 
            // labelPassword
            // 
            this.labelPassword.AutoSize = true;
            this.labelPassword.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.labelPassword.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(30)))), ((int)(((byte)(41)))), ((int)(((byte)(59)))));
            this.labelPassword.Location = new System.Drawing.Point(36, 190);
            this.labelPassword.Name = "labelPassword";
            this.labelPassword.Size = new System.Drawing.Size(57, 15);
            this.labelPassword.TabIndex = 6;
            this.labelPassword.Text = "Password";
            // 
            // textBoxPassword
            // 
            this.textBoxPassword.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.textBoxPassword.Font = new System.Drawing.Font("Segoe UI", 10F);
            this.textBoxPassword.Location = new System.Drawing.Point(38, 210);
            this.textBoxPassword.Name = "textBoxPassword";
            this.textBoxPassword.Size = new System.Drawing.Size(362, 25);
            this.textBoxPassword.TabIndex = 7;
            this.textBoxPassword.UseSystemPasswordChar = true;
            // 
            // buttonLogin
            // 
            this.buttonLogin.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(37)))), ((int)(((byte)(99)))), ((int)(((byte)(235)))));
            this.buttonLogin.Cursor = System.Windows.Forms.Cursors.Hand;
            this.buttonLogin.FlatAppearance.BorderSize = 0;
            this.buttonLogin.FlatAppearance.MouseOverBackColor = System.Drawing.Color.FromArgb(((int)(((byte)(29)))), ((int)(((byte)(78)))), ((int)(((byte)(216)))));
            this.buttonLogin.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.buttonLogin.Font = new System.Drawing.Font("Segoe UI", 9.5F, System.Drawing.FontStyle.Bold);
            this.buttonLogin.ForeColor = System.Drawing.Color.White;
            this.buttonLogin.Location = new System.Drawing.Point(38, 258);
            this.buttonLogin.Name = "buttonLogin";
            this.buttonLogin.Size = new System.Drawing.Size(362, 40);
            this.buttonLogin.TabIndex = 8;
            this.buttonLogin.Text = "Masuk";
            this.buttonLogin.UseVisualStyleBackColor = false;
            this.buttonLogin.Click += new System.EventHandler(this.buttonLogin_Click);
            // 
            // labelPesan
            // 
            this.labelPesan.Font = new System.Drawing.Font("Segoe UI", 8.5F);
            this.labelPesan.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(185)))), ((int)(((byte)(28)))), ((int)(((byte)(28)))));
            this.labelPesan.Location = new System.Drawing.Point(38, 308);
            this.labelPesan.Name = "labelPesan";
            this.labelPesan.Size = new System.Drawing.Size(362, 40);
            this.labelPesan.TabIndex = 9;
            // 
            // labelFooter
            // 
            this.labelFooter.Font = new System.Drawing.Font("Segoe UI", 8.25F);
            this.labelFooter.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(148)))), ((int)(((byte)(163)))), ((int)(((byte)(184)))));
            this.labelFooter.Location = new System.Drawing.Point(38, 382);
            this.labelFooter.Name = "labelFooter";
            this.labelFooter.Size = new System.Drawing.Size(362, 18);
            this.labelFooter.TabIndex = 10;
            this.labelFooter.Text = "OmniPOS v1.0";
            this.labelFooter.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // LoginForm
            // 
            this.AcceptButton = this.buttonLogin;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.ClientSize = new System.Drawing.Size(440, 424);
            this.Controls.Add(this.labelFooter);
            this.Controls.Add(this.labelPesan);
            this.Controls.Add(this.buttonLogin);
            this.Controls.Add(this.textBoxPassword);
            this.Controls.Add(this.labelPassword);
            this.Controls.Add(this.textBoxUsername);
            this.Controls.Add(this.labelUsername);
            this.Controls.Add(this.panelGaris);
            this.Controls.Add(this.labelSubjudul);
            this.Controls.Add(this.labelJudul);
            this.Controls.Add(this.panelLogoMark);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "LoginForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "OmniPOS - Login";
            this.Load += new System.EventHandler(this.LoginForm_Load);
            this.panelLogoMark.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }
    }
}
