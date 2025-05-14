import cv2
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QImage, QPixmap
from utils.yolo_detector import YOLODetector
from utils.sound_alert import SoundAlert

class DriveScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.camera = None
        self.timer = None
        self.init_ui()
        self.setup_detector()
        self.setup_sound_alert()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Sol panel (Kamera görüntüsü)
        left_panel = QVBoxLayout()
        
        # Kamera frame
        self.camera_frame = QFrame()
        self.camera_frame.setFrameStyle(QFrame.StyledPanel)
        self.camera_frame.setMinimumSize(800, 600)
        self.camera_label = QLabel("Kamera başlatılıyor...")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_frame.layout = QVBoxLayout()
        self.camera_frame.layout.addWidget(self.camera_label)
        self.camera_frame.setLayout(self.camera_frame.layout)
        left_panel.addWidget(self.camera_frame)
        
        layout.addLayout(left_panel)
        
        # Sağ panel (Kontroller)
        right_panel = QVBoxLayout()
        
        # Durum etiketi
        self.status_label = QLabel("Sürüş Modu Aktif")
        self.status_label.setFont(QFont('Arial', 16, QFont.Bold))
        right_panel.addWidget(self.status_label)
        
        # Tespit edilen nesneler
        self.detection_label = QLabel("Tespit Edilen Nesneler:")
        self.detection_label.setFont(QFont('Arial', 12))
        right_panel.addWidget(self.detection_label)
        
        # Durdur butonu
        stop_button = QPushButton("Sürüşü Durdur")
        stop_button.setFont(QFont('Arial', 16, QFont.Bold))
        stop_button.setMinimumHeight(100)
        stop_button.clicked.connect(self.stop_driving)
        right_panel.addWidget(stop_button)
        
        layout.addLayout(right_panel)
        self.setLayout(layout)
    
    def setup_detector(self):
        """YOLO dedektörü ayarla"""
        model_paths = {
            'sign': 'models/sign_model.pt',
            'light': 'models/light_model.pt',
            'lane': 'models/lane_model.pt'
        }
        self.detector = YOLODetector(model_paths)
    
    def setup_sound_alert(self):
        """Ses uyarı sistemini ayarla"""
        self.sound_alert = SoundAlert()
    
    def start_camera(self):
        """Kamerayı başlat ve görüntü işleme döngüsünü başlat"""
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            self.status_label.setText("Kamera açılamadı!")
            return
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms = ~33 FPS
    
    def stop_camera(self):
        """Kamerayı durdur ve kaynakları temizle"""
        if self.timer:
            self.timer.stop()
        if self.camera:
            self.camera.release()
        self.camera_label.setText("Kamera durduruldu")
        self.sound_alert.stop()
        self.parent.stop_driving()
    
    def update_frame(self):
        """Kamera görüntüsünü al ve işle"""
        ret, frame = self.camera.read()
        if not ret:
            self.status_label.setText("Kamera görüntüsü alınamadı!")
            return
        
        # Nesne tespiti yap
        detections = self.detector.detect(frame)
        
        # Tespit edilen nesneleri göster
        detection_texts = []
        for model_name, label, confidence, (x1, y1, x2, y2) in detections:
            # Görüntüye kutu çiz
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Tespit bilgisini listeye ekle
            detection_texts.append(f"{model_name}: {label} ({confidence:.2f})")
            
            # Alarm çal
            if confidence > 0.5:  # Güven eşiği
                self.sound_alert.play()
        
        # Tespit edilen nesneleri göster
        self.detection_label.setText("Tespit Edilen Nesneler:\n" + "\n".join(detection_texts))
        
        # Görüntüyü Qt formatına dönüştür ve göster
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.camera_label.size(), Qt.KeepAspectRatio))
    
    def stop_driving(self):
        """Sürüşü durdur"""
        self.stop_camera()
