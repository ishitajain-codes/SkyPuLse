
from datetime import datetime

import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

# -------------------- HTML + CSS --------------------

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkyPulse | Weather Dashboard</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            min-height: 100vh;
            padding: 30px 16px;
            color: #f8fafc;
            background: linear-gradient(135deg, #0f172a, #1e3a5f);
        }

        body.night {
            background: linear-gradient(135deg, #090e20, #25234d);
        }

        main {
            max-width: 950px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 28px;
        }

        header h1 {
            font-size: clamp(2rem, 5vw, 3rem);
            margin-bottom: 10px;
        }

        header p, .muted {
            color: #cbd5e1;
            line-height: 1.6;
        }

        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
        }

        .search-box input {
            flex: 1;
            min-width: 0;
            padding: 15px;
            border: 1px solid #64748b;
            border-radius: 12px;
            font-size: 16px;
            outline: none;
        }

        .search-box button {
            border: none;
            border-radius: 12px;
            padding: 0 22px;
            color: white;
            background: #0ea5e9;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }

        .search-box button:hover {
            background: #0284c7;
        }

        .card {
            background: rgba(255, 255, 255, 0.09);
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 22px;
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        }

        .weather-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
        }

        .eyebrow {
            color: #7dd3fc;
            font-size: 12px;
            font-weight: bold;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        h2 {
            font-size: clamp(1.3rem, 4vw, 2rem);
            margin-bottom: 8px;
        }

        .weather-icon {
            font-size: 60px;
        }

        .temperature {
            font-size: clamp(3rem, 10vw, 5rem);
            font-weight: bold;
            margin: 22px 0 8px;
        }

        .temperature span {
            font-size: 0.5em;
        }

        .description {
            margin-bottom: 8px;
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 14px;
            margin-top: 25px;
        }

        .metric {
            background: rgba(15, 23, 42, 0.35);
            border-radius: 14px;
            padding: 17px;
            overflow-wrap: anywhere;
        }

        .metric-icon {
            font-size: 25px;
        }

        .metric p {
            color: #cbd5e1;
            margin: 9px 0;
            font-size: 14px;
        }

        .metric h3 {
            font-size: 21px;
        }

        .aqi-label {
            display: inline-block;
            margin-top: 8px;
            font-size: 13px;
            color: #bae6fd;
        }

        .section-heading {
            margin-bottom: 20px;
        }

        .forecast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
        }

        .forecast-day {
            text-align: center;
            background: rgba(15, 23, 42, 0.35);
            border-radius: 14px;
            padding: 17px 10px;
        }

        .day-name {
            font-weight: bold;
        }

        .forecast-icon {
            font-size: 32px;
            margin: 12px 0;
        }

        .forecast-condition {
            color: #cbd5e1;
            font-size: 13px;
            min-height: 32px;
        }

        .forecast-temp {
            font-size: 23px;
            font-weight: bold;
            margin-top: 12px;
        }

        .forecast-low {
            color: #cbd5e1;
            margin-top: 5px;
        }

        .rain-chance {
            color: #bae6fd;
            font-size: 12px;
            margin-top: 12px;
        }

        .error {
            background: rgba(127, 29, 29, 0.5);
            border: 1px solid #f87171;
            color: #fee2e2;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 20px;
        }

        .source {
            text-align: center;
            color: #cbd5e1;
            font-size: 12px;
            line-height: 1.8;
            margin: 20px 0;
        }

        footer {
            text-align: center;
            color: #cbd5e1;
            font-size: 12px;
            margin-top: 24px;
        }

        @media (max-width: 480px) {
            .search-box {
                flex-direction: column;
            }

            .search-box button {
                padding: 14px;
            }

            .card {
                padding: 18px;
            }

            .metrics {
                gap: 10px;
            }

            .metric {
                padding: 12px;
            }

            .metric h3 {
                font-size: 18px;
            }
        }
    </style>
</head>

<body class="{{ theme }}">
<main>
    <header>
        <h1>🌤️ SkyPulse</h1>
        <p>Your weather, your world. Check conditions anywhere.</p>
    </header>

    <form class="search-box" method="POST" action="/">
        <input
            type="text"
            name="city"
            placeholder="Enter a city, e.g. Aligarh"
            value="{{ searched_city }}"
            required
            maxlength="100"
            aria-label="City name"
        >
        <button type="submit">Search</button>
    </form>

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
                <p class="muted">
                    Feels like {{ weather.feels_like }}°C
                </p>

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
                        <span class="aqi-label">
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
                                <div class="forecast-temp">
                                    {{ day.max }}°
                                </div>
                                <div class="forecast-low">
                                    {{ day.min }}°
                                </div>
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

    <footer>
        Built with Python, Flask and Open-Meteo APIs
    </footer>
