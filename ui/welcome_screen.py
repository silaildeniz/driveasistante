from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class WelcomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Logo veya başlık
        title = QLabel("Sürücü Asistanına Hoş Geldiniz")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # İsim girişi için frame
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.StyledPanel)
        input_frame.setMaximumWidth(400)
        input_layout = QVBoxLayout()
        
        # İsim girişi etiketi
        name_label = QLabel("Lütfen İsminizi Giriniz:")
        name_label.setFont(QFont('Arial', 12))
        input_layout.addWidget(name_label)
        
        # İsim girişi alanı
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("İsminiz...")
        self.name_input.setFont(QFont('Arial', 12))
        self.name_input.setMinimumHeight(40)
        input_layout.addWidget(self.name_input)
        
        # Devam et butonu
        continue_btn = QPushButton("Devam Et")
        continue_btn.setFont(QFont('Arial', 12))
        continue_btn.setMinimumHeight(40)
        continue_btn.clicked.connect(self.on_continue)
        input_layout.addWidget(continue_btn)
        
        input_frame.setLayout(input_layout)
        layout.addWidget(input_frame)
        
        self.setLayout(layout)
    
    def on_continue(self):
        name = self.name_input.text().strip()
        if name:
            self.parent.set_user_name(name) 