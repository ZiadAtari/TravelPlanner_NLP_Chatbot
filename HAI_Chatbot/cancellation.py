# cancellation.py
from database import fetch_flight_bookings, fetch_hotel_bookings, cancel_flight_booking, cancel_hotel_booking

def process_cancellation(user_name):
    flight_bookings = fetch_flight_bookings(1)
    hotel_bookings = fetch_hotel_bookings(1)

    if not flight_bookings and not hotel_bookings:
        print(f"Travel Agent Bot: You have no bookings to cancel, {user_name}.")
        return

    print("Travel Agent Bot: Here are your current bookings:")
    for booking in flight_bookings:
        print(f"Flight Booking ID {booking[0]}: {booking[2]} from {booking[3]} to {booking[4]}")
    for booking in hotel_bookings:
        print(f"Hotel Booking ID {booking[0]}: {booking[2]} from {booking[3]} to {booking[4]}, Rooms: {booking[5]}")

    booking_id = input("Travel Agent Bot: Please enter the booking ID you wish to cancel: ")
    if any(str(booking[0]) == booking_id for booking in flight_bookings):
        cancel_flight_booking(booking_id)
        print(f"Travel Agent Bot: Your flight booking ID {booking_id} has been cancelled.")
    elif any(str(booking[0]) == booking_id for booking in hotel_bookings):
        cancel_hotel_booking(booking_id)
        print(f"Travel Agent Bot: Your hotel booking ID {booking_id} has been cancelled.")
    else:
        print(f"Travel Agent Bot: I couldn't find that booking ID, {user_name}.")
