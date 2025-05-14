# utils/map_api.py
import geocoder
import requests
from PyQt5.QtGui import QPixmap
from io import BytesIO

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
