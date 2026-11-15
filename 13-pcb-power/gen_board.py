#!/usr/bin/env python3
"""Generator board 'C210 POWER BOARD v1' (KiCad s-expression).

Versi 2 — routing bebas DRC error (lihat drc.txt).
  J1 36V IN (PSU WX-DC2416)        J7 +5V IN (buck 5V -> coil relay)
  J2 BUCK12 IN   J3 BUCK12 OUT     J8 K1 NC / NO / COM / GND
  J4 BUCK24 IN   J5 BUCK24 OUT     J9 OUT -> board utama J1 (+rail, GND)
  J6 K1 CTRL (1x3, 2.54): D2 IN / +5V / GND   -> dari socket Nano D2
  J10 TO NANO (D2, GND)            H1..H4 lubang M3
F.Cu = power + sinyal, B.Cu = GND bus (semua pad thru-hole, tanpa via).
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
NAME = "c210-power-v1"

NETS = [(0, ""), (1, "GND"), (2, "V36"), (3, "V12"), (4, "V24"), (5, "CTRL_D2"), (6, "V5"), (7, "VRAIL")]
NETMAP = dict(NETS)

def term_block(ref, x, y, nets, labels, pitch=5.08, drill=1.3, pad=2.9, label_dy=-4.0, ref_dy=4.2):
    L = [f'  (footprint "c210:TerminalBlock_{len(nets)}x{pitch}mm" (layer "F.Cu") (at {x} {y}) (attr through_hole)',
         f'    (fp_text reference "{ref}" (at 0 {ref_dy}) (layer "F.SilkS") (effects (font (size 1 1))))',
         f'    (fp_text value "conn" (at 0 -4.2) (layer "F.Fab") hide (effects (font (size 1 1))))']
    for i, (net, lab) in enumerate(zip(nets, labels)):
        px, py = i * pitch, 0
        L.append(f'    (pad "{i+1}" thru_hole rect (at {px} {py}) (size {pad} {pad}) (drill {drill}) '
                 f'(layers "*.Cu" "*.Mask") (net {net} "{NETMAP[net]}"))')
        if lab:
            L.append(f'    (fp_text user "{lab}" (at {px} {label_dy}) (layer "F.SilkS") (effects (font (size 0.85 0.85))))')
    L.append('  )')
    return "\n".join(L)

SEG = []
def path(points, net, width, layer):
    for a, b in zip(points, points[1:]):
        SEG.append(f'  (segment (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (width {width}) (layer "{layer}") (net {net}))')

def pads(x, y, n, pitch=5.08):
    return [(round(x + i * pitch, 2), y) for i in range(n)]

J1  = pads(8, 10, 2)          # 36V in
J2  = pads(8, 20, 2)          # buck12 in
J3  = pads(8, 30, 2)          # buck12 out
J4  = pads(52, 10, 2)         # buck24 in
J5  = pads(52, 20, 2)         # buck24 out
J6  = pads(78, 26, 3, 2.54)   # relay ctrl: D2 IN / +5V / GND
J7  = pads(80.54, 34, 2)      # +5V in
J8  = pads(30, 42, 4)         # K1 NC / NO / COM / GND
J9  = pads(8, 52, 2)          # OUT -> board utama
J10 = pads(52, 52, 2)         # TO NANO D2 / GND

FPS = [term_block("J1", 8, 10, [2, 1], ["36V+", "GND"], label_dy=-6.2),
       term_block("J2", 8, 20, [2, 1], ["BUCK12 IN+", "GND"]),
       term_block("J3", 8, 30, [3, 1], ["12V OUT", "GND"]),
       term_block("J4", 52, 10, [2, 1], ["BUCK24 IN+", "GND"], label_dy=-6.2),
       term_block("J5", 52, 20, [4, 1], ["24V OUT", "GND"]),
       term_block("J6", 78, 26, [5, 6, 1], ["D2", "5V", "G"], pitch=2.54, drill=1.0, pad=1.9, label_dy=-3.6, ref_dy=4.6),
       term_block("J7", 80.54, 34, [6, 1], ["+5V IN", "GND"], label_dy=4.2, ref_dy=-4.6),
       term_block("J8", 30, 42, [3, 4, 7, 1], ["K1 NC", "K1 NO", "K1 COM", "GND"], label_dy=4.6, ref_dy=-4.6),
       term_block("J9", 8, 52, [7, 1], ["", ""], ref_dy=-4.6),
       term_block("J10", 52, 52, [5, 1], ["", ""], ref_dy=-4.6)]

# ---- F.Cu ----
path([J1[0], (8, 6), (52, 6), J4[0]], 2, 2.0, "F.Cu")            # V36 distribusi (lane y=6)
path([J1[0], J2[0]], 2, 2.0, "F.Cu")                              # V36 -> buck12 IN
path([J3[0], (8, 38), (30, 38), J8[0]], 3, 2.0, "F.Cu")           # V12 -> K1 NC
path([J5[0], (52, 32), (35.08, 32), J8[1]], 4, 2.0, "F.Cu")       # V24 -> K1 NO
path([J8[2], (40.16, 48), (8, 48), J9[0]], 7, 2.0, "F.Cu")        # K1 COM -> RAIL OUT
path([J7[0], J6[1]], 6, 1.0, "F.Cu")                              # +5V -> relay VCC (jalur pendek)
path([J6[0], (78, 46), (52, 46), J10[0]], 5, 0.6, "F.Cu")         # D2 -> TO NANO

# ---- B.Cu: GND bus ----
BUS_Y = 47
GND_PAD = [J1[1], J2[1], J3[1], J4[1], J5[1], J6[2], J7[1], J8[3], J9[1], J10[1]]
for p in GND_PAD:
    path([p, (p[0], BUS_Y)], 1, 1.5, "B.Cu")
path([(min(p[0] for p in GND_PAD), BUS_Y), (max(p[0] for p in GND_PAD), BUS_Y)], 1, 2.5, "B.Cu")

# ---- mekanik + silkscreen ----
MECH = []
for (x, y) in [(5, 5), (85, 5), (5, 55), (85, 55)]:
    MECH.append(f'''  (footprint "c210:MountingHole_M3" (layer "F.Cu") (at {x} {y}) (attr exclude_from_pos_files)
    (fp_text reference "H" (at 0 0) (layer "F.Fab") hide (effects (font (size 1 1))))
    (fp_text value "M3" (at 0 0) (layer "F.Fab") hide (effects (font (size 1 1))))
    (pad "" np_thru_hole circle (at 0 0) (size 3.2 3.2) (drill 3.2) (layers "F.Mask" "B.Mask"))
  )''')

GR = ['  (gr_rect (start 0 0) (end 90 60) (stroke (width 0.1) (type default)) (fill none) (layer "Edge.Cuts"))']
def txt(s, x, y, size=1.2, bold=False, layer="F.SilkS"):
    GR.append(f'  (gr_text "{s}" (at {x} {y}) (layer "{layer}") (effects (font (size {size} {size})'
              + (' bold' if bold else '') + ')))')
txt("36V -> BUCK12 -> K1 NC | 36V -> BUCK24 -> K1 NO | K1 COM -> J9 RAIL OUT", 6, 59.4, 0.9)
txt("J10 = TO NANO (D2, GND)   J6 = relay ctrl   J7 = +5V", 6, 56.6, 0.8, layer="F.Fab")
txt("C210 POWER BOARD v1 - relay + step-down", 40, 60.6 - 1.0, 1.0, layer="F.Fab")
txt("GND bus B.Cu y=47", 60, 49.6, 0.8, layer="F.Fab")

body = f'''(kicad_pcb (version 20221018) (generator "c210-gen")

  (general (thickness 1.6))

  (paper "A4")

  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user)
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (37 "F.SilkS" user)
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
print("tulis", NAME + ".kicad_pcb:", len(body), "byte,", len(SEG), "segmen")
