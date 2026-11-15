# 09 — GANTIAN GAGANG: C210 ↔ T210 (satu board, dua gagang)

Ditambahkan: 15 November 2026. Kartrid tetap C210 (kelas 12V) untuk kedua gagang.

## Kesimpulan cepat

| Aspek | Perlu diubah? |
|---|---|
| Elektronik/rail | **Tidak.** 12V, MOSFET 30V cukup, sekring ikut R kartrid (lihat bagian angka) |
| Firmware | Ya, pakai varian `10-firmware-gantian` (basis fail-safe 08 + autodetect gagang) |
| Konektor | **Satu soket GX12-5, colok gantian.** Dua soket paralel = DILARANG |
| Kalibrasi | Per slot (gagang), sekali per gagang/kartrid |

Alasan dua soket paralel dilarang: dua gagang ikut panas bersamaan, dan pembacaan
termokopel jadi paralel → angka suhu ngawur, PID bisa ngegas terus.

## Peta pin GX12-5 (seragam di kedua gagang)

```unknown
1 = H+        heater +
2 = H-/TC-    heater- dan tc- (nyambung di dalam kartrid C210)
3 = TC+       termokopel +
4 = E         badan kartrid -> chassis -> PE   (target: tip-ke-earth < 2 ohm)
5 = SW / ID   switch getar (C210) ATAU ID gagang (T210)
```

Jangan kebalik TC+ (3) dengan TC-/H- (2): suhu terbaca turun saat dipanaskan →
heater ngegas terus (runaway). Uji di setpoint 150 °C dulu, ukur pakai TC meter.

## ID gagang (autodetect slot tip)

Firmware v1.3-C210g membaca pin **D10** (pin sisa di board ini — `SWITCH_PIN` sudah
dipindah ke D3) dan memilih slot tip otomatis:

| Gagang | Pin 5 konektor (SP) | D10 | Slot tip |
|---|---|---|---|
| C210 | kosong | HIGH (pull-up internal) | 0 → nama `C210` |
| T210 | disambung ke GND | LOW | 1 → nama `T210` |

**PCB sudah menyediakan jalurnya** — silkscreen J3 board: `1:P+  2:P-  3:E  4:SW  5:SP`.
Pin 5 bernama **SP (spare)** dan pad-nya punya trace + via sendiri (sesuai komentar
firmware: pin sisa board ini = D10). Jadi tidak perlu edit PCB: yang dikerjakan hanya
**di dalam gagang** — gagang T210: pin 5 disambung ke badan/ground gagang;
gagang C210: pin 5 dibiarkan terbuka.

Verifikasi 5 detik saat board jadi (multimeter, station mati): kontinuitas
**J3 pin 5 ↔ socket Nano D10**. Kalau ternyata SP bukan ke D10, tambah 1 flywire
dari socket Nano D10 ke J3 pin 5 — tetap tidak perlu ubah gerber.

Pembacaan di-*majority vote* 5 sampel biar tahan noise kontak, dan dicek ulang
berkala saat station hidup (± 250 siklus baca) → colok gagang lain, display
otomatis pindah slot + beep. Tanpa autodetect pun tetap bisa: pilih manual di
`Tip Settings → Change Tip`.

## Yang berubah di firmware (`10-firmware-gantian`)

1. `VERSION` → `v1.3-C210g` (muncul di menu Information).
2. Default tip 2 slot: `C210` (slot 0) dan `T210` (slot 1), `NumberOfTips = 2`.
3. Kalibrasi default slot 1 ikut terisi (TEMP200/280/360) — **bukan nol**, supaya
   gagang kedua tidak dibaca dengan kurva rusak sebelum dikalibrasi.
4. `HANDLE_ID_PIN 10`, `TIP_ID_LOW 1`, `TIP_ID_HIGH 0`, `TIP_AUTOSELECT true`.
5. `getEEPROM()` diklem: `NumberOfTips` dijaga 1..TIPMAX dan `CurrentTip` <
   `NumberOfTips`. (EEPROM rusak/aneh dulu bisa membuat indeks lewat array.)
6. Patch fail-safe FLT1/FLT2/FLT3 dari varian 08 tetap ada, tidak diubah.

Hasil kompilasi (arduino-cli, `arduino:avr:nano:cpu=atmega328old`):

```
flash 24.412 byte (79%)   [varian 08: 24.260 (78%), asli: 23.614 (76%)]
RAM    1.075 byte (52%)
hex      1.528 record, 0 checksum rusak, alamat 0x0000..0x5F5B
         (area bootloader > 0x7600 tidak tersentuh)
```

