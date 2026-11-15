# 14 — PCB POWER BOARD v2 (140×90 mm): relay + zona modul step-down di PCB

Dibuat: 15 November 2026, KiCad 10 (`kicad-cli`), DRC diverifikasi.
Folder: `13-pcb-power/` (file v2 ada di situ, nama berawalan `c210-power-v2`).

## Bedanya dari v1 (90×60)

v1 cuma relay + terminal (modul ditaruh di samping board di dalam box).
**v2 = board diperbesar 140×90** supaya modul benar-benar duduk di PCB:
dua zona modul step-down, zona relay, zona modul 5V.

Zona modul memakai **grid lubang M3 (3,2 mm)** — bukan footprint modul. Alasannya:
dimensi dan posisi lubang modul murah (XL4016/XH-M404, XL4015, relay, MP1584) beda-beda
antar penjual. Dengan grid, kamu pilih 4 lubang yang cocok dengan modul yang datang,
pasang spacer 5 mm, lalu sambung kabel pendek ke terminal. Tidak ada risiko
"footprint salah, board tidak bisa dipakai".

## Terminal (semua screw terminal 5,08 mm / header 2,54 mm)

| Ref | Fungsi | Posisi |
|---|---|---|
| J1 | 36V IN dari PSU | kiri y=10 |
| J2 | BUCK12 IN (ke modul XL4016) | kiri y=22 |
| J3 | BUCK12 OUT — rail C210 12 V | kiri y=34 |
| J5 | BUCK24 OUT — rail T12 24 V | kiri y=58 |
| J4 | BUCK24 IN (ke modul XL4015) | kiri y=70 |
| J8 | K1 NC / NO / COM / GND | tengah (60,46) |
| J9 | RAIL OUT → J1 (+) board C210 | kanan (96,58) |
| J6 | K1 CTRL: D2 / +5V / GND (1×3, 2,54) | kanan (96,44) |
| J7 | 5V IN (diambil dari rail 12 V) | kanan bawah (96,84) |
| J11 | 5V OUT (ke coil relay J6) | kanan bawah (110,84) |
| J10 | TO NANO: D2 / GND | kanan bawah (124,84) |

Alur: `36V → J2/J4 → modul step-down → J3 (12V) & J5 (24V) → K1 NC/NO → K1 COM →
J9 RAIL OUT → J1 (+) board C210`. Relay dipilih firmware (pin D2).

## Layer & routing

- **F.Cu**: power + sinyal. Lebar jalur: 2,5 mm (rail 12/24 V & RAIL OUT), 0,6 mm (D2),
  1,0 mm (5 V coil).
- **B.Cu**: distribusi 36 V (trunk x=5,5) + GND (trunk kiri x=20,08, trunk kanan x=103,
  trunk bawah y=87,5). Tanpa via — semua pad thru-hole, jadi bisa pindah layer lewat pad.
- GND trunk lebar 2,5 mm karena return rail C210 bisa 6 A.

## Verifikasi (bukan klaim)

```unknown
kicad-cli pcb drc --exit-code-violations -o drc-v2.txt c210-power-v2.kicad_pcb
  -> 0 error, 0 unconnected pad (semua net tersambung penuh)
  -> 47 warning: 43 lib_footprint_issues (footprint custom, bukan dari library),
     2 silk_overlap + 2 silk_over_copper (teks silkscreen dekat copper) - kosmetik
export gerber + drill -> 9 file di c210-power-v2-gerber.zip
  drill: T1 1,0 mm (header), T2 1,3 mm (terminal), T3 3,2 mm (32 lubang M3)
```

DRC v2 sempat menemukan 49 violation di iterasi pertama (GND nyerempet lubang grid,
jalur 36 V nyilang jalur 12 V, stub GND lewat pad net lain) — sudah diperbaiki di layout.

## Cara pakai

1. Order `c210-power-v2-gerber.zip` (2 layer, 1,6 mm, HASL). 140×90 mm, 5 pcs
   kira-kira Rp60.000–100.000 + ongkir.
2. Pasang modul sesuai rencana: XL4016 (rail 12 V) + XL4015 (rail 24 V) +
   modul 5 V (MP1584) + modul relay SPDT 5 V.
3. Set output dengan multimeter sebelum disambung ke board C210:
   **12,0 V** di J3, **24,0 V** di J5. Rail 24 V masuk ke profil C210 = kartrid rusak.
4. Sambung J9 (RAIL OUT, GND) ke J1 board C210; J10 – atau langsung – ke socket Nano D2.
5. Urutan uji lengkap ada di `12-dual-rail-c210-t12.md`.

## Catatan

- Sisi 36 V tetap perlu pengaman: sekring inline di kabel J1 (3 A slow untuk 36 V,
  arus sisi 36 V cuma ~2,2 A) dan enclosure tertutup (board PSU telanjang = bahaya sentuh).
- Modul step-down panas (~8 W masing-masing) — beri jarak dari modul lain, jangan ditutup rapat.
- Kalau nanti mau buck diskret (IC + induktor di PCB, bukan modul), itu desain baru:
  perlu perhitungan induktor + verifikasi di bangku, tidak bisa diverifikasi dari sini.
