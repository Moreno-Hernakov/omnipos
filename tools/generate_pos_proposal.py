import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCX_OUT = os.path.join(BASE_DIR, "docs", "PROPOSAL POS.docx")
MD_OUT = os.path.join(BASE_DIR, "docs", "PROPOSAL_POS.md")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "image1.png")
if not os.path.exists(LOGO_PATH):
    LOGO_PATH = os.path.join(BASE_DIR, "..", "UAS", "image1.png")

# Glosarium istilah asing yang wajib dicetak miring (PUEBI/EYD V & docx-anti-slop B4)
GLOSSARY_TERMS = [
    "Point of Sales",
    "point of sales",
    "Configurable POS Engine",
    "Onboarding Wizard",
    "onboarding wizard",
    "Bill of Materials",
    "bill of materials",
    "Single-Shell",
    "single-shell",
    "Presentation Layer",
    "Business Logic Layer",
    "Data Access Layer",
    "Service Layer",
    "Repository Layer",
    "Role-Based Access Control",
    "Parameterized Query",
    "parameterized query",
    "SQL Injection",
    "Primary Key",
    "Foreign Key",
    "UserControl",
    "DataGridView",
    "feature flags",
    "feature toggle",
    "petty cash",
    "stock opname",
    "blind close",
    "Hold Bill",
    "hold bill",
    "Paid",
    "Hold",
    "Void",
    "void",
    "Rollback",
    "Commit",
    "hashing",
    "hash",
    "Timer",
    "barcode",
    "Barcode",
    "cash and carry",
    "dine-in",
    "takeaway",
    "multi-branch",
    "multi-sector",
    "dashboard",
    "dropdown",
    "login",
    "Login",
    "badge",
    "surplus",
    "shortage",
    "toggle",
]

_SORTED_TERMS = sorted(GLOSSARY_TERMS, key=len, reverse=True)
_GLOSSARY_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(t) for t in _SORTED_TERMS) + r")(?![A-Za-z0-9_])"
)


def add_formatted_runs(p, text, font_size=Pt(12), bold=False, color=None, italic_glossary=True):
    """Menambahkan teks ke paragraf dengan memiringkan istilah asing di glosarium (B4)."""
    if not italic_glossary:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = font_size
        r.font.bold = bold
        if color:
            r.font.color.rgb = color
        return

    pos = 0
    for m in _GLOSSARY_PATTERN.finditer(text):
        if m.start() > pos:
            r_plain = p.add_run(text[pos:m.start()])
            r_plain.font.name = "Times New Roman"
            r_plain.font.size = font_size
            r_plain.font.bold = bold
            if color:
                r_plain.font.color.rgb = color
        r_ital = p.add_run(m.group(0))
        r_ital.font.name = "Times New Roman"
        r_ital.font.size = font_size
        r_ital.font.bold = bold
        r_ital.font.italic = True
        if color:
            r_ital.font.color.rgb = color
        pos = m.end()

    if pos < len(text):
        r_tail = p.add_run(text[pos:])
        r_tail.font.name = "Times New Roman"
        r_tail.font.size = font_size
        r_tail.font.bold = bold
        if color:
            r_tail.font.color.rgb = color


