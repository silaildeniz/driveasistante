import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from threading import Thread
from utils.yolo_detector import YOLODetector
from utils.sound_alert import play_alert
from utils.weather_api import get_weather_description

class DriveScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        # YOLO Modelleri
        model_paths = [
            "models/sign_model.pt",
            "models/lane_model.pt",
            "models/light_model.pt"
        ]
        self.detector = YOLODetector(model_paths)

        self.capture = cv2.VideoCapture(0)
        self.video_label = QLabel("Kamera başlatılıyor...")
        self.weather_label = QLabel("Hava Durumu: Alınıyor...")

        self.back_button = QPushButton("Ana Menüye Dön")
        self.back_button.clicked.connect(self.back_to_home)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.weather_label)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

        # Frame sayaç başlat
        self.frame_counter = 0  # Her 5. karede model çalıştırılacak

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Bu 30 ms her kareyi işler

        self.update_weather()

        # Başka bir thread ile video okuma başlatıyoruz
        self.thread = Thread(target=self.video_thread)
        self.thread.start()

    def video_thread(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                continue
            # Çözünürlüğü 640x480'e düşürme
            frame = cv2.resize(frame, (640, 480))

            self.frame_counter += 1
            if self.frame_counter % 5 != 0:  # Her 5 karede bir model çalıştırsın
                continue

            results = self.detector.detect(frame)
            for label, box in results:
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            self.update_frame(frame)  # GUI'yi güncelle

    def update_frame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(image))

    def update_weather(self):
        weather = get_weather_description()
        self.weather_label.setText(f"Hava Durumu: {weather}")

    def back_to_home(self):
        self.capture.release()
        self.thread.join()  # Thread'i durdur
        self.timer.stop()
        self.parent.setCurrentWidget(self.parent.home_screen)
