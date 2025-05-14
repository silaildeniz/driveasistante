from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Dashboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Gösterge Paneli")
        label.setFont(QFont("Arial", 18))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        back_button = QPushButton("Ana Menüye Dön")
        back_button.setFixedSize(200, 50)
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def go_back(self):
        self.parent.setCurrentWidget(self.parent.home_screen)
