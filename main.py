import cv2
import numpy as np

# Bağlı kameraları bulma
index = 0  # Kamera indeksini başlat
connected_cameras = []  # Bağlı kameraları saklamak için liste
while True:
    cap = cv2.VideoCapture(index)  # Kamerayı açmayı dene
    if not cap.read()[0]:  # Kameradan görüntü okuma başarısızsa
        break  # Döngüyü sonlandır
    else:
        connected_cameras.append(index)  # Bağlı kamerayı listeye ekle
    cap.release()  # Kamerayı serbest bırak
    index += 1  # Bir sonraki kamerayı kontrol et

print(f"Bağlı kameralar: {connected_cameras}")  # Bulunan kameraları yazdır

# Madeni para değerlerini belirleme (çap kullanarak)
def get_coin_value(diameter):
    if diameter < 60:  # 60 piksel çap = 30 piksel yarıçap, küçük çapları dikkate alma
        return 0  # Geçersiz çap, değer 0
    if diameter < 170:
        return 0.05  # 5 kuruş
    elif diameter < 185:
        return 0.10  # 10 kuruş
    elif diameter < 205:
        return 0.25  # 25 kuruş
    elif diameter < 240:
        return 0.50  # 50 kuruş
    else:
        return 1.00  # 1 TL

# Bir görüntü karesini işleme fonksiyonu
def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Görüntüyü gri tonlamaya çevir
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Görüntüyü bulanıklaştır
    
    # Eşikleme (thresholding) işlemi
    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Kenar tespiti (Canny algoritması)
    canny = cv2.Canny(blur, 30, 150)
    
    # Kenarları kalınlaştırma (dilate işlemi)
    dilated = cv2.dilate(canny, (3, 3), iterations=2)
    
    # Kontur tespiti
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Görüntüyü RGB formatına çevir
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Tespit edilen konturları çiz
    cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)

    total_value = 0  # Toplam madeni para değeri
    valid_contours = []  # Geçerli konturları saklamak için liste

    for contour in contours:
        # En küçük çemberi bul ve çapını hesapla
        (x, y), radius = cv2.minEnclosingCircle(contour)
        diameter = radius * 2
        if diameter >= 60:  # 60 pikselden küçük çaplar dikkate alınmayacak
            total_value += get_coin_value(diameter)  # Madeni paranın değerini ekle
            valid_contours.append(contour)  # Geçerli konturu listeye ekle

    coin_count = len(valid_contours)  # Geçerli madeni paraların sayısı
    return rgb, coin_count, total_value  # İşlenmiş görüntü, madeni para sayısı ve toplam değer

# Kameranın indeksini burada kullanın
camera_index = 1  # Kullanılacak kamera indeksi
cap = cv2.VideoCapture(camera_index)  # Kamera kaynağını başlat

if not cap.isOpened():  # Kamera açılamadıysa
    raise Exception("Kamera açılamadı.")  # Hata fırlat

while True:
    ret, frame = cap.read()  # Kameradan bir kare oku
    if not ret:  # Kare okuma başarısızsa
        break  # Döngüyü sonlandır

    # Görüntü karesini işle
    processed_frame, coin_count, total_value = process_frame(frame)

    # İşlenmiş görüntü üzerine metin ekle
    cv2.putText(processed_frame, f'Madeni Para Sayisi: {coin_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Toplam Deger: {total_value:.2f} TL', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Gercek Zamanli Madeni Para Sayma', processed_frame)  # İşlenmiş görüntüyü göster

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 'q' tuşuna basılınca döngüyü sonlandır
        break

cap.release()  # Kamera kaynağını serbest bırak
cv2.destroyAllWindows()  # Tüm OpenCV pencerelerini kapat
