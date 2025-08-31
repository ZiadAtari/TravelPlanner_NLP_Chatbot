from utils import validate_date, validate_positive_integer, is_cancel_request
from database import add_hotel_booking
from cancellation import process_cancellation


def handle_hotel_booking(user_name):
    while True:
        city = input(f"Travel Agent Bot: Which city would you like to stay in, {user_name}? ")
        if is_cancel_request(city):
            process_cancellation(user_name)
            return

        print(f"Travel Agent Bot: Please choose a hotel from the following options:")
        hotels = ["Hilton", "Marriott", "Mövenpick", "Crown Plaza"]
        for i, hotel in enumerate(hotels, 1):
            print(f"  {i}. {hotel}")

        hotel_choice = input(f"Travel Agent Bot: Enter the number corresponding to your choice (1-{len(hotels)}): ")
        if is_cancel_request(hotel_choice):
            process_cancellation(user_name)
            return

        try:
            hotel_choice = int(hotel_choice)
            if 1 <= hotel_choice <= len(hotels):
                selected_hotel = hotels[hotel_choice - 1]
                print(f"Travel Agent Bot: You selected {selected_hotel}.")
            else:
                print("Travel Agent Bot: Invalid choice. Please select a valid option.")
                continue
        except ValueError:
            print("Travel Agent Bot: Please enter a number corresponding to the hotel options.")
            continue

        check_in_date = input(
            f"Travel Agent Bot: When would you like to check in at {city}? (Please use YYYY-MM-DD format) ")
        if is_cancel_request(check_in_date):
            process_cancellation(user_name)
            return

        if not validate_date(check_in_date):
            print("Travel Agent Bot: Please enter a valid date in the format YYYY-MM-DD.")
            continue

        check_out_date = input(
            f"Travel Agent Bot: When will you be checking out from {city}? (Please use YYYY-MM-DD format) ")
        if is_cancel_request(check_out_date):
            process_cancellation(user_name)
            return

        if not validate_date(check_out_date) or check_out_date < check_in_date:
            print("Travel Agent Bot: The check-out date must be after the check-in date.")
            continue

        num_rooms = input(f"Travel Agent Bot: How many rooms will you need, {user_name}? ")
        if is_cancel_request(num_rooms):
            process_cancellation(user_name)
            return

        if not validate_positive_integer(num_rooms):
            print("Travel Agent Bot: Please enter a valid positive number for the number of rooms.")
            continue

        confirmation = input("Travel Agent Bot: Confirm your hotel booking details (yes/no): ").strip().lower()
        if is_cancel_request(confirmation):
            process_cancellation(user_name)
            return

        if confirmation == 'yes':
            add_hotel_booking(1, city, selected_hotel, check_in_date, check_out_date, num_rooms)
            print(f"Travel Agent Bot: Awesome! Your hotel booking at {selected_hotel} is being processed.")
            break
        else:
            print("Travel Agent Bot: Let's modify your booking details.")
