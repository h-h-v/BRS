import psycopg2
from datetime import date
# Define your database connection details
DATABASE_URL = 'postgres://ermmmhea:o3nwulL9fesvtV9VHHcPAiXIlC6irytd@snuffleupagus.db.elephantsql.com/ermmmhea'

def add_bus(bus_number, route, capacity, manufacturer, year, bus_date):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # SQL statement to insert a new bus into the buses table
        insert_query = """
        INSERT INTO buses (bus_number, route, capacity, manufacturer, year, date)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Execute the SQL statement with the provided values
        cursor.execute(insert_query, (bus_number, route, capacity, manufacturer, year, bus_date))

        # Commit the transaction
        conn.commit()

    except Exception as e:
        # Handle any database errors
        print("Error:", e)
        conn.rollback()  # Rollback the transaction in case of error

    finally:
        if conn is not None:
            conn.close()  # Close the database connection

# Example usage:
add_bus("S R T", "Chennai to Karur", 16, "Volvo AC Seater Pushback", 2023, date(2024, 5, 30))