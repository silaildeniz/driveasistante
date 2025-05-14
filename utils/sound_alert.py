import playsound
import os

def play_alert():
    # Tek bir ses dosyası
    alert_sound_path = "assets/sounds/alert.mp3"

    # Ses dosyasının var olup olmadığını kontrol et
    if os.path.exists(alert_sound_path):  # Dosya var mı diye kontrol et
        print(f"Çalınacak ses: {alert_sound_path}")  # Debug mesajı
        playsound.playsound(alert_sound_path, block=False)
    else:
        print(f"Ses dosyası bulunamadı: {alert_sound_path}")
