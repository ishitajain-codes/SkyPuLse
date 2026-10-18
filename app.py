from flask import Flask, render_template_string, request
import requests
from datetime import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SkyPulse | Weather Dashboard</title>
    <style>
        :root {
            --bg-color: #f4f8fc;
            --text-color: #111827;
            --card-bg: #ffffff;
            --card-border: #e2e8f0;
            --sub-text: #64748b;
            --accent: #2563eb;
        }

        .dark-theme {
            --bg-color: #0b0f19;
            --text-color: #f8fafc;
            --card-bg: #111827;
            --card-border: #1f2937;
            --sub-text: #94a3b8;
            --accent: #38bdf8;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            transition: background 0.3s ease, color 0.3s ease;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 20px;
        }

        .tagline {
            font-size: 13px;
            color: var(--sub-text);
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            flex-grow: 1;
            width: 100%;
        }

        .hero {
            text-align: center;
            margin-bottom: 30px;
        }

        .sub-title {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: var(--accent);
            margin-bottom: 12px;
        }

        .hero h1 {
            font-size: 40px;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 10px;
        }

        .description {
            font-size: 15px;
            color: var(--sub-text);
            margin-bottom: 25px;
        }

        .search-box {
            display: flex;
            justify-content: center;
            gap: 10px;
            max-width: 450px;
            margin: 0 auto;
        }

        .search-box input {
            flex: 1;
            padding: 12px 18px;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            background-color: var(--card-bg);
            color: var(--text-color);
        }

        .search-box button {
            background-color: var(--accent);
            color: white;
            border: none;
            padding: 12px 22px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }

        .error-card {
            border: 1px solid #fca5a5;
            background-color: rgba(239, 68, 68, 0.1);
            color: #ef4444;
            padding: 14px;
            border-radius: 8px;
            text-align: center;
            margin-top: 20px;
        }

        .weather-card {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 14px;
            border: 1px solid var(--card-border);
            margin-top: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            position: relative;
        }

        .weather-icon-large {
            position: absolute;
            top: 30px;
            right: 30px;
            font-size: 48px;
        }

        .section-title {
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            color: var(--sub-text);
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .city-name {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .date-time {
            font-size: 13px;
            color: var(--sub-text);
            margin-bottom: 20px;
        }

        .main-temp-area {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .temp-val {
            font-size: 54px;
            font-weight: 800;
        }

        .temp-unit {
            font-size: 22px;
            color: var(--accent);
            font-weight: 600;
        }

        .weather-condition {
            font-size: 18px;
            font-weight: 600;
            margin-top: 5px;
        }

        .feels-like {
            font-size: 13px;
            color: var(--sub-text);
        }

        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 15px;
            border-top: 1px solid var(--card-border);
            padding-top: 20px;
        }

        .detail-item {
            background: var(--bg-color);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid var(--card-border);
        }

        .detail-label {
            font-size: 12px;
            color: var(--sub-text);
            margin-bottom: 6px;
        }

        .detail-value {
            font-size: 16px;
            font-weight: 700;
        }

        .forecast-container {
            margin-top: 25px;
        }

        .forecast-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-top: 10px;
        }

        .forecast-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 15px;
            border-radius: 10px;
            text-align: center;
        }

        .forecast-day {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }

        .forecast-emoji {
            font-size: 24px;
            margin: 5px 0;
        }

        .forecast-temp {
            font-size: 15px;
            font-weight: 700;
            margin-top: 6px;
        }

        .forecast-temp span {
            color: var(--sub-text);
            font-weight: 400;
            font-size: 13px;
        }

        footer {
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: var(--sub-text);
        }
    </style>
</head>
<body class="{{ theme_class }}">

    <header class="navbar">
        <div class="logo">
            <span>☁️</span>
            <span>SkyPulse</span>
        </div>
        <div class="tagline">Know the sky. Plan your day.</div>
    </header>

    <main class="container">
        <div class="hero">
            <p class="sub-title">YOUR PERSONAL WEATHER DASHBOARD</p>
            <h1>Feel the weather.<br>Plan your day.</h1>
            <p class="description">Real-time weather and air quality for your city</p>

            <form action="/" method="POST" class="search-box">
                <input type="text" name="city" placeholder="Search city (e.g. London)" required autocomplete="off">
                <button type="submit">Search ↗</button>
            </form>
        </div>

        {% if error %}
        <div class="error-card">
            <p>⚠️ {{ error }}</p>
        </div>
        {% endif %}

        {% if weather %}
        <div class="weather-card">
            <div class="weather-icon-large">{{ weather.emoji }}</div>
            <div class="section-title">Current Weather</div>
            <div class="city-name">📍 {{ weather.city }}{% if weather.country %}, {{ weather.country }}{% endif %}</div>
            <div class="date-time">🕒 {{ weather.current_time }}</div>

            <div class="main-temp-area">
                <div>
                    <div>
                        <span class="temp-val">{{ weather.temperature }}</span>
                        <span class="temp-unit">°C</span>
                    </div>
                    <div class="weather-condition">{{ weather.emoji }} {{ weather.condition_text }}</div>
                    <div class="feels-like">Feels like {{ weather.apparent_temp }}°C</div>
                </div>
            </div>

            <div class="details-grid">
                <div class="detail-item">
                    <div class="detail-label">💧 Humidity</div>
                    <div class="detail-value">{{ weather.humidity }}%</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">🌬️ Wind Speed</div>
                    <div class="detail-value">{{ weather.windspeed }} km/h</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">🌧️ Precipitation</div>
                    <div class="detail-value">{{ weather.precipitation }} mm</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">🍃 Air Quality (AQI)</div>
                    <div class="detail-value">{{ weather.aqi }}</div>
                </div>
            </div>
        </div>

        {% if forecast %}
        <div class="forecast-container">
            <div class="section-title">Plan Ahead</div>
            <div class="city-name" style="font-size: 18px;">📅 5-Day Forecast</div>
            <div class="forecast-grid">
                {% for day in forecast %}
                <div class="forecast-card">
                    <div class="forecast-day">{{ day.date }}</div>
                    <div class="forecast-emoji">{{ day.emoji }}</div>
                    <div style="font-size: 12px; color: var(--sub-text);">{{ day.condition }}</div>
                    <div class="forecast-temp">{{ day.max_temp }}° <span>/ {{ day.min_temp }}°</span></div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        {% endif %}
    </main>

    <footer>
        <p>SkyPulse · Built with Python, HTML and CSS ⚡</p>
    </footer>

