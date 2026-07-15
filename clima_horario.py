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


def main():
    for cidade, info in CIDADES.items():
        hora_local = datetime.now(ZoneInfo(info["tz"])).strftime("%d/%m/%Y %H:%M:%S")

        clima_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={info['lat']}&longitude={info['lon']}&current_weather=true"
        )
        clima = buscar_json(clima_url)["current_weather"]

        ar_url = (
            f"https://air-quality-api.open-meteo.com/v1/air-quality?"
            f"latitude={info['lat']}&longitude={info['lon']}&current=us_aqi,pm2_5"
        )
        ar = buscar_json(ar_url)["current"]

        print(f"--- {cidade} ---")
        print(f"Hora local: {hora_local}")
        print(f"Temperatura: {clima['temperature']}°C | Vento: {clima['windspeed']} km/h")
        print(f"Qualidade do ar (US AQI): {ar['us_aqi']} | PM2.5: {ar['pm2_5']} µg/m³")
        print()


if __name__ == "__main__":
    main()
