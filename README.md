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

## Sebelum dipakai menyolder board HP

1. PSU harus **SELV/floating** — jangan pakai adaptor atau charger yang outputnya terhubung ke earth.
2. Sambungkan **kabel earth dari soket kartrid ke chassis** lalu ke PE. Ukur: tip-ke-earth < 2 Ω, kebocoran < 2 mV.
3. Kalibrasi suhu di 250/300/350 °C dengan thermocouple meter — target error < ±20 °C.
4. Uji fail-safe: cabut kartrid / satu kabel termokopel saat heater ON, daya harus terputus.
5. Kalau OPA2387 dipasang menggantikan LMV358, kalibrasi wajib diulang.

Catatan: seluruh angka harga adalah estimasi snapshot dan perlu dicek ulang saat membeli.

## Live

Checklist interaktif: https://mift2609.github.io/c210-diy-station-bom/
