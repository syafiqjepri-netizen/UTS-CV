import cv2
import numpy as np
import os

def buat_folder_output():
    """Membuat folder output jika belum ada"""
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('img'):
        os.makedirs('img')

def buat_karakter_robot():
    """Membuat karakter robot sederhana"""
    # Buat kanvas putih berukuran 400x400
    kanvas = np.full((400, 400, 3), 255, dtype=np.uint8)
    
    # Gambar badan robot (persegi panjang biru)
    cv2.rectangle(kanvas, (100, 150), (300, 350), (255, 0, 0), -1)  # Badan biru
    cv2.rectangle(kanvas, (100, 150), (300, 350), (0, 0, 0), 2)     # Outline hitam
    
    # Gambar kepala robot (lingkaran)
    cv2.circle(kanvas, (200, 100), 50, (0, 255, 255), -1)  # Kepala kuning
    cv2.circle(kanvas, (200, 100), 50, (0, 0, 0), 2)       # Outline hitam
    
    # Gambar mata robot
    cv2.circle(kanvas, (180, 90), 10, (0, 0, 0), -1)  # Mata kiri
    cv2.circle(kanvas, (220, 90), 10, (0, 0, 0), -1)  # Mata kanan
    
    # Gambar senyum
    cv2.ellipse(kanvas, (200, 110), (20, 10), 0, 0, 180, (0, 0, 0), 2)
    
    # Gambar antena
    cv2.line(kanvas, (200, 50), (200, 30), (0, 0, 0), 3)      # Batang antena
    cv2.circle(kanvas, (200, 25), 8, (255, 0, 0), -1)         # Ujung antena
    
    # Gambar lengan
    cv2.rectangle(kanvas, (70, 180), (100, 220), (0, 255, 0), -1)  # Lengan kiri
    cv2.rectangle(kanvas, (300, 180), (330, 220), (0, 255, 0), -1) # Lengan kanan
    
    # Gambar kaki
    cv2.rectangle(kanvas, (150, 350), (180, 380), (255, 0, 255), -1)  # Kaki kiri
    cv2.rectangle(kanvas, (220, 350), (250, 380), (255, 0, 255), -1)  # Kaki kanan
    
    # Tambahkan teks
    cv2.putText(kanvas, 'ROBOT', (150, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, (0, 0, 0), 2)
    
    return kanvas

def translasi(gambar, x, y):
    """Mentranslasikan gambar"""
    rows, cols = gambar.shape[:2]
    M = np.float32([[1, 0, x], [0, 1, y]])
    return cv2.warpAffine(gambar, M, (cols, rows))

def rotasi(gambar, sudut):
    """Memutar gambar"""
    rows, cols = gambar.shape[:2]
    center = (cols // 2, rows // 2)
    M = cv2.getRotationMatrix2D(center, sudut, 1.0)
    return cv2.warpAffine(gambar, M, (cols, rows))

def resize_gambar(gambar, scale_percent):
    """Mengubah ukuran gambar"""
    width = int(gambar.shape[1] * scale_percent / 100)
    height = int(gambar.shape[0] * scale_percent / 100)
    return cv2.resize(gambar, (width, height), interpolation=cv2.INTER_AREA)

def crop_gambar(gambar, x1, y1, x2, y2):
    """Memotong bagian tertentu dari gambar"""
    return gambar[y1:y2, x1:x2]

def operasi_bitwise():
    """Melakukan operasi bitwise antara dua gambar"""
    # Buat dua gambar dengan ukuran sama
    img1 = np.zeros((300, 300, 3), dtype=np.uint8)
    img2 = np.zeros((300, 300, 3), dtype=np.uint8)
    
    # Gambar lingkaran di img1
    cv2.circle(img1, (150, 150), 100, (255, 255, 255), -1)
    
    # Gambar persegi di img2
    cv2.rectangle(img2, (50, 50), (250, 250), (255, 255, 255), -1)
    
    # Operasi bitwise AND
    result_and = cv2.bitwise_and(img1, img2)
    
    # Operasi bitwise OR
    result_or = cv2.bitwise_or(img1, img2)
    
    # Operasi bitwise XOR
    result_xor = cv2.bitwise_xor(img1, img2)
    
    return result_and, result_or, result_xor

def buat_background():
    """Membuat background gradient jika file tidak ada"""
    background = np.zeros((500, 500, 3), dtype=np.uint8)
    
    # Buat gradient vertikal
    for i in range(500):
        color = int(255 * (i / 500))
        background[i, :] = [color, color//2, 255-color]
    
    cv2.imwrite('img/background.jpg', background)
    return background

def gabungkan_dengan_background(karakter, background):
    """Menggabungkan karakter dengan background"""
    # Resize karakter agar sesuai dengan background
    karakter_resized = cv2.resize(karakter, (200, 200))
    
    # Posisi untuk menempatkan karakter di background
    y_offset, x_offset = 150, 150
    
    # Region of Interest (ROI) di background
    roi = background[y_offset:y_offset+200, x_offset:x_offset+200]
    
    # Buat mask dari karakter (konversi ke grayscale dan threshold)
    karakter_gray = cv2.cvtColor(karakter_resized, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(karakter_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    
    # Area background di ROI
    bg_roi = cv2.bitwise_and(roi, roi, mask=mask_inv)
    
    # Area karakter
    karakter_fg = cv2.bitwise_and(karakter_resized, karakter_resized, mask=mask)
    
    # Gabungkan karakter dengan background
    dst = cv2.add(bg_roi, karakter_fg)
    background[y_offset:y_offset+200, x_offset:x_offset+200] = dst
    
    return background

def main():
    """Program utama"""
    buat_folder_output()
    
    print("Membuat karakter robot...")
    # 1. Buat karakter robot
    karakter = buat_karakter_robot()
    cv2.imwrite('output/karakter.png', karakter)
    
    print("Melakukan transformasi...")
    # 2. Transformasi - Translasi
    karakter_translasi = translasi(karakter, 50, 30)
    cv2.imwrite('output/translate.png', karakter_translasi)
    
    # 3. Transformasi - Rotasi
    karakter_rotasi = rotasi(karakter, 45)  # Rotasi 45 derajat
    cv2.imwrite('output/rotate.png', karakter_rotasi)
    
    # 4. Transformasi - Resize
    karakter_resize = resize_gambar(karakter, 50)  # 50% dari ukuran asli
    cv2.imwrite('output/resize.png', karakter_resize)
    
    # 5. Transformasi - Crop
    karakter_crop = crop_gambar(karakter, 50, 50, 350, 350)
    cv2.imwrite('output/crop.png', karakter_crop)
    
    print("Melakukan operasi bitwise...")
    # 6. Operasi Bitwise
    and_result, or_result, xor_result = operasi_bitwise()
    cv2.imwrite('output/bitwise_and.png', and_result)
    cv2.imwrite('output/bitwise_or.png', or_result)
    cv2.imwrite('output/bitwise_xor.png', xor_result)
    
    print("Membuat gambar final...")
    # 7. Gabungkan dengan background
    if os.path.exists('img/background.jpg'):
        background = cv2.imread('img/background.jpg')
    else:
        background = buat_background()
    
    final_result = gabungkan_dengan_background(karakter, background)
    cv2.imwrite('output/final.png', final_result)
    
    print("Menampilkan hasil...")
    # Tampilkan semua hasil
    cv2.imshow('Karakter Asli', karakter)
    cv2.imshow('Translasi', karakter_translasi)
    cv2.imshow('Rotasi 45 derajat', karakter_rotasi)
    cv2.imshow('Resize 50%', karakter_resize)
    cv2.imshow('Crop', karakter_crop)
    cv2.imshow('Bitwise AND', and_result)
    cv2.imshow('Bitwise OR', or_result)
    cv2.imshow('Bitwise XOR', xor_result)
    cv2.imshow('Final Result', final_result)
    
    print("Semua gambar telah disimpan di folder 'output'")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()