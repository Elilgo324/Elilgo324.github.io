import json

import folium
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

# Load cities from JSON file
with open('cities.json', 'r') as f:
    cities = json.load(f)

# Convert cities dictionary to DataFrame
cities_df = pd.DataFrame(list(cities.values()), index=cities.keys(), columns=['Latitude', 'Longitude'])

# Nearest Neighbor algorithm
def nearest_neighbor(cities_df):
    cities_list = list(cities_df.index)
    current_city = cities_list[0]
    tour = [current_city]
    unvisited_cities = set(cities_list)
    unvisited_cities.remove(current_city)
    while unvisited_cities:
        next_city = min(unvisited_cities, key=lambda city: euclidean_distances([cities_df.loc[current_city]], [cities_df.loc[city]]))
        tour.append(next_city)
        unvisited_cities.remove(next_city)
        current_city = next_city
    return tour

# Calculate tour using Nearest Neighbor algorithm
tour = nearest_neighbor(cities_df)
print("Tour using Nearest Neighbor algorithm:", tour)

# Create map with Folium
mymap = folium.Map(location=[32, 35], zoom_start=8)

# Plot cities
for city, (lat, lon) in cities.items():
    folium.Marker([lat, lon], popup=city).add_to(mymap)

# Plot tour
tour_coordinates = [(cities[city][0], cities[city][1]) for city in tour]
folium.PolyLine(locations=tour_coordinates + [tour_coordinates[0]], color='red').add_to(mymap)

# Save map to HTML file
mymap.save("tour_map.html")
