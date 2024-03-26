import folium
import requests
import random


def sample_points(num_points):
    # Fetch data from Overpass API
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area[name="Petah Tikva"]->.searchArea;
    (
      node(area.searchArea);
      way(area.searchArea);
      rel(area.searchArea);
    );
    out center;
    make stat area;
    nwr[building](area.searchArea);
    out geom;
    """
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()

    elements = data['elements']
    sampled_points = []

    for _ in range(num_points):
        element = random.choice(elements)
        lat = element['center']['lat']
        lon = element['center']['lon']
        sampled_points.append((lat, lon))

    return sampled_points


def on_button_click(num_points):
    num_points = int(num_points)
    sampled_points = sample_points(num_points)

    # Clear previous markers
    for marker in markers:
        m.remove_layer(marker)

    # Add new markers
    for point in sampled_points:
        folium.Marker(location=point).add_to(m)
        markers.append(point)

    # Fit map to bounds of sampled points
    m.fit_bounds(sampled_points)


# Create map centered at Petah Tikva
m = folium.Map(location=[32.0872, 34.8875], zoom_start=13)

# Create input field and button
input_box = "<input type='number' id='num_points' placeholder='Enter number of points' style='margin-right: 5px;'>"
button = "<button onclick='handleButtonClick()'>Sample Points</button>"
script = """
<script>
    function handleButtonClick() {
        var num_points = document.getElementById('num_points').value;
        if (num_points.trim() === '') {
            alert('Please enter a number of points.');
            return;
        }
        var kernel = IPython.notebook.kernel;
        kernel.execute("on_button_click('" + num_points + "')");
    }
</script>
"""

# Add input field and button to map
folium.Marker(location=[32.0872, 34.8875], icon=folium.DivIcon(html=input_box + button + script)).add_to(m)

# Keep track of markers
markers = []

# Display the map
m.save("sampled_points_map.html")
