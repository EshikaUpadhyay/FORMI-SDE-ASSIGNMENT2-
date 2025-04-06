import json
import os
import requests
import pandas as pd
from geopy.distance import geodesic
from rapidfuzz import process
from django.conf import settings

PROPERTY_FILE = os.path.join(settings.BASE_DIR, 'locator', 'static', 'property_data.json')
CITY_DATA_FILE = os.path.join(settings.BASE_DIR, 'locator', 'static', 'indian_cities.csv')

# Load property data once
with open(PROPERTY_FILE, 'r') as file:
    PROPERTIES = json.load(file)

# Load city dataset for fuzzy match
city_df = pd.read_csv(CITY_DATA_FILE)
KNOWN_LOCATIONS = set(city_df['City'].dropna().str.lower().unique())
KNOWN_LOCATIONS.update(city_df['State'].dropna().str.lower().unique())
KNOWN_LOCATIONS.update([prop['name'].split()[-1].lower() for prop in PROPERTIES])

def correct_location(query):
    query = query.lower()
    match, score, _ = process.extractOne(query, list(KNOWN_LOCATIONS), score_cutoff=60)
    return match if match else query

def get_coordinates_from_query(query):
    
    # try finding in json
    for prop in PROPERTIES:
        if query.lower() in prop['name'].lower():
            return prop['latitude'], prop['longitude']

    # Try resolving from dataset
    row = city_df[city_df['City'].str.lower() == query]
    if not row.empty:
        lat = float(row.iloc[0]['Lat'])
        lon = float(row.iloc[0]['Long'])
        return lat, lon

    # Fallback to Nominatim
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={query}"
    headers = { "User-Agent": "location-finder/1.0" }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    return None

def find_nearest_properties(user_query):
    corrected_query = correct_location(user_query)
    location = get_coordinates_from_query(corrected_query)
    if not location:
        return []

    matches = []
    for prop in PROPERTIES:
        dist = geodesic(location, (prop['latitude'], prop['longitude'])).km
        if dist <= 50:
            matches.append({
                'name': prop['name'],
                'distance_km': round(dist)
            })
    return sorted(matches, key=lambda x: x['distance_km'])
