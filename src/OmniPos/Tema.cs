using System.Drawing;

namespace OmniPos
{
    // Token visual shell: satu sumber warna dan font untuk kontrol yang dibuat dari kode.
    public static class Tema
    {
        public static readonly Color Primer = Color.FromArgb(37, 99, 235);
        public static readonly Color PrimerGelap = Color.FromArgb(29, 78, 216);

        public static readonly Color LatarKonten = Color.FromArgb(241, 245, 249);
        public static readonly Color TeksLembut = Color.FromArgb(100, 116, 139);

        public static readonly Color Sidebar = Color.FromArgb(17, 24, 39);
        public static readonly Color SidebarHover = Color.FromArgb(31, 41, 55);
        public static readonly Color SidebarTeks = Color.FromArgb(209, 213, 219);
        public static readonly Color SidebarMuted = Color.FromArgb(148, 163, 184);

        public static readonly Color InfoLatar = Color.FromArgb(239, 246, 255);
        public static readonly Color InfoTeks = Color.FromArgb(29, 78, 216);
        public static readonly Color PeringatanLatar = Color.FromArgb(255, 247, 237);
        public static readonly Color PeringatanTeks = Color.FromArgb(194, 65, 12);
        public static readonly Color SuksesLatar = Color.FromArgb(236, 253, 245);
        public static readonly Color SuksesTeks = Color.FromArgb(4, 120, 87);

        public static readonly Font FontMenu = new Font("Segoe UI", 9.5F);
        public static readonly Font FontGrup = new Font("Segoe UI", 8F, FontStyle.Bold);
        public static readonly Font FontChip = new Font("Segoe UI", 8.5F, FontStyle.Bold);
    }
}
