import os
import requests
import tkinter as tk
from tkinter import messagebox

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    if not API_KEY:
        messagebox.showerror(
            "Error",
            "Missing OPENWEATHER_API_KEY. Set it in your environment before running the app.",
        )
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        messagebox.showerror("Error", "Unable to fetch weather data. Please try again.")
        return

    data = response.json()
    if response.status_code != 200 or "main" not in data:
        messagebox.showerror("Error", "City not found. Please try again.")
        return

    weather_info = (
        f"City: {data['name']}\n"
        f"Temperature: {data['main']['temp']}°C\n"
        f"Weather: {data['weather'][0]['description'].title()}\n"
        f"Humidity: {data['main']['humidity']}%\n"
        f"Wind Speed: {data['wind']['speed']} m/s"
    )
    result_label.config(text=weather_info)


root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

tk.Label(root, text="Enter City Name:", font=("Arial", 14)).pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14))
city_entry.pack(pady=10)
tk.Button(root, text="Get Weather", font=("Arial", 14), command=get_weather).pack(pady=10)
result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()