from flask import Flask, request, render_template_string
import requests
import time
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SkyPulse | Weather Dashboard</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    min-height: 100vh;
    font-family: Arial, Helvetica, sans-serif;
    transition: 0.3s;
}

body.day {
    background: linear-gradient(135deg, #eaf5ff, #f8fbff);
    color: #172d4d;
    --card: #ffffff;
    --muted: #63758d;
    --border: #e0e9f4;
    --accent: #2878ed;
    --soft: #edf5ff;
}

body.night {
    background: linear-gradient(135deg, #101a31, #202b48);
    color: #f2f5ff;
    --card: #202c46;
    --muted: #b0bdd4;
    --border: #35435e;
    --accent: #83b5ff;
    --soft: #293953;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 8%;
    gap: 15px;
}

.logo { font-size: 25px; font-weight: bold; }
.tagline { font-size: 13px; color: var(--muted); }

main {
    width: min(950px, 90%);
    margin: 35px auto;
}

.hero { text-align: center; margin-bottom: 35px; }

.eyebrow {
    color: var(--accent);
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 2px;
    margin-bottom: 14px;
}

h1 {
    font-size: clamp(36px, 6vw, 55px);
    line-height: 1.15;
    margin-bottom: 15px;
}

.subtitle { color: var(--muted); margin-bottom: 25px; }

.search-form {
    display: flex;
    max-width: 510px;
    margin: auto;
    gap: 10px;
}

input {
    flex: 1;
    min-width: 0;
    padding: 15px;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: var(--card);
    color: inherit;
    outline: none;
}

input:focus { border-color: var(--accent); }

button {
    padding: 0 23px;
    border: none;
    border-radius: 12px;
    background: var(--accent);
    color: white;
    font-weight: bold;
    cursor: pointer;
}

button:hover { opacity: 0.85; }

.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 12px 35px #0000000a;
}

.weather-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
}

.weather-top h2 { font-size: 25px; margin: 10px 0; }

.weather-icon { font-size: 55px; }

.muted {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.7;
}

.temperature {
    font-size: clamp(65px, 12vw, 90px);
    font-weight: bold;
    letter-spacing: -4px;
    margin-top: 18px;
}

.temperature span {
    font-size: 38px;
    vertical-align: top;
}

.description { font-size: 22px; margin: 6px 0; }

.metrics {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
    margin-top: 28px;
}

.metric {
    padding: 16px 13px;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow-wrap: anywhere;
}

.metric-icon { font-size: 24px; }

.metric p {
    font-size: 12px;
    color: var(--muted);
    margin: 11px 0 8px;
}

.metric h3 { font-size: 17px; }

.aqi-label {
    display: inline-block;
    margin-top: 8px;
    padding: 5px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: bold;
    background: var(--soft);
}

