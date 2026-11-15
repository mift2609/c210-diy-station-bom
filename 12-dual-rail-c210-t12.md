# 12 — DUAL RAIL: satu board, satu colokan, C210 (12V) ↔ T12 (24V) otomatis

Ditambahkan: 15 November 2026. Melanjutkan `09-gantian-gagang.md`.
Status: firmware selesai & terverifikasi; hardware (relay + 2 buck) belum dipasang.

## Rencana yang dipakai

```unknown
PSU 36V 5A (WX-DC2416 yang sudah ada — output terukur 36 V)
   ├─ buck A → 24V  (rail T12)
   └─ buck B → 12V  (rail C210)
        │
        └─ relay SPDT: NC = buck 12V, NO = buck 24V  → terminal J1 (+) board
                                                       (D2 kendalikan coil relay)
satu konektor gagang GX12-5 → colok C210 atau T12
ID gagang: pin 5 gagang T12 → GND → dibaca D10 → slot tip + rail ikut otomatis
```

Ini benar dan itu satu-satunya cara "satu colokan, dua kelas tegangan" tanpa
mencabut adaptor. Yang WAJIB ada karena ini: **satu relay** (bukan dua soket),
solid state atau mekanik sama-sama boleh.

## Kenapa harus ada pemilih rail

| Kartrid | 12 V | 24 V |
|---|---|---|
| C210 ~2 Ω (kelas 12V) | 72 W / 6,0 A ✅ | 288 W / 12 A → rusak |
| T12 ~8 Ω (kelas 24V) | 18 W / 1,5 A (lemah) | 72 W / 3,0 A ✅ |

Sumber angka: README proyek asal (Wagiminator) — tabel daya tip T12: 12 V = 1,50 A /
18 W, 24 V = 3,00 A / 72 W; TC tip T12 ≈ 22 μV/°C.
Front-end: menurut issue #26 proyek asal, C210 "pretty much the same as T12 tip"
(tap TC terpisah C210 tidak dipakai) → satu front-end melayani keduanya, yang
berbeda hanya **tegangan rail + konstanta kalibrasi**.

## Yang dipakai ganti rail: relay atau MOSFET?

| | Relay SPDT mekanik (disarankan) | MOSFET high-side |
|---|---|---|
| Harga | modul relay 5V ~Rp15-25rb | 2× P-MOSFET + driver, ~Rp20-30rb |
| Ganti dua sumber → satu output | 1 komponen (NC/NO/COM) | butuh 2 switch, rangkaian lebih rumit |
| Kontak | hanya ganti saat pemanas OFF (arus 0) → tidak ada busur | tidak ada kontak bergerak |
| Risiko | coil 70 mA (ambil dari rail 5V buck), klik mekanik | gate drive rail 24V perlu hati-hati |

Keputusan: **relay SPDT 1-channel 5V** (kontak ≥6 A DC) di jalur feed J1 (+).
Coil dari rail 5V (buck 5V, bukan 78M05 — lihat upgrade wajib).

## Wiring (yang berubah dari varian 09)

1. D2 (socket Nano) → modul relay IN. Sisi daya: COM → J1 (+), NC → buck 12V (+),
   NO → buck 24V (+). Buck 12V/24V ground disambung bareng (ground common PSU).
2. D10 → pin 5 konektor gagang = ID. Gagang T12: pin 5 disambung ke GND **di dalam
   gagang**. Gagang C210: pin 5 dibiarkan terbuka.
3. Kabel ID harus dibuat di dalam gagang, bukan di soket — kalau ID dipasang di
   soket, colok gagang yang salah = 24 V masuk ke kartrid C210.

## Firmware `11-firmware-dualrail` (v1.3-dual)

| Fitur | Detail |
|---|---|
| Slot tip | 0 = `C210` (rail 12V), 1 = `T12` (rail 24V) |
| Autodetect | D10 LOW (T12) → slot 1 + rail 24V; D10 terbuka → slot 0 + rail 12V |
| Ganti rail | pemanas OFF → jeda 300 ms → relay klik → jeda 300 ms → PID mulai nol |
| FLT3 | ambang ikut rail: 15,5 V (12V) / 30 V (24V); sekaligus pemeriksa relay nyangkut |
| Boot | pin relay ditulis LOW (rail 12V, relay mati) sebelum autodetect |
| Fail-safe | FLT1/FLT2 dari varian 08 tetap; indeks tip tetap diklem di EEPROM |

