import logging
from database import initialize_db, get_user_name, update_user_name, fetch_flight_bookings, fetch_hotel_bookings
from small_talk import load_small_talk, handle_small_talk
from intent_model import load_or_train_model, match_intent
from flight_booking import handle_flight_booking
from hotel_booking import handle_hotel_booking
from cancellation import process_cancellation
from utils import extract_name_from_input

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ChatbotContext:
    def __init__(self):
        self.user_name = None
        self.last_intent = None
        self.flight_details = None
        self.hotel_details = None
        self.has_pending_hotel_booking = False
        self.has_pending_flight_booking = False
        self.pending_prompt = None

    def clear_pending_prompt(self):
        self.pending_prompt = None


# Decorator for error handling and logging
def log_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            print("\nTravel Agent Bot: Something went wrong. Please try again.\n")

    return wrapper

def greet_user(user_context, intent_model):
    user_context.user_name = get_user_name()
    if not user_context.user_name:
        print("\nTravel Agent Bot: I don't know your name yet. What's your name?")
        user_input = input("\nYou: ").strip()
        intent = match_intent(user_input, intent_model)

        if intent == "name_introduction":
            extracted_name = extract_name_from_input(user_input)
            if extracted_name:
                user_context.user_name = extracted_name
                update_user_name(extracted_name)
                print(f"\nTravel Agent Bot: Nice to meet you, {user_context.user_name}!")
            else:
                print("\nTravel Agent Bot: Sorry, I couldn't catch your name. Please try again.")
                greet_user(user_context, intent_model)
        else:
            fallback_name = user_input.split()[0].capitalize()
            user_context.user_name = fallback_name
            update_user_name(fallback_name)
            print(f"\nTravel Agent Bot: Nice to meet you, {user_context.user_name}!")
    else:
        print(f"\nTravel Agent Bot: Welcome back, {user_context.user_name}!")

@log_exceptions
def initialize_bot():
    initialize_db()
    small_talk_data = load_small_talk()
    intent_model = load_or_train_model()
    return small_talk_data, intent_model


@log_exceptions
def handle_user_input(user_context, small_talk_data, intent_model):
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\nTravel Agent Bot: Goodbye, {user_context.user_name}! Have a great day!")
            break

        intent = match_intent(user_input, intent_model)

        if intent == "flight_booking":
            handle_flight_booking(user_context.user_name)
        elif intent == "hotel_booking":
            handle_hotel_booking(user_context.user_name)
        elif intent == "current_bookings":
            display_user_bookings(user_context.user_name)
        elif intent == "cancel_booking":
            process_cancellation(user_context.user_name)
        elif intent == "small_talk":
            response = handle_small_talk(user_input, small_talk_data, user_context.user_name)
            print(f"\nTravel Agent Bot: {response}")
        else:
            print("\nTravel Agent Bot: I'm not sure how to help with that. Please try rephrasing.")

@log_exceptions
def process_intent(user_input, intent, user_context, small_talk_data, intent_model):
    print(f"DEBUG: Processing intent: {intent} for input: {user_input}")  # Debugging log
    if intent == "get_name":
        if user_context.user_name:
            print(f"\nTravel Agent Bot: Your name is {user_context.user_name}.")
        else:
            print("\nTravel Agent Bot: I don't know your name yet. What's your name?")
            greet_user(user_context, intent_model)
    elif intent == "flight_booking":
        handle_flight_booking(user_context.user_name)
        user_context.has_pending_hotel_booking = True
    elif intent == "hotel_booking":
        handle_hotel_booking(user_context.user_name)
        user_context.has_pending_flight_booking = True
    elif intent == "current_bookings":
        display_user_bookings(user_context.user_name)
    elif intent == "cancel_booking":
        process_cancellation(user_context.user_name)
    elif intent == "small_talk":
        response = handle_small_talk(user_input, small_talk_data, user_context.user_name)
        if response:
            print(f"\nTravel Agent Bot: {response}")
    elif intent == "goodbye":
        print(f"\nTravel Agent Bot: Goodbye, {user_context.user_name}! Have a great day!")
        return "exit"
    else:
        print("\nTravel Agent Bot: I'm not sure how to help with that. Please try rephrasing.")
    return None

