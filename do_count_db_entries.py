import sqlite3

# Function to count rows in the database
def count_rows():
    try:
        conn = sqlite3.connect('gps_data.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM gps_data")
        row_count = c.fetchone()[0]
        print("Number of rows in the database:", row_count)
    except sqlite3.Error as e:
        print("Error:", e)
    finally:
        conn.close()

# Main function
def main():
    count_rows()

if __name__ == "__main__":
    main()