</body>
</html>
"""

def get_weather_info(code):
    # Returns a tuple of (Description, Emoji)
    weather_map = {
        0: ("Clear Sky", "☀️"),
        1: ("Mainly Clear", "🌤️"),
        2: ("Partly Cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Foggy", "🌫️"),
        48: ("Depositing Rime Fog", "🌫️"),
        51: ("Light Drizzle", "🌦️"),
        53: ("Moderate Drizzle", "🌧️"),
        55: ("Dense Drizzle", "🌧️"),
        61: ("Slight Rain", "🌦️"),
        63: ("Moderate Rain", "🌧️"),
        65: ("Heavy Rain", "🌧️"),
        71: ("Slight Snow", "🌨️"),
        73: ("Moderate Snow", "❄️"),
        75: ("Heavy Snow", "❄️"),
        95: ("Thunderstorm", "⚡")
    }
    return weather_map.get(code, ("Clear Sky", "☀️"))

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    forecast_data = None
    error_message = None
    
    current_hour = datetime.now().hour
    theme_class = "" if (6 <= current_hour < 18) else "dark-theme"

    if request.method == "POST":
        city = request.form.get("city")
        if city and city.strip():
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.strip()}&count=1"
                geo_res = requests.get(geo_url, timeout=10).json()

                if "results" in geo_res and len(geo_res["results"]) > 0:
                    loc = geo_res["results"][0]
                    lat, lon = loc["latitude"], loc["longitude"]
                    city_name, country = loc["name"], loc.get("country", "")

                    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=relative_humidity_2m,apparent_temperature,precipitation&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
                    w_res = requests.get(w_url, timeout=10).json()

                    aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi"
                    aqi_res = requests.get(aqi_url, timeout=10).json()
                    aqi_val = aqi_res.get("current", {}).get("us_aqi", "N/A")

                    current = w_res.get("current_weather", {})
                    hourly = w_res.get("hourly", {})
                    daily = w_res.get("daily", {})

                    humidity = 50
                    apparent_temp = current.get("temperature", 0)
                    precipitation = 0.0

                    if "relative_humidity_2m" in hourly and len(hourly["relative_humidity_2m"]) > 0:
                        humidity = hourly["relative_humidity_2m"][0]
                    if "apparent_temperature" in hourly and len(hourly["apparent_temperature"]) > 0:
                        apparent_temp = hourly["apparent_temperature"][0]
                    if "precipitation" in hourly and len(hourly["precipitation"]) > 0:
                        precipitation = hourly["precipitation"][0]

                    weather_code = current.get("weathercode", 0)
                    cond_text, cond_emoji = get_weather_info(weather_code)

                    weather_data = {
                        "city": city_name,
                        "country": country,
                        "current_time": datetime.now().strftime("%A, %d %B %Y · %I:%M %p"),
                        "temperature": round(current.get("temperature", 0)),
                        "apparent_temp": round(apparent_temp),
                        "humidity": round(humidity),
                        "windspeed": round(current.get("windspeed", 0)),
                        "precipitation": precipitation,
                        "condition_text": cond_text,
                        "emoji": cond_emoji,
                        "aqi": aqi_val
                    }

                    forecast_data = []
                    if "time" in daily:
                        for i in range(min(5, len(daily["time"]))):
                            date_str = daily["time"][i]
                            formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %d %b")
                            f_code = daily["weather_code"][i]
                            f_text, f_emoji = get_weather_info(f_code)
                            forecast_data.append({
                                "date": formatted_date,
                                "max_temp": round(daily["temperature_2m_max"][i]),
                                "min_temp": round(daily["temperature_2m_min"][i]),
                                "condition": f_text,
                                "emoji": f_emoji
                            })
                else:
                    error_message = f"City '{city}' not found. Please check the spelling."
            except Exception as e:
                print("ERROR:", str(e))
                error_message = "Unable to connect to the weather service. Check your internet"

    return render_template_string(HTML_TEMPLATE, weather=weather_data, forecast=forecast_data, error=error_message, theme_class=theme_class)

if __name__ == "__main__":
    app.run(debug=True)