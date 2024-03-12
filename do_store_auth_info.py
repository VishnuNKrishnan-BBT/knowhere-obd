import sqlite3
from tabulate import tabulate
from utils import log

def create_table():
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()

        # Create the auth_info table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS auth_info
                          (parameter TEXT PRIMARY KEY, value TEXT)''')

        conn.commit()
        conn.close()
    except Exception as e:
        log("store_auth_info", f"Error occurred while creating auth info table: {e}")

def store_auth_info(device_id, auth_key):
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()

        # Insert or replace the device ID and auth key into the auth_info table
        cursor.execute('''REPLACE INTO auth_info (parameter, value) VALUES (?, ?)''',
                       ('Device ID', device_id))
        cursor.execute('''REPLACE INTO auth_info (parameter, value) VALUES (?, ?)''',
                       ('Auth Key', auth_key))

        conn.commit()
        conn.close()
        log("store_auth_info", "Auth information stored successfully.")
    except Exception as e:
        log("store_auth_info", f"Error occurred while storing auth information: {e}")

def main():
    # Create the auth_info table if it doesn't exist
    create_table()

    # Accept Device ID and Auth Key from the user
    device_id = input("Enter Device ID: ")
    auth_key = input("Enter Auth Key: ")

    # Store the auth information
    store_auth_info(device_id, auth_key)

if __name__ == "__main__":
    main()