def set_cell_background(cell, hex_color):
    """Mengatur warna latar belakang sel tabel."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=110, bottom=110, left=130, right=130):
    """Mengatur padding internal sel tabel."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_cell_borders(cell, color="CCCCCC", sz="4", val="single"):
    """Mengatur garis batas sel tabel yang rapi dan halus."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def style_table(table, col_widths, header_bg="202020", alt_bg="F7F7F7", border_color="D0D0D0"):
    """
    Format tabel akademis standar:
    - Header: Charcoal pekat (#202020) dengan teks putih tebal (Bukan biru AI).
    - Baris selang-seling: Abu-abu hangat muda (#F7F7F7) dan putih murni (#FFFFFF).
    - Garis pembatas: Abu-abu halus (#D0D0D0).
    - CantSplit dan TblHeader terpasang untuk mencegah tabel terpotong jelek.
    """
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        is_header = (i == 0)
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for j, cell in enumerate(row.cells):
            if j < len(col_widths):
                cell.width = col_widths[j]
            set_cell_margins(cell, top=110, bottom=110, left=130, right=130)
            set_cell_borders(cell, color=border_color, sz="4")

            if is_header:
                set_cell_background(cell, header_bg)
                for p in cell.paragraphs:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(255, 255, 255)
            else:
                if i % 2 == 1:
                    set_cell_background(cell, "FFFFFF")
                else:
                    set_cell_background(cell, alt_bg)
                for p in cell.paragraphs:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(30, 30, 30)


def set_style_language_id(doc):
    """Atur bahasa dokumen ke id-ID dan aktifkan widowControl (docx-anti-slop B3)."""
    normal_rPr = doc.styles['Normal'].element.get_or_add_rPr()
    lang = parse_xml(f'<w:lang {nsdecls("w")} w:val="id-ID" w:eastAsia="id-ID" w:bidi="ar-SA"/>')
    normal_rPr.append(lang)


def build_proposal():
    doc = docx.Document()

    # Core Properties (docx-anti-slop B3)
    doc.core_properties.title = (
        "Proposal Proyek Akhir: Omni-Industry Configurable POS Engine: "
        "Sistem Point of Sales Terpadu Multi-Sektor Berbasis Desktop C# Windows Forms dan MySQL"
    )
    doc.core_properties.author = "Tim Omni-POS (S1 Informatika ISTTS)"
    doc.core_properties.subject = "Proposal Proyek Akhir Pemrograman Visual Semester 3"
    doc.core_properties.language = "id-ID"

    # Page Setup (A4 standard: 8.27 x 11.69 inches / 21.0 x 29.7 cm)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.18)      # 3.0 cm
    section.bottom_margin = Inches(1.18)   # 3.0 cm
    section.left_margin = Inches(1.38)     # 3.5 cm (standar jilid kiri)
    section.right_margin = Inches(1.18)    # 3.0 cm
    section.different_first_page_header_footer = True

    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.widow_control = True
    set_style_language_id(doc)

    # ==========================================
    # COVER PAGE
    # ==========================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(32)
    p_title.paragraph_format.line_spacing = 1.15
    r_title = p_title.add_run(
        "OMNI-INDUSTRY CONFIGURABLE POS ENGINE: SISTEM POINT OF SALES TERPADU "
        "MULTI-SEKTOR BERBASIS DESKTOP C# WINDOWS FORMS DAN BASIS DATA MYSQL"
    )
    r_title.font.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = RGBColor(17, 17, 17) # Hitam pekat akademis

    # Logo ISTTS
    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(32)
        r_logo = p_logo.add_run()
        r_logo.add_picture(LOGO_PATH, width=Inches(2.1))

    # Keterangan Pengajuan
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("PROPOSAL PROYEK AKHIR\nMATA KULIAH PEMROGRAMAN VISUAL (GASAL 2026/2027)")
    r_sub.font.bold = True
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.font.color.rgb = RGBColor(50, 50, 50)

    # Disusun oleh
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(8)
    r_by = p_by.add_run("Disusun oleh:")
    r_by.font.name = "Times New Roman"
    r_by.font.size = Pt(11)

    team_members = [
        ("BAGAS RIZKY PUTRA WARDANA", "225310690"),
        ("FX THIARNIKA EKA ATUR RANGGA", "225310691"),
        ("GREGORIUS PRIYAGUNG", "225310692"),
        ("MORENO HERNAKOV", "225310693"),
        ("RAYMOND SUGIHARTO", "225310694"),
        ("VALENCIA ANGIE KURNIAWAN", "225310695"),
    ]

    t_team_cover = doc.add_table(rows=len(team_members), cols=2)
    t_team_cover.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (nama, nim) in enumerate(team_members):
        row = t_team_cover.rows[idx]
        cell_nama = row.cells[0]
        cell_nim = row.cells[1]
        cell_nama.width = Inches(3.2)
        cell_nim.width = Inches(1.8)
        
        p_n = cell_nama.paragraphs[0]
        p_n.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_n.paragraph_format.space_after = Pt(2)
        r_n = p_n.add_run(nama)
        r_n.font.name = "Times New Roman"
        r_n.font.size = Pt(10.5)
        r_n.font.bold = True
        
        p_m = cell_nim.paragraphs[0]
        p_m.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_m.paragraph_format.space_after = Pt(2)
        r_m = p_m.add_run(f"NRP: {nim}")
        r_m.font.name = "Times New Roman"
        r_m.font.size = Pt(10.5)

    # Dosen Pengampu & Institusi
    p_dosen = doc.add_paragraph()
    p_dosen.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dosen.paragraph_format.space_before = Pt(28)
    p_dosen.paragraph_format.space_after = Pt(4)
    r_dosen_lbl = p_dosen.add_run("Dosen Pengampu:\n")
    r_dosen_lbl.font.name = "Times New Roman"
    r_dosen_lbl.font.size = Pt(11)
    r_dosen_name = p_dosen.add_run("Hansel Santoso, S.Kom., M.Kom.")
    r_dosen_name.font.name = "Times New Roman"
    r_dosen_name.font.size = Pt(12)
    r_dosen_name.font.bold = True

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(24)
    p_inst.paragraph_format.space_after = Pt(0)
    p_inst.paragraph_format.line_spacing = 1.15
    r_inst = p_inst.add_run(
        "PROGRAM STUDI S1 INFORMATIKA\n"
        "FAKULTAS TEKNOLOGI INFORMASI DAN INDUSTRI KREATIF\n"
        "INSTITUT SAINS DAN TEKNOLOGI TERPADU SURABAYA\n"
        "2026"
    )
    r_inst.font.bold = True
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(11.5)
    r_inst.font.color.rgb = RGBColor(17, 17, 17)

    # Page Break ke Halaman Pengesahan
    doc.add_page_break()

    # ==========================================
    # HALAMAN PENGESAHAN
    # ==========================================
    p_peng_title = doc.add_paragraph()
    p_peng_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_peng_title.paragraph_format.space_before = Pt(12)
    p_peng_title.paragraph_format.space_after = Pt(18)
    r_peng_title = p_peng_title.add_run("LEMBAR PENGESAHAN PROPOSAL PROYEK AKHIR")
    r_peng_title.font.bold = True
    r_peng_title.font.name = "Times New Roman"
    r_peng_title.font.size = Pt(13)
    r_peng_title.font.color.rgb = RGBColor(17, 17, 17)

    p_peng_meta = doc.add_paragraph()
    p_peng_meta.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_peng_meta.paragraph_format.space_after = Pt(12)
    p_peng_meta.paragraph_format.line_spacing = 1.15
    add_formatted_runs(p_peng_meta, "Proposal Proyek Akhir ini telah diajukan dan disetujui untuk dilaksanakan sebagai bagian dari evaluasi Ujian Akhir Semester (UAS) mata kuliah Pemrograman Visual Semester Gasal 2026/2027 di Institut Sains dan Teknologi Terpadu Surabaya.")

    peng_data = [
        ("Judul Proyek", ": Omni-Industry Configurable POS Engine"),
        ("Mata Kuliah", ": Pemrograman Visual (Gasal 2026/2027)"),
        ("Program Studi", ": S1 Informatika"),
        ("Institusi", ": Institut Sains dan Teknologi Terpadu Surabaya"),
        ("Jumlah Anggota", ": 6 (Enam) Orang Mahasiswa"),
    ]
    t_peng = doc.add_table(rows=len(peng_data), cols=2)
    t_peng.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (k, v) in enumerate(peng_data):
        r_c = t_peng.rows[idx]
        r_c.cells[0].width = Inches(2.0)
        r_c.cells[1].width = Inches(4.5)
        p0 = r_c.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.name = "Times New Roman"
        r0.font.size = Pt(10.5)

        p1 = r_c.cells[1].paragraphs[0]
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(v)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(10.5)

    p_peng_ttd_intro = doc.add_paragraph()
    p_peng_ttd_intro.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_peng_ttd_intro.paragraph_format.space_before = Pt(30)
    p_peng_ttd_intro.paragraph_format.space_after = Pt(10)
    r_ttd_date = p_peng_ttd_intro.add_run("Surabaya, 14 November 2026")
    r_ttd_date.font.name = "Times New Roman"
    r_ttd_date.font.size = Pt(11)

    t_ttd = doc.add_table(rows=2, cols=1)
    t_ttd.alignment = WD_TABLE_ALIGNMENT.RIGHT
    t_ttd.rows[0].cells[0].width = Inches(3.2)

    p_ttd_kanan = t_ttd.rows[0].cells[0].paragraphs[0]
    p_ttd_kanan.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ttd_kanan.paragraph_format.space_after = Pt(60)
    r_kanan = p_ttd_kanan.add_run("Menyetujui,\nDosen Pengampu Pemrograman Visual")
    r_kanan.font.name = "Times New Roman"
    r_kanan.font.size = Pt(11)

    p_nama_kanan = t_ttd.rows[1].cells[0].paragraphs[0]
    p_nama_kanan.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_nama_kanan.paragraph_format.space_after = Pt(0)
    r_nka = p_nama_kanan.add_run("Hansel Santoso, S.Kom., M.Kom.")
    r_nka.font.bold = True
    r_nka.font.name = "Times New Roman"
    r_nka.font.size = Pt(11)

    # Page Break ke Daftar Isi
    doc.add_page_break()

    # ==========================================
    # DAFTAR ISI
    # ==========================================
    p_toc_title = doc.add_paragraph()
    p_toc_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_title.paragraph_format.space_before = Pt(12)
    p_toc_title.paragraph_format.space_after = Pt(20)
    r_toc_title = p_toc_title.add_run("DAFTAR ISI")
    r_toc_title.font.bold = True
    r_toc_title.font.name = "Times New Roman"
    r_toc_title.font.size = Pt(14)
    r_toc_title.font.color.rgb = RGBColor(17, 17, 17)

    toc_items = [
        ("LEMBAR PENGESAHAN PROPOSAL PROYEK AKHIR", "ii", True, 0),
        ("DAFTAR ISI", "iii", True, 0),
        ("BAB I PENDAHULUAN", "1", True, 0),
        ("1.1 Latar Belakang", "1", False, 1),
        ("1.2 Rumusan Masalah", "2", False, 1),
        ("1.3 Tujuan Proyek", "2", False, 1),
        ("1.4 Manfaat Proyek", "3", False, 1),
        ("1.5 Batasan Masalah", "3", False, 1),
        ("BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM", "4", True, 0),
        ("2.1 Konsep & Deskripsi Program", "4", False, 1),
        ("2.2 Onboarding Wizard & Manajemen Konfigurasi Toko", "5", False, 1),
        ("2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)", "6", False, 1),
        ("2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir", "7", False, 1),
        ("2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang", "9", False, 1),
        ("2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)", "10", False, 1),
        ("2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan", "11", False, 1),
        ("BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK", "13", True, 0),
        ("3.1 Alur Kerja & Arsitektur 3-Tier", "13", False, 1),
        ("3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell", "14", False, 1),
        ("3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)", "15", False, 1),
        ("3.4 Alur Logika Bisnis Kritis & Transaksi Atomik", "22", False, 1),
        ("BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM", "24", True, 0),
        ("4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim", "24", False, 1),
        ("4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu", "25", False, 1),
        ("4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)", "26", False, 1),
        ("BAB V PENUTUP", "27", True, 0),
        ("5.1 Kesimpulan", "27", False, 1),
        ("5.2 Harapan Capaian", "27", False, 1),
    ]

    t_toc = doc.add_table(rows=len(toc_items), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (judul, hal, is_bold, lvl) in enumerate(toc_items):
        r_row = t_toc.rows[idx]
        cell_j = r_row.cells[0]
        cell_h = r_row.cells[1]
        cell_j.width = Inches(5.8)
        cell_h.width = Inches(0.7)

        p_j = cell_j.paragraphs[0]
        p_j.paragraph_format.space_after = Pt(2)
        p_j.paragraph_format.left_indent = Inches(0.25 * lvl)
        r_j = p_j.add_run(judul)
        r_j.font.name = "Times New Roman"
        r_j.font.size = Pt(10.5 if lvl > 0 else 11)
        r_j.font.bold = is_bold

        p_h = cell_h.paragraphs[0]
        p_h.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_h.paragraph_format.space_after = Pt(2)
        r_h = p_h.add_run(hal)
        r_h.font.name = "Times New Roman"
        r_h.font.size = Pt(10.5 if lvl > 0 else 11)
        r_h.font.bold = is_bold

    # Page Break ke BAB I
    doc.add_page_break()

    # Helper untuk Menambahkan Heading & Paragraf Terstandar
    def add_heading_1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.widow_control = True
        add_formatted_runs(p, text, font_size=Pt(14), bold=True, color=RGBColor(17, 17, 17), italic_glossary=False)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.widow_control = True
        add_formatted_runs(p, text, font_size=Pt(12.5), bold=True, color=RGBColor(25, 25, 25))
        return p

    def add_heading_3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.widow_control = True
        add_formatted_runs(p, text, font_size=Pt(11.5), bold=True, color=RGBColor(35, 35, 35))
        return p

    def add_body_p(text, indent=True):
        """Menambahkan paragraf isi dengan indentasi baku 0.5 inci dan perataan justify."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.5)
        p.paragraph_format.widow_control = True
        add_formatted_runs(p, text, font_size=Pt(12), bold=False, color=RGBColor(20, 20, 20))
        return p

    def add_bullet_p(number_str, text):
        """Menambahkan poin bernomor tanpa spasi Shift+Enter (docx-anti-slop)."""
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.widow_control = True
        
        r_num = p.add_run(f"{number_str} ")
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(12)
        r_num.font.bold = True
        
        add_formatted_runs(p, text, font_size=Pt(12), bold=False, color=RGBColor(20, 20, 20))
        return p

    # ==========================================
    # BAB I PENDAHULUAN
    # ==========================================
    add_heading_1("BAB I PENDAHULUAN")

    add_heading_2("1.1 Latar Belakang")
    add_body_p(
        "Efisiensi operasional pada sektor perdagangan dan jasa mikro, kecil, dan menengah (UMKM) sangat ditentukan oleh keandalan sistem pencatatan transaksi kasir. Sebagian besar perangkat lunak Point of Sales (POS) yang beredar di pasaran memiliki desain monolitik dan kaku. Aplikasi ritel murni hanya mengelola transaksi barang jadi berbasis kode barcode, sedangkan aplikasi kuliner (Food and Beverage / F&B) mengunci fungsionalitasnya pada manajemen pesanan meja dan resep dapur tanpa fleksibilitas penyesuaian multi-cabang. Pelaku usaha yang mengoperasikan model bisnis campuran (hybrid), seperti minimarket yang memiliki stan kopi cepat saji atau bengkel motor yang menjual suku cadang fisik sekaligus jasa perbaikan, sering kali terpaksa menggunakan dua hingga tiga aplikasi kasir terpisah yang membingungkan kasir dan menyulitkan rekapitulasi pembukuan."
    )
    add_body_p(
        "Tantangan teknis utama pada sektor kuliner terletak pada pemotongan persediaan. Penjualan satu porsi minuman kopi tidak memotong persediaan kopi siap saji di etalase, melainkan mengonsumsi sejumlah takaran bahan baku mentah dapur seperti biji kopi sangrai, susu segar, dan sirup perisa. Ketiadaan formulasi Bill of Materials (BOM) pada sistem kasir standar menyebabkan stok bahan baku mentah tidak terdata secara akurat, sehingga selisih fisik dapur sering kali baru terdeteksi pada akhir bulan. Selain itu, kalkulasi Harga Pokok Penjualan (HPP) menjadi tidak akurat karena fluktuasi harga beli bahan baku dari pemasok tidak tercermin secara langsung pada margin laba kotor setiap transaksi."
    )
    add_body_p(
        "Kerentanan operasional kasir juga kerap terjadi pada proses pergantian jam kerja (shift) kasir. Ketiadaan pencatatan modal awal kas kecil (petty cash) dan verifikasi penerimaan uang tunai fisik secara independen membuka celah selisih pembukuan dan kecurangan internal. Di sisi lain, ekspansi usaha ke beberapa lokasi cabang membutuhkan sistem basis data terpusat yang mampu memetakan kepemilikan data per cabang dan mengelola alur mutasi transfer stok antar-cabang secara tertib tanpa menimbulkan kompleksitas arsitektur yang berlebihan bagi pengembang perangkat lunak."
    )
    add_body_p(
        "Untuk menjawab seluruh kebutuhan tersebut, dikembangkan proyek akhir bertajuk Omni-Industry Configurable POS Engine berbasis desktop C# Windows Forms dan basis data relasional MySQL via pustaka ADO.NET. Sistem ini memanfaatkan arsitektur 3-Tier yang memisahkan komponen antarmuka pengguna, logika bisnis, dan repositori basis data secara tegas. Fungsionalitas aplikasi diatur secara adaptif melalui panduan pengaturan awal (Onboarding Wizard) dan saklar fitur (feature flags), sehingga sistem kasir dapat bertransformasi menjadi sistem ritel murni, kasir restoran terintegrasi dapur, sistem jasa servis, atau gabungan ketiganya tanpa mengubah satu baris pun kode sumber aplikasi."
    )

    add_heading_2("1.2 Rumusan Masalah")
    add_body_p("Berdasarkan permasalahan operasional dan kebutuhan arsitektur perangkat lunak yang telah dipaparkan, rumusan masalah dalam penelitian dan pengembangan proyek ini dirumuskan sebagai berikut:", indent=False)
    add_bullet_p("1.", "Bagaimana merancang arsitektur perangkat lunak 3-Tier pada C# Windows Forms yang memisahkan antarmuka Single-Shell, logika bisnis layanan, dan akses repositori ADO.NET secara modular?")
    add_bullet_p("2.", "Bagaimana membangun mekanisme Onboarding Wizard berbasis saklar fitur (feature flags) di tabel konfigurasi untuk mengaktifkan atau menonaktifkan modul ritel, kuliner F&B, jasa, resep dapur, dan shift kasir secara dinamis?")
    add_bullet_p("3.", "Bagaimana mengimplementasikan mesin resep (Bill of Materials / BOM) yang mampu menghitung Harga Pokok Penjualan (HPP) menu secara otomatis serta memotong stok bahan baku mentah dapur secara proporsional?")
    add_bullet_p("4.", "Bagaimana menyusun mekanisme transaksi kasir dual-mode yang mendukung transaksi bayar langsung (cash and carry) maupun penangguhan tagihan (Hold Bill) untuk pesanan meja dan antrean pengerjaan jasa?")
    add_bullet_p("5.", "Bagaimana menjamin integritas data multi-tabel saat terjadi transaksi penjualan dan transfer stok antar-cabang menggunakan transaksi atomik basis data (MySqlTransaction)?")

    add_heading_2("1.3 Tujuan Proyek")
    add_body_p("Tujuan yang ingin dicapai melalui perancangan dan implementasi proyek akhir ini meliputi:", indent=False)
    add_bullet_p("1.", "Membangun aplikasi desktop Point of Sales modular menggunakan bahasa pemrograman C# pada kerangka kerja .NET Framework 4.7.2 dan basis data MySQL.")
    add_bullet_p("2.", "Menyediakan wizard konfigurasi bisnis awal yang memungkinkan Super Admin menyesuaikan identitas toko, persentase pajak, serta mode industri usaha tanpa rekayasa ulang basis data.")
    add_bullet_p("3.", "Mengintegrasikan modul bahan baku mentah dan relasi resep produk kuliner sehingga stok dapur berkurang secara otomatis dan margin laba kotor tercatat akurat.")
    add_bullet_p("4.", "Menerapkan sistem rekonsiliasi shift kasir dengan pencatatan modal awal dan pelaporan selisih kas fisik melalui metode blind close saat penutupan buku toko.")
    add_bullet_p("5.", "Merancang skema basis data relasional 12 tabel dengan partisi data cabang (branch_id) dan memvalidasi keutuhan transaksi melalui eksekusi parameterized query.")

    add_heading_2("1.4 Manfaat Proyek")
    add_body_p("Penerapan sistem Omni-Industry Configurable POS Engine memberikan manfaat nyata bagi berbagai pihak terkait:", indent=False)
    add_bullet_p("1.", "Bagi Pelaku Usaha UMKM: Memperoleh perangkat lunak kasir multifungsi yang fleksibel tanpa perlu membayar biaya langganan ganda untuk modul ritel, restoran, dan jasa servis terpisah.")
    add_bullet_p("2.", "Bagi Petugas Kasir dan Supervisor: Mempercepat proses pelayanan pembayaran pelanggan, mencegah kekeliruan perhitungan kembalian, serta mengamankan rekonsiliasi kas saat pergantian shift.")
    add_bullet_p("3.", "Bagi Tim Dapur dan Gudang: Memastikan ketersediaan stok bahan mentah terpantau secara berkala melalui peringatan stok menipis dan mempermudah pelacakan mutasi transfer barang antar-cabang.")
    add_bullet_p("4.", "Bagi Pengembangan Akademik: Menjadi percontohan implementasi rekayasa perangkat lunak desktop semester 3 yang taat pada kaidah pemisahan lapisan (separation of concerns), keamanan data parameterized query, dan transaksi atomik ACID.")

    add_heading_2("1.5 Batasan Masalah")
    add_body_p("Agar ruang lingkup perancangan sistem terarah dan sesuai dengan standar kurikulum mata kuliah Pemrograman Visual Semester 3, batasan masalah proyek ditetapkan sebagai berikut:", indent=False)
    add_bullet_p("1.", "Aplikasi dibangun sebagai perangkat lunak desktop Windows menggunakan bahasa C# pada lingkungan Microsoft Visual Studio 2022 dengan target .NET Framework 4.7.2.")
    add_bullet_p("2.", "Basis data menggunakan MySQL server lokal (XAMPP / MariaDB) yang diakses melalui pustaka ADO.NET murni (MySql.Data) dengan seluruh perintah SQL memanfaatkan parameterized query (@param) untuk mencegah celah SQL Injection.")
    add_bullet_p("3.", "Arsitektur multi-cabang dikelola melalui basis data relasional tunggal terpusat (single central database) dengan partisi kepemilikan rekaman data menggunakan kolom foreign key branch_id.")
    add_bullet_p("4.", "Pencetakan nota transaksi dan lembar rekapitulasi shift kasir disimulasikan melalui komponen PrintDocument Windows Forms dalam format teks struk termal standar lebar 58 mm dan 80 mm.")
    add_bullet_p("5.", "Sistem autentikasi menerapkan enkripsi searah (hashing) SHA-256 untuk seluruh kata sandi pengguna tanpa penyimpanan teks mentah di basis data.")

    # ==========================================
    # BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM
    # ==========================================
    add_heading_1("BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM")

    add_heading_2("2.1 Konsep & Deskripsi Program")
    add_body_p(
        "Omni-Industry Configurable POS Engine dirancang sebagai mesin kasir desktop cerdas yang mampu beradaptasi dengan model operasional berbagai sektor bisnis. Kata omni-industry merepresentasikan kemampuan adaptasi sistem dalam melayani tiga model operasional utama: ritel barang jadi (minimarket, butik, toko kelontong), operasional kuliner (kafe, kedai kopi, restoran cepat saji), serta penyedia jasa dan servis (bengkel, binatu/laundry, salon kecantikan). Karakteristik ketiga sektor tersebut dipadukan ke dalam satu mesin pemrosesan terintegrasi melalui mekanisme aktivasi saklar fitur."
    )
    add_body_p(
        "Kekuatan utama arsitektur ini terletak pada penghapusan redundansi sistem. Ketika pengguna memilih model bisnis ritel murni, antarmuka kasir hanya menampilkan input pemindai barcode, pencarian produk cepat, dan keranjang belanja kasir. Sebaliknya, saat model kuliner F&B diaktifkan, antarmuka menambahkan katalog visual berbasis kategori, opsi penandaan nomor meja pelanggan, dan pengiriman daftar pesanan ke dapur. Jika model jasa diaktifkan, kasir dapat mencatat nama teknisi atau penanggung jawab serta memantau status antrean pekerjaan tanpa memicu pemotongan stok barang fisik."
    )

    add_heading_2("2.2 Onboarding Wizard & Manajemen Konfigurasi Toko")
    add_body_p(
        "Saat aplikasi pertama kali dijalankan pasca instalasi basis data, sistem mendeteksi nilai parameter is_onboarded pada tabel app_config. Jika parameter bernilai 0, proses login Super Admin secara otomatis mengalihkan pengguna ke antarmuka Onboarding Wizard sebelum masuk ke jendela utama aplikasi. Wizard ini memandu pemilik usaha mengonfigurasi profil usaha dan memilih fitur fungsional yang dibutuhkan dalam empat tahapan terstruktur."
    )
    
    t_steps_data = [
        ("Tahap", "Nama Konfigurasi", "Parameter Basis Data", "Keterangan Operasional"),
        ("1", "Identitas Usaha", "business_name, business_address, business_phone", "Mencatat nama toko, alamat operasional, dan nomor telepon kontak yang akan dicetak pada kepala nota struk kasir."),
        ("2", "Pemilihan Sektor", "enable_retail, enable_fnb, enable_service", "Memilih jenis industri yang dijalankan toko untuk memfilter navigasi antarmuka dan jenis produk yang dapat diinput."),
        ("3", "Mesin & Operasional", "enable_recipe_bom, enable_shift, tax_percentage", "Mengaktifkan modul resep dapur, mewajibkan kasir membuka shift petty cash, serta menentukan tarif pajak transaksi (misal: 10,0%)."),
        ("4", "Cabang & Akun", "branches (HQ), users (Super Admin)", "Memverifikasi data cabang utama dan menetapkan kredensial administrator permanen sebelum flag is_onboarded diubah menjadi 1."),
    ]
    t_steps = doc.add_table(rows=len(t_steps_data), cols=4)
    for r_idx, r_val in enumerate(t_steps_data):
        for c_idx, c_val in enumerate(r_val):
            t_steps.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_steps, [Inches(0.6), Inches(1.7), Inches(2.1), Inches(2.4)])

    add_body_p(
        "Seluruh parameter yang tersimpan di tabel app_config bertindak sebagai feature flags global. Selama aplikasi berjalan, kelas penyedia layanan membaca konfigurasi ini untuk menentukan apakah tab navigasi resep dapur ditampilkan atau disembunyikan dari antarmuka kasir."
    )

    add_heading_2("2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)")
    add_body_p(
        "Katalog barang pada sistem dibagi menjadi tiga kelompok entitas yang terhubung: kategori produk (categories), master produk dan layanan (products), serta master bahan baku mentah dapur (raw_materials). Setiap produk memiliki penanda tipe bisnis (retail, fnb, atau service) yang menentukan perilaku pemotongan persediaan saat nota penjualan diterbitkan."
    )
    add_body_p(
        "Pada sektor kuliner F&B, produk olahan seperti Kopi Susu Gula Aren tidak memiliki stok fisik langsung di gudang barang jadi. Sebagai gantinya, produk tersebut dikaitkan dengan beberapa bahan baku mentah melalui tabel perantara product_recipes. Tabel ini menyimpan relasi banyak-ke-banyak antara produk dan bahan baku mentah lengkap dengan takaran pemakaian per porsi sajian (misalnya: 18,00 gram bubuk kopi, 120,00 ml susu segar cair, dan 25,00 ml sirup gula aren)."
    )
    add_body_p(
        "Mesin resep menjalankan algoritma kalkulasi Harga Pokok Penjualan (HPP) otomatis secara berkala. Setiap kali harga beli bahan mentah diperbarui pada master raw_materials, sistem menjumlahkan hasil kali antara takaran pemakaian resep dengan harga beli satuan terbaru untuk seluruh bahan penyusun menu tersebut. Nilai HPP terhitung kemudian disimpan ke dalam atribut hpp_manual pada tabel products, sehingga margin laba kotor per item menu dapat dihitung secara real-time tanpa memerlukan rekalkulasi manual oleh supervisor."
    )

    add_heading_2("2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir")
    add_body_p(
        "Modul transaksi kasir menyediakan antarmuka terpadu yang dirancang ergonomis bagi kecepatan kerja petugas kasir. Sistem mendukung dua mode penyelesaian transaksi penjualan yang dapat dipilih secara fleksibel sesuai situasi antrean toko:", indent=False
    )
    add_bullet_p("1.", "Mode Bayar Langsung (Paid): Diterapkan pada pola transaksi ritel cepat (cash and carry). Kasir memasukkan item belanja melalui pemindai barcode atau klik katalog, memilih metode pembayaran (tunai, transfer bank, atau QRIS), memasukkan nominal uang bayar pelanggan, dan sistem langsung menerbitkan struk nota pembayaran lunas.")
    add_bullet_p("2.", "Mode Simpan Tagihan (Hold Bill): Diterapkan pada pesanan makan di tempat (dine-in) restoran atau antrean unit pada layanan servis. Kasir mencatat pesanan belanja beserta label pengenal berupa nomor meja atau nomor polisi kendaraan. Transaksi disimpan ke basis data dengan status Hold. Saat pelanggan selesai bersantap atau servis rampung, kasir memanggil kembali nota gantung tersebut untuk menerima pembayaran dan mengubah status transaksi menjadi Paid.")

    add_body_p(
        "Untuk menjaga akuntabilitas keuangan tunai, sistem mewajibkan pengelolaan shift kasir. Saat memulai jam kerja, kasir harus membuka shift baru dengan memasukkan modal awal kas kecil (petty cash) yang diberikan bendahara. Sepanjang shift berlangsung, seluruh transaksi tunai yang berhasil dicatat oleh kasir akan diakumulasikan ke dalam variabel saldo sistem. Saat jam kerja berakhir, kasir melakukan proses penutupan buku kas (blind close). Kasir menghitung uang fisik yang ada di laci kasir dan menginput nominal tersebut ke dalam sistem tanpa melihat saldo rekapitulasi sistem terlebih dahulu."
    )
    add_body_p(
        "Sistem kemudian membandingkan uang fisik aktual dengan formula saldo akhir sistem: modal awal ditambah total transaksi tunai. Selisih yang terjadi dicatat secara otomatis ke dalam kolom selisih pada tabel shifts, baik bernilai 0 (cocok), bernilai positif (surplus), maupun bernilai negatif (shortage / defisit). Laporan penutupan shift dicetak sebagai bukti serah terima kasir kepada pengelola toko."
    )

    add_heading_2("2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang")
    add_body_p(
        "Manajemen persediaan membedakan penanganan antara stok barang jadi pada sektor ritel dan stok bahan baku mentah pada sektor kuliner F&B. Seluruh stok bahan baku mentah dipartisi per cabang pada tabel branch_materials, sehingga ketersediaan persediaan dapur di cabang utama tidak tercampur dengan ketersediaan di cabang pembantu."
    )
    add_body_p(
        "Sistem menyediakan tiga fungsi pengendalian persediaan utama:", indent=False
    )
    add_bullet_p("1.", "Restock (Barang Masuk): Mencatat penerimaan kiriman barang dari pemasok. Kuantitas stok produk atau bahan mentah di cabang terkait akan bertambah, disertai pembaruan harga beli satuan jika terjadi perubahan tarif pasokan.")
    add_bullet_p("2.", "Stock Opname (Penyesuaian Fisik): Formulir verifikasi berkala untuk mencocokkan jumlah stok tercatat pada sistem dengan stok fisik nyata di gudang atau rak toko. Selisih kerusakan, penyusutan, atau kehilangan dicatat secara transparan dengan riwayat keterangan penyesuaian.")
    add_bullet_p("3.", "Transfer Stok Antar-Cabang: Modul pergerakan persediaan antar-lokasi usaha. Pengiriman stok dari cabang asal ke cabang tujuan dicatat pada tabel stock_transfers dan stock_transfer_details dengan status alur kerja: Pending (barang dalam perjalanan) dan Completed (barang telah diterima dan diverifikasi di cabang tujuan). Stok di cabang asal berkurang saat transfer diterbitkan, dan stok cabang tujuan bertambah setelah penerimaan dikonfirmasi.")

    add_heading_2("2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)")
    add_body_p(
        "Pengelolaan hak akses menggunakan pendekatan Role-Based Access Control (RBAC) dengan tiga tingkatan hierarki peran pengguna. Seluruh kredensial akun diamankan menggunakan algoritma hashing SHA-256."
    )

    t_roles_data = [
        ("Tingkatan Peran", "Cakupan Hak Akses", "Lingkup Otoritas Cabang"),
        ("Super Admin", "Akses penuh ke seluruh menu sistem: Onboarding Wizard, manajemen master data, konfigurasi cabang, resep BOM, pembagian shift, seluruh transaksi kasir, mutasi stok antar-cabang, dan laporan laba rugi analitik.", "Seluruh Cabang (Pusat & Cabang Pembantu)"),
        ("Branch Manager", "Akses ke manajemen master data produk dan bahan cabang, verifikasi stock opname, persetujuan transfer stok masuk/keluar, evaluasi shift kasir harian cabang, dan laporan penjualan cabang.", "Terbatas pada Cabang Tempat Bertugas"),
        ("Cashier (Kasir)", "Akses operasional kasir: Buka/Tutup shift pribadi, input transaksi penjualan (Bayar Langsung & Hold Bill), pencarian katalog, pembatalan item nota sebelum bayar, dan pencetakan struk nota.", "Hanya Shift dan Meja Kasir Terdaftar"),
    ]
    t_roles = doc.add_table(rows=len(t_roles_data), cols=3)
    for r_idx, r_val in enumerate(t_roles_data):
        for c_idx, c_val in enumerate(r_val):
            t_roles.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_roles, [Inches(1.5), Inches(3.4), Inches(2.0)])

    add_heading_2("2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan")
    add_body_p(
        "Modul pelaporan dirancang untuk menyajikan data operasional bisnis yang akurat dan transparan bagi pemilik usaha. Fitur pelaporan terbagi menjadi empat jenis laporan analitik terstruktur:", indent=False
    )
    add_bullet_p("1.", "Laporan Penjualan Transaksi: Menampilkan rekapitulasi riwayat transaksi per periode tanggal dengan opsi filter berdasarkan cabang, kasir yang bertugas, status nota (Paid, Hold, Void), serta metode pembayaran (tunai, transfer, QRIS).")
    add_bullet_p("2.", "Laporan Laba Kotor (Gross Profit): Menghitung selisih antara nilai omzet penjualan bersih dengan total Harga Pokok Penjualan (HPP) tercatat pada tabel transaction_details, sehingga pemilik usaha mengetahui keuntungan riil operasional.")
    add_bullet_p("3.", "Laporan Kartu Mutasi Stok: Melacak rekam jejak keluar-masuk setiap item barang atau bahan mentah yang dipicu oleh transaksi kasir, penerimaan restock, penyesuaian stock opname, maupun transfer antar-cabang.")
    add_bullet_p("4.", "Dashboard Grafik Menu Terlaris: Menyajikan peringkat sepuluh item produk terlaris berdasarkan kuantitas terjual dan kontribusi nominal terhadap omzet toko.")

    # ==========================================
    # BAB III RANCANGAN SISTEM & ARSITEKTUR
    # ==========================================
    add_heading_1("BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK")

    add_heading_2("3.1 Alur Kerja & Arsitektur 3-Tier")
    add_body_p(
        "Untuk memastikan kemudahan pemeliharaan kode sumber, pengujian logika bisnis, dan kepatuhan terhadap prinsip rekayasa perangkat lunak, sistem Omni-Industry Configurable POS Engine menerapkan arsitektur 3-Tier yang terbagi menjadi tiga lapisan independen:"
    )
    add_bullet_p("1.", "Presentation Layer (Lapisan Antarmuka): Terdiri atas form dialog modal dan UserControl dinamis yang bertugas menampilkan elemen visual, menerima input tombol mouse/keyboard, dan memvalidasi kelengkapan teks form. Lapisan ini bebas dari penulisan query SQL maupun koneksi basis data langsung.")
    add_bullet_p("2.", "Service / Business Logic Layer (Lapisan Logika Bisnis): Berisi kelas-kelas layanan yang memproses aturan bisnis, meliputi validasi ketersediaan stok, kalkulasi HPP resep F&B, rekonsiliasi perhitungan selisih kas fisik shift, dan koordinasi pembungkusan transaksi atomik.")
    add_bullet_p("3.", "Repository / Data Access Layer (Lapisan Akses Data): Mengelola komunikasi langsung ke basis data MySQL via ADO.NET. Lapisan ini mengeksekusi perintah SQL terparameter (parameterized query) secara eksklusif menggunakan helper koneksi terpusat.")

    add_heading_2("3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell")
    add_body_p(
        "Aplikasi desktop mengadopsi pola antarmuka Single-Shell Navigation pada jendela utama MainForm. Pola ini memanfaatkan satu form induk tetap yang memuat panel navigasi bilah samping (sidebar) dan panel kontainer konten utama (panelContent). Saat pengguna mengklik salah satu menu di bilah samping, aplikasi tidak membuka form jendela pop-up baru yang saling bertumpuk di layar monitor kasir. Sebagai gantinya, kontrol antarmuka UserControl yang relevan dimuat secara dinamis ke dalam panelContent."
    )
    add_body_p(
        "Menu navigasi pada bilah samping bersifat adaptif. Komponen bilah samping membaca konfigurasi saklar fitur dan tingkatan peran pengguna saat proses inisialisasi form. Jika Super Admin menonaktifkan fitur kuliner F&B pada Onboarding Wizard, tombol navigasi Resep Dapur dan Bahan Baku otomatis disembunyikan dari antarmuka seluruh pengguna."
    )

    add_heading_2("3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)")
    add_body_p(
        "Penyimpanan data sistem menggunakan basis data relasional MySQL bernama db_uas_pos yang terdiri atas 12 tabel terstruktur. Struktur rinci setiap tabel dijabarkan pada tabel-tabel spesifikasi berikut:"
    )

    # Tabel 1: app_config
    add_heading_3("1. Tabel app_config (Konfigurasi Sistem & Feature Flags)")
    t_cfg_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama pengenal konfigurasi"),
        ("setting_key", "VARCHAR(50)", "NOT NULL, UNIQUE", "Kata kunci konfigurasi (misal: enable_fnb, is_onboarded)"),
        ("setting_value", "TEXT", "NULL", "Nilai konfigurasi yang tersimpan dalam format teks atau angka"),
    ]
    t_cfg = doc.add_table(rows=len(t_cfg_data), cols=4)
    for r_idx, r_val in enumerate(t_cfg_data):
        for c_idx, c_val in enumerate(r_val):
            t_cfg.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_cfg, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 2: branches
    add_heading_3("2. Tabel branches (Data Cabang & Kantor Pusat)")
    t_br_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama pengenal cabang"),
        ("nama_cabang", "VARCHAR(100)", "NOT NULL", "Nama identitas cabang toko"),
        ("alamat", "TEXT", "NULL", "Alamat fisik lokasi cabang operasional"),
        ("no_telp", "VARCHAR(20)", "NULL", "Nomor telepon kontak cabang"),
        ("is_pusat", "TINYINT(1)", "DEFAULT 0", "Penanda cabang utama/kantor pusat (1=Pusat, 0=Cabang)"),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Waktu pembuatan data cabang"),
    ]
    t_br = doc.add_table(rows=len(t_br_data), cols=4)
    for r_idx, r_val in enumerate(t_br_data):
        for c_idx, c_val in enumerate(r_val):
            t_br.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_br, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 3: users
    add_heading_3("3. Tabel users (Akun Pengguna & Hak Akses RBAC)")
    t_usr_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama pengguna"),
        ("branch_id", "INT", "FK -> branches.id, NULL", "Cabang tempat pengguna bertugas (NULL untuk Super Admin)"),
        ("username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Nama login unik untuk autentikasi sistem"),
        ("password_hash", "VARCHAR(64)", "NOT NULL", "Hash kata sandi terenkripsi algoritma SHA-256"),
        ("nama_lengkap", "VARCHAR(100)", "NOT NULL", "Nama lengkap petugas atau pengelola"),
        ("role", "ENUM", "'super_admin','branch_manager','cashier'", "Tingkatan hak akses operasional pengguna"),
        ("is_active", "TINYINT(1)", "DEFAULT 1", "Status keaktifan akun pengguna (1=Aktif, 0=Nonaktif)"),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Waktu pendaftaran akun pengguna"),
    ]
    t_usr = doc.add_table(rows=len(t_usr_data), cols=4)
    for r_idx, r_val in enumerate(t_usr_data):
        for c_idx, c_val in enumerate(r_val):
            t_usr.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_usr, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 4: categories
    add_heading_3("4. Tabel categories (Kategori Kelompok Item)")
    t_cat_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama kategori"),
        ("nama_kategori", "VARCHAR(100)", "NOT NULL", "Nama kelompok produk (misal: Minuman Kopi, Suku Cadang)"),
        ("tipe_bisnis", "ENUM", "'retail','fnb','service'", "Klasifikasi sektor bisnis pemilik kategori"),
    ]
    t_cat = doc.add_table(rows=len(t_cat_data), cols=4)
    for r_idx, r_val in enumerate(t_cat_data):
        for c_idx, c_val in enumerate(r_val):
            t_cat.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_cat, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 5: products
    add_heading_3("5. Tabel products (Master Produk, Menu Kuliner, & Layanan Jasa)")
    t_prd_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama produk"),
        ("branch_id", "INT", "FK -> branches.id, NOT NULL", "Cabang pemilik kepemilikan item barang"),
        ("category_id", "INT", "FK -> categories.id, NULL", "Kategori pengelompokan produk"),
        ("kode_item", "VARCHAR(50)", "NOT NULL", "Kode unik barcode atau penomoran inventaris toko"),
        ("nama_produk", "VARCHAR(150)", "NOT NULL", "Nama deskriptif barang jadi, menu, atau layanan jasa"),
        ("tipe", "ENUM", "'retail','fnb','service'", "Karakteristik item yang menentukan metode pemotongan stok"),
        ("harga_jual", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Tarif harga jual resmi yang ditagihkan kepada konsumen"),
        ("hpp_manual", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Harga Pokok Penjualan (HPP) modal per satuan item"),
        ("stok", "DECIMAL(10,2)", "NOT NULL, DEFAULT 0.00", "Kuantitas stok barang jadi (khusus item retail)"),
        ("is_active", "TINYINT(1)", "DEFAULT 1", "Status penjualan produk (1=Dijual, 0=Diarsipkan)"),
    ]
    t_prd = doc.add_table(rows=len(t_prd_data), cols=4)
    for r_idx, r_val in enumerate(t_prd_data):
        for c_idx, c_val in enumerate(r_val):
            t_prd.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_prd, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 6: raw_materials
    add_heading_3("6. Tabel raw_materials (Master Bahan Baku Mentah Dapur F&B)")
    t_rm_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama bahan baku mentah"),
        ("nama_bahan", "VARCHAR(100)", "NOT NULL", "Nama bahan mentah dapur (misal: Biji Kopi, Susu UHT)"),
        ("satuan", "VARCHAR(20)", "NOT NULL", "Satuan ukur takaran standar (gram, ml, butir, pcs)"),
        ("harga_beli_satuan", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Harga pembelian modal per satuan unit takaran"),
        ("stok_minimum", "DECIMAL(10,2)", "NOT NULL, DEFAULT 5.00", "Ambang batas peringatan stok bahan mentah menipis"),
    ]
    t_rm = doc.add_table(rows=len(t_rm_data), cols=4)
    for r_idx, r_val in enumerate(t_rm_data):
        for c_idx, c_val in enumerate(r_val):
            t_rm.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_rm, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 7: branch_materials
    add_heading_3("7. Tabel branch_materials (Stok Bahan Baku Mentah per Cabang)")
    t_bm_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama relasi stok cabang"),
        ("branch_id", "INT", "FK -> branches.id, NOT NULL", "Cabang lokasi penyimpanan bahan mentah"),
        ("raw_material_id", "INT", "FK -> raw_materials.id", "Bahan baku mentah yang disimpan"),
        ("stok", "DECIMAL(10,2)", "NOT NULL, DEFAULT 0.00", "Jumlah kuantitas stok fisik bahan mentah yang tersedia"),
    ]
    t_bm = doc.add_table(rows=len(t_bm_data), cols=4)
    for r_idx, r_val in enumerate(t_bm_data):
        for c_idx, c_val in enumerate(r_val):
            t_bm.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_bm, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 8: product_recipes
    add_heading_3("8. Tabel product_recipes (Resep & Formulasi Bill of Materials / BOM)")
    t_rec_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama komponen resep"),
        ("product_id", "INT", "FK -> products.id, NOT NULL", "Menu olahan kuliner yang memiliki resep takaran"),
        ("raw_material_id", "INT", "FK -> raw_materials.id", "Bahan mentah yang digunakan pada komposisi menu"),
        ("takaran", "DECIMAL(10,2)", "NOT NULL", "Besaran volume/berat bahan yang dikonsumsi per porsi menu"),
    ]
    t_rec = doc.add_table(rows=len(t_rec_data), cols=4)
    for r_idx, r_val in enumerate(t_rec_data):
        for c_idx, c_val in enumerate(r_val):
            t_rec.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_rec, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 9: shifts
    add_heading_3("9. Tabel shifts (Pencatatan Shift & Rekonsiliasi Kasir)")
    t_sh_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama sesi shift kasir"),
        ("branch_id", "INT", "FK -> branches.id, NOT NULL", "Cabang tempat sesi shift kasir berlangsung"),
        ("user_id", "INT", "FK -> users.id, NOT NULL", "Petugas kasir yang bertanggung jawab atas sesi shift"),
        ("waktu_buka", "DATETIME", "NOT NULL", "Waktu presisi pembukaan buku laci kasir"),
        ("waktu_tutup", "DATETIME", "NULL", "Waktu presisi penutupan buku dan serah terima kasir"),
        ("modal_awal", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Nominal saldo awal kas kecil (petty cash) saat buka shift"),
        ("uang_sistem", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Total akumulasi saldo kasir menurut perhitungan transaksi sistem"),
        ("uang_fisik", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Total nominal uang kertas/logam riil yang dihitung kasir"),
        ("selisih", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Selisih rekonsiliasi kas (uang_fisik dikurangi uang_sistem)"),
        ("status", "ENUM", "'open','closed'", "Status sesi kerja kasir (open=Berjalan, closed=Selesai)"),
    ]
    t_sh = doc.add_table(rows=len(t_sh_data), cols=4)
    for r_idx, r_val in enumerate(t_sh_data):
        for c_idx, c_val in enumerate(r_val):
            t_sh.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_sh, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 10: transactions
    add_heading_3("10. Tabel transactions (Header Nota Penjualan Kasir)")
    t_tr_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama transaksi penjualan"),
        ("nomor_nota", "VARCHAR(50)", "NOT NULL, UNIQUE", "Kode pengenal unik nota struk kasir (misal: TRX-202611-0001)"),
        ("branch_id", "INT", "FK -> branches.id, NOT NULL", "Cabang tempat transaksi kasir diterbitkan"),
        ("user_id", "INT", "FK -> users.id, NOT NULL", "Petugas kasir yang melayani transaksi penjualan"),
        ("shift_id", "INT", "FK -> shifts.id, NULL", "Sesi shift kerja kasir tempat transaksi dibukukan"),
        ("waktu", "DATETIME", "NOT NULL", "Waktu penerbitan nota transaksi penjualan"),
        ("subtotal", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Total nilai belanja sebelum potongan diskon dan pajak"),
        ("diskon", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Besaran potongan promosi atau potongan member"),
        ("pajak", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Nilai pertambahan pajak toko terhitung"),
        ("total_akhir", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Nilai tagihan akhir bersih yang wajib dibayar konsumen"),
        ("uang_bayar", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Jumlah uang tunai atau nominal transfer yang diterima"),
        ("kembalian", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Uang kembalian yang diserahkan kembali kepada konsumen"),
        ("tipe_bayar", "ENUM", "'cash','qris','transfer'", "Metode pembayaran transaksi kasir"),
        ("status", "ENUM", "'paid','hold','void'", "Status nota (paid=Lunas, hold=Gantung/Meja, void=Batal)"),
        ("label_meja_pelanggan", "VARCHAR(100)", "NULL", "Nomor meja makan (F&B) atau nomor antrean kendaraan (Jasa)"),
    ]
    t_tr = doc.add_table(rows=len(t_tr_data), cols=4)
    for r_idx, r_val in enumerate(t_tr_data):
        for c_idx, c_val in enumerate(r_val):
            t_tr.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_tr, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 11: transaction_details
    add_heading_3("11. Tabel transaction_details (Rincian Item Belanja Transaksi)")
    t_td_data = [
        ("Nama Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi"),
        ("id", "INT", "PK, AUTO_INCREMENT", "Kunci utama baris detail item transaksi"),
        ("transaction_id", "INT", "FK -> transactions.id", "Nota transaksi induk pemilik baris belanja"),
        ("product_id", "INT", "FK -> products.id, NOT NULL", "Produk, menu, atau layanan yang dibeli konsumen"),
        ("qty", "DECIMAL(10,2)", "NOT NULL", "Banyaknya kuantitas barang yang ditransaksikan"),
        ("harga_satuan", "DECIMAL(12,2)", "NOT NULL", "Harga jual satuan produk saat nota dicetak"),
        ("hpp_satuan", "DECIMAL(12,2)", "NOT NULL, DEFAULT 0.00", "Harga Pokok Penjualan (HPP) modal saat nota dicetak"),
        ("subtotal", "DECIMAL(12,2)", "NOT NULL", "Total harga baris item (qty dikali harga_satuan)"),
    ]
    t_td = doc.add_table(rows=len(t_td_data), cols=4)
    for r_idx, r_val in enumerate(t_td_data):
        for c_idx, c_val in enumerate(r_val):
            t_td.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_td, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    # Tabel 12: stock_transfers & stock_transfer_details
    add_heading_3("12. Tabel stock_transfers & stock_transfer_details (Mutasi Stok Cabang)")
    t_st_data = [
        ("Tabel / Kolom", "Tipe Data", "Atribut", "Keterangan Fungsi Alur Mutasi"),
        ("stock_transfers.id", "INT", "PK, AUTO_INCREMENT", "Kunci utama berkas transfer antar-cabang"),
        ("nomor_transfer", "VARCHAR(50)", "NOT NULL, UNIQUE", "Kode dokumen jalan mutasi stok (TRF-YYYYMM-XXXX)"),
        ("dari_branch_id", "INT", "FK -> branches.id", "Cabang asal pengirim persediaan barang/bahan"),
        ("ke_branch_id", "INT", "FK -> branches.id", "Cabang tujuan penerima persediaan barang/bahan"),
        ("user_id", "INT", "FK -> users.id", "Petugas penanggung jawab pembuatan dokumen mutasi"),
        ("tanggal", "DATETIME", "NOT NULL", "Waktu penerbitan dokumen mutasi stok"),
        ("status", "ENUM", "'pending','completed'", "Status perjalanan kiriman (pending=Jalan, completed=Diterima)"),
        ("detail.transfer_id", "INT", "FK -> stock_transfers.id", "Kunci pengait dokumen induk transfer"),
        ("detail.tipe_item", "ENUM", "'product','material'", "Jenis item yang dimutasi (barang retail atau bahan mentah)"),
        ("detail.item_id", "INT", "NOT NULL", "ID pengenal item produk atau bahan mentah yang dimutasi"),
        ("detail.qty", "DECIMAL(10,2)", "NOT NULL", "Volume/kuantitas persediaan yang dipindahkan"),
    ]
    t_st = doc.add_table(rows=len(t_st_data), cols=4)
    for r_idx, r_val in enumerate(t_st_data):
        for c_idx, c_val in enumerate(r_val):
            t_st.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_st, [Inches(1.5), Inches(1.3), Inches(1.8), Inches(2.3)])

    add_heading_2("3.4 Alur Logika Bisnis Kritis & Transaksi Atomik")
    add_body_p(
        "Keandalan perangkat lunak kasir bertumpu pada pencegahan inkonsistensi data ketika sistem memproses transaksi multi-item. Penyimpanan transaksi penjualan diimplementasikan menggunakan blok transaksi atomik MySqlTransaction. Saat kasir menekan tombol Simpan atau Bayar, sistem menjalankan urutan operasi basis data berikut di dalam satu transaksi utuh:", indent=False
    )
    add_bullet_p("1.", "Penyimpanan Header Transaksi: Perintah INSERT dieksekusi pada tabel transactions untuk menyimpan nomor nota unik, total belanja, potongan harga, metode pembayaran, serta identitas kasir yang bertugas.")
    add_bullet_p("2.", "Penyimpanan Rincian Item: Seluruh item belanja pada keranjang kasir di-iterasi dan dimasukkan ke tabel transaction_details lengkap dengan nilai harga_satuan dan nilai hpp_satuan riil saat itu.")
    add_bullet_p("3.", "Pemotongan Stok Kondisional Atomik: Untuk setiap item belanja, sistem memeriksa tipe item. Jika item bertipe retail, perintah UPDATE memotong kolom stok pada tabel products di cabang terkait. Jika item bertipe fnb, sistem membaca formulasi resep pada product_recipes dan mengeksekusi UPDATE untuk memotong persediaan takaran bahan baku mentah pada branch_materials secara proporsional. Jika item bertipe service, proses pemotongan stok dilewati.")
    add_bullet_p("4.", "Commit atau Rollback: Jika seluruh perintah eksekusi berhasil tanpa ada kendala kekurangan kuantitas stok atau kendala kegagalan jaringan, transaksi diresmikan via perintah Commit(). Sebaliknya, jika salah satu item mengalami galat (error), transaksi langsung di-Rollback() secara keseluruhan, sehingga tidak ada data nota separuh jadi yang mengotori basis data.")

    # ==========================================
    # BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL TIM
    # ==========================================
    add_heading_1("BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM")

    add_heading_2("4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim")
    add_body_p(
        "Untuk memaksimalkan efektivitas pengerjaan proyek akhir dan memastikan seluruh anggota tim memiliki tanggung jawab kode yang terdistribusi secara adil, tanggung jawab pengembangan dibagi menjadi enam modul independen berbasis pembagian arsitektur 3-Tier:"
    )

    t_team_matrix_data = [
        ("NRP", "Nama Anggota", "Peran / Modul Tanggung Jawab", "Ruang Lingkup Pengerjaan Modul"),
        ("225310690", "Bagas Rizky Putra Wardana", "Modul 1: Autentikasi & Konfigurasi", "Mengembangkan LoginForm, OnboardingWizardForm, AuthService (hashing SHA-256), OnboardingService, dan manajemen cabang usaha (BranchRepository)."),
        ("225310691", "FX Thiarnika Eka Atur Rangga", "Modul 2: Master Data & Resep BOM", "Mengembangkan UcMasterProduk, UcResepBOM, RecipeService, manajemen bahan mentah dapur, dan kalkulasi otomatis Harga Pokok Penjualan (HPP)."),
        ("225310692", "Gregorius Priyagung", "Modul 3: Kasir & Transaksi", "Mengembangkan UcKasir, katalog pencarian produk, keranjang belanja, mode Bayar Langsung, mode Hold Bill (pesanan meja), dan cetak struk nota."),
        ("225310693", "Moreno Hernakov", "Modul 4: Inventaris & Stok Cabang", "Mengembangkan UcInventaris, InventoryService, modul restock barang masuk, stock opname fisik, dan transfer stok antar-cabang."),
        ("225310694", "Raymond Sugiharto", "Modul 5: Operasional Kasir & Layanan", "Mengembangkan UcShift, ShiftService (buka modal awal petty cash & tutup kasir blind close), manajemen pelanggan/member, dan status pengerjaan antrean jasa."),
        ("225310695", "Valencia Angie Kurniawan", "Modul 6: Laporan & Analitik", "Mengembangkan UcLaporan, ReportService, visualisasi dashboard produk terlaris, laporan laba kotor harian/bulanan, dan kartu riwayat mutasi stok."),
    ]
    t_tm = doc.add_table(rows=len(t_team_matrix_data), cols=4)
    for r_idx, r_val in enumerate(t_team_matrix_data):
        for c_idx, c_val in enumerate(r_val):
            t_tm.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_tm, [Inches(1.0), Inches(1.8), Inches(1.8), Inches(2.2)])

    add_heading_2("4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu")
    add_body_p(
        "Kolaborasi teknis tim dijalankan dengan menerapkan standar rekayasa perangkat lunak yang ketat:", indent=False
    )
    add_bullet_p("1.", "Standar Antarmuka 3-Tier: Setiap anggota tim wajib mematuhi pemisahan lapisan. Kode pada UserControl dilarang menulis perintah SQL mentah (seperti SELECT atau INSERT). Seluruh pemanggilan basis data harus didelegasikan ke kelas Service dan Repository.")
    add_bullet_p("2.", "Pemeriksaan Kode (Code Review): Integrasi modul ke dalam solusi proyek utama (MainForm) dilakukan bersama oleh seluruh anggota tim guna memverifikasi penamaan variabel, penanganan eksepsi (try-catch), dan ketiadaan kebocoran koneksi basis data (seluruh koneksi wajib dibungkus blok using).")
    add_bullet_p("3.", "Pengujian Transaksi Basis Data: Pengujian fungsi transaksi kasir dan mutasi persediaan wajib diverifikasi menggunakan kasus uji transaksi gagal untuk membuktikan keandalan fitur Rollback pada MySqlTransaction.")

    add_heading_2("4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)")
    add_body_p(
        "Rencana pengerjaan proyek akhir terbagi ke dalam enam tahapan mingguan terukur hingga pelaksanaan demonstrasi evaluasi UAS:", indent=False
    )

    t_timeline_data = [
        ("Minggu", "Tahapan Pengerjaan", "Fokus Aktivitas Utama", "Target Luaran / Deliverables"),
        ("Minggu 1", "Analisis & Skema Basis Data", "Penyusunan proposal, spesifikasi arsitektur sistem, dan pembuatan skrip DDL SQL 12 tabel.", "Dokumen proposal resmi & skrip basis data MySQL."),
        ("Minggu 2", "Infrastruktur & Modul 1-2", "Setup project Visual Studio 2022 (.NET 4.7.2), DbHelper ADO.NET, LoginForm, Onboarding Wizard, dan Master Data.", "Pondasi arsitektur 3-tier, form autentikasi, dan katalog master data."),
        ("Minggu 3", "Modul Resep BOM & Kasir", "Implementasi relasi product_recipes, kalkulasi HPP otomatis, form kasir dual-mode, dan cetak nota struk.", "Mesin HPP berjalan dan transaksi kasir dapat menyimpan nota."),
        ("Minggu 4", "Inventaris & Shift Kasir", "Implementasi restock bahan, stock opname fisik, mutasi antar-cabang, dan alur kerja shift kasir blind close.", "Pemotongan stok dapur otomatis dan rekonsiliasi kasir."),
        ("Minggu 5", "Pelaporan & Dashboard", "Pengembangan modul analitik omzet, laporan laba kotor (omzet minus HPP), kartu stok, dan antrean jasa.", "Laporan keuangan lengkap dan dashboard visual."),
        ("Minggu 6", "Uji Coba & Finalisasi", "Pengujian integrasi menyeluruh, pembersihan bug, uji coba transaksi atomik, dan penyusunan laporan akhir UAS.", "Aplikasi siap demonstrasi dan naskah laporan lengkap."),
    ]
    t_time = doc.add_table(rows=len(t_timeline_data), cols=4)
    for r_idx, r_val in enumerate(t_timeline_data):
        for c_idx, c_val in enumerate(r_val):
            t_time.rows[r_idx].cells[c_idx].paragraphs[0].text = c_val
    style_table(t_time, [Inches(0.8), Inches(1.6), Inches(2.3), Inches(2.1)])

    # ==========================================
    # BAB V PENUTUP
    # ==========================================
    add_heading_1("BAB V PENUTUP")

    add_heading_2("5.1 Kesimpulan")
    add_body_p(
        "Omni-Industry Configurable POS Engine dihadirkan sebagai jawaban atas tantangan operasional kasir dan manajemen inventaris pada bisnis multi-sektor yang membutuhkan fleksibilitas tinggi tanpa mengorbankan kesederhanaan arsitektur sistem. Dengan memanfaatkan arsitektur 3-Tier yang kokoh pada platform C# Windows Forms dan basis data MySQL terpusat, sistem mampu memisahkan antarmuka pengguna, logika bisnis, dan akses data secara tertib. Keberadaan Onboarding Wizard berbasis saklar konfigurasi (feature flags) memungkinkan aplikasi bertransformasi secara instan memenuhi kebutuhan spesifik sektor ritel, restoran kuliner F&B, dan layanan jasa tanpa memerlukan perubahan struktur kode."
    )
    add_body_p(
        "Inovasi formulasi Bill of Materials (BOM) pada modul kuliner berhasil menghubungkan menu sajian dengan persediaan bahan baku mentah dapur secara proporsional sekaligus menghitung Harga Pokok Penjualan (HPP) secara otomatis. Ditambah dengan dukungan transaksi atomik MySqlTransaction pada alur transaksi kasir dual-mode dan transfer stok antar-cabang, serta akuntabilitas rekonsiliasi shift kasir melalui metode blind close, perangkat lunak ini dirancang untuk memberikan keandalan data transaksi bisnis yang tinggi."
    )

    add_heading_2("5.2 Harapan Capaian")
    add_body_p(
        "Melalui penyusunan proposal dan pelaksanaan proyek akhir ini, tim pengembang berharap dapat menghasilkan aplikasi Point of Sales desktop yang fungsional, andal, dan siap dioperasikan dalam lingkungan kerja nyata. Implementasi proyek ini diharapkan dapat menjadi tolak ukur pemahaman praktis mahasiswa dalam menerapkan konsep pemrograman visual berbasis event, arsitektur perangkat lunak 3-Tier, keamanan basis data parameterized query, dan kerja sama tim yang terstruktur sesuai dengan standar kompetensi akademik Program Studi S1 Informatika di Institut Sains dan Teknologi Terpadu Surabaya."
    )

    # Simpan berkas Word (.docx)
    doc.save(DOCX_OUT)
    print(f"Berhasil menghasilkan dokumen proposal: {DOCX_OUT}")


def build_markdown_proposal():
    """Menghasilkan salinan proposal dalam format Markdown untuk dokumentasi repositori."""
    # Menuliskan berkas PROPOSAL_POS.md
    md_content = """# OMNI-INDUSTRY CONFIGURABLE POS ENGINE: SISTEM POINT OF SALES TERPADU MULTI-SEKTOR BERBASIS DESKTOP C# WINDOWS FORMS DAN BASIS DATA MYSQL

**PROPOSAL PROYEK AKHIR**  
**MATA KULIAH PEMROGRAMAN VISUAL (GASAL 2026/2027)**  

**Disusun oleh:**  
1. BAGAS RIZKY PUTRA WARDANA (NRP: 225310690)  
2. FX THIARNIKA EKA ATUR RANGGA (NRP: 225310691)  
3. GREGORIUS PRIYAGUNG (NRP: 225310692)  
4. MORENO HERNAKOV (NRP: 225310693)  
5. RAYMOND SUGIHARTO (NRP: 225310694)  
6. VALENCIA ANGIE KURNIAWAN (NRP: 225310695)  

**Dosen Pengampu:**  
Hansel Santoso, S.Kom., M.Kom.  

**PROGRAM STUDI S1 INFORMATIKA**  
**FAKULTAS TEKNOLOGI INFORMASI DAN INDUSTRI KREATIF**  
**INSTITUT SAINS DAN TEKNOLOGI TERPADU SURABAYA**  
**2026**  

---

# LEMBAR PENGESAHAN PROPOSAL PROYEK AKHIR

Proposal Proyek Akhir ini telah diajukan dan disetujui untuk dilaksanakan sebagai bagian dari evaluasi Ujian Akhir Semester (UAS) mata kuliah Pemrograman Visual Semester Gasal 2026/2027 di Institut Sains dan Teknologi Terpadu Surabaya.

| Parameter | Keterangan |
| :--- | :--- |
| **Judul Proyek** | Omni-Industry Configurable POS Engine |
| **Mata Kuliah** | Pemrograman Visual (Gasal 2026/2027) |
| **Program Studi** | S1 Informatika |
| **Institusi** | Institut Sains dan Teknologi Terpadu Surabaya |
| **Jumlah Anggota** | 6 (Enam) Orang Mahasiswa |

*Surabaya, 14 November 2026*  

**Menyetujui,**  
Dosen Pengampu Pemrograman Visual: **Hansel Santoso, S.Kom., M.Kom.**  

---

# DAFTAR ISI

- **BAB I PENDAHULUAN**
  - 1.1 Latar Belakang
  - 1.2 Rumusan Masalah
  - 1.3 Tujuan Proyek
  - 1.4 Manfaat Proyek
  - 1.5 Batasan Masalah
- **BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM**
  - 2.1 Konsep & Deskripsi Program
  - 2.2 Onboarding Wizard & Manajemen Konfigurasi Toko
  - 2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)
  - 2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir
  - 2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang
  - 2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)
  - 2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan
- **BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK**
  - 3.1 Alur Kerja & Arsitektur 3-Tier
  - 3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell
  - 3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)
  - 3.4 Alur Logika Bisnis Kritis & Transaksi Atomik
- **BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM**
  - 4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim
  - 4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu
  - 4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)
- **BAB V PENUTUP**
  - 5.1 Kesimpulan
  - 5.2 Harapan Capaian

---

# BAB I PENDAHULUAN

## 1.1 Latar Belakang
Efisiensi operasional pada sektor perdagangan dan jasa mikro, kecil, dan menengah (UMKM) sangat ditentukan oleh keandalan sistem pencatatan transaksi kasir. Sebagian besar perangkat lunak *Point of Sales* (POS) yang beredar di pasaran memiliki desain monolitik dan kaku. Aplikasi ritel murni hanya mengelola transaksi barang jadi berbasis kode *barcode*, sedangkan aplikasi kuliner (*Food and Beverage* / F&B) mengunci fungsionalitasnya pada manajemen pesanan meja dan resep dapur tanpa fleksibilitas penyesuaian multi-cabang. Pelaku usaha yang mengoperasikan model bisnis campuran (*hybrid*), seperti minimarket yang memiliki stan kopi cepat saji atau bengkel motor yang menjual suku cadang fisik sekaligus jasa perbaikan, sering kali terpaksa menggunakan dua hingga tiga aplikasi kasir terpisah yang membingungkan kasir dan menyulitkan rekapitulasi pembukuan.

Tantangan teknis utama pada sektor kuliner terletak pada pemotongan persediaan. Penjualan satu porsi minuman kopi tidak memotong persediaan kopi siap saji di etalase, melainkan mengonsumsi sejumlah takaran bahan baku mentah dapur seperti biji kopi sangrai, susu segar, dan sirup perisa. Ketiadaan formulasi *Bill of Materials* (BOM) pada sistem kasir standar menyebabkan stok bahan baku mentah tidak terdata secara akurat, sehingga selisih fisik dapur sering kali baru terdeteksi pada akhir bulan. Selain itu, kalkulasi Harga Pokok Penjualan (HPP) menjadi tidak akurat karena fluktuasi harga beli bahan baku dari pemasok tidak tercermin secara langsung pada margin laba kotor setiap transaksi.

Kerentanan operasional kasir juga kerap terjadi pada proses pergantian jam kerja (*shift*) kasir. Ketiadaan pencatatan modal awal kas kecil (*petty cash*) dan verifikasi penerimaan uang tunai fisik secara independen membuka celah selisih pembukuan dan kecurangan internal. Di sisi lain, ekspansi usaha ke beberapa lokasi cabang membutuhkan sistem basis data terpusat yang mampu memetakan kepemilikan data per cabang dan mengelola alur mutasi transfer stok antar-cabang secara tertib tanpa menimbulkan kompleksitas arsitektur yang berlebihan bagi pengembang perangkat lunak.

Untuk menjawab seluruh kebutuhan tersebut, dikembangkan proyek akhir bertajuk Omni-Industry Configurable POS Engine berbasis desktop C# Windows Forms dan basis data relasional MySQL via pustaka ADO.NET. Sistem ini memanfaatkan arsitektur 3-Tier yang memisahkan komponen antarmuka pengguna, logika bisnis, dan repositori basis data secara tegas. Fungsionalitas aplikasi diatur secara adaptif melalui panduan pengaturan awal (*Onboarding Wizard*) dan saklar fitur (*feature flags*), sehingga sistem kasir dapat bertransformasi menjadi sistem ritel murni, kasir restoran terintegrasi dapur, sistem jasa servis, atau gabungan ketiganya tanpa mengubah satu baris pun kode sumber aplikasi.

## 1.2 Rumusan Masalah
Berdasarkan permasalahan operasional dan kebutuhan arsitektur perangkat lunak yang telah dipaparkan, rumusan masalah dalam penelitian dan pengembangan proyek ini dirumuskan sebagai berikut:
1. Bagaimana merancang arsitektur perangkat lunak 3-Tier pada C# Windows Forms yang memisahkan antarmuka *Single-Shell*, logika bisnis layanan, dan akses repositori ADO.NET secara modular?
2. Bagaimana membangun mekanisme *Onboarding Wizard* berbasis saklar fitur (*feature flags*) di tabel konfigurasi untuk mengaktifkan atau menonaktifkan modul ritel, kuliner F&B, jasa, resep dapur, dan shift kasir secara dinamis?
3. Bagaimana mengimplementasikan mesin resep (*Bill of Materials* / BOM) yang mampu menghitung Harga Pokok Penjualan (HPP) menu secara otomatis serta memotong stok bahan baku mentah dapur secara proporsional?
4. Bagaimana menyusun mekanisme transaksi kasir *dual-mode* yang mendukung transaksi bayar langsung (*cash and carry*) maupun penangguhan tagihan (*Hold Bill*) untuk pesanan meja dan antrean pengerjaan jasa?
5. Bagaimana menjamin integritas data multi-tabel saat terjadi transaksi penjualan dan transfer stok antar-cabang menggunakan transaksi atomik basis data (`MySqlTransaction`)?

## 1.3 Tujuan Proyek
Tujuan yang ingin dicapai melalui perancangan dan implementasi proyek akhir ini meliputi:
1. Membangun aplikasi desktop *Point of Sales* modular menggunakan bahasa pemrograman C# pada kerangka kerja .NET Framework 4.7.2 dan basis data MySQL.
2. Menyediakan wizard konfigurasi bisnis awal yang memungkinkan Super Admin menyesuaikan identitas toko, persentase pajak, serta mode industri usaha tanpa rekayasa ulang basis data.
3. Mengintegrasikan modul bahan baku mentah dan relasi resep produk kuliner sehingga stok dapur berkurang secara otomatis dan margin laba kotor tercatat akurat.
4. Menerapkan sistem rekonsiliasi shift kasir dengan pencatatan modal awal dan pelaporan selisih kas fisik melalui metode *blind close* saat penutupan buku toko.
5. Merancang skema basis data relasional 12 tabel dengan partisi data cabang (`branch_id`) dan memvalidasi keutuhan transaksi melalui eksekusi *parameterized query*.

## 1.4 Manfaat Proyek
Penerapan sistem Omni-Industry Configurable POS Engine memberikan manfaat nyata bagi berbagai pihak terkait:
1. **Bagi Pelaku Usaha UMKM**: Memperoleh perangkat lunak kasir multifungsi yang fleksibel tanpa perlu membayar biaya langganan ganda untuk modul ritel, restoran, dan jasa servis terpisah.
2. **Bagi Petugas Kasir dan Supervisor**: Mempercepat proses pelayanan pembayaran pelanggan, mencegah kekeliruan perhitungan kembalian, serta mengamankan rekonsiliasi kas saat pergantian shift.
3. **Bagi Tim Dapur dan Gudang**: Memastikan ketersediaan stok bahan mentah terpantau secara berkala melalui peringatan stok menipis dan mempermudah pelacakan mutasi transfer barang antar-cabang.
4. **Bagi Pengembangan Akademik**: Menjadi percontohan implementasi rekayasa perangkat lunak desktop semester 3 yang taat pada kaidah pemisahan lapisan (*separation of concerns*), keamanan data *parameterized query*, dan transaksi atomik ACID.

## 1.5 Batasan Masalah
Agar ruang lingkup perancangan sistem terarah dan sesuai dengan standar kurikulum mata kuliah Pemrograman Visual Semester 3, batasan masalah proyek ditetapkan sebagai berikut:
1. Aplikasi dibangun sebagai perangkat lunak desktop Windows menggunakan bahasa C# pada lingkungan Microsoft Visual Studio 2022 dengan target .NET Framework 4.7.2.
2. Basis data menggunakan MySQL server lokal (XAMPP / MariaDB) yang diakses melalui pustaka ADO.NET murni (`MySql.Data`) dengan seluruh perintah SQL memanfaatkan *parameterized query* (`@param`) untuk mencegah celah *SQL Injection*.
3. Arsitektur multi-cabang dikelola melalui basis data relasional tunggal terpusat (*single central database*) dengan partisi kepemilikan rekaman data menggunakan kolom foreign key `branch_id`.
4. Pencetakan nota transaksi dan lembar rekapitulasi shift kasir disimulasikan melalui komponen `PrintDocument` Windows Forms dalam format teks struk termal standar lebar 58 mm dan 80 mm.
5. Sistem autentikasi menerapkan enkripsi searah (*hashing*) SHA-256 untuk seluruh kata sandi pengguna tanpa penyimpanan teks mentah di basis data.

---

# BAB II PEMBAHASAN & STRUKTUR FITUR SISTEM

## 2.1 Konsep & Deskripsi Program
Omni-Industry Configurable POS Engine dirancang sebagai mesin kasir desktop cerdas yang mampu beradaptasi dengan model operasional berbagai sektor bisnis. Kata *omni-industry* merepresentasikan kemampuan adaptasi sistem dalam melayani tiga model operasional utama: ritel barang jadi (minimarket, butik, toko kelontong), operasional kuliner (kafe, kedai kopi, restoran cepat saji), serta penyedia jasa dan servis (bengkel, binatu/laundry, salon kecantikan). Karakteristik ketiga sektor tersebut dipadukan ke dalam satu mesin pemrosesan terintegrasi melalui mekanisme aktivasi saklar fitur.

Kekuatan utama arsitektur ini terletak pada penghapusan redundansi sistem. Ketika pengguna memilih model bisnis ritel murni, antarmuka kasir hanya menampilkan input pemindai barcode, pencarian produk cepat, dan keranjang belanja kasir. Sebaliknya, saat model kuliner F&B diaktifkan, antarmuka menambahkan katalog visual berbasis kategori, opsi penandaan nomor meja pelanggan, dan pengiriman daftar pesanan ke dapur. Jika model jasa diaktifkan, kasir dapat mencatat nama teknisi atau penanggung jawab serta memantau status antrean pekerjaan tanpa memicu pemotongan stok barang fisik.

## 2.2 Onboarding Wizard & Manajemen Konfigurasi Toko
Saat aplikasi pertama kali dijalankan pasca instalasi basis data, sistem mendeteksi nilai parameter `is_onboarded` pada tabel `app_config`. Jika parameter bernilai `0`, proses login Super Admin secara otomatis mengalihkan pengguna ke antarmuka Onboarding Wizard sebelum masuk ke jendela utama aplikasi. Wizard ini memandu pemilik usaha mengonfigurasi profil usaha dan memilih fitur fungsional yang dibutuhkan dalam empat tahapan terstruktur:

| Tahap | Nama Konfigurasi | Parameter Basis Data | Keterangan Operasional |
| :---: | :--- | :--- | :--- |
| **1** | Identitas Usaha | `business_name`, `business_address`, `business_phone` | Mencatat nama toko, alamat operasional, dan nomor telepon kontak yang akan dicetak pada kepala nota struk kasir. |
| **2** | Pemilihan Sektor | `enable_retail`, `enable_fnb`, `enable_service` | Memilih jenis industri yang dijalankan toko untuk memfilter navigasi antarmuka dan jenis produk yang dapat diinput. |
| **3** | Mesin & Operasional | `enable_recipe_bom`, `enable_shift`, `tax_percentage` | Mengaktifkan modul resep dapur, mewajibkan kasir membuka shift petty cash, serta menentukan tarif pajak transaksi (misal: 10,0%). |
| **4** | Cabang & Akun | `branches` (HQ), `users` (Super Admin) | Memverifikasi data cabang utama dan menetapkan kredensial administrator permanen sebelum flag `is_onboarded` diubah menjadi 1. |

Seluruh parameter yang tersimpan di tabel `app_config` bertindak sebagai *feature flags* global. Selama aplikasi berjalan, kelas penyedia layanan membaca konfigurasi ini untuk menentukan apakah tab navigasi resep dapur ditampilkan atau disembunyikan dari antarmuka kasir.

## 2.3 Manajemen Master Data & Mesin Resep (Bill of Materials / BOM)
Katalog barang pada sistem dibagi menjadi tiga kelompok entitas yang terhubung: kategori produk (`categories`), master produk dan layanan (`products`), serta master bahan baku mentah dapur (`raw_materials`). Setiap produk memiliki penanda tipe bisnis (*retail*, *fnb*, atau *service*) yang menentukan perilaku pemotongan persediaan saat nota penjualan diterbitkan.

Pada sektor kuliner F&B, produk olahan seperti Kopi Susu Gula Aren tidak memiliki stok fisik langsung di gudang barang jadi. Sebagai gantinya, produk tersebut dikaitkan dengan beberapa bahan baku mentah melalui tabel perantara `product_recipes`. Tabel ini menyimpan relasi banyak-ke-banyak antara produk dan bahan baku mentah lengkap dengan takaran pemakaian per porsi sajian (misalnya: 18,00 gram bubuk kopi, 120,00 ml susu segar cair, dan 25,00 ml sirup gula aren).

Mesin resep menjalankan algoritma kalkulasi Harga Pokok Penjualan (HPP) otomatis secara berkala. Setiap kali harga beli bahan mentah diperbarui pada master `raw_materials`, sistem menjumlahkan hasil kali antara takaran pemakaian resep dengan harga beli satuan terbaru untuk seluruh bahan penyusun menu tersebut. Nilai HPP terhitung kemudian disimpan ke dalam atribut `hpp_manual` pada tabel `products`, sehingga margin laba kotor per item menu dapat dihitung secara real-time tanpa memerlukan rekalkulasi manual oleh supervisor.

## 2.4 Transaksi Kasir Dual-Mode & Rekonsiliasi Shift Kasir
Modul transaksi kasir menyediakan antarmuka terpadu yang dirancang ergonomis bagi kecepatan kerja petugas kasir. Sistem mendukung dua mode penyelesaian transaksi penjualan yang dapat dipilih secara fleksibel sesuai situasi antrean toko:
1. **Mode Bayar Langsung (*Paid*)**: Diterapkan pada pola transaksi ritel cepat (*cash and carry*). Kasir memasukkan item belanja melalui pemindai barcode atau klik katalog, memilih metode pembayaran (tunai, transfer bank, atau QRIS), memasukkan nominal uang bayar pelanggan, dan sistem langsung menerbitkan struk nota pembayaran lunas.
2. **Mode Simpan Tagihan (*Hold Bill*)**: Diterapkan pada pesanan makan di tempat (*dine-in*) restoran atau antrean unit pada layanan servis. Kasir mencatat pesanan belanja beserta label pengenal berupa nomor meja atau nomor polisi kendaraan. Transaksi disimpan ke basis data dengan status *Hold*. Saat pelanggan selesai bersantap atau servis rampung, kasir memanggil kembali nota gantung tersebut untuk menerima pembayaran dan mengubah status transaksi menjadi *Paid*.

Untuk menjaga akuntabilitas keuangan tunai, sistem mewajibkan pengelolaan shift kasir. Saat memulai jam kerja, kasir harus membuka shift baru dengan memasukkan modal awal kas kecil (*petty cash*) yang diberikan bendahara. Sepanjang shift berlangsung, seluruh transaksi tunai yang berhasil dicatat oleh kasir akan diakumulasikan ke dalam variabel saldo sistem. Saat jam kerja berakhir, kasir melakukan proses penutupan buku kas (*blind close*). Kasir menghitung uang fisik yang ada di laci kasir dan menginput nominal tersebut ke dalam sistem tanpa melihat saldo rekapitulasi sistem terlebih dahulu.

Sistem kemudian membandingkan uang fisik aktual dengan formula saldo akhir sistem: modal awal ditambah total transaksi tunai. Selisih yang terjadi dicatat secara otomatis ke dalam kolom `selisih` pada tabel `shifts`, baik bernilai 0 (cocok), bernilai positif (*surplus*), maupun bernilai negatif (*shortage* / defisit). Laporan penutupan shift dicetak sebagai bukti serah terima kasir kepada pengelola toko.

## 2.5 Manajemen Inventaris, Stock Opname, & Transfer Antar-Cabang
Manajemen persediaan membedakan penanganan antara stok barang jadi pada sektor ritel dan stok bahan baku mentah pada sektor kuliner F&B. Seluruh stok bahan baku mentah dipartisi per cabang pada tabel `branch_materials`, sehingga ketersediaan persediaan dapur di cabang utama tidak tercampur dengan ketersediaan di cabang pembantu.

Sistem menyediakan tiga fungsi pengendalian persediaan utama:
1. **Restock (Barang Masuk)**: Mencatat penerimaan kiriman barang dari pemasok. Kuantitas stok produk atau bahan mentah di cabang terkait akan bertambah, disertai pembaruan harga beli satuan jika terjadi perubahan tarif pasokan.
2. **Stock Opname (Penyesuaian Fisik)**: Formulir verifikasi berkala untuk mencocokkan jumlah stok tercatat pada sistem dengan stok fisik nyata di gudang atau rak toko. Selisih kerusakan, penyusutan, atau kehilangan dicatat secara transparan dengan riwayat keterangan penyesuaian.
3. **Transfer Stok Antar-Cabang**: Modul pergerakan persediaan antar-lokasi usaha. Pengiriman stok dari cabang asal ke cabang tujuan dicatat pada tabel `stock_transfers` dan `stock_transfer_details` dengan status alur kerja: *Pending* (barang dalam perjalanan) dan *Completed* (barang telah diterima dan diverifikasi di cabang tujuan). Stok di cabang asal berkurang saat transfer diterbitkan, dan stok cabang tujuan bertambah setelah penerimaan dikonfirmasi.

## 2.6 Hak Akses Pengguna (Role-Based Access Control / RBAC)
Pengelolaan hak akses menggunakan pendekatan *Role-Based Access Control* (RBAC) dengan tiga tingkatan hierarki peran pengguna. Seluruh kredensial akun diamankan menggunakan algoritma *hashing* SHA-256.

| Tingkatan Peran | Cakupan Hak Akses | Lingkup Otoritas Cabang |
| :--- | :--- | :--- |
| **Super Admin** | Akses penuh ke seluruh menu sistem: Onboarding Wizard, manajemen master data, konfigurasi cabang, resep BOM, pembagian shift, seluruh transaksi kasir, mutasi stok antar-cabang, dan laporan laba rugi analitik. | Seluruh Cabang (Pusat & Cabang Pembantu) |
| **Branch Manager** | Akses ke manajemen master data produk dan bahan cabang, verifikasi stock opname, persetujuan transfer stok masuk/keluar, evaluasi shift kasir harian cabang, dan laporan penjualan cabang. | Terbatas pada Cabang Tempat Bertugas |
| **Cashier (Kasir)** | Akses operasional kasir: Buka/Tutup shift pribadi, input transaksi penjualan (Bayar Langsung & Hold Bill), pencarian katalog, pembatalan item nota sebelum bayar, dan pencetakan struk nota. | Hanya Shift dan Meja Kasir Terdaftar |

## 2.7 Modul Pelaporan, Laba Kotor, & Analisis Penjualan
Modul pelaporan dirancang untuk menyajikan data operasional bisnis yang akurat dan transparan bagi pemilik usaha. Fitur pelaporan terbagi menjadi empat jenis laporan analitik terstruktur:
1. **Laporan Penjualan Transaksi**: Menampilkan rekapitulasi riwayat transaksi per periode tanggal dengan opsi filter berdasarkan cabang, kasir yang bertugas, status nota (*Paid*, *Hold*, *Void*), serta metode pembayaran (tunai, transfer, QRIS).
2. **Laporan Laba Kotor (*Gross Profit*)**: Menghitung selisih antara nilai omzet penjualan bersih dengan total Harga Pokok Penjualan (HPP) tercatat pada tabel `transaction_details`, sehingga pemilik usaha mengetahui keuntungan riil operasional.
3. **Laporan Kartu Mutasi Stok**: Melacak rekam jejak keluar-masuk setiap item barang atau bahan mentah yang dipicu oleh transaksi kasir, penerimaan restock, penyesuaian stock opname, maupun transfer antar-cabang.
4. **Dashboard Grafik Menu Terlaris**: Menyajikan peringkat sepuluh item produk terlaris berdasarkan kuantitas terjual dan kontribusi nominal terhadap omzet toko.

---

# BAB III RANCANGAN SISTEM & ARSITEKTUR PERANGKAT LUNAK

## 3.1 Alur Kerja & Arsitektur 3-Tier
Untuk memastikan kemudahan pemeliharaan kode sumber, pengujian logika bisnis, dan kepatuhan terhadap prinsip rekayasa perangkat lunak, sistem Omni-Industry Configurable POS Engine menerapkan arsitektur 3-Tier yang terbagi menjadi tiga lapisan independen:
1. **Presentation Layer (Lapisan Antarmuka)**: Terdiri atas form dialog modal dan `UserControl` dinamis yang bertugas menampilkan elemen visual, menerima input tombol mouse/keyboard, dan memvalidasi kelengkapan teks form. Lapisan ini bebas dari penulisan query SQL maupun koneksi basis data langsung.
2. **Service / Business Logic Layer (Lapisan Logika Bisnis)**: Berisi kelas-kelas layanan yang memproses aturan bisnis, meliputi validasi ketersediaan stok, kalkulasi HPP resep F&B, rekonsiliasi perhitungan selisih kas fisik shift, dan koordinasi pembungkusan transaksi atomik.
3. **Repository / Data Access Layer (Lapisan Akses Data)**: Mengelola komunikasi langsung ke basis data MySQL via ADO.NET. Lapisan ini mengeksekusi perintah SQL terparameter (*parameterized query*) secara eksklusif menggunakan helper koneksi terpusat.

## 3.2 Pola Antarmuka Pengguna & Navigasi Single-Shell
Aplikasi desktop mengadopsi pola antarmuka *Single-Shell Navigation* pada jendela utama `MainForm`. Pola ini memanfaatkan satu form induk tetap yang memuat panel navigasi bilah samping (*sidebar*) dan panel kontainer konten utama (`panelContent`). Saat pengguna mengklik salah satu menu di bilah samping, aplikasi tidak membuka form jendela pop-up baru yang saling bertumpuk di layar monitor kasir. Sebagai gantinya, kontrol antarmuka `UserControl` yang relevan dimuat secara dinamis ke dalam `panelContent`.

Menu navigasi pada bilah samping bersifat adaptif. Komponen bilah samping membaca konfigurasi saklar fitur dan tingkatan peran pengguna saat proses inisialisasi form. Jika Super Admin menonaktifkan fitur kuliner F&B pada Onboarding Wizard, tombol navigasi Resep Dapur dan Bahan Baku otomatis disembunyikan dari antarmuka seluruh pengguna.

## 3.3 Perancangan Basis Data Relasional (12 Tabel Terpusat)
Penyimpanan data sistem menggunakan basis data relasional MySQL bernama `db_uas_pos` yang terdiri atas 12 tabel terstruktur. Struktur rinci setiap tabel dijabarkan pada spesifikasi berikut:

### 1. Tabel app_config (Konfigurasi Sistem & Feature Flags)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengenal konfigurasi |
| `setting_key` | VARCHAR(50) | NOT NULL, UNIQUE | Kata kunci konfigurasi (misal: enable_fnb, is_onboarded) |
| `setting_value` | TEXT | NULL | Nilai konfigurasi yang tersimpan dalam format teks atau angka |

### 2. Tabel branches (Data Cabang & Kantor Pusat)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengenal cabang |
| `nama_cabang` | VARCHAR(100) | NOT NULL | Nama identitas cabang toko |
| `alamat` | TEXT | NULL | Alamat fisik lokasi cabang operasional |
| `no_telp` | VARCHAR(20) | NULL | Nomor telepon kontak cabang |
| `is_pusat` | TINYINT(1) | DEFAULT 0 | Penanda cabang utama/kantor pusat (1=Pusat, 0=Cabang) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu pembuatan data cabang |

### 3. Tabel users (Akun Pengguna & Hak Akses RBAC)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama pengguna |
| `branch_id` | INT | FK -> branches.id, NULL | Cabang tempat pengguna bertugas (NULL untuk Super Admin) |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | Nama login unik untuk autentikasi sistem |
| `password_hash` | VARCHAR(64) | NOT NULL | Hash kata sandi terenkripsi algoritma SHA-256 |
| `nama_lengkap` | VARCHAR(100) | NOT NULL | Nama lengkap petugas atau pengelola |
| `role` | ENUM | 'super_admin','branch_manager','cashier' | Tingkatan hak akses operasional pengguna |
| `is_active` | TINYINT(1) | DEFAULT 1 | Status keaktifan akun pengguna (1=Aktif, 0=Nonaktif) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Waktu pendaftaran akun pengguna |

### 4. Tabel categories (Kategori Kelompok Item)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama kategori |
| `nama_kategori` | VARCHAR(100) | NOT NULL | Nama kelompok produk (misal: Minuman Kopi, Suku Cadang) |
| `tipe_bisnis` | ENUM | 'retail','fnb','service' | Klasifikasi sektor bisnis pemilik kategori |

### 5. Tabel products (Master Produk, Menu Kuliner, & Layanan Jasa)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama produk |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang pemilik kepemilikan item barang |
| `category_id` | INT | FK -> categories.id, NULL | Kategori pengelompokan produk |
| `kode_item` | VARCHAR(50) | NOT NULL | Kode unik barcode atau penomoran inventaris toko |
| `nama_produk` | VARCHAR(150) | NOT NULL | Nama deskriptif barang jadi, menu, atau layanan jasa |
| `tipe` | ENUM | 'retail','fnb','service' | Karakteristik item yang menentukan metode pemotongan stok |
| `harga_jual` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Tarif harga jual resmi yang ditagihkan kepada konsumen |
| `hpp_manual` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga Pokok Penjualan (HPP) modal per satuan item |
| `stok` | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | Kuantitas stok barang jadi (khusus item retail) |
| `is_active` | TINYINT(1) | DEFAULT 1 | Status penjualan produk (1=Dijual, 0=Diarsipkan) |

### 6. Tabel raw_materials (Master Bahan Baku Mentah Dapur F&B)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama bahan baku mentah |
| `nama_bahan` | VARCHAR(100) | NOT NULL | Nama bahan mentah dapur (misal: Biji Kopi, Susu UHT) |
| `satuan` | VARCHAR(20) | NOT NULL | Satuan ukur takaran standar (gram, ml, butir, pcs) |
| `harga_beli_satuan` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga pembelian modal per satuan unit takaran |
| `stok_minimum` | DECIMAL(10,2) | NOT NULL, DEFAULT 5.00 | Ambang batas peringatan stok bahan mentah menipis |

### 7. Tabel branch_materials (Stok Bahan Baku Mentah per Cabang)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama relasi stok cabang |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang lokasi penyimpanan bahan mentah |
| `raw_material_id` | INT | FK -> raw_materials.id | Bahan baku mentah yang disimpan |
| `stok` | DECIMAL(10,2) | NOT NULL, DEFAULT 0.00 | Jumlah kuantitas stok fisik bahan mentah yang tersedia |

### 8. Tabel product_recipes (Resep & Formulasi Bill of Materials / BOM)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama komponen resep |
| `product_id` | INT | FK -> products.id, NOT NULL | Menu olahan kuliner yang memiliki resep takaran |
| `raw_material_id` | INT | FK -> raw_materials.id | Bahan mentah yang digunakan pada komposisi menu |
| `takaran` | DECIMAL(10,2) | NOT NULL | Besaran volume/berat bahan yang dikonsumsi per porsi menu |

### 9. Tabel shifts (Pencatatan Shift & Rekonsiliasi Kasir)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama sesi shift kasir |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang tempat sesi shift kasir berlangsung |
| `user_id` | INT | FK -> users.id, NOT NULL | Petugas kasir yang bertanggung jawab atas sesi shift |
| `waktu_buka` | DATETIME | NOT NULL | Waktu presisi pembukaan buku laci kasir |
| `waktu_tutup` | DATETIME | NULL | Waktu presisi penutupan buku dan serah terima kasir |
| `modal_awal` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nominal saldo awal kas kecil (petty cash) saat buka shift |
| `uang_sistem` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total akumulasi saldo kasir menurut perhitungan transaksi sistem |
| `uang_fisik` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total nominal uang kertas/logam riil yang dihitung kasir |
| `selisih` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Selisih rekonsiliasi kas (uang_fisik dikurangi uang_sistem) |
| `status` | ENUM | 'open','closed' | Status sesi kerja kasir (open=Berjalan, closed=Selesai) |

### 10. Tabel transactions (Header Nota Penjualan Kasir)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama transaksi penjualan |
| `nomor_nota` | VARCHAR(50) | NOT NULL, UNIQUE | Kode pengenal unik nota struk kasir (misal: TRX-202611-0001) |
| `branch_id` | INT | FK -> branches.id, NOT NULL | Cabang tempat transaksi kasir diterbitkan |
| `user_id` | INT | FK -> users.id, NOT NULL | Petugas kasir yang melayani transaksi penjualan |
| `shift_id` | INT | FK -> shifts.id, NULL | Sesi shift kerja kasir tempat transaksi dibukukan |
| `waktu` | DATETIME | NOT NULL | Waktu penerbitan nota transaksi penjualan |
| `subtotal` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Total nilai belanja sebelum potongan diskon dan pajak |
| `diskon` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Besaran potongan promosi atau potongan member |
| `pajak` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nilai pertambahan pajak toko terhitung |
| `total_akhir` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Nilai tagihan akhir bersih yang wajib dibayar konsumen |
| `uang_bayar` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Jumlah uang tunai atau nominal transfer yang diterima |
| `kembalian` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Uang kembalian yang diserahkan kembali kepada konsumen |
| `tipe_bayar` | ENUM | 'cash','qris','transfer' | Metode pembayaran transaksi kasir |
| `status` | ENUM | 'paid','hold','void' | Status nota (paid=Lunas, hold=Gantung/Meja, void=Batal) |
| `label_meja_pelanggan` | VARCHAR(100) | NULL | Nomor meja makan (F&B) atau nomor antrean kendaraan (Jasa) |

### 11. Tabel transaction_details (Rincian Item Belanja Transaksi)
| Nama Kolom | Tipe Data | Atribut | Keterangan Fungsi |
| :--- | :--- | :--- | :--- |
| `id` | INT | PK, AUTO_INCREMENT | Kunci utama baris detail item transaksi |
| `transaction_id` | INT | FK -> transactions.id | Nota transaksi induk pemilik baris belanja |
| `product_id` | INT | FK -> products.id, NOT NULL | Produk, menu, atau layanan yang dibeli konsumen |
| `qty` | DECIMAL(10,2) | NOT NULL | Banyaknya kuantitas barang yang ditransaksikan |
| `harga_satuan` | DECIMAL(12,2) | NOT NULL | Harga jual satuan produk saat nota dicetak |
| `hpp_satuan` | DECIMAL(12,2) | NOT NULL, DEFAULT 0.00 | Harga Pokok Penjualan (HPP) modal saat nota dicetak |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Total harga baris item (qty dikali harga_satuan) |

### 12. Tabel stock_transfers & stock_transfer_details (Mutasi Stok Cabang)
| Tabel / Kolom | Tipe Data | Atribut | Keterangan Fungsi Alur Mutasi |
| :--- | :--- | :--- | :--- |
| `stock_transfers.id` | INT | PK, AUTO_INCREMENT | Kunci utama berkas transfer antar-cabang |
| `nomor_transfer` | VARCHAR(50) | NOT NULL, UNIQUE | Kode dokumen jalan mutasi stok (TRF-YYYYMM-XXXX) |
| `dari_branch_id` | INT | FK -> branches.id | Cabang asal pengirim persediaan barang/bahan |
| `ke_branch_id` | INT | FK -> branches.id | Cabang tujuan penerima persediaan barang/bahan |
| `user_id` | INT | FK -> users.id | Petugas penanggung jawab pembuatan dokumen mutasi |
| `tanggal` | DATETIME | NOT NULL | Waktu penerbitan dokumen mutasi stok |
| `status` | ENUM | 'pending','completed' | Status perjalanan kiriman (pending=Jalan, completed=Diterima) |
| `detail.transfer_id` | INT | FK -> stock_transfers.id | Kunci pengait dokumen induk transfer |
| `detail.tipe_item` | ENUM | 'product','material' | Jenis item yang dimutasi (barang retail atau bahan mentah) |
| `detail.item_id` | INT | NOT NULL | ID pengenal item produk atau bahan mentah yang dimutasi |
| `detail.qty` | DECIMAL(10,2) | NOT NULL | Volume/kuantitas persediaan yang dipindahkan |

## 3.4 Alur Logika Bisnis Kritis & Transaksi Atomik
Keandalan perangkat lunak kasir bertumpu pada pencegahan inkonsistensi data ketika sistem memproses transaksi multi-item. Penyimpanan transaksi penjualan diimplementasikan menggunakan blok transaksi atomik `MySqlTransaction`. Saat kasir menekan tombol Simpan atau Bayar, sistem menjalankan urutan operasi basis data berikut di dalam satu transaksi utuh:
1. **Penyimpanan Header Transaksi**: Perintah `INSERT` dieksekusi pada tabel `transactions` untuk menyimpan nomor nota unik, total belanja, potongan harga, metode pembayaran, serta identitas kasir yang bertugas.
2. **Penyimpanan Rincian Item**: Seluruh item belanja pada keranjang kasir di-iterasi dan dimasukkan ke tabel `transaction_details` lengkap dengan nilai `harga_satuan` dan nilai `hpp_satuan` riil saat itu.
3. **Pemotongan Stok Kondisional Atomik**: Untuk setiap item belanja, sistem memeriksa tipe item. Jika item bertipe retail, perintah `UPDATE` memotong kolom stok pada tabel `products` di cabang terkait. Jika item bertipe fnb, sistem membaca formulasi resep pada `product_recipes` dan mengeksekusi `UPDATE` untuk memotong persediaan takaran bahan baku mentah pada `branch_materials` secara proporsional. Jika item bertipe service, proses pemotongan stok dilewati.
4. **Commit atau Rollback**: Jika seluruh perintah eksekusi berhasil tanpa ada kendala kekurangan kuantitas stok atau kendala kegagalan jaringan, transaksi diresmikan via perintah `Commit()`. Sebaliknya, jika salah satu item mengalami galat (error), transaksi langsung di-`Rollback()` secara keseluruhan, sehingga tidak ada data nota separuh jadi yang mengotori basis data.

---

# BAB IV RENCANA PEMBAGIAN TUGAS & JADWAL KERJA TIM

## 4.1 Matriks Rencana Pembagian Tugas 6 Anggota Tim
Untuk memaksimalkan efektivitas pengerjaan proyek akhir dan memastikan seluruh anggota tim memiliki tanggung jawab kode yang terdistribusi secara adil, tanggung jawab pengembangan dibagi menjadi enam modul independen berbasis pembagian arsitektur 3-Tier:

| NRP | Nama Anggota | Peran / Modul Tanggung Jawab | Ruang Lingkup Pengerjaan Modul |
| :---: | :--- | :--- | :--- |
| **225310690** | Bagas Rizky Putra Wardana | Modul 1: Autentikasi & Konfigurasi | Mengembangkan LoginForm, OnboardingWizardForm, AuthService (hashing SHA-256), OnboardingService, dan manajemen cabang usaha (BranchRepository). |
| **225310691** | FX Thiarnika Eka Atur Rangga | Modul 2: Master Data & Resep BOM | Mengembangkan UcMasterProduk, UcResepBOM, RecipeService, manajemen bahan mentah dapur, dan kalkulasi otomatis Harga Pokok Penjualan (HPP). |
| **225310692** | Gregorius Priyagung | Modul 3: Kasir & Transaksi | Mengembangkan UcKasir, katalog pencarian produk, keranjang belanja, mode Bayar Langsung, mode Hold Bill (pesanan meja), dan cetak struk nota. |
| **225310693** | Moreno Hernakov | Modul 4: Inventaris & Stok Cabang | Mengembangkan UcInventaris, InventoryService, modul restock barang masuk, stock opname fisik, dan transfer stok antar-cabang. |
| **225310694** | Raymond Sugiharto | Modul 5: Operasional Kasir & Layanan | Mengembangkan UcShift, ShiftService (buka modal awal petty cash & tutup kasir blind close), manajemen pelanggan/member, dan status pengerjaan antrean jasa. |
| **225310695** | Valencia Angie Kurniawan | Modul 6: Laporan & Analitik | Mengembangkan UcLaporan, ReportService, visualisasi dashboard produk terlaris, laporan laba kotor harian/bulanan, dan kartu riwayat mutasi stok. |

## 4.2 Kolaborasi Tim, Integrasi Repositori, & Kendali Mutu
Kolaborasi teknis tim dijalankan dengan menerapkan standar rekayasa perangkat lunak yang ketat:
1. **Standar Antarmuka 3-Tier**: Setiap anggota tim wajib mematuhi pemisahan lapisan. Kode pada UserControl dilarang menulis perintah SQL mentah (seperti `SELECT` atau `INSERT`). Seluruh pemanggilan basis data harus didelegasikan ke kelas Service dan Repository.
2. **Pemeriksaan Kode (*Code Review*)**: Integrasi modul ke dalam solusi proyek utama (`MainForm`) dilakukan bersama oleh seluruh anggota tim guna memverifikasi penamaan variabel, penanganan eksepsi (*try-catch*), dan ketiadaan kebocoran koneksi basis data (seluruh koneksi wajib dibungkus blok `using`).
3. **Pengujian Transaksi Basis Data**: Pengujian fungsi transaksi kasir dan mutasi persediaan wajib diverifikasi menggunakan kasus uji transaksi gagal untuk membuktikan keandalan fitur *Rollback* pada `MySqlTransaction`.

## 4.3 Linimasa & Tahapan Pengerjaan Proyek (6 Minggu)
Rencana pengerjaan proyek akhir terbagi ke dalam enam tahapan mingguan terukur hingga pelaksanaan demonstrasi evaluasi UAS:

| Minggu | Tahapan Pengerjaan | Fokus Aktivitas Utama | Target Luaran / Deliverables |
| :---: | :--- | :--- | :--- |
| **Minggu 1** | Analisis & Skema Basis Data | Penyusunan proposal, spesifikasi arsitektur sistem, dan pembuatan skrip DDL SQL 12 tabel. | Dokumen proposal resmi & skrip basis data MySQL. |
| **Minggu 2** | Infrastruktur & Modul 1-2 | Setup project Visual Studio 2022 (.NET 4.7.2), DbHelper ADO.NET, LoginForm, Onboarding Wizard, dan Master Data. | Pondasi arsitektur 3-tier, form autentikasi, dan katalog master data. |
| **Minggu 3** | Modul Resep BOM & Kasir | Implementasi relasi product_recipes, kalkulasi HPP otomatis, form kasir dual-mode, dan cetak nota struk. | Mesin HPP berjalan dan transaksi kasir dapat menyimpan nota. |
| **Minggu 4** | Inventaris & Shift Kasir | Implementasi restock bahan, stock opname fisik, mutasi antar-cabang, dan alur kerja shift kasir blind close. | Pemotongan stok dapur otomatis dan rekonsiliasi kasir. |
| **Minggu 5** | Pelaporan & Dashboard | Pengembangan modul analitik omzet, laporan laba kotor (omzet minus HPP), kartu stok, dan antrean jasa. | Laporan keuangan lengkap dan dashboard visual. |
| **Minggu 6** | Uji Coba & Finalisasi | Pengujian integrasi menyeluruh, pembersihan bug, uji coba transaksi atomik, dan penyusunan laporan akhir UAS. | Aplikasi siap demonstrasi dan naskah laporan lengkap. |

---

# BAB V PENUTUP

## 5.1 Kesimpulan
Omni-Industry Configurable POS Engine dihadirkan sebagai jawaban atas tantangan operasional kasir dan manajemen inventaris pada bisnis multi-sektor yang membutuhkan fleksibilitas tinggi tanpa mengorbankan kesederhanaan arsitektur sistem. Dengan memanfaatkan arsitektur 3-Tier yang kokoh pada platform C# Windows Forms dan basis data MySQL terpusat, sistem mampu memisahkan antarmuka pengguna, logika bisnis, dan akses data secara tertib. Keberadaan Onboarding Wizard berbasis saklar konfigurasi (*feature flags*) memungkinkan aplikasi bertransformasi secara instan memenuhi kebutuhan spesifik sektor ritel, restoran kuliner F&B, dan layanan jasa tanpa memerlukan perubahan struktur kode.

Inovasi formulasi *Bill of Materials* (BOM) pada modul kuliner berhasil menghubungkan menu sajian dengan persediaan bahan baku mentah dapur secara proporsional sekaligus menghitung Harga Pokok Penjualan (HPP) secara otomatis. Ditambah dengan dukungan transaksi atomik `MySqlTransaction` pada alur transaksi kasir *dual-mode* dan transfer stok antar-cabang, serta akuntabilitas rekonsiliasi shift kasir melalui metode *blind close*, perangkat lunak ini dirancang untuk memberikan keandalan data transaksi bisnis yang tinggi.

## 5.2 Harapan Capaian
Melalui penyusunan proposal dan pelaksanaan proyek akhir ini, tim pengembang berharap dapat menghasilkan aplikasi Point of Sales desktop yang fungsional, andal, dan siap dioperasikan dalam lingkungan kerja nyata. Implementasi proyek ini diharapkan dapat menjadi tolak ukur pemahaman praktis mahasiswa dalam menerapkan konsep pemrograman visual berbasis event, arsitektur perangkat lunak 3-Tier, keamanan basis data *parameterized query*, dan kerja sama tim yang terstruktur sesuai dengan standar kompetensi akademik Program Studi S1 Informatika di Institut Sains dan Teknologi Terpadu Surabaya.
"""
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md_content.strip() + "\n")
    print(f"Berhasil menghasilkan dokumen Markdown: {MD_OUT}")


if __name__ == "__main__":
    build_proposal()
    build_markdown_proposal()
