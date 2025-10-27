# UTS Computer Vision - Karakter Robot

## Informasi Mahasiswa
- **Nama:** [Mohd Syafiq]
- **NIM:** [43050230039]

## Deskripsi Karakter
Karakter yang dibuat adalah **Robot Sederhana** dengan komponen-komponen berikut:

### Komponen Karakter:
1. **Kepala**: Lingkaran kuning dengan mata hitam dan senyum
2. **Badan**: Persegi panjang biru sebagai tubuh utama
3. **Antena**: Garis vertikal dengan bola biru di ujungnya
4. **Lengan**: Persegi panjang hijau di sisi kiri dan kanan
5. **Kaki**: Persegi panjang magenta di bagian bawah
6. **Teks**: Tulisan "ROBOT" di atas kepala

Karakter ini dirancang sederhana namun memiliki semua elemen dasar yang membentuk figur robot klasik.

## Transformasi yang Diterapkan

### 1. Translasi (Pergeseran)
- **Fungsi**: `translasi()`
- **Parameter**: Geser 50 piksel horizontal, 30 piksel vertikal
- **Tujuan**: Mengubah posisi karakter tanpa mengubah bentuk

### 2. Rotasi (Pemutaran)
- **Fungsi**: `rotasi()`
- **Parameter**: Sudut 45 derajat
- **Tujuan**: Memutar karakter sekitar titik pusat

### 3. Resize (Pengubahan Ukuran)
- **Fungsi**: `resize_gambar()`
- **Parameter**: Skala 50% dari ukuran asli
- **Tujuan**: Mengecilkan ukuran karakter

### 4. Crop (Pemotongan)
- **Fungsi**: `crop_gambar()`
- **Parameter**: Koordinat (50,50) hingga (350,350)
- **Tujuan**: Memotong bagian tepi gambar

## Operasi yang Diterapkan

### 1. Operasi Bitwise
- **Bitwise AND**: Irisan antara lingkaran dan persegi
- **Bitwise OR**: Gabungan antara lingkaran dan persegi  
- **Bitwise XOR**: Area yang tidak tumpang tindih antara lingkaran dan persegi

### 2. Operasi Aritmatika
- **Penggabungan dengan Background**: Menggunakan operasi bitwise untuk menempatkan karakter di atas background gradient dengan transparansi

## Teknik yang Digunakan
- **Masking**: Untuk isolasi area karakter
- **ROI (Region of Interest)**: Untuk penempatan presisi
- **Color Space Manipulation**: Untuk operasi bitwise

## Hasil Output
Semua hasil transformasi dan operasi disimpan dalam folder `output/` dengan format PNG.