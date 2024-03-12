import sqlite3
from utils import log

# Function to clear the contents of the database
def clear_database():
    try:
        conn = sqlite3.connect('gps_data.db')
        c = conn.cursor()
        c.execute("DELETE FROM gps_data")
        conn.commit()
        log("clear_db", "Database cleared successfully")
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

# Main function
def main():
    clear_database()

if __name__ == "__main__":
    main()
