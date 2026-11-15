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
| J12 | FAN 12V: VFAN / GND | bawah (32,84) |
| J13 | THERMO: 12V / KE FAN (seri ke fan) | bawah (50,84) |

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

## Pemeriksaan tambahan (permintaan "lihat PCB-nya")

Selain DRC, aku jalankan pemeriksaan geometri sendiri dari file `.kicad_pcb`
(pad + segmen, toleransi lebar jalur):

| Uji | Hasil |
|---|---|
| Semua pad tersambung ke copper | ya — 25 pad, **0 pad tanpa copper** |
| Net terpecah (pad tidak nyambung ke grup net-nya) | **tidak ada** |
| Jarak tepi-ke-tepi minimum antar net berbeda (layer sama) | **0,34 mm** (pad V5 J6.2 ke GND trunk) — di atas rule 0,2 mm |
| Jarak minimum pad ke jalur net lain | 0,34 mm; berikutnya 0,80 mm |
| Lebar jalur per net | V12/V24/VRAIL 2,5 mm · V36 2,0 mm · GND 2,5/1,5 mm · V5 1,0 mm · D2 0,6 mm |
| Layer per net | F.Cu: V12, V24, VRAIL, V5, D2 · B.Cu: V36, GND |

## Kipas (fan) di box

Board sudah menyediakan koneksinya:

- **J13 = jalur fan (V12 masuk, KE FAN keluar)** — di sinilah termostat dipasang seri.
  Tanpa termostat: cukup jumper/short kedua pad J13 → fan nyala terus.
- **J12 = konektor fan** (VFAN + GND). Fan 12 V 60 mm ≈ 0,06-0,15 A (1-1,8 W),
  jalurnya 1 mm (batas ~2,4 A) — lega.
- Rail 12 V dari buck **selalu hidup** selama PSU nyala (relay hanya memilih rail
  mana yang masuk ke board C210), jadi fan ikut nyala saat PSU dinyalakan.
- Termostat murah: bimetal 45 °C seri (Rp5-8 rb), atau modul NTC 12 V (Rp10-15 rb)
  kalau mau setpoint yang bisa diatur. Fan yang lebih "hening": 12 V dijalankan lewat
  resistor seri 22-47 ohm (turun kecepatan, tapi pendinginan berkurang).

Pemasangan di box: intake bawah + exhaust atas, arah udara melewati modul step-down
(bukan ke sisi 220 V), kasih filter mesh di intake supaya flux/debu tidak menempel
di bilah fan, dan jauhkan fan dari terminal 220 V board PSU.

## Kapasitas arus jalur (IPC-2221, 1 oz = 35 um)

| Jalur | Arus | Lebar | Batas @10 °C rise | Kenaikan suhu saat beban penuh |
|---|---|---|---|---|
| rail 12 V C210 (kartrid 2 ohm) | 6,0 A | 2,5 mm | 4,65 A | **~18 °C** |
| rail 12 V C210 (kartrid 2,5 ohm) | 4,8 A | 2,5 mm | 4,65 A | ~11 °C |
| rail 24 V T12 | 3,0 A | 2,5 mm | 4,65 A | ~3,7 °C |
| distribusi 36 V | 2,2 A | 2,0 mm | 3,95 A | ~2,6 °C |
| return GND | 6,0 A | 2,5 mm | 4,65 A | ~18 °C |
| coil relay 5 V | 70 mA | 1,0 mm | 2,39 A | ~0 °C |
| sinyal D2 | - | 0,6 mm | 1,65 A | ~0 °C |

Artinya: **aman, tapi rail 12 V hangat (~18 °C di atas ambient, hanya saat pemanas
menarik penuh; PID memotong duty jadi rata-ratanya lebih rendah)**. Dua cara
memperbaiki kalau mau dingin:
1. Order PCB **2 oz copper** -> batas jadi 7,68 A @10 °C (tambahan biaya kecil di JLCPCB).
2. Atau pakai kartrid C210 >= 2,5 ohm (4,8 A) -> kenaikan hanya ~11 °C.

Yang DRC tidak bisa jamin (cek di rakitan, bukan di file): panas modul step-down
(~8 W masing-masing, butuh udara), kualitas crimp/sekrup kabel (pakai 18AWG untuk
rail 6 A), usia kontak relay, sekring 3 A slow di sisi 36 V, dan enclosure tertutup
untuk board PSU teladan.

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
