import json

# Load your JSON data
with open("properties_data.json", "r") as file:
    data = json.load(file)

# Get list of properties
properties = data.get("meta", {}).get("properties", [])

# Create a new list to store formatted properties
formatted_properties = []

# Process each property to exclude image data and save required details
for prop in properties:
    formatted_property = {
        "title": prop.get("title"),
        "description": prop.get("description"),
        "price": prop.get("price"),
        "discountPrice": prop.get("discountPrice"),
        "area": prop.get("area"),
        "floor": prop.get("floor"),
        "numberOfBedrooms": prop.get("numberOfBedrooms"),
        "numberOfBathrooms": prop.get("numberOfBathrooms"),
        "constructionYear": prop.get("constructionYear"),
        "city": prop.get("city"),
        "state": prop.get("state"),
        "country": prop.get("country"),
        "pincode": prop.get("pincode"),
        "agentName": prop.get("agentName"),
        "agentPhone": prop.get("agentPhone"),
        "agentEmail": prop.get("agentEmail"),
        "nearbyPlaces": prop.get("nearbyPlaces", []),
        "amenities": prop.get("amenities", []),
        "status": prop.get("status"),
        "totalQuantity": prop.get("totalQuantity"),
        "availableQuantity": prop.get("availableQuantity")
    }
    formatted_properties.append(formatted_property)

# Create a new dictionary to save the cleaned data
output_data = {
    "error": data.get("error"),
    "message": data.get("message"),
    "meta": {
        "properties": formatted_properties
    }
}

# Save the cleaned data to a new JSON file
with open("formatted_properties.json", "w") as output_file:
    json.dump(output_data, output_file, indent=4)

print("Properties saved to 'formatted_properties.json'.")
