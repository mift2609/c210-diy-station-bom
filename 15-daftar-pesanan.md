# 15 — Daftar pesanan per seller (station solder C210/T12)

Disusun dari BOM board station + board power v2. Harga = estimasi, cek saat checkout.
Tujuan: **2–4 paket saja**, bukan belasan — ongkir lebih besar dari harga komponen kecil.

## Prioritas beli (urut)

1. **Order PCB dulu** (paling lama): board station (`01b-gerber-c210-maskfix.zip`) +
   board power (`13-pcb-power/c210-power-v2-gerber.zip`). Sekalian, biar ongkir sekali.
2. **Modul power** (determinan fungsi): XL4016 8A, XL4015 5A, MP1584, modul relay 5V.
3. **Komponen PCB** (SMD + THT kecil): kit pasif + semikonduktor + Nano + OLED.
4. **Gagang & kartrid**: soket/gagang T210, kartrid C210 (kualitas tip menentukan hasil).
5. **Mekanik & perkabelan** (bisa lokal/offline): PVC, standoff, kabel, sekring, fan, termostat.

## Paket A — seller komponen elektronik (SMD + THT + otak)

| Qty | Item | Spek / kata kunci |
|---|---|---|
| 1 | Kit resistor SMD 0805 | "kit resistor 0805 assorted" |
| 1 | Kit kapasitor SMD 1206 | "kit kapasitor smd 1206 assorted" |
| 1 | Cap 10µF/35V, 22µF/35V, 1µF/35V, 2n2 | pack 100 pcs (sering tidak ada di kit) |
| 1 | LMV358 | SOIC-8 (opsional upgrade: OPA2387) |
| 1 | FMMT619 | SOT-23 — jangan diganti tipe lain |
| 1 | IRLR7843 | TO-252 (30V; cukup untuk 12V saja) |
| 1 | 78M05 | TO-252 (tidak perlu kalau 5V pakai MP1584) |
| 1 | SS54 | SMA |
| 1 | 1N4148W | SOD-123 |
| 1 | Zener 5V1 | SOD-123 |
| 1 | Arduino Nano V3 clone | ATmega328P, cek chip CH340/FTDI |
| 1 | OLED 0,96" SSD1306 I2C | pin harus GND-VCC-SCL-SDA |
| 1 | Rotary encoder EC11 + knob | "encoder ec11 tombol" |
| 1 | Buzzer 5030 | **PASIF** 5V, bukan aktif |
| 1 | Pin header female 1×40 | potong 2×15 untuk socket Nano |
| 1 | Pin header male 1×2 + jumper | untuk J2 |
| 1 set | Sekring 5×20 8A + klip PCB | 8A untuk kartrid ~2 ohm |
| 1 | Saklar getar SW-520D | untuk fitur sleep |
Estimasi: **± Rp220.000** (termasuk Nano + OLED).

## Paket B — seller modul power & konektor

| Qty | Item | Spek |
|---|---|---|
| 1 | Step-down XL4016 8A (XH-M404) | rail 12V C210 |
| 1 | Step-down XL4015 5A CC/CV | rail 24V T12 |
| 1 | Step-down MP1584 | 5V (78M05 di rail 24V terlalu panas) |
| 1 | Modul relay 5V 1 channel | kontak ≥10A; low-trigger boleh (ubah define firmware) |
| 2 | Terminal KF350 2 pin (isi 6 buah) | untuk J1..J13 |
| 1 | Terminal KF350 5 pin | J3 board station (earth tip) |
| 1 set | GX12-5 male + female | konektor gagang |
| 1 | Fan 12V 60×60×25 | ke J12 |
| 1 | Termostat bimetal 45 °C | seri di J13 |
Estimasi: **± Rp250.000**.

## Paket C — seller soldering (gagang & tip)

| Qty | Item | Catatan |
|---|---|---|
| 1 | Soket/sparepart gagang T210 | bagian yang tidak boleh diakali |
| 1 | Kartrid C210 | mechanic / maant / relife |
| 1 | Stand besi + sponge | |
| 1 | Kabel silikon 4-5 core 20AWG 1,5 m | gagang |
| 1 | Kabel silikon 18AWG | rail 6A (J3 → J9 → J1) |
Estimasi: **± Rp200.000 – Rp400.000** (paling menentukan hasil solder).

## Paket D — lokal/offline (bisa Glodok atau toko listrik)

PVC 3 mm 30×40 cm · standoff M3 + sekrup M3 · mesh filter fan · kabel 220V + gland/strain
relief · sekring inline 3A slow · sleeving + heat shrink. Estimasi **± Rp60.000**.

## Teks siap tempel (tanya stok ke seller)

```
Paket A (komponen):
kit resistor 0805 + kit cap 1206; cap 10uF/35V, 22uF/35V, 1uF/35V, 2n2 (pack 100);
LMV358 SOIC-8; FMMT619 SOT-23; IRLR7843 TO-252; 78M05 TO-252; SS54 SMA; 1N4148W SOD-123;
zener 5V1 SOD-123; Arduino Nano V3; OLED 0.96 SSD1306 I2C; encoder EC11 + knob;
buzzer 5030 passive; pin header female 1x40; pin header male 1x2 + jumper;
sekring 5x20 8A + klip; saklar getar SW-520D.

Paket B (modul):
XL4016 8A XH-M404; XL4015 5A CC/CV; MP1584; modul relay 5V 1 channel 10A;
terminal KF350 2 pin 6 pcs; KF350 5 pin; GX12-5 male+female; fan 12V 60x60x25;
termostat bimetal 45C.

Semua dikirim ke Bogor Barat. Ada stok lengkap? kalau ada, minta total + ongkir.
```
