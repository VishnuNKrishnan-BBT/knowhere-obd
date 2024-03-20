import json
import time
import websocket
from utils import log, get_device_id, get_device_auth_key, collect_gps_data

# WebSocket URL
ws_url = "wss://kw-ms-ws-livelocation-a6364ce6d3cd.herokuapp.com/"

# Reconnection parameters
reconnect_interval = 5  # Interval between reconnection attempts (in seconds)

# Function to establish WebSocket connection
def establish_connection():
    while True:
        try:
            log('update_live_location', "Attempting to establish WebSocket connection...")
            ws = websocket.create_connection(ws_url)
            log('update_live_location', "WebSocket connection established.")
            return ws
        except Exception as e:
            log('update_live_location', f"Failed to establish WebSocket connection: {e}")
            log('update_live_location', f"Retrying in {reconnect_interval} seconds...")
            time.sleep(reconnect_interval)

# Function to send payload to WebSocket server
def send_payload():
    gps_data = collect_gps_data(False)
    
    if gps_data:
        try:
            ws = establish_connection()
            payload = {"authToken": get_device_auth_key(), "trackerId": get_device_id(), "latitude": gps_data["latitude"], "longitude": gps_data["longitude"], "speed": gps_data["speed"], "heading": gps_data["heading"]}
            payload_json = json.dumps(payload)
            ws.send(payload_json)
            log('update_live_location', f"Sent payload: {payload_json}")
            ws.close()
        except Exception as e:
            log('update_live_location', f"Error sending payload: {e}")
    else:
        log('update_live_location', "No GPS fix available.")

try:
    # Send payload every 2 seconds
    while True:
        send_payload()
        time.sleep(2)
except KeyboardInterrupt:
    log('update_live_location', "Stopping...")
