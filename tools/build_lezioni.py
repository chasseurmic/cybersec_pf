#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_lezioni.py - rende i documenti Word (Dispensa + Manuale) di tutte le
lezioni che hanno una sorgente in tools/lezioni_src/lezNN.py.

Ogni sorgente lezNN.py espone:
  NUM     int      numero lezione
  SLUG    str      slug per il nome file (kebab-case, niente apostrofi)
  TITOLO  str      titolo esteso (usato nell'intestazione)
  dispensa(d)      riempie il Doc della dispensa studenti
  manuale(d)       riempie il Doc del manuale docente

Uso:
  python3 tools/build_lezioni.py            # rende tutte le lezioni trovate
  python3 tools/build_lezioni.py 4 5 12     # rende solo le lezioni indicate
"""
import os
import sys
import importlib
import zipfile
import xml.dom.minidom as minidom

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "lezioni_src")
OUTDIR = os.path.join(HERE, "..", "lezioni", "Lezioni")
sys.path.insert(0, HERE)
sys.path.insert(0, SRC)

import docxgen  # noqa: E402


def valida(path):
    """Controllo minimo: zip integro e ogni parte XML ben formata."""
    z = zipfile.ZipFile(path)
    if z.testzip() is not None:
        raise RuntimeError("zip corrotto: %s" % path)
    for n in z.namelist():
        if n.endswith(".xml") or n.endswith(".rels"):
            minidom.parseString(z.read(n))
    return True


def rendi(mod):
    num = "%02d" % mod.NUM
    header = "Lezione %d · %s" % (mod.NUM, mod.TITOLO)
    # Dispensa
    d = docxgen.Doc("Lezione %d - %s" % (mod.NUM, mod.TITOLO))
    d.titolo = header  # header con il middot; core.xml usa il trattino
    d.body = []
    d._intestazione()
    mod.dispensa(d)
    p1 = os.path.join(OUTDIR, "Lezione-%s-%s-Dispensa.docx" % (num, mod.SLUG))
    d.save(p1)
    valida(p1)
    # Manuale
    m = docxgen.Doc("Lezione %d - %s (Manuale docente)" % (mod.NUM, mod.TITOLO))
    m.titolo = header + "  ·  Manuale docente"
    m.body = []
    m._intestazione()
    mod.manuale(m)
    p2 = os.path.join(OUTDIR, "Lezione-%s-%s-Manuale.docx" % (num, mod.SLUG))
    m.save(p2)
    valida(p2)
    return p1, p2


def main(argv):
    voluti = set(int(x) for x in argv) if argv else None
    trovati = []
    for fn in sorted(os.listdir(SRC)) if os.path.isdir(SRC) else []:
        if fn.startswith("lez") and fn.endswith(".py") and fn != "__init__.py":
            trovati.append(fn[:-3])
    if not trovati:
        print("Nessuna sorgente in %s" % SRC)
        return 0
    n = 0
    for name in trovati:
        mod = importlib.import_module(name)
        if voluti and mod.NUM not in voluti:
            continue
        p1, p2 = rendi(mod)
        print("[OK] L%02d  %s" % (mod.NUM, os.path.basename(p1)))
        print("[OK] L%02d  %s" % (mod.NUM, os.path.basename(p2)))
        n += 1
    print("Reso/i %d documento/i-lezione (%d file .docx)." % (n, n * 2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
