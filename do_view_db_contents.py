import sqlite3
from tabulate import tabulate

# Function to view contents of the database
def view_database():
    try:
        conn = sqlite3.connect('gps_data.db')
        c = conn.cursor()
        c.execute("SELECT * FROM gps_data")
        rows = c.fetchall()
        if not rows:
            print("Database is empty")
        else:
            headers = [description[0] for description in c.description]
            print(tabulate(rows, headers=headers, tablefmt="grid"))
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

# Main function
def main():
    view_database()

if __name__ == "__main__":
    main()
