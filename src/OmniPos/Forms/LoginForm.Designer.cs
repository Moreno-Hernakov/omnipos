namespace OmniPos.Forms
{
    partial class LoginForm
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Label labelJudul;
        private System.Windows.Forms.Label labelSubjudul;
        private System.Windows.Forms.Label labelUsername;
        private System.Windows.Forms.TextBox textBoxUsername;
        private System.Windows.Forms.Label labelPassword;
        private System.Windows.Forms.TextBox textBoxPassword;
        private System.Windows.Forms.Button buttonLogin;
        private System.Windows.Forms.Label labelPesan;

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
            this.labelSubjudul = new System.Windows.Forms.Label();
            this.labelUsername = new System.Windows.Forms.Label();
            this.textBoxUsername = new System.Windows.Forms.TextBox();
            this.labelPassword = new System.Windows.Forms.Label();
            this.textBoxPassword = new System.Windows.Forms.TextBox();
            this.buttonLogin = new System.Windows.Forms.Button();
            this.labelPesan = new System.Windows.Forms.Label();
            this.SuspendLayout();
            //
            // labelJudul
            //
            this.labelJudul.AutoSize = true;
            this.labelJudul.Font = new System.Drawing.Font("Segoe UI", 16F, System.Drawing.FontStyle.Bold);
            this.labelJudul.Location = new System.Drawing.Point(28, 24);
            this.labelJudul.Name = "labelJudul";
            this.labelJudul.Size = new System.Drawing.Size(104, 30);
            this.labelJudul.TabIndex = 0;
            this.labelJudul.Text = "OmniPOS";
            //
            // labelSubjudul
            //
            this.labelSubjudul.AutoSize = true;
            this.labelSubjudul.ForeColor = System.Drawing.Color.DimGray;
            this.labelSubjudul.Location = new System.Drawing.Point(31, 58);
            this.labelSubjudul.Name = "labelSubjudul";
            this.labelSubjudul.Size = new System.Drawing.Size(163, 15);
            this.labelSubjudul.TabIndex = 1;
            this.labelSubjudul.Text = "Masuk dengan akun pengguna";
            //
            // labelUsername
            //
            this.labelUsername.AutoSize = true;
            this.labelUsername.Location = new System.Drawing.Point(31, 96);
            this.labelUsername.Name = "labelUsername";
            this.labelUsername.Size = new System.Drawing.Size(63, 15);
            this.labelUsername.TabIndex = 2;
            this.labelUsername.Text = "Username";
            //
            // textBoxUsername
            //
            this.textBoxUsername.Location = new System.Drawing.Point(34, 114);
            this.textBoxUsername.Name = "textBoxUsername";
            this.textBoxUsername.Size = new System.Drawing.Size(320, 23);
            this.textBoxUsername.TabIndex = 3;
            //
            // labelPassword
            //
            this.labelPassword.AutoSize = true;
            this.labelPassword.Location = new System.Drawing.Point(31, 148);
            this.labelPassword.Name = "labelPassword";
            this.labelPassword.Size = new System.Drawing.Size(60, 15);
            this.labelPassword.TabIndex = 4;
            this.labelPassword.Text = "Password";
            //
            // textBoxPassword
            //
            this.textBoxPassword.Location = new System.Drawing.Point(34, 166);
            this.textBoxPassword.Name = "textBoxPassword";
            this.textBoxPassword.Size = new System.Drawing.Size(320, 23);
            this.textBoxPassword.TabIndex = 5;
            this.textBoxPassword.UseSystemPasswordChar = true;
            //
            // buttonLogin
            //
            this.buttonLogin.Location = new System.Drawing.Point(34, 210);
            this.buttonLogin.Name = "buttonLogin";
            this.buttonLogin.Size = new System.Drawing.Size(320, 34);
            this.buttonLogin.TabIndex = 6;
            this.buttonLogin.Text = "Login";
            this.buttonLogin.UseVisualStyleBackColor = true;
            this.buttonLogin.Click += new System.EventHandler(this.buttonLogin_Click);
            //
            // labelPesan
            //
            this.labelPesan.ForeColor = System.Drawing.Color.Firebrick;
            this.labelPesan.Location = new System.Drawing.Point(31, 252);
            this.labelPesan.Name = "labelPesan";
            this.labelPesan.Size = new System.Drawing.Size(323, 36);
            this.labelPesan.TabIndex = 7;
            //
            // LoginForm
            //
            this.AcceptButton = this.buttonLogin;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(394, 301);
            this.Controls.Add(this.labelPesan);
            this.Controls.Add(this.buttonLogin);
            this.Controls.Add(this.textBoxPassword);
            this.Controls.Add(this.labelPassword);
            this.Controls.Add(this.textBoxUsername);
            this.Controls.Add(this.labelUsername);
            this.Controls.Add(this.labelSubjudul);
            this.Controls.Add(this.labelJudul);
            this.Font = new System.Drawing.Font("Segoe UI", 9F);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "LoginForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "OmniPOS - Login";
            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}