</main>
</body>
</html>
"""


# -------------------- WEATHER DESCRIPTIONS --------------------

def get_weather_description(code):
    descriptions = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Depositing rime fog", "🌫️"),
        51: ("Light drizzle", "🌦️"),
        53: ("Moderate drizzle", "🌦️"),
        55: ("Dense drizzle", "🌧️"),
        56: ("Light freezing drizzle", "🌧️"),
        57: ("Dense freezing drizzle", "🌧️"),
        61: ("Slight rain", "🌦️"),
        63: ("Moderate rain", "🌧️"),
        65: ("Heavy rain", "🌧️"),
        66: ("Light freezing rain", "🌧️"),
        67: ("Heavy freezing rain", "🌧️"),
        71: ("Slight snowfall", "🌨️"),
        73: ("Moderate snowfall", "🌨️"),
        75: ("Heavy snowfall", "❄️"),
        77: ("Snow grains", "❄️"),
        80: ("Slight rain showers", "🌦️"),
        81: ("Moderate rain showers", "🌧️"),
        82: ("Violent rain showers", "⛈️"),
        85: ("Slight snow showers", "🌨️"),
        86: ("Heavy snow showers", "❄️"),
        95: ("Thunderstorm", "⛈️"),
        96: ("Thunderstorm with hail", "⛈️"),
        99: ("Thunderstorm with heavy hail", "⛈️")
    }

    return descriptions.get(code, ("Weather unavailable", "🌡️"))


# -------------------- AIR QUALITY DETAILS --------------------

def get_aqi_details(aqi):
    if aqi is None:
        return "Unavailable"

    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for sensitive groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very unhealthy"
    else:
        return "Hazardous"


# -------------------- WEATHER API --------------------

def get_weather(city):
    try:
        # 1. Find city coordinates
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=15
        )
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return {
                "error": "City not found. Please check the spelling."
            }, []

        place = geo_data["results"][0]
        latitude = place["latitude"]
        longitude = place["longitude"]

        # 2. Get current weather and forecast
        weather_response = requests.get(
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
            timeout=15
        )
        weather_response.raise_for_status()
        data = weather_response.json()

        current = data["current"]
        units = data["current_units"]
        local_time = datetime.fromisoformat(current["time"])

        description, icon = get_weather_description(
            current["weather_code"]
        )

        # 3. Get air quality. If unavailable, weather still works.
        aqi = None

        try:
            aqi_response = requests.get(
                "https://air-quality-api.open-meteo.com/v1/air-quality",
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "us_aqi",
                    "timezone": "auto"
                },
                timeout=10
            )
            aqi_response.raise_for_status()
            aqi_data = aqi_response.json()
            aqi = aqi_data.get("current", {}).get("us_aqi")

        except (requests.RequestException, ValueError, TypeError) as e:
            print(
                f"AIR QUALITY API ERROR: {type(e).__name__}: {e}",
                flush=True
            )

        aqi_label = get_aqi_details(aqi)

        # 4. Build forecast
        daily = data["daily"]
        forecast = []

        for index, date_string in enumerate(daily["time"]):
            forecast_date = datetime.fromisoformat(date_string)

            day_description, day_icon = get_weather_description(
                daily["weather_code"][index]
            )

            rain_value = daily["precipitation_probability_max"][index]

            forecast.append({
                "day": (
                    "Today" if index == 0
                    else forecast_date.strftime("%a")
                ),
                "description": day_description,
                "icon": day_icon,
                "max": round(daily["temperature_2m_max"][index]),
                "min": round(daily["temperature_2m_min"][index]),
                "rain": rain_value if rain_value is not None else 0
            })

        # 5. Prepare final weather dictionary
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
            "date": local_time.strftime("%d %B %Y"),
            "time": local_time.strftime("%I:%M %p"),
            "day": local_time.strftime("%A"),
            "is_day": current["is_day"] == 1
        }

        return weather, forecast

    except requests.RequestException as e:
        print(
            f"WEATHER API ERROR: {type(e).__name__}: {e}",
            flush=True
        )
        return {
            "error": (
                "Weather service is temporarily unavailable. "
                "Please try again."
            )
        }, []

    except (KeyError, ValueError, TypeError, IndexError) as e:
        print(
            f"WEATHER DATA ERROR: {type(e).__name__}: {e}",
            flush=True
        )
        return {
            "error": "Weather data could not be processed. Please try again."
        }, []


# -------------------- HOME ROUTE --------------------

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


# -------------------- RUN APP --------------------

if __name__ == "__main__":
    app.run(debug=True)
