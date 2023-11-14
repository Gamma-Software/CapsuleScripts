import folium
import paho.mqtt.client as mqtt

from flask import Flask
import folium
import webbrowser

app = Flask(__name__)

# Function to create Leaflet map
@app.route('/')
def create_map():
    # Function to update map markers
    def on_message(client, userdata, message):
    global leaflet_map
    if message.topic == "router/gps/longitude":
        longitude = float(message.payload)
        print(longitude)
        if 'latitude' in globals():
            leaflet_map.location = [latitude, longitude]
            leaflet_map.add_child(folium.Marker([latitude, longitude], popup='Current Location'))
            leaflet_map.save("index.html")
    elif message.topic == "router/gps/latitude":
        latitude = float(message.payload)
        if 'longitude' in globals():
            leaflet_map.location = [latitude, longitude]
            leaflet_map.add_child(folium.Marker([latitude, longitude], popup='Current Location'))
            leaflet_map.save("map.html")

    # MQTT setup
    client = mqtt.Client("Leaflet_Map")
    client.username_pw_set("rudloff", "y4uv3jpc")
    client.connect("192.168.10.1", port=1334)

    client.on_message = on_message
    client.subscribe("router/gps/longitude")
    client.subscribe("router/gps/latitude")
    client.loop_start()

    # Leaflet map setup
    leaflet_map = folium.Map(location=[0, 0], zoom_start=10)  # Initial location
    leaflet_map.save("templates/index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')