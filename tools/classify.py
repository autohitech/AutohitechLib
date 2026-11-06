#!/usr/bin/env python3
"""Classify footprint variants: FORMAT-ONLY vs REAL (pads+layers+bbox)."""
import re
import glob
import os
import sys
from collections import defaultdict

os.chdir('/tmp/AutohitechLib/Autohitech.pretty')
groups = defaultdict(list)
for f in glob.glob('*.kicad_mod'):
    base = f[:-len('.kicad_mod')]
    if '__' in base:
        n, tag = base.rsplit('__', 1)
    else:
        n, tag = base, None
    groups[n].append((f, tag))


def pads(t):
    out = []
    for m in re.finditer(
            r'\(pad\s+"?([^"\s]+)"?\s+(\S+)\s+(\S+)\s+(\([^)]*\)\s+)?'
            r'\(at\s+([-\d.]+)\s+([-\d.]+)', t):
        num, typ, sh, _, x, y = m.groups()
        seg = t[m.start():m.start() + 800]
        layers = re.findall(r'\(layer "([^"]+)"', seg[:seg.find('(at') + 200] if '(at' in seg else seg)
        lay = layers[0] if layers else '?'
        out.append((num, typ, sh, lay, round(float(x), 3), round(float(y), 3)))
    return sorted(out)


for n in sorted(groups):
    if len(groups[n]) < 2:
        continue
    ps = [(f, tag, pads(open(f, encoding='utf-8', errors='replace').read()))
          for f, tag in sorted(groups[n])]
    sigs = set()
    for _, _, plist in ps:
        sigs.add(tuple((p[0], p[1], p[2], p[4], p[5]) for p in plist))
    # layer-aware signature
    lsigs = set()
    for _, _, plist in ps:
        lsigs.add(tuple((p[0], p[1], p[2], p[3], p[4], p[5]) for p in plist))
    if len(sigs) == 1 and len(lsigs) == 1:
        print(f'{n}: FORMAT-ONLY ({len(ps)} variants, {len(ps[0][2])} pads identical incl. layers)')
    elif len(sigs) == 1:
        print(f'{n}: SIDE-ONLY {[(t, len(p)) for _, t, p in ps]}')
    else:
        print(f'{n}: REAL {[(t, len(p)) for _, t, p in ps]}')
