import requests
from flask import Flask, render_template
import json
from key import api_key

app = Flask(__name__)

API_KEY = api_key

@app.route("/")
def index():
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": 40.5169,
        "lon": -74.4063,
        "appid": API_KEY,
        "units": "imperial"
    }

    response = requests.get(url, params=params)
    data = response.json()

    daily_forecasts = []
    for i in range(0, 40, 8):
        chunk = data["list"][i:i+8]
        temps = [entry["main"]["temp"] for entry in chunk]
        avg_temp = round(sum(temps) / len(temps), 1)
        condition = chunk[0]["weather"][0]["main"]
        icon = chunk[0]["weather"][0]["icon"]
        daily_forecasts.append({
            "temp": avg_temp,
            "condition": condition,
            "icon": f"https://openweathermap.org/img/wn/{icon}@2x.png"
        })

    city = data["city"]["name"]
    current = data["list"][0]
    return render_template("index.html",
        city=city,
        temp=current["main"]["temp"],
        weather=current["weather"][0]["main"],
        condition=current["weather"][0]["description"],
        humidity=current["main"]["humidity"],
        wind_speed=current["wind"]["speed"],
        feels_like=current["main"]["feels_like"],
        icon=f"https://openweathermap.org/img/wn/{current['weather'][0]['icon']}@2x.png",
        forecast=daily_forecasts
    )

if __name__ == "__main__":
    app.run(debug=True)
