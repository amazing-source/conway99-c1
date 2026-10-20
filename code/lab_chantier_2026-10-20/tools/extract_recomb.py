"""Extract every 'Matériaux pour la recombinaison' section of the fiches into one file (verbatim, with origin lines).
usage: python extract_recomb.py <fiches dir> <out.md>"""
import os
import re
import sys

HDR = re.compile(r"^(#+)\s")


def sections(lines):
    out = []
    for i, l in enumerate(lines):
        m = HDR.match(l)
        if m and "recombinaison" in l.lower():
            lvl = len(m.group(1))
            j = i + 1
            while j < len(lines):
                m2 = HDR.match(lines[j])
                if m2 and len(m2.group(1)) <= lvl:
                    break
                j += 1
            out.append((i, j))
    # drop sections nested inside an earlier extracted one
    keep = []
    for a, b in out:
        if not any(a0 < a and b <= b0 for a0, b0 in out):
            keep.append((a, b))
    return keep


def main():
    d, out = sys.argv[1], sys.argv[2]
    total = 0
    with open(out, "w", encoding="utf-8") as f:
        f.write("# Matériaux pour la recombinaison : extraits bruts des fiches (copie verbatim)\n\n")
        f.write("Chaque bloc renvoie à fiches/<lot>.md:<lignes>. Les statuts et sources sont ceux des fiches.\n\n")
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            lines = open(os.path.join(d, fn), encoding="utf-8").read().splitlines()
            for a, b in sections(lines):
                f.write("\n\n<!-- ===== %s:%d-%d ===== -->\n\n" % (fn, a + 1, b))
                f.write("\n".join(lines[a:b]) + "\n")
                total += b - a
                print("%-34s lignes %5d-%5d  (%d)" % (fn, a + 1, b, b - a))
    print("total lignes", total)


if __name__ == "__main__":
    main()
