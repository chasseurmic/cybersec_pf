# -*- coding: utf-8 -*-
"""
docxgen.py - generatore .docx condiviso per il corso cybersec_pf.

Sola libreria standard di Python (zipfile), nessuna dipendenza esterna.
Produce documenti Word con lo stile grafico gia' usato nelle Lezioni 2 e 3:
intestazione col titolo, riquadri colorati con bordo di accento, blocchi di
codice su sfondo scuro, tabelle a righe alternate.

Palette (obbligatoria dal brief):
  blu   1F3A5F   verde 2E7D32   rosso B71C1C

API sintetica (vedi la classe Doc):
  d = Doc("Lezione 4 - ...", "Sottotitolo")
  d.h1("Parte 1 - ...")
  d.h2("..."); d.h3("...")
  d.p("testo con **grassetto** e `codice inline`")
  d.bullets(["voce", "voce"])
  d.numbered(["passo", "passo"])
  d.box("blu", "In breve", ["riga", "riga"])
  d.code(["comando 1", "# commento", "comando 2"])
  d.table(["Col A", "Col B"], [["1","2"],["3","4"]], widths=[3000,6026])
  d.save("percorso/file.docx")

Formattazione inline nel testo: **grassetto**  e  `codice`.
"""
import os
import re
import zipfile
import datetime

# ---- Palette e costanti di stile -------------------------------------------
BLU = "1F3A5F"
VERDE = "2E7D32"
ROSSO = "B71C1C"
GRIGIO = "5A5A5A"
CODE_BG = "1E1E1E"
CODE_FG = "D4F0C0"
CODE_COMMENT = "8FA8B2"
ROW_ALT = "F0F0F0"
BORDER_LIGHT = "BBBBBB"
BORDER_INNER = "DDDDDD"
FONT = "Calibri"
MONO = "Consolas"
TABLE_W = 9026  # larghezza tabelle/riquadri in dxa (coerente con L2/L3)

# fill chiaro per i riquadri, per colore di accento
BOX_FILL = {
    "blu": "EAF1F8",
    "verde": "E7F3E8",
    "rosso": "FBEAEA",
    "grigio": "F0F0F0",
}
BOX_ACCENT = {
    "blu": BLU,
    "verde": VERDE,
    "rosso": ROSSO,
    "grigio": GRIGIO,
}


def esc(s):
    """Escape per un nodo di testo XML."""
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace('"', "&quot;").replace("'", "&apos;")
    return s


def _rpr(bold=False, italic=False, color=None, size=None, mono=False,
         shade=None, spacing=None):
    """Costruisce un blocco <w:rPr>."""
    font = MONO if mono else FONT
    out = ["<w:rPr>"]
    out.append('<w:rFonts w:ascii="%s" w:cs="%s" w:eastAsia="%s" w:hAnsi="%s"/>'
               % (font, font, font, font))
    if bold:
        out.append("<w:b/><w:bCs/>")
    if italic:
        out.append("<w:i/><w:iCs/>")
    if color:
        out.append('<w:color w:val="%s"/>' % color)
    if spacing is not None:
        out.append('<w:spacing w:val="%d"/>' % spacing)
    if shade:
        out.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    if size:
        out.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    out.append("</w:rPr>")
    return "".join(out)