@log_exceptions
def display_user_bookings(user_name):
    print(f"\nTravel Agent Bot: Retrieving your bookings, {user_name}...")
    user_id = 1  # Assuming single-user mode for now.

    flight_bookings = fetch_flight_bookings(user_id)
    hotel_bookings = fetch_hotel_bookings(user_id)

    if not flight_bookings and not hotel_bookings:
        print(f"\nTravel Agent Bot: You have no bookings, {user_name}.")
        return

    if flight_bookings:
        print("\nYour Flight Bookings:")
        for booking in flight_bookings:
            print(
                f"  - Booking ID {booking[0]}: From {booking[2]} to {booking[3]}, Departure {booking[4]}, Return {booking[5]}")

    if hotel_bookings:
        print("\nYour Hotel Bookings:")
        for booking in hotel_bookings:
            print(
                f"  - Booking ID {booking[0]}: City {booking[2]}, Hotel {booking[3]}, Check-in {booking[4]}, Check-out {booking[5]}, Rooms {booking[6]}"
            )
    print()


@log_exceptions
def suggest_next_step(user_context):
    if user_context.has_pending_hotel_booking:
        print("\nTravel Agent Bot: Would you like me to help you find a hotel for your trip?")
        user_context.pending_prompt = "hotel_booking_suggestion"
        user_context.has_pending_hotel_booking = False
    elif user_context.has_pending_flight_booking:
        print("\nTravel Agent Bot: Would you like me to help you book a flight?")
        user_context.pending_prompt = "flight_booking_suggestion"
        user_context.has_pending_flight_booking = False


@log_exceptions
def handle_user_input(user_context, small_talk_data, intent_model):
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print(f"\nTravel Agent Bot: Goodbye, {user_context.user_name}!")
            break

        if user_context.pending_prompt:
            handle_prompt_response(user_input, user_context)
            continue

        if "call me" in user_input.lower() or "my name is" in user_input.lower():
            new_name = extract_name_from_input(user_input)
            if new_name:
                update_user_name(new_name)
                user_context.user_name = new_name
                print(f"\nTravel Agent Bot: I'll call you {new_name} from now on!")
            continue

        intent = match_intent(user_input, intent_model)
        result = process_intent(user_input, intent, user_context, small_talk_data, intent_model)
        if result == "exit":
            break

        suggest_next_step(user_context)


@log_exceptions
def handle_prompt_response(user_input, user_context):
    user_input = user_input.lower()
    if user_context.pending_prompt == "hotel_booking_suggestion":
        if user_input in ["yes", "sure", "okay"]:
            handle_hotel_booking(user_context.user_name)
        elif user_input in ["no", "not now"]:
            print("\nTravel Agent Bot: Alright, let me know if you need any help!")
        else:
            print("\nTravel Agent Bot: Do you want me to book a hotel?")
    elif user_context.pending_prompt == "flight_booking_suggestion":
        if user_input in ["yes", "sure", "okay"]:
            handle_flight_booking(user_context.user_name)
        elif user_input in ["no", "not now"]:
            print("\nTravel Agent Bot: Let me know if you need any assistance!")
        else:
            print("\nTravel Agent Bot: Do you want me to book a flight?")
    user_context.clear_pending_prompt()


@log_exceptions
def main():
    print("\nTravel Agent Bot: Welcome to your personal travel assistant! Type 'exit' to quit.")
    initialize_db()
    intent_model = load_or_train_model()
    small_talk_data = load_small_talk()

    user_context = ChatbotContext()
    greet_user(user_context, intent_model)
    handle_user_input(user_context, small_talk_data, intent_model)

if __name__ == "__main__":
    main()
