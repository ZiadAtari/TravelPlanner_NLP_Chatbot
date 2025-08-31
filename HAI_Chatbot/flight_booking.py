import csv
from utils import validate_date, is_cancel_request
from database import add_flight_booking
from cancellation import process_cancellation

def load_iata_codes(file_path='IATA_Codes.csv'):
    """Load IATA codes into a dictionary for quick lookup."""
    iata_lookup = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['City'].strip().capitalize()
            code = row['IATA Code'].strip().upper()
            if city not in iata_lookup:
                iata_lookup[city] = []
            iata_lookup[city].append(code)
    return iata_lookup

def handle_flight_booking(user_name):
    iata_lookup = load_iata_codes()

    while True:
        departure_city = input(
            f"Travel Agent Bot: Which city are you departing from, {user_name}? ").strip().capitalize()
        if is_cancel_request(departure_city):
            process_cancellation(user_name)
            return

        if departure_city in iata_lookup:
            departure_code = iata_lookup[departure_city][0]
            print(f"Travel Agent Bot: Flights departing from {departure_city} ({departure_code}) found.")
        else:
            print(f"Travel Agent Bot: No airports found for {departure_city}. Please try another city.")
            continue

        destination_city = input(
            f"Travel Agent Bot: Which city are you flying to, {user_name}? ").strip().capitalize()
        if is_cancel_request(destination_city):
            process_cancellation(user_name)
            return

        if destination_city in iata_lookup:
            destination_code = iata_lookup[destination_city][0]
            print(f"Travel Agent Bot: Flights to {destination_city} ({destination_code}) found.")
        else:
            print(f"Travel Agent Bot: No airports found for {destination_city}. Please try another city.")
            continue

        # Get the departure date
        departure_date = input(f"Travel Agent Bot: When do you want to leave for {destination_code}? (YYYY-MM-DD format) ")
        if is_cancel_request(departure_date):
            process_cancellation(user_name)
            return

        if not validate_date(departure_date):
            print("Travel Agent Bot: Please enter a valid date in the format YYYY-MM-DD.")
            continue

        # Get the return date
        return_date = input(f"Travel Agent Bot: When will you return from {destination_code}? (YYYY-MM-DD format) ")
        if is_cancel_request(return_date):
            process_cancellation(user_name)
            return

        if not validate_date(return_date) or return_date < departure_date:
            print("Travel Agent Bot: The return date must be after the departure date.")
            continue

        # Confirm and add the booking
        confirmation = input("Travel Agent Bot: Confirm your flight details (yes/no): ").strip().lower()
        if is_cancel_request(confirmation):
            process_cancellation(user_name)
            return

        if confirmation == 'yes':
            add_flight_booking(1, departure_city, destination_code, departure_date, return_date)
            print("Travel Agent Bot: Your flight has been booked successfully!")
            break
        else:
            print("Travel Agent Bot: Let's revise your booking details.")
