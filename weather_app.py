import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
API_KEY = "33166fa3dae3422fb11190326263103"   # Replace with your real key
current_temp_c = None
def get_weather():
    global current_temp_c
    city = city_entry.get().strip()
    if city == "":
        messagebox.showerror("Input Error", "Please enter a city name")
        return
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    try:
        response = requests.get(url)
        data = response.json()
        if "error" in data:
            messagebox.showerror("Error", data["error"]["message"])
            return
        temp_c = data["current"]["temp_c"]
        desc = data["current"]["condition"]["text"]
        humidity = data["current"]["humidity"]
        wind = data["current"]["wind_kph"]
        icon_url = data["current"]["condition"]["icon"]
        icon_code = icon_url.split("/")[-1].split(".")[0] 
        temp_label.config(text=f"{temp_c}°C")
        desc_label.config(text=desc)
        humid_label.config(text=f"Humidity: {humidity}%")
        wind_label.config(text=f"Wind: {wind} kph")
        load_icon(icon_code)
        current_temp_c = temp_c
    except Exception as e:
        messagebox.showerror("Network Error", "Unable to fetch data.")
        print(e)
def load_icon(icon_code):
    mapping = {
        "113": "01d",  # Sunny
        "116": "02d",  # Partly cloudy
        "119": "03d",  # Cloudy
        "122": "04d",  # Overcast
        "176": "09d",  # Patchy rain
        "296": "10d",  # Light rain
        "302": "11d",  # Heavy rain
        "308": "11d",  # Very heavy rain
        "389": "11d",  # Thunderstorm
        "179": "13d",  # Snow
        "182": "13d",  # Snow/rain
        "227": "13d",  # Blizzard
        "143": "50d",  # Mist
        "248": "50d",  # Fog

    }
    final_icon = mapping.get(icon_code, "01d")
    icon_path = f"icons/{final_icon}.png"
    if not os.path.exists(icon_path):
        icon_path = "icons/default.png"
    img = Image.open(icon_path)
    img = img.resize((110, 110))
    img_icon = ImageTk.PhotoImage(img)
    icon_label.config(image=img_icon)
    icon_label.image = img_icon
def toggle_temp():
    global current_temp_c
    if current_temp_c is None:
        return
    if temp_toggle_btn["text"] == "Show °F":
        temp_f = round((current_temp_c * 9/5) + 32, 1)
        temp_label.config(text=f"{temp_f}°F")
        temp_toggle_btn.config(text="Show °C")
    else:
        temp_label.config(text=f"{current_temp_c}°C")
        temp_toggle_btn.config(text="Show °F")
root = tk.Tk()
root.title("Weather App")
root.geometry("400x520")
root.config(bg="#E3F2FD")
title = tk.Label(root, text="Weather App", font=("Arial", 22, "bold"), bg="#E3F2FD")
title.pack(pady=10)
city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.pack(pady=10)
search_btn = tk.Button(root, text="Get Weather", font=("Arial", 14), bg="#2196F3", fg="white", command=get_weather)
search_btn.pack(pady=10)
icon_label = tk.Label(root, bg="#E3F2FD")
icon_label.pack()
temp_label = tk.Label(root, text="", font=("Arial", 36), bg="#E3F2FD")
temp_label.pack(pady=5)
desc_label = tk.Label(root, text="", font=("Arial", 18), bg="#E3F2FD")
desc_label.pack(pady=5)
humid_label = tk.Label(root, text="", font=("Arial", 14), bg="#E3F2FD")
humid_label.pack()
wind_label = tk.Label(root, text="", font=("Arial", 14), bg="#E3F2FD")
wind_label.pack(pady=5)
temp_toggle_btn = tk.Button(root, text="Show °F", font=("Arial", 12), command=toggle_temp)
temp_toggle_btn.pack(pady=10)
root.mainloop()