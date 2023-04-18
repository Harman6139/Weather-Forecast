import requests
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedStyle
from geopy.geocoders import Nominatim

API = "d25f731ce49aa2aaa4c2ee5947c78a2c"
Base_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to retrieve weather data based on user's choice
def get_weather():
    location_choice = location_var.get()
    if location_choice == 1:
        city = city_entry.get()
        request_URL = f"{Base_URL}?appid={API}&q={city}"
    elif location_choice == 2:
        # Use geopy to get current location
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode("")
        if location is not None:
            # Retrieve latitude and longitude from the location
            lat = location.latitude
            lon = location.longitude
            request_URL = f"{Base_URL}?appid={API}&lat={lat}&lon={lon}"
        else:
            messagebox.showerror("Error", "Unable to retrieve current location.")
            return
    else:
        messagebox.showerror("Error", "Invalid input. Please select a location option.")
        return

    response = requests.get(request_URL)
    if response.status_code == 200:
        data = response.json()
        country = data["sys"]["country"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        temperature = round(data["main"]["temp"] - 273.15, 2)
        result_label.config(
            text=f"Country: {country}\nWeather: {weather}\nTemperature: {temperature} Celsius\nHumidity: {humidity}"
        )
    else:
        messagebox.showerror("Error", "An error occurred.")

# Create main window
root = tk.Tk()
root.title("Weather App")

# Create themed style for the GUI
style = ThemedStyle(root)
style.set_theme("plastik")

# Create GUI components
city_label = tk.Label(root, text="Enter city name:", font=("Helvetica", 14))
city_entry = tk.Entry(root, font=("Helvetica", 14))
location_var = tk.IntVar()
location_var.set(1)
city_radio = tk.Radiobutton(root, text="City", variable=location_var, value=1, font=("Helvetica", 12))
current_loc_radio = tk.Radiobutton(root, text="Current Location", variable=location_var, value=2, font=("Helvetica", 12))
get_weather_button = tk.Button(root, text="Get Weather", command=get_weather, font=("Helvetica", 14))
result_label = tk.Label(root, text="Weather result will be displayed here", font=("Helvetica", 14), wraplength=400, justify="left")

# Add GUI components to the window with padding
city_label.pack(pady=10)
city_entry.pack(pady=10)
city_radio.pack()
current_loc_radio.pack()
get_weather_button.pack(pady=10)
result_label.pack(pady=10)

# Run GUI event loop
root.mainloop()
