import requests

def get_weather_description():
    try:
        api_key = "48f6c06054e0ca97d85db9ebbecc9826"
        lat, lon = 41.01, 28.97  # örnek: İstanbul
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=tr"
        response = requests.get(url)
        data = response.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{desc}, {temp}°C"
    except Exception as e:
        return f"Hava bilgisi alınamadı: {e}"
