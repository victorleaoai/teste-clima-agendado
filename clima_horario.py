from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import urllib.request
import urllib.parse
import json
import os

CIDADES = {
    "Dubai": {"tz": "Asia/Dubai", "lat": 25.2048, "lon": 55.2708},
    "São Paulo": {"tz": "America/Sao_Paulo", "lat": -23.5505, "lon": -46.6333},
}

HISTORICO_FILE = "historico.json"
PAGINA_URL = "https://victorleaoai.github.io/teste-clima-agendado/"


def buscar_json(url):
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read())


def bloco(titulo, valor):
    print(titulo)
    print(valor)
    print()
    return titulo, valor


def registrar_atualizacao():
    agora = datetime.now(timezone.utc)

    if os.path.exists(HISTORICO_FILE):
        with open(HISTORICO_FILE, "r", encoding="utf-8") as f:
            timestamps = json.load(f)
    else:
        timestamps = []

    timestamps.append(agora.isoformat())

    limite = agora - timedelta(hours=24)
    timestamps = [t for t in timestamps if datetime.fromisoformat(t) > limite]

    with open(HISTORICO_FILE, "w", encoding="utf-8") as f:
        json.dump(timestamps, f)

    return len(timestamps)


def gerar_html(resultado, atualizado_em, qtd_atualizacoes):
    partes = [f"<p><em>Ultima atualizacao: {atualizado_em}</em></p>"]
    for cidade, blocos in resultado.items():
        partes.append(f"<h2>{cidade}</h2>")
        for titulo, valor in blocos:
            partes.append(f"<p><strong>{titulo}</strong><br>{valor}</p>")

    badge_url = "https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=" + urllib.parse.quote(PAGINA_URL, safe="")

    rodape = (
        "<hr>"
        f"<p>Atualizado {qtd_atualizacoes}x nas ultimas 24h</p>"
        f'<p>Visitantes: <img src="{badge_url}" alt="contador de visitas"></p>'
    )

    html = (
        "<!DOCTYPE html>\n"
        "<html lang=\"pt\">\n"
        "<head><meta charset=\"UTF-8\"><title>Clima e hora - Dubai e Sao Paulo</title></head>\n"
        "<body>\n"
        + "\n".join(partes) +
        "\n" + rodape +
        "\n</body></html>"
    )

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def main():
    resultado = {}

    for cidade, info in CIDADES.items():
        hora_local = datetime.now(ZoneInfo(info["tz"])).strftime("%d/%m/%Y %H:%M:%S")

        clima_url = f"https://api.open-meteo.com/v1/forecast?latitude={info['lat']}&longitude={info['lon']}&current_weather=true"
        clima = buscar_json(clima_url)["current_weather"]

        ar_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={info['lat']}&longitude={info['lon']}&current=us_aqi,pm2_5"
        ar = buscar_json(ar_url)["current"]

        print(f"=== {cidade} ===\n")

        blocos = [
            bloco("Hora local | Local time | 当地时间 | يلحملا تقولا", hora_local),
            bloco("Temperatura (°C) | Temperature (°C) | 温度 (°C) | ةرارحلا ةجرد (°C)", clima["temperature"]),
            bloco("Vento (km/h) | Wind (km/h) | 风速 (km/h) | حايرلا ةعرس (km/h)", clima["windspeed"]),
            bloco("Qualidade do ar (US AQI) | Air quality (US AQI) | 空气质量 (US AQI) | ءاوهلا ةدوج (US AQI)", ar["us_aqi"]),
            bloco("PM2.5 (µg/m³)", ar["pm2_5"]),
        ]

        resultado[cidade] = blocos

    atualizado_em = datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
    qtd_atualizacoes = registrar_atualizacao()
    gerar_html(resultado, atualizado_em, qtd_atualizacoes)


if __name__ == "__main__":
    main()
