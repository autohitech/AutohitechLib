#!/usr/bin/env python3
"""Compare copper geometry of footprint variants (pads + Cu drawings)."""
import re
import glob
import os
import sys
from collections import defaultdict


def blocks(text):
    """Yield all balanced paren blocks with their head token."""
    out = []
    depth = 0
    start = None
    in_str = False
    esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == '(':
            if depth >= 1 and start is None:
                pass
            depth += 1
            if depth == 2 and start is None:
                # record every depth>=2 block start; simpler: track stack
                pass
        elif ch == ')':
            depth -= 1
    return out


def children(text):
    """Top-level children spans of one S-expr's inner content."""
    depth = 0
    start = None
    in_str = False
    esc = False
    kids = []
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == '(':
            depth += 1
            if depth == 1:
                start = i
        elif ch == ')':
            if depth == 1 and start is not None:
                kids.append((start, i + 1))
                start = None
            depth -= 1
    assert depth == 0, f'unbalanced: {depth}'
    return kids

def copper_sig(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    inner = text[text.find('(') + 1:text.rfind(')')]
    modlayer = re.search(r'\(\s*module\s+\S+\s+\(layer\s+([^)]+)\)', text)
    modlayer = modlayer.group(1) if modlayer else None
    sig = []
    for ss, se in children(inner):
        blk = inner[ss:se]
        m = re.match(r'\(\s*([^\s()]+)', blk)
        if not m:
            continue
        head = m.group(1)
        if head == 'pad':
            # normalize: drop tstamp/uuid/locked/path, round numbers
            b = re.search(r'\(pad.*', blk, re.S).group(0)
            b = re.sub(r'\(tstamp [^)]*\)', '', b)
            b = re.sub(r'\(uuid "[^"]*"\)', '', b)
            b = re.sub(r'\blocked\b', '', b)
            b = b.replace('"', '')
            b = re.sub(r'\(remove_unused_layers [^)]*\)', '', b)
            if '(layers' not in b and modlayer:
                b += f' (layers {modlayer})'
            b = re.sub(r'-?\d+\.\d+', lambda mo: str(round(float(mo.group(0)), 3)), b)
            b = re.sub(r'\s+', ' ', b).strip()
            b = re.sub(r'\s+\)', ')', b)
            sig.append(('pad', b))
        elif head in ('fp_line', 'fp_arc', 'fp_circle', 'fp_poly'):
            if 'F.Cu' in blk or 'B.Cu' in blk:
                b = re.sub(r'\(tstamp [^)]*\)', '', blk)
                b = re.sub(r'\(uuid [^)]*\)', '', b)
                b = re.sub(r'-?\d+\.\d+', lambda mo: str(round(float(mo.group(0)), 3)), b)
                b = re.sub(r'\s+', ' ', b).strip()
                b = re.sub(r'\s+\)', ')', b)
                sig.append(('cu', b))
    return sorted(sig)


if __name__ == '__main__':
    os.chdir('/tmp/AutohitechLib/Autohitech.pretty')
    groups = defaultdict(list)
    for f in glob.glob('*.kicad_mod'):
        base = f[:-len('.kicad_mod')]
        if '__' in base:
            n, tag = base.rsplit('__', 1)
        else:
            n, tag = base, None
        groups[n].append((f, tag))

    for n in sorted(groups):
        if len(groups[n]) < 2:
            continue
        sigs = {}
        for f, tag in sorted(groups[n]):
            sigs[tag] = copper_sig(f)
        uniq = set(map(tuple, sigs.values()))
        if len(uniq) == 1:
            print(f'{n}: COPPER-IDENTICAL {sorted(sigs)}')
        else:
            print(f'{n}: COPPER-DIFFERS')
            for tag in sorted(sigs):
                print(f'    [{tag}] pads={sum(1 for k, _ in sigs[tag] if k=="pad")} cushapes={sum(1 for k, _ in sigs[tag] if k=="cu")}')
