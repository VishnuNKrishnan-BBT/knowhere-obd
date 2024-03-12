import sqlite3
import requests
import json
import time
import sys
from utils import log, get_device_id

# Function to send data to the endpoint and delete successfully processed waypoints
def send_data(payload):
    try:
        waypoints_count = len(payload)
        log("periodic_uploader", f"Uploading {waypoints_count} waypoints")
        headers = {"authorization": "your-secret-token"}
        response = requests.post("https://knowhere-ms-obdcomms-b17d30ba7749.herokuapp.com/addWaypoints", headers=headers, json=payload)
        if response.status_code == 200:
            log("periodic_uploader", f"{waypoints_count} waypoints sent successfully.")
            try:
                json_response = response.json()
                log("periodic_uploader", f"Response: {json_response}")
                processed_timestamps = json_response.get('processedTimestamps', [])
                if processed_timestamps:
                    try:
                        conn = sqlite3.connect('gps_data.db')
                        c = conn.cursor()
                        # Delete successfully processed waypoints from the database
                        for timestamp in processed_timestamps:
                            c.execute("DELETE FROM gps_data WHERE timestamp = ?", (timestamp,))
                        conn.commit()
                        log("periodic_uploader", f"{len(processed_timestamps)} waypoints deleted from gps_data.db.")
                    except sqlite3.Error as e:
                        log("periodic_uploader", f"SQLite Error: {str(e)}")
                    finally:
                        conn.close()
            except json.JSONDecodeError:
                log("periodic_uploader", "Invalid JSON data received.")
        else:
            log("periodic_uploader", f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        log("periodic_uploader", f"Error: {str(e)}")

# Main function
def main():
    try:
        # Connect to the database
        conn = sqlite3.connect('gps_data.db')
        c = conn.cursor()

        # Retrieve data from the database
        c.execute("SELECT * FROM gps_data ORDER BY timestamp ASC LIMIT 500")
        data = c.fetchall()

        # Check if there are more than 10 entries
        if len(data) > 10:
            # Read tracker ID from file
            tracker_id = get_device_id()
            if tracker_id is not None:
                # Prepare payload
                payload = []
                for waypoint in data:
                    payload.append({
                        "timestamp": waypoint[0],
                        "latitude": waypoint[1],
                        "longitude": waypoint[2],
                        "speed": waypoint[3],
                        "heading": waypoint[4],
                        "new_leg": waypoint[5]
                    })
                # Send data to endpoint
                send_data(payload)
    except sqlite3.Error as e:
        log("SQLite Error:", e)
    finally:
        conn.close()

# Redirect stdout to both terminal and file
sys.stdout = open('logs.txt', 'a')

# Loop to run the script every 5 seconds
while True:
    main()
    time.sleep(5)
