import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


class WeatherAPI:
    def __init__(self, cache_duration_minutes=30):
        """
        Hava durumu API'si

        Args:
            cache_duration_minutes (int): Önbellek süresi (dakika)
        """
        load_dotenv()
        # API anahtarını doğrudan tanımla
        self.api_key = "48f6c06054e0ca97d85db9ebbecc9826"
        self.cache = {}
        self.cache_duration = timedelta(minutes=cache_duration_minutes)

    def get_weather(self, city="Istanbul"):
        """
        Belirtilen şehir için hava durumu bilgisini al

        Args:
            city (str): Şehir adı

        Returns:
            dict: Hava durumu bilgileri
                {
                    'city': str,
                    'temperature': float,
                    'description': str,
                    'humidity': int,
                    'last_update': str
                }
        """
        # Önbellekte varsa ve süresi geçmemişse önbellekten döndür
        if city in self.cache:
            cache_time, cache_data = self.cache[city]
            if datetime.now() - cache_time < self.cache_duration:
                return cache_data

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'tr'
            }

            response = requests.get(url, params=params, timeout=10)  # 10 saniye timeout
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    'city': city,
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'last_update': datetime.now().strftime('%H:%M')
                }

                # Önbelleğe kaydet
                self.cache[city] = (datetime.now(), weather_data)

                return weather_data
            else:
                error_msg = data.get('message', 'Bilinmeyen hata')
                raise Exception(f"Hava durumu bilgisi alınamadı: {error_msg}")

        except requests.Timeout:
            raise Exception("Hava durumu API'sine bağlantı zaman aşımına uğradı")
        except requests.RequestException as e:
            raise Exception(f"Hava durumu API bağlantı hatası: {str(e)}")
        except Exception as e:
            raise Exception(f"Hava durumu API hatası: {str(e)}")

    def format_weather_text(self, weather_data):
        """
        Hava durumu bilgilerini formatlı metne dönüştür

        Args:
            weather_data (dict): get_weather() metodundan dönen veri

        Returns:
            str: Formatlı hava durumu metni
        """
        return f"""
        Şehir: {weather_data['city']}
        Sıcaklık: {weather_data['temperature']}°C
        Durum: {weather_data['description']}
        Nem: {weather_data['humidity']}%
        Son Güncelleme: {weather_data['last_update']}
        """

    def clear_cache(self):
        """Önbelleği temizle"""
        self.cache.clear()
