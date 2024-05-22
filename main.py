import cv2
import numpy as np

# Bağlı kameraları bulma
index = 0
connected_cameras = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        connected_cameras.append(index)
    cap.release()
    index += 1

print(f"Bağlı kameralar: {connected_cameras}")

def get_coin_value(radius):
    if radius < 76:
        return 0.05  # 5 kuruş
    elif radius < 81:
        return 0.10  # 10 kuruş
    elif radius < 87:
        return 0.25  # 25 kuruş
    elif radius < 103:
        return 0.50  # 50 kuruş
    else:
        return 1.00  # 1 TL

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Eşikleme
    _, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
    
    # Kenar Tespiti
    canny = cv2.Canny(blur, 30, 150)
    
    # Kenarları kalınlaştırma
    dilated = cv2.dilate(canny, (3, 3), iterations=2)
    
    # Kontur Tespiti
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # RGB formatına dönüştürme
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Konturları çizme
    cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)

    total_value = 0
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        total_value += get_coin_value(radius)

    coin_count = len(contours)
    return rgb, coin_count, total_value

# Kameranın indeksini burada kullanın
camera_index = 1
cap = cv2.VideoCapture(camera_index)  # Kamera kaynağını başlat 

if not cap.isOpened():
    raise Exception("Kamera açılamadı.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame, coin_count, total_value = process_frame(frame)

    cv2.putText(processed_frame, f'Madeni Para Sayisi: {coin_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(processed_frame, f'Toplam Deger: {total_value:.2f} TL', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Gercek Zamanli Madeni Para Sayma', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
