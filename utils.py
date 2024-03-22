from datetime import datetime
import time
import gpsd
import sqlite3

def log(heading, content, max_entries=50000):
    # Format timestamp
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    # Format log entry
    log_entry = f"=== {heading} ===\n{timestamp}\n{content}\n\n"

    # Print to terminal
    print(log_entry)

    # Check if logs.txt file exists, create it if it doesn't
    try:
        file = open('logs.txt', 'r+')
    except FileNotFoundError:
        file = open('logs.txt', 'w+')

    # Read existing log entries
    logs = file.readlines()

    # Calculate the number of lines to remove
    lines_to_remove = max(0, len(logs) + 1 - max_entries)  # +1 to account for the incoming log

    # Remove the oldest log entries if needed
    if lines_to_remove > 0:
        logs = logs[lines_to_remove:]

    # Move the cursor to the beginning of the file
    file.seek(0)

    # Write updated logs
    file.writelines(logs)

    # Append the new log entry
    file.write(log_entry)

    # Close the file
    file.close()




# Function to collect GPS data
def collect_gps_data(new_leg=False):
    # # Connect to the local gpsd
    gpsd.connect()

    # Generate timestamp
    timestamp = int(time.time())

    # Retrieve GPS data
    try:
        packet = gpsd.get_current()
        
        if packet.mode >= 2:  # Check if GPS has a fix
            speed = packet.speed()
            return {
                "latitude": packet.lat,
                "longitude": packet.lon,
                "speed": speed,
                "heading": packet.track,
                "timestamp": timestamp,
                "new_leg": new_leg
            }
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None




def get_device_id():
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()

        # Retrieve the Device ID from the auth_info table
        cursor.execute('''SELECT value FROM auth_info WHERE parameter = ?''', ('Device ID',))
        device_id = cursor.fetchone()

        conn.close()

        if device_id:
            return device_id[0]  # Extracting the device ID from the result tuple
        else:
            log("utils/get_device_id", "Device ID not found in auth.db.")
            return None
    except Exception as e:
        log("utils/get_device_id", f"Error occurred while reading device ID: {e}")
        return None




def get_device_auth_key():
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()

        # Retrieve the Device ID from the auth_info table
        cursor.execute('''SELECT value FROM auth_info WHERE parameter = ?''', ('Auth Key',))
        device_id = cursor.fetchone()

        conn.close()

        if device_id:
            return device_id[0]  # Extracting the device ID from the result tuple
        else:
            log("utils/get_device_auth_key", "Auth key not found in auth.db.")
            return None
    except Exception as e:
        log("utils/get_device_auth_key", f"Error occurred while reading auth key: {e}")
        return None