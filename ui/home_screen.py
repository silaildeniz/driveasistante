from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomeScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Sürücü Asistanı Uygulamasına Hoş Geldiniz")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        start_button = QPushButton("Sürüşü Başlat")
        start_button.setFixedSize(200, 60)
        start_button.clicked.connect(self.go_to_drive)
        layout.addWidget(start_button)

        dashboard_button = QPushButton("Gösterge Paneli")
        dashboard_button.setFixedSize(200, 60)
        dashboard_button.clicked.connect(self.go_to_dashboard)
        layout.addWidget(dashboard_button)

        self.setLayout(layout)

    def go_to_drive(self):
        self.parent.setCurrentWidget(self.parent.drive_screen)

    def go_to_dashboard(self):
        self.parent.setCurrentWidget(self.parent.dashboard)
