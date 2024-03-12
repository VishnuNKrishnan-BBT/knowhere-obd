import sqlite3
from tabulate import tabulate

def view_auth_info():
    try:
        conn = sqlite3.connect('auth.db')
        cursor = conn.cursor()

        # Retrieve the device ID and auth key from the auth_info table
        cursor.execute('''SELECT * FROM auth_info''')
        rows = cursor.fetchall()

        # Format the rows into a table
        table = [[row[0], row[1]] for row in rows]

        conn.close()

        # Print the table using tabulate
        print("Device Auth Information")
        print(tabulate(table, tablefmt="grid"))
    except Exception as e:
        print(f"Error occurred while viewing auth information: {e}")

def main():
    view_auth_info()

if __name__ == "__main__":
    main()