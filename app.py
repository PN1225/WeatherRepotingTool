from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)
api_key = "a7aba80dc2986aebc3808a64a2f89cde"
base_url = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        print(f"City received from form: {city}")  # Debug print
        url = f"{base_url}?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        print(f"API response: {data}")  # Debug print
        if data["cod"] == 200:
            description = data["weather"][0]["description"]
            icon = ""
            if "cloud" in description:
                icon = "☁️"
            elif "rain" in description:
                icon = "🌧️"
            elif "clear" in description:
                icon = "☀️"
            elif "haze" in description:
                icon = "🌫️"
            elif "snow" in description:
                icon = "❄️"
            else:
                icon = "🌈"

            now = datetime.now()
            time_str = now.strftime("%d-%m-%Y %I:%M %p")

            weather_data = {
                "city": city.title(),
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": description.title(),
                "icon": icon,
                "time": time_str
            }
            print(f"Weather data prepared: {weather_data}")  # Debug print
        else:
            print(f"Error from API: {data.get('message', 'Unknown error')}")

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)

