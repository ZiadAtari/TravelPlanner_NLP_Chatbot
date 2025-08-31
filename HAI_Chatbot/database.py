import sqlite3
from random import randint
from utils import extract_name_from_input

from utils import extract_name_from_input
import sqlite3

def initialize_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_info
                          (user_id INTEGER PRIMARY KEY, name TEXT, history TEXT, last_intent TEXT)''')
        cursor.execute("INSERT OR IGNORE INTO user_info (user_id, name, history, last_intent) VALUES (1, '', '', '')")
        cursor.execute('''CREATE TABLE IF NOT EXISTS flight_bookings
                          (booking_id INTEGER PRIMARY KEY, user_id INTEGER, 
                           departure_city TEXT, destination TEXT, departure_date TEXT, return_date TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS hotel_bookings
                          (booking_id INTEGER PRIMARY KEY, user_id INTEGER, 
                           city TEXT, hotel_name TEXT, check_in_date TEXT, check_out_date TEXT, num_rooms INTEGER)''')
        conn.commit()

def get_user_name():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user_info WHERE user_id=1")
        user = cursor.fetchone()
        if user and user[0]:
            return user[0]
        return None

def update_user_name(new_name):
    with sqlite3.connect('database.db') as conn:
        extracted_name = extract_name_from_input(new_name)
        if extracted_name:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_info SET name = ? WHERE user_id = 1", (extracted_name,))
            conn.commit()

def get_user_name():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM user_info WHERE user_id=1")
        user = cursor.fetchone()

        if user and user[0]:
            return user[0]
        else:
            name = input("Travel Agent Bot: I don't know your name yet. What's your name? ").strip()
            extracted_name = extract_name_from_input(name)
            if extracted_name:
                cursor.execute("UPDATE user_info SET name = ? WHERE user_id = 1", (extracted_name,))
                conn.commit()
                return extracted_name
            else:
                print("Travel Agent Bot: Sorry, I couldn't understand your name.")
                return None

def update_user_name(new_name):
    with sqlite3.connect('database.db') as conn:
        extracted_name = extract_name_from_input(new_name)
        if extracted_name:
            cursor = conn.cursor()
            cursor.execute("UPDATE user_info SET name = ? WHERE user_id = 1", (extracted_name,))
            conn.commit()

def generate_unique_booking_id(table_name):
    """Generate a unique 4-digit booking ID with retry logic."""
    for _ in range(10):  # Retry up to 10 times
        booking_id = randint(1000, 9999)
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE booking_id = ?", (booking_id,))
            if cursor.fetchone()[0] == 0:
                return booking_id
    raise ValueError(f"Failed to generate a unique booking ID after 10 attempts.")

def add_flight_booking(user_id, departure_city, destination, departure_date, return_date):
    try:
        booking_id = generate_unique_booking_id('flight_bookings')
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO flight_bookings (booking_id, user_id, departure_city, destination, departure_date, return_date) 
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (booking_id, user_id, departure_city, destination, departure_date, return_date))
            conn.commit()
            print(f"DEBUG: Added flight booking: ID {booking_id}, User ID {user_id}, From {departure_city} to {destination}.")
        print(f"Travel Agent Bot: Your flight booking ID is {booking_id}.")
    except Exception as e:
        print(f"Travel Agent Bot: Failed to add flight booking. Error: {e}")

def add_hotel_booking(user_id, city, hotel_name, check_in_date, check_out_date, num_rooms):
    try:
        booking_id = generate_unique_booking_id('hotel_bookings')
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO hotel_bookings (booking_id, user_id, city, hotel_name, check_in_date, check_out_date, num_rooms) 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (booking_id, user_id, city, hotel_name, check_in_date, check_out_date, num_rooms))
            conn.commit()
            print(f"Travel Agent Bot: Your hotel booking ID is {booking_id}.")
    except Exception as e:
        print(f"Travel Agent Bot: Failed to add hotel booking. Error: {e}")

def fetch_flight_bookings(user_id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM flight_bookings WHERE user_id = ?", (user_id,))
            bookings = cursor.fetchall()
            print(f"DEBUG: Fetched flight bookings for User ID {user_id}: {bookings}")
            return bookings
    except Exception as e:
        print(f"Travel Agent Bot: Failed to fetch flight bookings. Error: {e}")
        return []

def fetch_hotel_bookings(user_id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hotel_bookings WHERE user_id = ?", (user_id,))
            bookings = cursor.fetchall()
            return bookings
    except Exception as e:
        print(f"Travel Agent Bot: Failed to fetch hotel bookings. Error: {e}")
        return []

def cancel_flight_booking(booking_id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flight_bookings WHERE booking_id = ?", (booking_id,))
            conn.commit()
    except Exception as e:
        print(f"Travel Agent Bot: Failed to cancel flight booking. Error: {e}")

def cancel_hotel_booking(booking_id):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hotel_bookings WHERE booking_id = ?", (booking_id,))
            conn.commit()
    except Exception as e:
        print(f"Travel Agent Bot: Failed to cancel hotel booking. Error: {e}")

def save_user_context(user_id, last_intent, history):
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            history_str = str(history)  # Convert history list to string
            cursor.execute("UPDATE user_info SET last_intent = ?, history = ? WHERE user_id = ?",
                           (last_intent, history_str, user_id))
            conn.commit()
    except Exception as e:
        print(f"Travel Agent Bot: Failed to save user context. Error: {e}")

def load_user_context(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_intent, history FROM user_info WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
        if data and data[1]:
            return data[0], eval(data[1])  # Convert history string back to list
        return None