Kompilasi: 24.570 byte (79%), RAM 1.078 (52%). Hex 1.537 record, 0 checksum rusak,
alamat 0x0000..0x5FF9. Detail + prosedur uji: `11-firmware-dualrail/BACA-DULU.txt`.

### Batas jujur firmware

Firmware tidak bisa mengukur resistansi kartrid. Kalau kabel ID salah, C210 akan
diberi 24 V → kartrid rusak. Jadi: wiring ID di dalam gagang, satu soket, label
gagang. Rencana tambahan (belum diterapkan, perlu data bangku): deteksi laju
kenaikan suhu — C210 di 24 V naik kira-kira 4× lebih cepat daripada T12 di 24 V.

## Hardware wajib sebelum rail 24V dipakai

| Item | Alasan |
|---|---|
| MOSFET ≥40 V (ganti IRLR7843 30 V) | spike induktif kabel gagang di 24 V bisa menjebol Vds 30 V |
| 5V dari buck (MP1584 / MP2315) | 78M05 di 24 V buang ~2,3 W; sekaligus suplai coil relay |
| Relay SPDT 5V, kontak ≥6 A DC | pemilih rail 12/24 V |
| Buck 24V ≥4 A dan buck 12V ≥8 A | PSU 36 V → modul **input ≥50 V** (mis. tipe 8-60V → 1-36V 15A 200W). XL4015/XL4016 mentok 36-40 V (datasheet XL4016: 5-40 V): **JANGAN** |
| Sekring ikut R kartrid | C210 ~2 Ω → 8 A; T12 ~8 Ω → 3 A fast |
| Kabel ID (D10 → pin 5) | autodetect |

## Urutan uji (jangan dilompati)

1. Pasang relay + 2 buck, **belum** pasang gagang. Ukur: NC = 12 V, NO = 24 V di J1.
2. Flash `11-firmware-dualrail`, buka menu Information → `v1.3-dual`.
3. Colok gagang C210 (ID terbuka) → menu Tip harus `C210`, J1 ≈ 12 V.
4. Colok gagang T12 (pin 5 → GND) saat station hidup → pindah ke `T12` + relay klik,
   J1 ≈ 24 V, pemanas OFF selama ganti.
5. Setpoint 150 °C untuk kedua gagang, ukur tip pakai TC meter: harus naik dan
   berhenti di setpoint. Kalau naik terus → TC kebalik, matikan.
6. Kalibrasi tiap slot (200/280/360 °C) lalu `Store Settings → Yes`.
7. Uji FLT3: beri 24 V ke profil C210 → harus `FLT3` (pemanas terkunci).
8. Uji FLT2: tarik kartrid saat heater ON → heater mati + beep 2× + `FLT2`.
9. Cek panas: 2 menit di 350 °C, kontak soket/kabel gagang tidak hangat berlebih.

## Biaya tambahan (estimasi Shopee)

| Item | Estimasi |
|---|---|
| Modul relay 1 channel 5V | Rp15.000 – 25.000 |
| Buck 24V ≥4A (input ≥50V, mis. 8-60V 15A) | Rp60.000 – 100.000 |
| Buck 12V ≥8A (input ≥50V, mis. 8-60V 15A) | Rp60.000 – 100.000 |
| Buck 5V (MP1584/MP2315) | Rp10.000 – 15.000 |
| MOSFET ≥40V TO-252 | Rp10.000 – 20.000 |
| Kabel ID + flywire D2 | ~Rp0 (sisa kabel) |

Total tambahan ± Rp95.000 – Rp260.000 di atas rencana 12V-only.

## Catatan PSU 36 V (terkonfirmasi)

PSU-mu **36 V 5 A = 180 W**. Beban maksimum hanya satu rail pada satu waktu
(24 V × 3 A = 72 W untuk T12, atau 12 V × 6 A = 72 W untuk C210) → headroom besar,
tidak perlu ganti PSU.

Yang berubah karena 36 V (bukan 32 V):
- Buck **wajib** rating input ≥50 V. XL4015/XL4016 punya batas 40 V (XL4016 datasheet:
  input 5-40 V) — dengan 36 V masuk, ringing + spike saat switching tidak punya margin.
- Disipasi di buck tetap kecil (switching, bukan linear): 36→24 V @3 A ≈ 8 W panas,
  36→12 V @6 A ≈ 8 W panas → modul perlu heatsink, kasih udara.
- Set output **diukur pakai multimeter sebelum tersambung ke board** (rail 24 V
  ke profil C210 = kartrid rusak).
