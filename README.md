# Checklist Belanja — Station Solder C210 DIY

Halaman checklist komponen untuk membangun station solder C210 (kartrid JBC C210) berbasis
Arduino Nano / ATmega328P + LMV358, ditujukan untuk service HP dan elektronik kecil.

- `index.html` — checklist interaktif: centang per komponen, harga bisa diedit, total otomatis,
  tombol salin daftar yang belum dibeli, dan link pencarian Shopee per komponen.
- `c210-station-belanja-uji.xlsx` — versi spreadsheet: daftar belanja, daftar upgrade,
  item off-PCB/gagang DIY, checklist uji terima, dan tabel kalibrasi suhu.
- `checklist.html` (kalau ada) — versi tanpa data harga Shopee.

## Estimasi biaya

| Bagian | Biaya |
|---|---|
| Komponen PCB wajib (otak + SMD + THT) | Rp159.500 |
| Off-PCB & gagang DIY (fab PCB, tip, soket, kabel, PSU, stand, enclosure) | Rp345.000 – Rp830.000 |
| Upgrade elektronik opsional (OPA2387, buck 5V, MOSFET ≥40V, earth tip, snubber) | +Rp87.000 |
| **Total** | **Rp504.500 – Rp989.500** (dengan upgrade: Rp587.500 – Rp1.072.500) |

## Varian gagang & rail (15 Nov 2026)

Satu board, satu colokan, gantian gagang:

- **C210 (12 V)** — rail dasar, kartrid ~2 ohm.
- **T210 / gagang 12 V** — lihat [`09-gantian-gagang.md`](09-gantian-gagang.md):
  autodetect gagang lewat ID pin (D10), 2 slot tip, firmware `firmware-gantian/`
  (v1.3-C210g, 24.412 byte).
- **T12 (24 V)** — lihat [`12-dual-rail-c210-t12.md`](12-dual-rail-c210-t12.md):
  PSU 32-36 V -> buck 24 V (T12) + buck 12 V (C210), dipilih **relay SPDT** yang
  dikendalikan D2; rail ikut profil tip otomatis. Firmware `firmware-dualrail/`
  (v1.3-dual, 24.570 byte). Wajib untuk rail 24 V: MOSFET >= 40 V, 5 V dari buck,
  sekring ikut R kartrid.

Tabel daya tip: C210 ~2 ohm -> 12 V = 72 W (24 V = 288 W, jangan);
T12 ~8 ohm -> 12 V = 18 W, 24 V = 72 W.

## Angka sekring & PSU: ukur R kartrid dulu

Doc lama memakai 8,5 ohm / ~1,4 A (angka tip T12). Rumus: `I = 12 / R`.

| R kartrid | Arus puncak @12 V | Sekring | PSU/rail |
|---|---|---|---|
| ~2 ohm (C210) | ~6,0 A | 8 A | >=8 A |
| ~2,5-3 ohm | ~4,0-4,8 A | 6,3-8 A | >=6 A |
| ~8 ohm (T12) | ~1,5 A | 3 A fast | >=3 A (lemah di 12 V) |

## Sebelum dipakai menyolder board HP

1. PSU harus **SELV/floating** — jangan pakai adaptor atau charger yang outputnya terhubung ke earth.
2. Sambungkan **kabel earth dari soket kartrid ke chassis** lalu ke PE. Ukur: tip-ke-earth < 2 Ω, kebocoran < 2 mV.
3. Kalibrasi suhu di 250/300/350 °C dengan thermocouple meter — target error < ±20 °C.
4. Uji fail-safe: cabut kartrid / satu kabel termokopel saat heater ON, daya harus terputus.
5. Kalau OPA2387 dipasang menggantikan LMV358, kalibrasi wajib diulang.

Catatan: seluruh angka harga adalah estimasi snapshot dan perlu dicek ulang saat membeli.

## Catatan gerber (penting)

File gerber asli yang beredar untuk board ini punya **cacat ekspor**: layer solder
mask (`F_Mask`/`B_Mask`) hanya memuat 56 bukaan untuk pad through-hole dan mounting
hole, sedangkan **pad SMD tidak punya bukaan sama sekali** (F_Cu punya 209 pad,
F_Mask hanya 56 objek; pad SMD terlihat tertutup mask pada render). Preview desainer
sendiri menunjukkan pad SMD terbuka, jadi ini murni cacat ekspor, bukan salah desain.

Kalau diorder apa adanya, pad SMD akan tertutup solder mask dan tidak bisa disolder.
Dua jalan keluar: minta desainer ekspor ulang gerber, atau pakai versi perbaikan
(mask di-generate ulang dari copper: bukaan THT dipertahankan + bukaan pad SMD
ditambahkan dengan ekspansi 0,1 mm, via tetap tertutup).

## Live

Checklist interaktif: https://mift2609.github.io/c210-diy-station-bom/
