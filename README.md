# 🌦️ SkyPulse — Weather & Air Quality Dashboard

### Feel the weather. Plan your day.

SkyPulse is a Python-based weather web application that provides current weather conditions, air quality information, and a 5-day forecast for your city through a clean and user-friendly interface.

<p align="center">
  <a href="https://skypulse-mlu1.onrender.com">
    <strong>🌐 Visit Live Website</strong>
  </a>
  &nbsp; • &nbsp;
  <a href="https://github.com/ishitajain-codes/SkyPuLse">
    <strong>📂 GitHub Repository</strong>
  </a>
</p>

---

## ✨ Features

- 🌡️ **Current Weather:** View temperature, feels-like temperature, and current weather conditions.
- 💧 **Humidity:** Check the current humidity level.
- 🌬️ **Wind Speed:** Get wind speed information in km/h.
- 🌧️ **Precipitation:** View precipitation information and forecast chances.
- 🌿 **Air Quality Index:** Check the US AQI and its corresponding air quality category.
- 📅 **5-Day Forecast:** View daily maximum and minimum temperatures.
- 🔎 **City Search:** Search for weather information by city.
- 📊 **Weather Dashboard:** Explore important weather details in one place.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Web application framework |
| HTML | Page structure |
| CSS | Styling and layout |
| Requests | Sending HTTP requests to APIs |
| Open-Meteo Weather API | Weather and forecast data |
| Open-Meteo Air Quality API | Air quality data |
| Gunicorn | Production application server |
| Render | Web application deployment |

## 🔌 APIs

SkyPulse uses the following APIs to retrieve weather and air quality information:

- **Open-Meteo Weather API:** https://open-meteo.com/
- **Open-Meteo Air Quality API:** https://open-meteo.com/en/docs/air-quality-api

## 🚀 Getting Started

Follow these steps to run SkyPulse on your local machine.

### Prerequisites

- Python installed on your computer
- Git installed on your computer

### 1. Clone the repository

```bash
git clone https://github.com/ishitajain-codes/SkyPuLse.git
```

### 2. Navigate to the project directory

```bash
cd SkyPuLse
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open the application

Open this address in your browser:

`http://127.0.0.1:5000`

## 📁 Project Structure

```text
SkyPuLse/
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 📚 Key Learnings

Building SkyPulse helped me practise:

- Integrating external APIs into a Python application.
- Making HTTP requests and working with JSON responses.
- Building web applications using Flask.
- Displaying dynamic weather and air quality data.
- Managing project files using Git and GitHub.
- Deploying a Python web application with Render.

## 🔮 Future Improvements

- Add hourly weather forecasts.
- Improve error handling for invalid city searches.
- Enhance the mobile-responsive interface.
- Add a saved-cities feature.
- Improve weather visualizations and forecast details.

## 👩‍💻 Developer

**Ishita Jain**

- GitHub: https://github.com/ishitajain-codes
- Project Repository: https://github.com/ishitajain-codes/SkyPuLse
- Live Demo: https://skypulse-mlu1.onrender.com

---

*Built with Python, Flask, HTML, CSS, and Open-Meteo APIs.*
