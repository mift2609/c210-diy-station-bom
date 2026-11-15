# 13 — PCB POWER BOARD v1 (relay + slot step-down, gerber siap order)

Dibuat: 15 November 2026, KiCad 10 (`kicad-cli`), diverifikasi DRC.
Folder: `13-pcb-power/`

## Kenapa board terpisah, bukan digabung ke board C210

Board C210 yang kita punya hanya **gerber hasil ekspor** (`01b-gerber-c210-maskfix.zip`),
bukan project KiCad. Menambah relay + 2 modul step-down di board itu berarti
menggambar ulang seluruh layout — dan bagian analog (front-end termokopel ~20 µV/°C)
justru harus **jauh** dari node switching 36 V / arus 6 A (noise + drift panas
op-amp). Jadi: board power terpisah, ditumpuk/dipasang di dalam box, disambung
4 kabel. Kalau nanti mau benar-benar satu board, itu proyek baru (redraw penuh) —
bilang saja.

## Isi board (90 × 60 mm, 2 layer, 4 lubang M3)

| Ref | Fungsi | Catatan |
|---|---|---|
| J1 | 36V IN | dari PSU WX-DC2416 (ukur dulu outputnya) |
| J2 | BUCK12 IN | + dan − ke modul buck 1 |
| J3 | BUCK12 OUT | 12 V → kontak relay NC (rail C210) |
| J4 | BUCK24 IN | ke modul buck 2 |
| J5 | BUCK24 OUT | 24 V → kontak relay NO (rail T12) |
| J6 | K1 CTRL (1×3, 2.54) | `D2` / `+5V` / `GND` — D2 flywire dari socket Nano |
| J7 | +5V IN (1×2) | dari modul buck 5 V (suplai coil relay) |
| J8 | K1 NC / NO / COM / GND | kawat ke terminal kontak modul relay |
| J9 | RAIL OUT / GND | → J1 (+) dan (−) board C210 |
| J10 | TO NANO (D2, GND) | titik ukur/jumper ke socket Nano |

Routing: power + sinyal di F.Cu, GND bus di B.Cu (y=47) — semua pad thru-hole,
tanpa via. Lebar jalur: 2,0 mm untuk power, 1,0 mm +5 V, 0,6 mm sinyal D2.

## Verifikasi (bukan klaim)

```unknown
kicad-cli pcb drc --exit-code-violations -o drc.txt c210-power-v1.kicad_pcb
  -> 0 error, 0 unconnected pad
  -> 15 warning: 14 lib_footprint_issues (footprint custom, memang bukan dari library),
     1 silk_edge_clearance (teks dekat tepi) — kosmetik, tidak menghalangi fab
kicad-cli pcb export gerbers ... ; kicad-cli pcb export drill ...
  -> 9 file (F/B Cu, F/B Mask, F/B Silk, Edge_Cuts, drl) di c210-power-v1-gerber.zip
drill: T1 1,0 mm (header J6), T2 1,3 mm (terminal), T3 3,2 mm (mounting M3)
```

## Cara order

1. Upload `c210-power-v1-gerber.zip` ke JLCPCB/PCBWay (2 layer, 1,6 mm, HASL).
   Ukuran 90×60 mm → 5 pcs kira-kira Rp30.000–60.000 + ongkir.
2. Modul yang dibeli: 2 × step-down **input ≥50 V** (mis. 8-60V → 1-36V 15A),
   1 × step-down 5 V, 1 × modul relay SPDT 5 V (high-level trigger).
3. Pasang terminal, modul dipasang dengan spacer + kawat pendek 20AWG.
4. Set output buck **diukur pakai multimeter dulu**: 12,0 V dan 24,0 V.
   Rail 24 V masuk ke profil C210 = kartrid rusak.

## Wiring akhir

```unknown
PSU 36V -> J1(36V+) ; J1(GND) -> GND bus
J2 -> buck12 (30x25mm) -> J3 (set 12,0V) -> J8 NC
J4 -> buck24           -> J5 (set 24,0V) -> J8 NO
J8 COM -> J9 RAIL OUT -> J1 (+) board C210 ; GND -> J1 (-) board C210
modul 5V -> J7 (+5V IN) -> J6 +5V (coil relay)
socket Nano D2 -> J6 D2 (atau J10 pin1)
```
Untuk pengaman tambahan: sekring 8 A (rail 12 V) bisa dipasang inline di jalur
J9 → board C210; PSU 36 V sudah punya sekring sendiri bila ada.

## Kalau ingin sekalian relay-nya (bukan modul)

Board ini memakai **modul relay** (socket 1×3 + terminal kontak), jadi tidak ada
footprint relay yang harus ditebak. Kalau nanti mau relay telanjang (SRD-05VDC)
ditempel langsung + transistor + dioda flyback di board ini, tinggal ganti bagian
J6/J8 dengan footprint relay — butuh 1 revisi kecil.

## File

| File | Isi |
|---|---|
| `gen_board.py` | generator board (s-expression KiCad) — ubah angka di sini lalu jalankan ulang |
| `c210-power-v1.kicad_pcb` | board, bisa dibuka di KiCad GUI |
| `c210-power-v1-gerber.zip` | siap order |
| `c210-power-v1-render.png` | render 3D sisi atas |
| `render-front.svg` | render vektor (layer F.Cu/B.Cu/silk/edge) |
| `drc.txt` | hasil DRC (bukti 0 error) |
