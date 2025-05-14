import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt
from ui.welcome_screen import WelcomeScreen
from ui.dashboard import Dashboard
from ui.drive_screen import DriveScreen

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sürücü Asistanı")
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        # Kullanıcı bilgilerini saklamak için
        self.user_name = None
        
        # Ekranları oluştur
        self.welcome_screen = WelcomeScreen(self)
        self.dashboard = Dashboard(self)
        self.drive_screen = DriveScreen(self)
        
        # Ekranları widget'a ekle
        self.addWidget(self.welcome_screen)
        self.addWidget(self.dashboard)
        self.addWidget(self.drive_screen)
        
        # Başlangıç ekranını ayarla
        self.setCurrentWidget(self.welcome_screen)
    
    def set_user_name(self, name):
        """Kullanıcı adını ayarla ve dashboard'a geç"""
        self.user_name = name
        self.dashboard.update_welcome_message(name)
        self.setCurrentWidget(self.dashboard)
    
    def start_driving(self):
        """Sürüş ekranına geç"""
        self.drive_screen.start_camera()
        self.setCurrentWidget(self.drive_screen)
    
    def stop_driving(self):
        """Sürüşü durdur ve dashboard'a dön"""
        self.drive_screen.stop_camera()
        self.setCurrentWidget(self.dashboard)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
