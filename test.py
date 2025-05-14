from ultralytics import YOLO
import cv2

def test_model_on_camera(model_path):
    # Modeli yükle
    try:
        model = YOLO(model_path)
        print(f"\n✅ Model yüklendi: {model_path}")
        print("🔍 Model sınıfları:", model.names)
    except Exception as e:
        print(f"❌ Model yüklenemedi: {e}")
        return

    # Kamera başlat
    cap = cv2.VideoCapture(0)  # 0, varsayılan kamera

    if not cap.isOpened():
        print("❌ Kamera açılamadı.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Kamera görüntüsü alınamadı.")
            break

        # Model ile tahmin yap
        results = model(frame)[0]

        # Algılanan nesneleri kutu içine al
        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            label = model.names.get(cls_id, "bilinmeyen")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Sonuçları göster
        cv2.imshow("Kamera - Nesne Tespiti", frame)

        # 'q' tuşuna basıldığında çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test etmek istediğin model dosyasını buraya yaz
    test_model_on_camera("models/sign_model.pt")  # Buraya kendi model yolunu yaz
