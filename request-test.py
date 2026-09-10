import requests

API_KEY = "HMMD9X7PF55UVTSMAJWFTGV42"   # paste your real key for now, just to test
CITY = "Lahore"

url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{CITY}"

params = {
    "key": API_KEY,
    "unitGroup": "metric"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()
print(data["resolvedAddress"])
print(data["currentConditions"])