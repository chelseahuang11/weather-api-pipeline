import requests
import json
import time
import pandas as pd

API_KEY = "9317b9c5ea38448395355443260705"

api_url = "https://api.weatherapi.com/v1/forecast.json"

zip_codes = [
    # Original 5
    "90045",  # Los Angeles, CA
    "10001",  # New York, NY
    "60601",  # Chicago, IL
    "98101",  # Seattle, WA
    "33101",  # Miami, FL
    # 15 additional major US cities
    "77001",  # Houston, TX
    "85001",  # Phoenix, AZ
    "19101",  # Philadelphia, PA
    "78201",  # San Antonio, TX
    "92101",  # San Diego, CA
    "75201",  # Dallas, TX
    "95101",  # San Jose, CA
    "78701",  # Austin, TX
    "30301",  # Atlanta, GA
    "28201",  # Charlotte, NC
    "80201",  # Denver, CO
    "37201",  # Nashville, TN
    "97201",  # Portland, OR
    "89101",  # Las Vegas, NV
    "63101",  # St. Louis, MO
]

results = []

for zip_code in zip_codes:
    params = {
        "key": API_KEY,
        "q": zip_code,
        "days": 7
    }
    response = requests.get(api_url, params=params)
    data = response.json()

    city = data["location"]["name"]

    for day in data["forecast"]["forecastday"]:
        date = day["date"]
        max_temp = day["day"]["maxtemp_f"]
        min_temp = day["day"]["mintemp_f"]
        condition = day["day"]["condition"]["text"]

        results.append({
            "zip_code": zip_code,
            "city": city,
            "date": date,
            "max_temp_f": max_temp,
            "min_temp_f": min_temp,
            "condition": condition
        })

        print(f"{city} {date}: {max_temp}°F / {min_temp}°F, {condition}")

    time.sleep(1)

print(f"\nCollected {len(results)} rows of forecast data.")

df = pd.DataFrame(results)
print(df.to_string(index=False))
print(f"\nShape: {df.shape[0]} rows x {df.shape[1]} columns")

df.to_csv("weather_data.csv", index=False)
print("Saved to weather_data.csv")
