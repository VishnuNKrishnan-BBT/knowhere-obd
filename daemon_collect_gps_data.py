import time
import sqlite3
from utils import log, collect_gps_data

# New leg
new_leg = True

# Function to add GPS data to local SQLite database
def add_to_database(data):
    global new_leg  # Declare new_leg as global
    if data is not None:
        conn = sqlite3.connect('gps_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS gps_data (timestamp INTEGER, latitude REAL, longitude REAL, speed REAL, heading REAL, new_leg BOOLEAN)")
        try:
            c.execute("INSERT INTO gps_data VALUES (?, ?, ?, ?, ?, ?)", (data["timestamp"], data["latitude"], data["longitude"], data["speed"], data["heading"], new_leg))
            conn.commit()
            # print("Saved to local DB successfully")

            # Modify new_leg to be false after first iteration
            new_leg = False

        except sqlite3.Error as e:
            print("Failed:", e)
        finally:
            conn.close()


# Main function
def main():
    while True:
        try:
            # Collect GPS data
            gps_data = collect_gps_data(new_leg)
            
            # Add GPS data to database
            add_to_database(gps_data)
            
            # Format message to be saved
            message = "No GPS fix available" if gps_data is None else "Saved: " + str(gps_data)
            
            # Print message to file
            log("collect_gps_data", message)
            
            # Wait for 2 seconds before collecting next GPS data
            time.sleep(2)
        except Exception as e:
            print("Error:", e)
            # If there's an error, wait for 10 seconds before retrying
            time.sleep(10)

if __name__ == "__main__":
    main()