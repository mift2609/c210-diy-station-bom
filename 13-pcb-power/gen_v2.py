#!/usr/bin/env python3
"""C210 POWER BOARD v2 — 140x90mm, dual rail (C210 12V / T12 24V).

Zona modul = GRID lubang M3 (bukan footprint modul), jadi modul XL4016 (rail 12V),
XL4015 (rail 24V), relay, dan modul 5V bisa disekrup di posisi yang cocok.

Kiri (pitch 5.08): J1 36V IN y=10 | J2 BUCK12 IN y=22 | J3 BUCK12 OUT y=34
                   J5 BUCK24 OUT y=58 | J4 BUCK24 IN y=70 | J9 RAIL OUT y=82
Tengah: J8 K1 NC/NO/COM/GND (60,46)
Kanan: J6 K1 CTRL 1x3 (96,44) | J7 5V IN (96,84) | J11 5V OUT (110,84)
       J10 TO NANO (124,84) | J9b RAIL OUT (96,58)
Layer: F.Cu = power/sinyal, B.Cu = V36 distribusi + GND trunk. Tanpa via.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
NAME = "c210-power-v2"

NETS = [(0, ""), (1, "GND"), (2, "V36"), (3, "V12"), (4, "V24"), (5, "CTRL_D2"), (6, "V5"), (7, "VRAIL")]
NM = dict(NETS)

def term(ref, x, y, nets, labels, pitch=5.08, drill=1.3, pad=2.9, label_dy=-4.2, ref_dy=4.2):
    L = [f'  (footprint "c210:TB_{len(nets)}x{pitch}" (layer "F.Cu") (at {x} {y}) (attr through_hole)',
         f'    (fp_text reference "{ref}" (at 0 {ref_dy}) (layer "F.SilkS") (effects (font (size 1 1))))',
         f'    (fp_text value "conn" (at 0 0) (layer "F.Fab") hide (effects (font (size 1 1))))']
    for i, (net, lab) in enumerate(zip(nets, labels)):
        px = i * pitch
        L.append(f'    (pad "{i+1}" thru_hole rect (at {px} 0) (size {pad} {pad}) (drill {drill}) '
                 f'(layers "*.Cu" "*.Mask") (net {net} "{NM[net]}"))')
        if lab:
            L.append(f'    (fp_text user "{lab}" (at {px} {label_dy}) (layer "F.SilkS") (effects (font (size 0.85 0.85))))')
    L.append('  )')
    return "\n".join(L)

def hole(x, y):
    return f'''  (footprint "c210:MH_M3" (layer "F.Cu") (at {x} {y}) (attr exclude_from_pos_files)
    (fp_text reference "H" (at 0 0) (layer "F.Fab") hide (effects (font (size 1 1))))
    (fp_text value "M3" (at 0 0) (layer "F.Fab") hide (effects (font (size 1 1))))
    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "F.Mask" "B.Mask"))
  )'''

def pads(x, y, n, pitch=5.08):
    return [(round(x + i * pitch, 2), y) for i in range(n)]

J1 = pads(15, 10, 2); J2 = pads(15, 22, 2); J3 = pads(15, 34, 2)
J5 = pads(15, 58, 2); J4 = pads(15, 70, 2)
J8 = pads(60, 46, 4)             # NC / NO / COM / GND
J6 = pads(96, 44, 3, 2.54)       # relay ctrl: D2 / 5V / GND
J9 = pads(96, 58, 2)             # RAIL OUT
J7 = pads(96, 84, 2); J11 = pads(110, 84, 2); J10 = pads(124, 84, 2)

FPS = [term("J1", 15, 10, [2, 1], ["36V+", "GND"], label_dy=-5.6),
       term("J2", 15, 22, [2, 1], ["BUCK12 IN+", "GND"], label_dy=-5.6),
       term("J3", 15, 34, [3, 1], ["BUCK12 OUT", "GND"], label_dy=-5.6),
       term("J5", 15, 58, [4, 1], ["BUCK24 OUT", "GND"], label_dy=-5.6),
       term("J4", 15, 70, [2, 1], ["BUCK24 IN+", "GND"], label_dy=-5.6),
       term("J8", 60, 46, [3, 4, 7, 1], ["K1 NC", "K1 NO", "K1 COM", "GND"], label_dy=5.8, ref_dy=-4.6),
       term("J6", 96, 44, [5, 6, 1], ["D2", "5V", "G"], pitch=2.54, drill=1.0, pad=1.9, label_dy=-3.6, ref_dy=4.6),
       term("J9", 96, 58, [7, 1], ["RAIL OUT", "GND"], label_dy=5.8, ref_dy=-4.6),
       term("J7", 96, 84, [3, 1], ["5V IN", "GND"], label_dy=-5.6),
       term("J11", 110, 84, [6, 1], ["5V OUT", "GND"], label_dy=-5.6),
       term("J10", 124, 84, [5, 1], ["TO NANO", "GND"], label_dy=-5.6)]

SEG = []
def path(pts, net, w, layer):
    for a, b in zip(pts, pts[1:]):
        SEG.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width {w}) (layer "{layer}") (net {net}))')

# ---------- B.Cu: V36 distribusi ----------
path([(5.5, 10), (5.5, 70)], 2, 2.0, "B.Cu")
for p in (J1[0], J2[0], J4[0]):
    path([(5.5, p[1]), p], 2, 2.0, "B.Cu")

# ---------- B.Cu: GND trunk ----------
path([(20.08, 10), (20.08, 87.5)], 1, 2.5, "B.Cu")              # trunk kiri (semua GND kolom kiri)
path([(75.24, 46), (75.24, 50), (20.08, 50)], 1, 1.5, "B.Cu")   # J8.4 -> trunk
path([(103, 44), (103, 87.5)], 1, 2.5, "B.Cu")                 # trunk kanan (geser dari lubang)
path([(101.08, 44), (103, 44)], 1, 2.5, "B.Cu")                 # stub J6.3
path([(101.08, 84), (103, 84)], 1, 2.5, "B.Cu")                 # stub J7.2
for x in (115.08, 129.08):                                      # J11.2, J10.2
    path([(x, 84), (x, 87.5)], 1, 1.5, "B.Cu")
path([(20.08, 87.5), (129.08, 87.5)], 1, 2.5, "B.Cu")           # trunk bawah

# ---------- F.Cu: rail ----------
# V12: J3 -> corridor x=9 -> cabang ke J8.1 (NC) & terus ke J7.1 (5V in)
path([J3[0], (9, 34), (9, 87), (96, 87), J7[0]], 3, 2.5, "F.Cu")
path([(9, 42), (60, 42), J8[0]], 3, 2.5, "F.Cu")
# V24: J5 -> corridor x=12 -> lane y=50.5 -> J8.2 (NO)
path([J5[0], (12, 58), (12, 50.5), (65.08, 50.5), J8[1]], 4, 2.5, "F.Cu")
# VRAIL: J8.3 (COM) -> corridor x=71.5 -> J9B.1 (RAIL OUT)
path([J8[2], (71.5, 47.5), (71.5, 58), J9[0]], 7, 2.5, "F.Cu")
# V5: J11.1 (5V OUT) -> J6.2 (coil relay)
path([J11[0], (112, 82), (112, 48), (98.54, 48), J6[1]], 6, 1.0, "F.Cu")
# D2: J6.1 -> lane y=41.5 -> J10.1
path([J6[0], (96, 41.5), (128, 41.5), (128, 80), (124, 80), J10[0]], 5, 0.6, "F.Cu")

# ---------- lubang M3 (grid zona modul + sudut) ----------
HOLES = [(5, 5), (135, 5), (5, 85), (135, 85)]
for gx in (32, 50, 68, 86):
    for gy in (10, 38, 54, 76):
        HOLES.append((gx, gy))
for gx in (108, 124, 134):
    for gy in (12, 36, 58, 74):
        HOLES.append((gx, gy))
MECH = [hole(x, y) for (x, y) in HOLES]

GR = ['  (gr_rect (start 0 0) (end 140 90) (stroke (width 0.1) (type default)) (fill none) (layer "Edge.Cuts"))']
def txt(s, x, y, size=1.0, layer="F.SilkS", bold=False):
    GR.append(f'  (gr_text "{s}" (at {x} {y}) (layer "{layer}") (effects (font (size {size} {size})'
              + (" bold" if bold else "") + ')))')
txt("C210 POWER BOARD v2 - dual rail (C210 12V / T12 24V)", 82, 5.0, 1.2, bold=True)
txt("zona modul: grid M3 3,2mm - pakai spacer 5mm", 32, 87.0, 0.9)
txt("36V -> J2/J4 -> modul -> J3/J5 -> K1 NC/NO -> COM -> J9B RAIL OUT", 90, 6.5, 0.8, layer="F.Fab")
txt("GND: trunk kiri/bawah + V36 distribusi di B.Cu", 88, 86.5, 0.8, layer="F.Fab")

body = f'''(kicad_pcb (version 20221018) (generator "c210-gen")

  (general (thickness 1.6))

  (paper "A4")

  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user)
    (37 "F.SilkS" user)
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
    (46 "B.CrtYd" user)
    (47 "F.CrtYd" user)
  )

  (setup (pad_to_mask_clearance 0))

{chr(10).join(f'  (net {n} "{nm}")' for n, nm in NETS)}

{chr(10).join(FPS)}

{chr(10).join(MECH)}

{chr(10).join(SEG)}

{chr(10).join(GR)}
)
'''
open(os.path.join(OUT, NAME + ".kicad_pcb"), "w").write(body)
print("tulis", NAME + ".kicad_pcb:", len(body), "byte,", len(SEG), "segmen,", len(HOLES), "lubang")
