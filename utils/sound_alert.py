from playsound import playsound
import threading
import os
from pygame import mixer
import time

class SoundAlert:
    def __init__(self, sound_file='assets/sounds/alert.mp3', volume=0.7):
        """
        Ses uyarı sistemi
        
        Args:
            sound_file (str): Alarm ses dosyasının yolu
            volume (float): Ses seviyesi (0.0 - 1.0)
        """
        self.sound_file = sound_file
        self.volume = max(0.0, min(1.0, volume))  # 0.0 ile 1.0 arasında sınırla
        self.is_playing = False
        self.play_thread = None
        
        # Pygame mixer'ı başlat
        mixer.init()
    
    def set_volume(self, volume):
        """
        Ses seviyesini ayarla
        
        Args:
            volume (float): Yeni ses seviyesi (0.0 - 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        if mixer.get_init():
            mixer.music.set_volume(self.volume)
    
    def play(self):
        """Alarm sesini çal"""
        if not self.is_playing:
            self.is_playing = True
            self.play_thread = threading.Thread(target=self._play_sound)
            self.play_thread.daemon = True  # Ana program kapandığında thread de kapansın
            self.play_thread.start()
    
    def _play_sound(self):
        """Ses dosyasını çal"""
        try:
            if os.path.exists(self.sound_file):
                # Pygame ile ses çal
                mixer.music.load(self.sound_file)
                mixer.music.set_volume(self.volume)
                mixer.music.play()
                
                # Ses bitene kadar bekle
                while mixer.music.get_busy():
                    time.sleep(0.1)
            else:
                print(f"❌ Ses dosyası bulunamadı: {self.sound_file}")
        except Exception as e:
            print(f"❌ Ses çalınamadı: {str(e)}")
        finally:
            self.is_playing = False
    
    def stop(self):
        """Ses çalmayı durdur"""
        self.is_playing = False
        if mixer.get_init():
            mixer.music.stop()
        if self.play_thread and self.play_thread.is_alive():
            self.play_thread.join(timeout=1.0)  # 1 saniye timeout ile bekle
    
    def __del__(self):
        """Nesne yok edildiğinde mixer'ı kapat"""
        if mixer.get_init():
            mixer.quit()
