import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from ui.home_screen import HomeScreen
from ui.drive_screen import DriveScreen
from ui.dashboard import Dashboard

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sürücü Asistanı Uygulaması")
        self.setGeometry(100, 100, 1280, 720)

        # Ekranlar
        self.home_screen = HomeScreen(self)
        self.drive_screen = DriveScreen(self)
        self.dashboard = Dashboard(self)
        self.addWidget(self.home_screen)
        self.addWidget(self.drive_screen)
        self.addWidget(self.dashboard)

        self.setCurrentWidget(self.home_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
