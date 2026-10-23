# -*- coding: utf-8 -*-
"""Validate DOCX paragraph/run property child ordering and re-extract text."""
import sys
import zipfile
from lxml import etree

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}

PPR_ORDER = """pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr
suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct
topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind
contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment
textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange""".split()

RPR_ORDER = """rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow
emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz
szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout
specVanish oMath""".split()

PATH = "DeepSeek-大模型算法工程师-简历.docx"
errors = []

with zipfile.ZipFile(PATH) as z:
    for name in ("word/document.xml", "word/footer1.xml", "word/styles.xml"):
        try:
            root = etree.fromstring(z.read(name))
        except KeyError:
            print("missing part:", name)
            continue
        for tag, order in (("pPr", PPR_ORDER), ("rPr", RPR_ORDER)):
            for el in root.iter("{%s}%s" % (W, tag)):
                kids = [etree.QName(c).localname for c in el if isinstance(c.tag, str)]
                idx = []
                for k in kids:
                    if k not in order:
                        errors.append("%s %s: unknown child %s" % (name, tag, k))
                        idx.append(None)
                    else:
                        idx.append(order.index(k))
                seq = [i for i in idx if i is not None]
                if seq != sorted(seq):
                    parent = etree.QName(el.getparent()).localname
                    errors.append("%s %s (in %s): bad order %s" % (name, tag, parent, kids))

print("order errors:", len(errors))
for e in errors[:20]:
    print(" -", e)

# reopen with python-docx and dump text
from docx import Document

d = Document(PATH)
paras = [p.text for p in d.paragraphs]
print("paragraphs:", len(paras), "| chars:", sum(len(t) for t in paras))
print("sections:", len(d.sections), "| footer:", d.sections[0].footer.paragraphs[0].text)
print("first:", paras[0], "|", paras[1])
print("last:", paras[-1][:60])
