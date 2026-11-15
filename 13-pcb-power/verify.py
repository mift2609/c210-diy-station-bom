#!/usr/bin/env python3
"""Cek independen board (bukan DRC): konektivitas + clearance antar net.

Pakai: python3 verify.py c210-power-v2.kicad_pcb
- union-find pad+segmen (T-junction & lebar jalur dihitung) -> deteksi pad lepas
- jarak tepi minimum antar net berbeda di layer sama -> laporan clearance
"""
import re, sys, math, collections

path = sys.argv[1] if len(sys.argv) > 1 else "c210-power-v2.kicad_pcb"
txt = open(path).read()
nets = dict(re.findall(r'\(net (\d+) "([^"]*)"\)', txt))

pads = []   # (net, x, y, size)
for fpm in re.finditer(r'\(footprint [^\n]*\(at ([\d.]+) ([\d.]+)\)(.*?)\n  \)', txt, re.S):
    fx, fy, body = float(fpm.group(1)), float(fpm.group(2)), fpm.group(3)
    for pm in re.finditer(r'\(pad "[^"]*" thru_hole \w+ \(at ([\d.]+) ([\d.]+)\) \(size ([\d.]+) ([\d.]+)\)[^\n]*\(net (\d+)', body):
        pads.append((int(pm.group(5)), round(fx + float(pm.group(1)), 2),
                     round(fy + float(pm.group(2)), 2), float(pm.group(3))))

segs = []   # (net, a, b, width, layer)
for sm in re.finditer(r'\(segment \(start ([\d.]+) ([\d.]+)\) \(end ([\d.]+) ([\d.]+)\) \(width ([\d.]+)\) \(layer "([^"]+)"\) \(net (\d+)\)', txt):
    segs.append((int(sm.group(7)), (float(sm.group(1)), float(sm.group(2))),
                 (float(sm.group(3)), float(sm.group(4))), float(sm.group(5)), sm.group(6)))

def d_pt_seg(pt, a, b):
    (x, y), (x1, y1), (x2, y2) = pt, a, b
    dx, dy = x2 - x1, y2 - y1
    if dx == dy == 0:
        return math.hypot(x - x1, y - y1)
    t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(x - (x1 + t * dx), y - (y1 + t * dy))

def d_seg_seg(a1, b1, a2, b2):
    return min(d_pt_seg(a1, a2, b2), d_pt_seg(b1, a2, b2),
               d_pt_seg(a2, a1, b1), d_pt_seg(b2, a1, b1))

parent = {}
def find(x):
    parent.setdefault(x, x)
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    parent[find(a)] = find(b)

for i, (n1, a1, b1, w1, l1) in enumerate(segs):
    for j, (n2, a2, b2, w2, l2) in enumerate(segs):
        if i >= j or n1 != n2:
            continue
        if d_seg_seg(a1, b1, a2, b2) <= (w1 + w2) / 2 + 1e-6:
            union(('seg', i), ('seg', j))

for n, px, py, sz in pads:
    for i, (n2, a, b, w, l) in enumerate(segs):
        if n2 == n and d_pt_seg((px, py), a, b) <= w / 2 + sz / 2 + 1e-6:
            union(('pad', n, (px, py)), ('seg', i))

split, lone = [], []
for net in sorted({n for n, _, _, _ in pads}):
    grp = collections.defaultdict(list)
    for n, px, py, sz in pads:
        if n == net:
            grp[find(('pad', n, (px, py)))].append((px, py))
    if len(grp) > 1:
        split.append((nets.get(str(net), '?'), [(len(v), v[:3]) for v in grp.values()]))
for n, px, py, sz in pads:
    if all(not (n2 == n and d_pt_seg((px, py), a, b) <= w / 2 + sz / 2 + 1e-6) for n2, a, b, w, l in segs):
        lone.append((nets.get(str(n), '?'), (px, py)))

gaps = []
for i, (n1, a1, b1, w1, l1) in enumerate(segs):
    for j, (n2, a2, b2, w2, l2) in enumerate(segs):
        if i >= j or n1 == n2 or l1 != l2:
            continue
        gaps.append((d_seg_seg(a1, b1, a2, b2) - w1 / 2 - w2 / 2,
                     nets.get(str(n1)), nets.get(str(n2)), l1))
pad_gaps = []
for n, px, py, sz in pads:
    for n2, a, b, w, l in segs:
        if n2 != n:
            pad_gaps.append((d_pt_seg((px, py), a, b) - w / 2 - sz / 2, nets.get(str(n)), nets.get(str(n2)), (px, py)))
gaps.sort(); pad_gaps.sort()

print(f"== {path}: {len(pads)} pad, {len(segs)} segmen, {len(nets) - 1} net")
print(f"  net terpecah          : {split if split else 'TIDAK ADA'}")
print(f"  pad tanpa copper      : {lone if lone else 'TIDAK ADA'}")
print(f"  clearance jalur-jalur : min {gaps[0][0]:.2f} mm ({gaps[0][1]} vs {gaps[0][2]} di {gaps[0][3]})" if gaps else "  clearance jalur-jalur : -")
print(f"  clearance pad-jalur   : min {pad_gaps[0][0]:.2f} mm ({pad_gaps[0][1]} pad vs jalur {pad_gaps[0][2]} @{pad_gaps[0][3]})" if pad_gaps else "  clearance pad-jalur   : -")
per_net = collections.defaultdict(set)
for n, a, b, w, l in segs:
    per_net[nets.get(str(n), '?')].add(w)
print("  lebar per net         :", {k: sorted(v) for k, v in sorted(per_net.items())})