.aqi-good { color: #16834a; }
.aqi-moderate { color: #a56a00; }
.aqi-sensitive { color: #b45b12; }
.aqi-unhealthy { color: #d64242; }
.aqi-very-unhealthy { color: #a02bc1; }
.aqi-hazardous { color: #9e2434; }
.aqi-unknown { color: var(--muted); }

.section-heading { margin-bottom: 20px; }

.section-heading h2 {
    font-size: 22px;
    margin-bottom: 7px;
}

.forecast-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 12px;
}

.forecast-day {
    text-align: center;
    padding: 17px 8px;
    background: var(--soft);
    border-radius: 15px;
    border: 1px solid var(--border);
}

.forecast-day .day-name {
    font-size: 12px;
    color: var(--muted);
}

.forecast-icon { font-size: 28px; margin: 14px 0; }

.forecast-condition {
    font-size: 11px;
    min-height: 28px;
    line-height: 1.4;
}

.forecast-temp {
    font-weight: bold;
    font-size: 14px;
    margin-top: 12px;
}

.forecast-low {
    color: var(--muted);
    font-size: 12px;
    margin-top: 5px;
}

.rain-chance {
    color: var(--accent);
    font-size: 11px;
    margin-top: 10px;
}

.error {
    padding: 20px;
    background: var(--card);
    border: 1px solid #e99;
    border-radius: 12px;
    text-align: center;
    line-height: 1.6;
}

.source {
    text-align: center;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.8;
    margin: 20px 0;
}

footer {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    padding: 25px;
}

@media (max-width: 650px) {
    header { padding: 20px 5%; flex-wrap: wrap; }
    main { margin-top: 25px; }
    .card { padding: 19px; }
    .weather-top h2 { font-size: 20px; }
    .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .forecast-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .forecast-day:last-child { grid-column: 1 / -1; }
    button { padding: 0 15px; }
}
</style>
</head>

<body class="{{ theme }}">
<header>
    <div class="logo">☁ SkyPulse</div>
    <div class="tagline">Know the sky. Plan your day.</div>
</header>

<main>
    <section class="hero">
        <p class="eyebrow">YOUR PERSONAL WEATHER DASHBOARD</p>
        <h1>Feel the weather.<br>Plan your day.</h1>
        <p class="subtitle">
            Real-time weather and air quality for your city.
        </p>

        <form method="POST" class="search-form">
            <input type="text" name="city"
                   placeholder="Enter city name..."
                   value="{{ searched_city }}" required>
            <button type="submit">Search ↗</button>
        </form>
    </section>

    {% if weather %}
        {% if weather.error %}
            <div class="error">{{ weather.error }}</div>
        {% else %}
            <section class="card">
                <div class="weather-top">
                    <div>
                        <p class="eyebrow">CURRENT WEATHER</p>
                        <h2>{{ weather.city }}, {{ weather.country }}</h2>
                        <p class="muted">
                            {{ weather.day }}, {{ weather.date }}
                            · {{ weather.time }}
                        </p>
                    </div>
                    <div class="weather-icon">{{ weather.icon }}</div>
                </div>

                <div class="temperature">
                    {{ weather.temperature }}<span>°C</span>
                </div>

                <h3 class="description">{{ weather.description }}</h3>
                <p class="muted">Feels like {{ weather.feels_like }}°C</p>

                <div class="metrics">
                    <div class="metric">
                        <span class="metric-icon">💧</span>
                        <p>Humidity</p>
                        <h3>{{ weather.humidity }}%</h3>
                    </div>

                    <div class="metric">
                        <span class="metric-icon">🌬️</span>
                        <p>Wind Speed</p>
                        <h3>{{ weather.wind }} {{ weather.wind_unit }}</h3>
                    </div>

                    <div class="metric">
                        <span class="metric-icon">🌧️</span>
                        <p>Precipitation</p>
                        <h3>{{ weather.precipitation }} mm</h3>
                    </div>

                    <div class="metric">
                        <span class="metric-icon">🌿</span>
                        <p>Air Quality (US AQI)</p>
                        <h3>{{ weather.aqi }}</h3>
                        <span class="aqi-label {{ weather.aqi_class }}">
                            {{ weather.aqi_label }}
                        </span>
                    </div>
                </div>
            </section>

            {% if forecast %}
                <section class="card">
                    <div class="section-heading">
                        <p class="eyebrow">PLAN AHEAD</p>
                        <h2>5-Day Forecast</h2>
                        <p class="muted">
                            Daily maximum and minimum temperatures
                        </p>
                    </div>

                    <div class="forecast-grid">
                        {% for day in forecast %}
                            <div class="forecast-day">
                                <div class="day-name">{{ day.day }}</div>
                                <div class="forecast-icon">{{ day.icon }}</div>
                                <div class="forecast-condition">
                                    {{ day.description }}
                                </div>
                                <div class="forecast-temp">{{ day.max }}°</div>
                                <div class="forecast-low">{{ day.min }}°</div>
                                <div class="rain-chance">
                                    🌧 {{ day.rain }}% chance
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                </section>
            {% endif %}

            <p class="source">
                Weather and forecast: Open-Meteo<br>
                Air quality: Open-Meteo Air Quality API<br>
                Temperatures in °C · Wind speed in km/h
            </p>
        {% endif %}
    {% endif %}
</main>

<footer>SkyPulse · Built with Python, HTML and CSS</footer>
</body>
</html>
"""


def get_weather_description(code):
    weather_codes = {
        0: ("Clear Sky", "☀️"),
        1: ("Mainly Clear", "🌤️"),
        2: ("Partly Cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Rime Fog", "🌫️"),
        51: ("Light Drizzle", "🌦️"),
        53: ("Moderate Drizzle", "🌦️"),
        55: ("Dense Drizzle", "🌧️"),
        56: ("Freezing Drizzle", "🌧️"),
        57: ("Heavy Freezing Drizzle", "🌧️"),
        61: ("Slight Rain", "🌧️"),
        63: ("Moderate Rain", "🌧️"),
        65: ("Heavy Rain", "🌧️"),
        66: ("Freezing Rain", "🌧️"),
        67: ("Heavy Freezing Rain", "🌧️"),
        71: ("Slight Snow", "🌨️"),
        73: ("Moderate Snow", "❄️"),
        75: ("Heavy Snow", "❄️"),
        77: ("Snow Grains", "🌨️"),
        80: ("Rain Showers", "🌦️"),
        81: ("Moderate Showers", "🌧️"),
        82: ("Heavy Showers", "⛈️"),
        85: ("Snow Showers", "🌨️"),
        86: ("Heavy Snow Showers", "❄️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with Hail", "⛈️"),
        99: ("Severe Thunderstorm", "⛈️")
    }
    return weather_codes.get(code, ("Weather Update", "🌡️"))


def get_aqi_details(aqi):
    if aqi is None:
        return "Unavailable", "aqi-unknown"
    if aqi <= 50:
        return "Good", "aqi-good"
    elif aqi <= 100:
        return "Moderate", "aqi-moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "aqi-sensitive"
    elif aqi <= 200:
        return "Unhealthy", "aqi-unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy", "aqi-very-unhealthy"
    else:
        return "Hazardous", "aqi-hazardous"


# Retry temporary API failures and cache successful results.
WEATHER_CACHE = {}
CACHE_TTL_SECONDS = 600


def get_api_response(url, params, retries=3, timeout=10):
    last_error = None

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(1 + attempt)

    raise last_error


def get_weather(city):
    cache_key = city.strip().casefold()
    cached = WEATHER_CACHE.get(cache_key)

    if cached and time.time() - cached["saved_at"] < CACHE_TTL_SECONDS:
        return cached["result"]

    try:
        geo_response = get_api_response(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            retries=3,
            timeout=10
        )
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {"error": "City not found. Please check the spelling."}, []

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        weather_response = get_api_response(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,is_day,precipitation,"
                    "weather_code,wind_speed_10m"
                ),
                "daily": (
                    "weather_code,temperature_2m_max,"
                    "temperature_2m_min,precipitation_probability_max"
                ),
                "forecast_days": 5,
                "timezone": "auto"
            },
            retries=3,
            timeout=15
        )
        data = weather_response.json()

        current = data["current"]
        units = data["current_units"]
        local_time = datetime.fromisoformat(current["time"])

        description, icon = get_weather_description(current["weather_code"])

        aqi = None

        try:
            aqi_response = get_api_response(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "us_aqi",
                    "timezone": "auto"
                },
                retries=2,
                timeout=10
            )
            aqi_data = aqi_response.json()
            aqi = aqi_data.get("current", {}).get("us_aqi")
        except (requests.RequestException, ValueError, TypeError):
            aqi = None

        aqi_label, aqi_class = get_aqi_details(aqi)

        daily = data["daily"]
        forecast = []

        for index in range(len(daily["time"])):
            forecast_date = datetime.fromisoformat(daily["time"][index])
            day_description, day_icon = get_weather_description(
                daily["weather_code"][index]
            )
            rain_value = daily["precipitation_probability_max"][index]

            forecast.append({
                "day": "Today" if index == 0 else forecast_date.strftime("%a"),
                "description": day_description,
                "icon": day_icon,
                "max": round(daily["temperature_2m_max"][index]),
                "min": round(daily["temperature_2m_min"][index]),
                "rain": rain_value if rain_value is not None else 0
            })

        weather = {
            "city": place["name"],
            "country": place.get("country", ""),
            "temperature": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"],
            "wind": current["wind_speed_10m"],
            "wind_unit": units["wind_speed_10m"],
            "precipitation": current["precipitation"],
            "description": description,
            "icon": icon,
            "aqi": aqi if aqi is not None else "N/A",
            "aqi_label": aqi_label,
            "aqi_class": aqi_class,
            "date": local_time.strftime("%d %B %Y"),
            "time": local_time.strftime("%I:%M %p"),
            "day": local_time.strftime("%A"),
            "is_day": current["is_day"] == 1
        }

        result = (weather, forecast)
        WEATHER_CACHE[cache_key] = {
            "saved_at": time.time(),
            "result": result
        }
        return result

    except requests.RequestException as error:
        print(f"Weather API error: {error!r}", flush=True)
        if cached:
            return cached["result"]

        return {
            "error": (
                "The weather service is temporarily unavailable. "
                "Please try again in a little while."
            )
        }, []

    except (KeyError, ValueError, TypeError, IndexError):
        return {
            "error": "Weather data could not be processed. Please try again."
        }, []


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    weather = None
    forecast = []
    theme = "day"

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if city:
            weather, forecast = get_weather(city)

            if not weather.get("error") and not weather["is_day"]:
                theme = "night"

    return render_template_string(
        HTML,
        weather=weather,
        forecast=forecast,
        theme=theme,
        searched_city=city
    )


if __name__ == "__main__":
    app.run(debug=True)