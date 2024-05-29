import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Ön işleme: Görüntüyü yükle ve gri tonlamaya dönüştür
image = cv2.imread(r'C:\coin_counting-main\Kontur1.jpg')
if image is None:
    raise FileNotFoundError("Görüntü dosyası bulunamadı. Dosya yolunu ve ismini kontrol edin.")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray, cmap='gray')
plt.title('Gri Tonlamalı Görüntü')
plt.axis('off')
plt.show()

# 2. Yumuşatma: Gürültüyü azaltmak için Gaussian yumuşatma uygula
blur = cv2.GaussianBlur(gray, (5, 5), 0)
plt.imshow(blur, cmap='gray')
plt.title('Yumuşatılmış Gri Tonlamalı Görüntü')
plt.axis('off')
plt.show()

# 3. Eşikleme: Yumuşatılmış görüntüye ikili (binary) eşikleme uygula
_, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
plt.imshow(thresh, cmap='gray')
plt.title('Eşiklenmiş Görüntü')
plt.axis('off')
plt.show()

# 4. Kenar Tespiti: Eşiklenmiş görüntüye Canny kenar tespiti uygula
canny = cv2.Canny(blur, 30, 150)
plt.imshow(canny, cmap='gray')
plt.title('Kenar Tespit Edilmiş Görüntü')
plt.axis('off')
plt.show()

# Kenarları kalınlaştırma (dilate) işlemi uygula
dilated = cv2.dilate(canny, (1, 1), iterations=2)
plt.imshow(dilated, cmap='gray')
plt.title('Kalınlaştırılmış Kenar Tespit Görüntüsü')
plt.axis('off')
plt.show()

# 5. Kontur Tespiti: Kenar tespit edilmiş görüntüde konturları bul
contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Madeni para değerlerini belirleme (madeni para boyutlarının bilindiği ve sabit olduğu varsayımıyla)
def get_coin_value(diameter):
    if diameter < 100:  # 60 piksel çap = 30 piksel yarıçap
        return 0
    if diameter < 100:
        return 0.05  # 5 kuruş
    elif diameter < 132:
        return 0.10  # 10 kuruş
    elif diameter < 145:
        return 0.25  # 25 kuruş
    elif diameter < 168:  
        return 0.50  # 50 kuruş
    else:
        return 1.00  # 1 TL

total_value = 0
filtered_contours = []

# Filtrelenmiş konturları toplama ve toplam değeri hesaplama
for contour in contours:
    (x, y), radius = cv2.minEnclosingCircle(contour)
    diameter = radius * 2
    if diameter >= 100:
        filtered_contours.append(contour)
        print(f'Kontur çapı: {diameter:.2f} piksel')  # Kontur çapını yazdırma
        total_value += get_coin_value(diameter)

# Filtrelenmiş konturların sayısı
print('Görüntüdeki madeni para sayısı: ', len(filtered_contours))

print(f'Toplam değer: {total_value:.2f} TL')

# Filtrelenmiş konturları çizme
rgb_filtered = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
cv2.drawContours(rgb_filtered, filtered_contours, -1, (0, 255, 0), 2)
plt.imshow(rgb_filtered)
plt.title('Filtrelenmiş Konturlu Görüntü')
plt.axis('off')
plt.show()
