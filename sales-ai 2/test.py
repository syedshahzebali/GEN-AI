import requests
import json

url = "https://eleganzaestatesolutions.com/api/user/public-listing"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()  # Convert JSON response to Python dictionary/list

    # Save the data to a JSON file
    with open("properties_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("✅ Data fetched and saved to 'properties_data.json' successfully.")

except requests.exceptions.RequestException as e:
    print("❌ Error fetching data:", e)
except Exception as ex:
    print("❌ Error saving JSON file:", ex)