# regex per la formattazione inline: **bold**  e  `code`
_INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`)")


def _runs_inline(text, base_color=None, base_size=None):
    """Trasforma un testo con **grassetto** e `codice` in una sequenza di run."""
    parts = _INLINE.split(text)
    runs = []
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            inner = part[2:-2]
            runs.append("<w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r>"
                        % (_rpr(bold=True, color=base_color, size=base_size),
                           esc(inner)))
        elif part.startswith("`") and part.endswith("`"):
            inner = part[1:-1]
            runs.append("<w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r>"
                        % (_rpr(mono=True, color=BLU, size=base_size,
                                shade="EFEFEF"), esc(inner)))
        else:
            runs.append("<w:r>%s<w:t xml:space=\"preserve\">%s</w:t></w:r>"
                        % (_rpr(color=base_color, size=base_size), esc(part)))
    return "".join(runs)


class Doc:
    def __init__(self, titolo, sottotitolo=None,
                 corso="CORSO DI SICUREZZA INFORMATICA"):
        self.titolo = titolo
        self.sottotitolo = sottotitolo
        self.corso = corso
        self.body = []
        self._intestazione()

    # ---- intestazione della prima pagina -----------------------------------
    def _intestazione(self):
        b = self.body
        # riga occhiello
        b.append(
            '<w:p><w:pPr><w:spacing w:after="40"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (_rpr(bold=True, color=GRIGIO, size=20, spacing=20),
               esc(self.corso)))
        # titolo con riga blu sotto
        b.append(
            '<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:color="%s" '
            'w:sz="12" w:space="6"/></w:pBdr><w:spacing w:after="40"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (BLU, _rpr(bold=True, color=BLU, size=36), esc(self.titolo)))
        # sottotitolo
        sub = self.sottotitolo or ("Progetto Formazione S.c.r.l. · Progetto "
                                   "P145 · Terzo anno informatico · a.f. "
                                   "2026/27 · Docente: Michelangelo Chasseur")
        b.append(
            '<w:p><w:pPr><w:spacing w:after="200"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (_rpr(italic=True, color=GRIGIO, size=18), esc(sub)))

    # ---- titoli -------------------------------------------------------------
    def h1(self, text):
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Heading1"/><w:pBdr><w:bottom '
            'w:val="single" w:color="%s" w:sz="8" w:space="4"/></w:pBdr>'
            '<w:spacing w:after="140" w:before="260"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (BLU, _rpr(bold=True, color=BLU, size=30), esc(text)))

    def h2(self, text):
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Heading2"/>'
            '<w:spacing w:after="100" w:before="200"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (_rpr(bold=True, color=VERDE, size=25), esc(text)))

    def h3(self, text):
        self.body.append(
            '<w:p><w:pPr><w:pStyle w:val="Heading3"/>'
            '<w:spacing w:after="60" w:before="140"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (_rpr(bold=True, color=BLU, size=22), esc(text)))

    # ---- paragrafi e liste --------------------------------------------------
    def p(self, text, after=120):
        self.body.append(
            '<w:p><w:pPr><w:spacing w:after="%d" w:line="264"/></w:pPr>%s</w:p>'
            % (after, _runs_inline(text)))

    def bullets(self, items):
        for it in items:
            self.body.append(
                '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr>'
                '<w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
                '<w:spacing w:after="60" w:line="264"/></w:pPr>%s</w:p>'
                % _runs_inline(it))

    def numbered(self, items):
        for it in items:
            self.body.append(
                '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr>'
                '<w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'
                '<w:spacing w:after="60" w:line="264"/></w:pPr>%s</w:p>'
                % _runs_inline(it))

    # ---- riquadro colorato con bordo di accento a sinistra ------------------
    def box(self, color, title, items=None, intro=None, numbered=False):
        accent = BOX_ACCENT.get(color, BLU)
        fill = BOX_FILL.get(color, BOX_FILL["blu"])
        inner = []
        if title:
            inner.append(
                '<w:p><w:pPr><w:spacing w:after="80"/></w:pPr>'
                '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
                % (_rpr(bold=True, color=accent, size=24), esc(title)))
        if intro:
            inner.append(
                '<w:p><w:pPr><w:spacing w:after="80" w:line="264"/></w:pPr>%s</w:p>'
                % _runs_inline(intro))
        for it in (items or []):
            nid = 2 if numbered else 1
            inner.append(
                '<w:p><w:pPr><w:pStyle w:val="ListParagraph"/><w:numPr>'
                '<w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>'
                '<w:spacing w:after="60" w:line="264"/></w:pPr>%s</w:p>'
                % (nid, _runs_inline(it)))
        body = "".join(inner)
        self.body.append(
            '<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="%d"/><w:tblBorders>'
            '<w:top w:val="single" w:color="%s" w:sz="8"/>'
            '<w:left w:val="single" w:color="%s" w:sz="18"/>'
            '<w:bottom w:val="single" w:color="%s" w:sz="8"/>'
            '<w:right w:val="single" w:color="%s" w:sz="8"/>'
            '<w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>'
            '</w:tblPr><w:tblGrid><w:gridCol w:w="%d"/></w:tblGrid>'
            '<w:tr><w:tc><w:tcPr><w:tcW w:type="dxa" w:w="%d"/>'
            '<w:shd w:fill="%s" w:val="clear"/><w:tcMar>'
            '<w:top w:type="dxa" w:w="120"/><w:left w:type="dxa" w:w="160"/>'
            '<w:bottom w:type="dxa" w:w="120"/><w:right w:type="dxa" w:w="160"/>'
            '</w:tcMar></w:tcPr>%s</w:tc></w:tr></w:tbl>'
            '<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>'
            % (TABLE_W, accent, accent, accent, accent, TABLE_W, TABLE_W,
               fill, body))

    # ---- blocco di codice su sfondo scuro -----------------------------------
    def code(self, lines):
        if isinstance(lines, str):
            lines = lines.split("\n")
        runs = []
        first = True
        for ln in lines:
            col = CODE_COMMENT if ln.strip().startswith("#") else CODE_FG
            br = "" if first else "<w:br/>"
            runs.append(
                '<w:r>%s%s<w:t xml:space="preserve">%s</w:t></w:r>'
                % (_rpr(mono=True, color=col, size=19), br, esc(ln)))
            first = False
        self.body.append(
            '<w:p><w:pPr><w:pBdr>'
            '<w:top w:val="single" w:color="%s" w:sz="4" w:space="6"/>'
            '<w:bottom w:val="single" w:color="%s" w:sz="4" w:space="6"/>'
            '<w:left w:val="single" w:color="%s" w:sz="4" w:space="8"/>'
            '<w:right w:val="single" w:color="%s" w:sz="4" w:space="8"/></w:pBdr>'
            '<w:shd w:fill="%s" w:val="clear"/>'
            '<w:spacing w:after="120" w:before="60"/></w:pPr>%s</w:p>'
            % (CODE_BG, CODE_BG, CODE_BG, CODE_BG, CODE_BG, "".join(runs)))

    # ---- tabella a righe alternate ------------------------------------------
    def table(self, headers, rows, widths=None):
        n = len(headers)
        if not widths:
            w = TABLE_W // n
            widths = [w] * (n - 1) + [TABLE_W - w * (n - 1)]
        grid = "".join('<w:gridCol w:w="%d"/>' % x for x in widths)

        def cell(txt, wdt, shade, bold=False, color=None, header=False):
            size = 20 if header else 20
            rpr = _rpr(bold=bold, color=color, size=size)
            return (
                '<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="%d"/>'
                '<w:shd w:fill="%s" w:val="clear"/><w:tcMar>'
                '<w:top w:type="dxa" w:w="60"/><w:left w:type="dxa" w:w="100"/>'
                '<w:bottom w:type="dxa" w:w="60"/><w:right w:type="dxa" w:w="100"/>'
                '</w:tcMar><w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:spacing w:after="0" w:line="252"/></w:pPr>%s</w:p>'
                '</w:tc>' % (wdt, shade, _runs_inline(txt, base_color=color,
                                                      base_size=size)
                            if not (bold or header) else
                            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                            % (rpr, esc(txt))))

        out = [
            '<w:tbl><w:tblPr><w:tblW w:type="dxa" w:w="%d"/><w:tblBorders>'
            '<w:top w:val="single" w:color="%s" w:sz="4"/>'
            '<w:left w:val="single" w:color="%s" w:sz="4"/>'
            '<w:bottom w:val="single" w:color="%s" w:sz="4"/>'
            '<w:right w:val="single" w:color="%s" w:sz="4"/>'
            '<w:insideH w:val="single" w:color="%s" w:sz="4"/>'
            '<w:insideV w:val="single" w:color="%s" w:sz="4"/></w:tblBorders>'
            '</w:tblPr><w:tblGrid>%s</w:tblGrid>'
            % (TABLE_W, BORDER_LIGHT, BORDER_LIGHT, BORDER_LIGHT, BORDER_LIGHT,
               BORDER_INNER, BORDER_INNER, grid)]
        # riga intestazione
        out.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>')
        for i, h in enumerate(headers):
            out.append(cell(h, widths[i], BLU, bold=True, color="FFFFFF",
                            header=True))
        out.append("</w:tr>")
        # righe dati (alternate)
        for r, row in enumerate(rows):
            shade = ROW_ALT if r % 2 == 1 else "FFFFFF"
            out.append("<w:tr>")
            for i in range(n):
                val = row[i] if i < len(row) else ""
                out.append(cell(val, widths[i], shade))
            out.append("</w:tr>")
        out.append("</w:tbl>")
        out.append('<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>')
        self.body.append("".join(out))

    def spacer(self, after=120):
        self.body.append('<w:p><w:pPr><w:spacing w:after="%d"/></w:pPr></w:p>'
                         % after)

    # ---- salvataggio --------------------------------------------------------
    def _document_xml(self):
        sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838" '
                'w:orient="portrait"/><w:pgMar w:top="1134" w:right="1134" '
                'w:bottom="1134" w:left="1134" w:header="708" w:footer="708" '
                'w:gutter="0"/><w:docGrid w:linePitch="360"/></w:sectPr>')
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/'
            'wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats'
            '.org/officeDocument/2006/relationships"><w:body>%s%s</w:body>'
            '</w:document>' % ("".join(self.body), sect))

    def save(self, path):
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        parts = _skeleton(self.titolo, now)
        parts["word/document.xml"] = self._document_xml()
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            for name, data in parts.items():
                z.writestr(name, data)
        return path


# ---- scheletro minimo e valido del pacchetto .docx -------------------------
def _skeleton(title, now):
    ct = ('<?xml version="1.0" encoding="UTF-8"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
          'content-types">'
          '<Default ContentType="application/vnd.openxmlformats-package.'
          'relationships+xml" Extension="rels"/>'
          '<Default ContentType="application/xml" Extension="xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-officedocument'
          '.wordprocessingml.document.main+xml" PartName="/word/document.xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-officedocument'
          '.wordprocessingml.styles+xml" PartName="/word/styles.xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-officedocument'
          '.wordprocessingml.numbering+xml" PartName="/word/numbering.xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-officedocument'
          '.wordprocessingml.settings+xml" PartName="/word/settings.xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-package.core-'
          'properties+xml" PartName="/docProps/core.xml"/>'
          '<Override ContentType="application/vnd.openxmlformats-officedocument'
          '.extended-properties+xml" PartName="/docProps/app.xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            '2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/'
            'package/2006/relationships/metadata/core-properties" '
            'Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/extended-properties" '
            'Target="docProps/app.xml"/></Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
             '2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
             'officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/'
             'officeDocument/2006/relationships/numbering" '
             'Target="numbering.xml"/>'
             '<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/'
             'officeDocument/2006/relationships/settings" '
             'Target="settings.xml"/></Relationships>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:styles xmlns:w="http://schemas.openxmlformats.org/'
              'wordprocessingml/2006/main"><w:docDefaults><w:rPrDefault><w:rPr>'
              '<w:rFonts w:ascii="Calibri" w:cs="Calibri" w:eastAsia="Calibri" '
              'w:hAnsi="Calibri"/><w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr>'
              '</w:rPrDefault><w:pPrDefault/></w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
              '<w:name w:val="Normal"/><w:qFormat/></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading1"><w:name '
              'w:val="Heading 1"/><w:basedOn w:val="Normal"/><w:next '
              'w:val="Normal"/><w:qFormat/><w:rPr><w:color w:val="1F3A5F"/>'
              '<w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading2"><w:name '
              'w:val="Heading 2"/><w:basedOn w:val="Normal"/><w:next '
              'w:val="Normal"/><w:qFormat/><w:rPr><w:color w:val="1F3A5F"/>'
              '<w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="Heading3"><w:name '
              'w:val="Heading 3"/><w:basedOn w:val="Normal"/><w:next '
              'w:val="Normal"/><w:qFormat/><w:rPr><w:color w:val="1F4D78"/>'
              '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
              '<w:style w:type="paragraph" w:styleId="ListParagraph"><w:name '
              'w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:qFormat/>'
              '</w:style></w:styles>')
    numbering = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:numbering xmlns:w="http://schemas.openxmlformats.org/'
        'wordprocessingml/2006/main">'
        '<w:abstractNum w:abstractNumId="1"><w:multiLevelType '
        'w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/>'
        '<w:numFmt w:val="bullet"/><w:lvlText w:val="&#9679;"/><w:lvlJc '
        'w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
        '</w:lvl></w:abstractNum>'
        '<w:abstractNum w:abstractNumId="2"><w:multiLevelType '
        'w:val="hybridMultilevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/>'
        '<w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc '
        'w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
        '</w:lvl></w:abstractNum>'
        '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>'
        '<w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>'
        '</w:numbering>')
    settings = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<w:settings xmlns:w="http://schemas.openxmlformats.org/'
                'wordprocessingml/2006/main"><w:compat><w:compatSetting '
                'w:val="15" w:name="compatibilityMode" w:uri="http://schemas.'
                'microsoft.com/office/word"/></w:compat></w:settings>')
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/'
            'package/2006/metadata/core-properties" xmlns:dc="http://purl.org/'
            'dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>%s</dc:title><dc:creator>Corso di Sicurezza '
            'Informatica</dc:creator><cp:revision>1</cp:revision>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
            '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified>'
            '</cp:coreProperties>' % (esc(title), now, now))
    app = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
           '<Properties xmlns="http://schemas.openxmlformats.org/'
           'officeDocument/2006/extended-properties"><Application>'
           'cybersec_pf docxgen</Application></Properties>')
    return {
        "[Content_Types].xml": ct,
        "_rels/.rels": rels,
        "word/_rels/document.xml.rels": drels,
        "word/styles.xml": styles,
        "word/numbering.xml": numbering,
        "word/settings.xml": settings,
        "docProps/core.xml": core,
        "docProps/app.xml": app,
    }
