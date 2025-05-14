# utils/map_api.py
import geocoder
import requests
from PyQt5.QtGui import QPixmap
from io import BytesIO
import folium
from geopy.geocoders import Nominatim
import os
from dotenv import load_dotenv

def get_map_pixmap():
    try:
        location = geocoder.ip('me')
        lat, lon = location.latlng
        api_key = "AIzaSyAslot15rRd4wpPcVLlwx5kh5UuivCzaQg"
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=14&size=400x300&markers=color:red%7C{lat},{lon}&key={api_key}"
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(BytesIO(response.content).read())
        return pixmap
    except:
        return None

class MapAPI:
    def __init__(self):
        """Harita API'si"""
        load_dotenv()
        self.geolocator = Nominatim(user_agent="driver_assistant")
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    def get_location(self, address="Istanbul"):
        """
        Adres için konum bilgisini al
        
        Args:
            address (str): Adres veya şehir adı
            
        Returns:
            tuple: (latitude, longitude, address)
        """
        try:
            location = self.geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude, location.address
            else:
                raise Exception(f"Konum bulunamadı: {address}")
        except Exception as e:
            raise Exception(f"Konum API hatası: {str(e)}")
    
    def create_map(self, latitude, longitude, zoom_start=13):
        """
        Harita oluştur
        
        Args:
            latitude (float): Enlem
            longitude (float): Boylam
            zoom_start (int): Başlangıç zoom seviyesi
            
        Returns:
            folium.Map: Oluşturulan harita
        """
        try:
            # Harita oluştur
            m = folium.Map(
                location=[latitude, longitude],
                zoom_start=zoom_start,
                tiles='OpenStreetMap'  # Ücretsiz harita servisi
            )
            
            # Konum işaretçisi ekle
            folium.Marker(
                [latitude, longitude],
                popup="Konumunuz",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            return m
        except Exception as e:
            raise Exception(f"Harita oluşturma hatası: {str(e)}")
    
    def save_map(self, map_obj, file_path="temp_map.html"):
        """
        Haritayı HTML dosyası olarak kaydet
        
        Args:
            map_obj (folium.Map): Kaydedilecek harita
            file_path (str): Kayıt yolu
            
        Returns:
            str: Kaydedilen dosyanın yolu
        """
        try:
            map_obj.save(file_path)
            return file_path
        except Exception as e:
            raise Exception(f"Harita kaydetme hatası: {str(e)}")
    
    def get_map_for_location(self, address="Istanbul"):
        """
        Belirtilen konum için harita oluştur ve kaydet
        
        Args:
            address (str): Adres veya şehir adı
            
        Returns:
            tuple: (map_path, location_address)
        """
        try:
            # Konum bilgisini al
            lat, lon, loc_address = self.get_location(address)
            
            # Harita oluştur
            map_obj = self.create_map(lat, lon)
            
            # Haritayı kaydet
            map_path = self.save_map(map_obj)
            
            return map_path, loc_address
        except Exception as e:
            raise Exception(f"Harita işlemi hatası: {str(e)}")
