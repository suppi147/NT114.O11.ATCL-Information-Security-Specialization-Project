using System;
using System.Collections.Generic;
using System.IO;
using System.Windows.Forms;
using OtpNet;
using Newtonsoft.Json;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace totp2
{
    public partial class Form1 : Form
    {
        private List<UserData> users;
        private Timer timer;
        public Form1()
        {
            InitializeComponent();
            this.users = LoadUsers();
            UpdateUserList();
            this.listBox1.MouseClick += ListBoxUsers_MouseClick;
            this.timer = new Timer();
            this.timer.Interval = 1000; 
            this.timer.Tick += Timer_Tick;
            this.timer.Start();
        }
        private void Timer_Tick(object sender, EventArgs e)
        {
            UpdateUserList();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            string username = texta.Text;
            string service = textb.Text;
            string key = textc.Text;

            if (key.Length < 16 || key.Length > 32) 
            {
                MessageBox.Show("Key không đúng định dạng");
                return;
            }

            var user = new UserData { Username = username, Service = service, SecretKey = key };
            this.users.Add(user);
            SaveUsers(this.users);

            UpdateUserList();
        }
        private void ListBoxUsers_MouseClick(object sender, MouseEventArgs e)
        {
            int index = this.listBox1.IndexFromPoint(e.Location);
            if (index != ListBox.NoMatches)
            {
                UserData selectedUser = this.users[index];
                Clipboard.SetText(selectedUser.TotpCode);
                MessageBox.Show("TOTP code copied to clipboard!");
            }
        }

        private void UpdateUserList()
        {
            this.listBox1.Items.Clear();
            foreach (var user in this.users)
            {
                var totp = new Totp(Base32Encoding.ToBytes(user.SecretKey));
                user.TotpCode = totp.ComputeTotp();
                this.listBox1.Items.Add($"{user.Username} ({user.Service}): {user.TotpCode}");
            }
        }
        private List<UserData> LoadUsers()
        {
            try
            {
                string json = File.ReadAllText("users.json");
                return JsonConvert.DeserializeObject<List<UserData>>(json);
            }
            catch
            {
                return new List<UserData>();
            }
        }


        private void SaveUsers(List<UserData> users)
        {
            string json = JsonConvert.SerializeObject(users);
            File.WriteAllText("users.json", json);
        }

        private void texta_TextChanged(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }
    }
    public class UserData
    {
        public string Username { get; set; }
        public string Service { get; set; }
        public string SecretKey { get; set; }
        public string TotpCode { get; set; }
    }
}