## Cara flash

Sama seperti varian 08 (lihat `08-firmware-safefix/BACA-DULU.txt`):

```unknown
arduino-cli upload -p /dev/ttyUSB0 --fqbn arduino:avr:nano:cpu=atmega328old \
    ~/Downloads/C210/10-firmware-gantian/SolderingStation2_C210_gantian
# atau hex langsung (butuh avrdude):
#   -U flash:w:$HOME/Downloads/C210/10-firmware-gantian/SolderingStation2_C210_gantian.hex:i
```

**LEPAS jumper J2 sebelum upload, pasang lagi setelah selesai.**

Rollback: flash `08-firmware-safefix/SolderingStation2_C210_safefix.hex` (profil
tip kembali 1 slot).

## Prosedur uji gagang kedua (urut, jangan dilompati)

1. **Ukur R kartrid** tiap gagang pakai multimeter (antar pin 1 dan 2).
   Catat: ini yang menentukan sekring + PSU (lihat bagian angka).
2. Wiring gagang T210 → set setpoint **150 °C** → tunggu 60–90 detik.
   Suhu harus naik dan berhenti di sekitar setpoint. Kalau naik terus → matikan,
   periksa polaritas TC.
3. Ukur tip pakai TC meter: selisih vs display masuk akal (< ±40 °C sebelum kalibrasi).
4. Kalibrasi per slot: `Tip Settings → Calibrate Tip` di 200/280/360 °C, lalu
   `Rename Tip` kalau mau (mis. `T210-SK`). Pilih `Store Settings → Yes` agar masuk EEPROM.
5. Uji autodetect: saat station hidup dan sudah mencapai suhu, cabut gagang C210,
   pasang gagang T210 → display harus lompat ke slot `T210` + beep. Kalau tidak:
   cek kabel D10 → pin 5 GX12 di gagang T210.
6. Uji FLT2 (kontak/kartrid): saat heater ON, tarik kartrid keluar → heater harus
   mati + buzzer 2× + tampil `FLT2`. Tekan encoder untuk acknowledge.
7. Uji mekanik: putar/tekuk kabel gagang saat ON → angka display tidak boleh melompat
   (kalau melompat: kontak soket jelek, ganti soket).
8. Cek panas kontak setelah 2 menit di 350 °C: soket/kabel tidak boleh hangat berlebih
   atau berbau. Di 12V arus puncak besar (lihat angka bawah) — kontak jelek di sini
   yang biasanya gagal.

## Angka: R kartrid menentukan sekring & PSU (WAJIB ukur)

Doc lama memakai 8,5 ohm / ~17 W / ~1,4 A — itu angka elemen gaya T12. Data
lapangan JBC C210 ≈ **2 ohm** (klon 2–3 ohm). Rumus: `I = 12 / R`, `P = 144 / R`.

| R kartrid | Arus puncak @12V | Daya | Sekring | PSU |
|---|---|---|---|---|
| ~2 ohm (C210 asli) | ~6,0 A | ~72 W | 8 A | ≥8 A (atau ≥5 A dengan PID, tapi pinggir) |
| ~2,5–3 ohm (klon) | ~4,8–4,0 A | ~58–48 W | 6,3–8 A | ≥6 A |
| ~8,5 ohm (kalau memang segitu) | ~1,4 A | ~17 W | 3 A fast | ≥3 A |

Sekring ≈ 1,25–1,5 × arus ukur. Jangan 3 A fast kalau kartridmu 2 ohm — langsung putus.
PSU tetap **12V, floating/SELV**, jangan yang outputnya terhubung ke earth.

## Biaya tambahan

| Item | Estimasi |
|---|---|
| Gagang kedua (soket T210 + kabel silikon 20AWG + GX12-5 + grip) | Rp60.000 – Rp150.000 |
| ID gagang: tidak ada belanja (pin 5 = SP sudah ada di PCB) | Rp0 |
| Kalau perlu flywire D10→J3 pin 5 (hanya jika SP tidak ke D10) | ~Rp0 (sisa kabel) |

## File terkait

- `10-firmware-gantian/` — source + hex + `BACA-DULU.txt`
- `08-firmware-safefix/` — varian failsafe tanpa autodetect (tetap dipakai/rollback)
- `04-checklist-belanja.html` / `05-belanja-uji.xlsx` — item gagang kedua + koreksi sekring/PSU
