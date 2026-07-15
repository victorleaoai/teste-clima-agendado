from datetime import datetime
from zoneinfo import ZoneInfo
import urllib.request
import json

CIDADES = {
    "Dubai": {"tz": "Asia/Dubai", "lat": 25.2048, "lon": 55.2708},
    "São Paulo": {"tz": "America/Sao_Paulo", "lat": -23.5505, "lon": -46.6333},
}


def buscar_json(url):
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


def bloco(titulo, valor):
    print(titulo)
    print(valor)
    print()


def main():
    for cidade, info in CIDADES.items():
        hora_local = datetime.now(ZoneInfo(info["tz"])).strftime("%d/%m/%Y %H:%M:%S")

        clima_url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current_weather=true"
        clima = buscar_json(clima_url)["current_weather"]

        ar_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={info['lat']}&longitude={info['lon']}&current=us_aqi,pm2_5"
        ar = buscar_json(ar_url)["current"]

        print(f"=== {cidade} ===\n")

        bloco("Hora local | Local time | 当地时间 | يلحملا تقولا", hora_local)
        bloco("Temperatura (°C) | Temperature (°C) | 温度 (°C) | ةرارحلا ةجرد (°C)", clima["temperature"])
        bloco("Vento (km/h) | Wind (km/h) | 风速 (km/h) | حايرلا ةعرس (km/h)", clima["windspeed"])
        bloco("Qualidade do ar (US AQI) | Air quality (US AQI) | 空气质量 (US AQI) | ءاوهلا ةدوج (US AQI)", ar["us_aqi"])
        bloco("PM2.5 (µg/m³)", ar["pm2_5"])


if __name__ == "__main__":
    main()
