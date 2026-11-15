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
Board yang dipakai: silkscreen **"Wagiminator mod – Nano" / "C210 CTRL 12V"** —
J1 +12V, J2 jumper (lepas saat flash), J4 OLED, J3 GX12-5 (P+/P-/E/SW/SP), FUSE 8A.
Silk 8A itu justru **benar** untuk C210 di 12 V (~6 A); angka lama 8,5 Ω / 1,4 A yang
salah. Untuk rail 24 V (T12, 3 A) sekring 8 A longgar tapi aman — kalau mau proteksi
lebih rapat bisa diturunkan ke 5 A, asal rail 12 V tidak dipakai menembak C210.
CATATAN: board ini berlabel 12 V — rail 24 V menuntut upgrade MOSFET ≥40 V + 5 V dari
buck seperti di tabel bawah.

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
2. ID gagang → **pin 5 konektor gagang = SP (spare)**. Jalur ini sudah ada di PCB
   (silkscreen J3: `1:P+ 2:P- 3:E 4:SW 5:SP`; pin 4 = SW getar, pin 5 = SP dengan
   trace + via sendiri). Tidak perlu edit gerber. Yang dikerjakan hanya di dalam
   gagang: T12 → pin 5 ke GND; C210 → pin 5 terbuka.
   Verifikasi saat board jadi: kontinuitas **J3 pin 5 ↔ socket Nano D10**
   (sesuai komentar firmware: pin sisa board = D10).
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
| ID gagang di dalam gagang (pin 5 = SP, jalur sudah ada di PCB) | autodetect; verifikasi kontinuitas SP ↔ D10 |

## Relay: modul di LUAR PCB (bukan di board)

PCB tidak diedit. Relay = **modul relay 5 V 1 channel** yang dipasang di dalam
enclosure, disambung kabel:

```unknown
buck 12V (+) --[NC]                    [COM]-- J1 (+) board
buck 24V (+) --[NO]   modul relay SPDT (SRD-05VDC)
D2 (socket Nano) --[IN]     VCC-> 5V buck    GND-> GND common
```

- Modul relay sudah berisi transistor + dioda flyback + optocoupler, jadi tidak
  perlu rangkaian tambahan. Yang di-PCB cuma tidak ada footprint-nya.
- Jumper trigger modul (kalau ada) set ke **HIGH trigger** → pin HIGH = coil nyala
  = rail 24 V, cocok dengan `RAIL_SEL_24V_LEVEL = HIGH`. Kalau modulmu cuma
  low-trigger, ubah define itu jadi `LOW` dan ulangi compile.
- Kontak relay hanya berganti saat pemanas OFF (arus 0) → tidak ada busur.
- Kabel: 20AWG minimal, terminal sekrup, jalur sependek mungkin.
- Coil ambil 5 V dari buck 5 V, bukan dari 78M05 (di rail 24 V 78M05 sudah panas).

Alternatif tanpa relay: **saklar SPDT manual ≥6 A DC** (Rp10-20 rb) yang memilih
buck 12 V atau buck 24 V. Otomatisnya hilang, tapi FLT3 tetap jadi penjaga: profil
C210 (rail 12 V) yang diberi 24 V langsung mengunci pemanas.

## Kalau pakai modul XL4015 (5A)

Fakta (datasheet XL4015 Rev 2.0): IC berlabel "5A 180KHz **36V** Buck", input 8-36 V,
abs max 40 V; output 1,25-32 V; modul komersial ditulis 5-36 V (ada yang 4-38 V).
"0-5 A" itu rating IC; kontinu realistis 3-4 A dengan heatsink.

| Rail | Kartrid | Arus | XL4015 |
|---|---|---|---|
| 24 V (T12) | 8 ohm | 3,0 A | cukup, lega |
| 12 V (C210) | 2 ohm | 6,0 A | **tidak cukup** |
| 12 V (C210 klon) | 2,5 ohm | 4,8 A | pinggir |
| 12 V (C210 klon) | 3 ohm | 4,0 A | cukup tanpa margin |

Aturan:
1. Input 36 V = tepat di batas rating IC (margin nol). Cek trimpot di board PSU:
   kalau output bisa diturunkan ke ~30 V, XL4015 aman dan 24 V out masih tercapai
   (dropout XL4015 ~1,5-2 V).
2. Rail 24 V (T12): XL4015 aman.
3. Rail 12 V (C210): pakai versi **CC/CV** (ada pot arus), set limit ~5 A -> tip panas
   lebih lambat (4 A x 12 V = 48 W, dari 72 W) tapi modul tidak mati. Mau panas penuh
   dengan kartrid 2 ohm: pakai modul >= 8 A dengan input >= 50 V.
4. Jangan paralel dua XL4015 untuk menambah arus: tanpa load sharing, satu modul
   menanggung hampir semua beban.
5. Board power (13-pcb-power) TIDAK perlu diubah: slot-nya terminal block, modul apa
   pun bisa dipasang.

## Alternatif modul step-down (selain XL4015)

Semua modul di bawah ini cocok dengan board power `13-pcb-power` (slot-nya terminal,
tidak ada perubahan PCB). Cek ukuran fisik modul sebelum memesan — SZBK07 sekitar
65x47 mm, jadi dua modul SZBK07 **tidak muat** di board 90x60 (taruh di samping board
di dalam box).

| Modul | Input | Output / arus | Catatan | Rail |
|---|---|---|---|---|
| **SZBK07** (CC/CV, 300W) | 6-40 V | 1,2-36 V, 20 A | headroom besar, bisa set limit arus; input 36 V margin 4 V | 12 V **dan** 24 V |
| **6A synchronous 5,5-60 V** | 5,5-60 V | 3,3-24 V, 6 A | margin input paling lega, kecil (~45x25 mm) | 12 V (pas) / 24 V (lega) |
| **10-90 V → 6 A (100W)** | 10-90 V | 1,5-60 V, 6 A | margin input terbesar, murah | 12 V / 24 V |
| **XL4016 (8 A)** | 5-40 V | 1,25-36 V, 8 A | keluarga XL4015, arus lebih besar; input 36 V tetap mepet | 12 V (lebih baik dari XL4015) |
| **Konverter 12 V fixed 10 A** (tipe mobil) | 8-40 V (ada 60-72 V) | 12 V, 10 A | tidak bisa diatur, tapi kokoh; ambil versi input >=60 V | 12 V |

Aturan pilih: **input rating >= 45 V** kalau bisa (rail PSU 36 V + spike), dan **arus
>= 1,5x beban kerja**. Untuk C210 2 ohm di 12 V (6 A) -> minimal modul 8-10 A, atau
modul CC/CV yang dibatasi ~6-7 A.

Kalau nanti mau rangkaian buck-nya diskret di PCB (bukan modul): pakai IC kelas 60 V —
TPS54560 (input 4,5-60 V, 5 A) untuk rail 24 V; untuk rail 12 V 6 A pakai controller
60-80 V + MOSFET eksternal (mis. LM5085 / LM5145). Itu desain baru + hitungan induktor
sendiri, bukan tempel modul.

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
| Kabel flywire D2 → relay IN (1 kabel) | ~Rp0 (sisa kabel) |

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
