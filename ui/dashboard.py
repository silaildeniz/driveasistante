from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from utils.weather_api import WeatherAPI
from utils.map_api import MapAPI
import os

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.weather_api = WeatherAPI()
        self.map_api = MapAPI()
        self.init_ui()
        self.setup_timers()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Sol panel (Harita ve Hava Durumu)
        left_panel = QVBoxLayout()
        
        # Karşılama mesajı
        self.welcome_label = QLabel("Hoş Geldiniz")
        self.welcome_label.setFont(QFont('Arial', 24, QFont.Bold))
        left_panel.addWidget(self.welcome_label)
        
        # Harita frame
        map_frame = QFrame()
        map_frame.setFrameStyle(QFrame.StyledPanel)
        map_frame.setMinimumHeight(300)
        self.map_label = QLabel("Harita Yükleniyor...")
        map_frame.layout = QVBoxLayout()
        map_frame.layout.addWidget(self.map_label)
        map_frame.setLayout(map_frame.layout)
        left_panel.addWidget(map_frame)
        
        # Hava durumu frame
        weather_frame = QFrame()
        weather_frame.setFrameStyle(QFrame.StyledPanel)
        weather_frame.setMinimumHeight(200)
        self.weather_label = QLabel("Hava Durumu Yükleniyor...")
        weather_frame.layout = QVBoxLayout()
        weather_frame.layout.addWidget(self.weather_label)
        weather_frame.setLayout(weather_frame.layout)
        left_panel.addWidget(weather_frame)
        
        layout.addLayout(left_panel)
        
        # Sağ panel (Sürüş başlatma butonu)
        right_panel = QVBoxLayout()
        start_button = QPushButton("Sürüşü Başlat")
        start_button.setFont(QFont('Arial', 24, QFont.Bold))
        start_button.setMinimumHeight(200)
        start_button.clicked.connect(self.start_driving)
        right_panel.addWidget(start_button)
        
        layout.addLayout(right_panel)
        self.setLayout(layout)
    
    def setup_timers(self):
        # Harita ve hava durumu güncelleme zamanlayıcıları
        self.map_timer = QTimer()
        self.map_timer.timeout.connect(self.update_map)
        self.map_timer.start(300000)  # 5 dakikada bir güncelle
        
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(1800000)  # 30 dakikada bir güncelle
        
        # İlk güncellemeleri yap
        self.update_map()
        self.update_weather()
    
    def update_welcome_message(self, name):
        self.welcome_label.setText(f"Hoş Geldiniz, {name}")
    
    def update_map(self):
        try:
            map_path, location_address = self.map_api.get_map_for_location()
            self.map_label.setText(f"Konum: {location_address}")
        except Exception as e:
            self.map_label.setText(f"Harita yüklenemedi: {str(e)}")
    
    def update_weather(self):
        try:
            weather_data = self.weather_api.get_weather()
            weather_text = self.weather_api.format_weather_text(weather_data)
            self.weather_label.setText(weather_text)
        except Exception as e:
            self.weather_label.setText(f"Hava durumu yüklenemedi: {str(e)}")
    
    def start_driving(self):
        self.parent.start_driving()
