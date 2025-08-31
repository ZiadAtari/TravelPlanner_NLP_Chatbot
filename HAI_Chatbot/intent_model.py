from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Training data for intent recognition
training_sentences = [
    # Flight Booking
    "I want to book a flight",
    "Can you book a flight for me?",
    "I need a flight ticket",
    "Book a plane ticket",
    "Can you help me find a flight to New York?",
    "I want to travel by air",
    "I need to fly to Paris",
    "Flight ticket to Tokyo please",
    "Reserve a seat on a flight",
    "Book my air travel",
    "I need a flight reservation",
    "Find me a flight",
    "I'd like to book an airline ticket",
    "Can I get a flight to Los Angeles?",
    "I need to travel by plane",
    "Arrange a flight for me",
    "I need a ticket to Sydney",
    "Get me a flight to Miami",
    "Can you reserve a flight for me?",
    "I want to fly to Chicago next week",
    "Book my flight for tomorrow",
    "Can I fly to Berlin on the 15th?",
    "What's the best flight to Dubai?",
    "Get me a ticket to Rome",
    "I'd like to take a flight",
    "Please arrange a flight from London to Madrid",
    "I want to catch a plane to Boston",
    "I want to schedule a flight for my vacation",
    "Flight booking needed",
    "I need a one-way ticket to Barcelona",

    # Hotel Booking
    "I need a hotel room",
    "Book a hotel for me",
    "Can you reserve a room in a hotel?",
    "I want to stay in a hotel",
    "Find me a place to stay in London",
    "Can you help me book accommodation?",
    "Hotel reservation for tonight",
    "Book a room for three nights",
    "I need a hotel for my vacation",
    "Reserve a suite in a hotel",
    "Where can I stay in Paris?",
    "I need to book accommodation in Tokyo",
    "Can you arrange a hotel for me?",
    "I need lodging for my trip",
    "Find a cheap hotel in New York",
    "I want a five-star hotel reservation",
    "Get me a room for two nights",
    "I'd like to stay in a hotel",
    "Can you find me a hotel near the airport?",
    "I need a place to stay",
    "Reserve a room with a nice view",
    "I want a hotel in downtown Chicago",
    "Book a luxury suite",
    "Can I get a reservation for a resort?",
    "I need to book a double room",
    "Where can I sleep for the night?",
    "Get me a hotel near the beach",
    "Book a family-friendly hotel",
    "I need a hotel for next weekend",
    "Reserve an apartment or a room",

    # Cancel Booking
    "I want to cancel my booking",
    "Can I cancel my reservation?",
    "I need to cancel a flight",
    "Cancel my hotel booking",
    "Cancel the reservation",
    "I need to remove my booking",
    "Can you cancel the flight for me?",
    "Please cancel my room reservation",
    "I made a mistake, cancel my booking",
    "Cancel the trip",
    "I don't need the flight anymore",
    "Cancel my travel plans",
    "I want to cancel my stay",
    "Can you please cancel everything?",
    "I changed my mind, cancel my reservations",
    "I need to cancel my trip",
    "Please remove my flight from the schedule",
    "Cancel the entire booking",
    "No longer need the reservation, cancel it",
    "Cancel my flight and hotel",
    "Cancel everything related to my trip",
    "I'd like to cancel my vacation plans",
    "Undo my reservation",
    "Revoke the booking I made earlier",
    "Cancel the tickets and reservations",

    # Get Name
    "What is my name?",
    "Can you tell me my name?",
    "Do you remember my name?",
    "What did I tell you my name is?",
    "Who am I?",
    "Can you recall my name?",
    "Do you still remember my name?",
    "What did I tell you before?",
    "What do you call me?",
    "Do you remember what I asked you to call me?",
    "What name did I give you?",
    "Tell me my name",

    # Name Introduction
    "My name is John",
    "You can call me Sarah",
    "I am Michael",
    "I go by Alice",
    "Call me Kevin",
    "They call me Mike",
    "I'm known as Emma",
    "Please call me Olivia",
    "You should call me Liam",
    "This is Sophia",

    # Small Talk
    "How are you?",
    "What's up?",
    "How's it going?",
    "Tell me a joke",
    "What can you do?",
    "What's the weather like?",
    "Do you like traveling?",
    "What's your favorite destination?",
    "Are you a real person?",
    "How old are you?",
    "Do you have feelings?",
    "What's your name?",
    "Do you like helping people?",
    "What's your favorite airline?",
    "How does a chatbot work?",
    "Can you talk to me?",
    "Do you get tired?",
    "What can you do?",
    "Are you alive?",
    "Do you have friends?",
    "Tell me something interesting",
    "What's your favorite color?",
    "Do you like coffee?",
    "Do you ever sleep?",
    "What's the meaning of life?",
    "Are you intelligent?",
    "Can you laugh?",
    "Do you eat food?",
    "Are you aware of time?",
    "Do you have hobbies?",
    "Can we be friends?",
    "Do you have a job?",
    "What do you do for fun?",
    "What's your story?",
    "Do you get bored?",
    "Are you happy?",

    # Current Bookings
    "Show me my current bookings",
    "What are my current bookings?",
    "Do I have any bookings?",
    "List my reservations",
    "Show my upcoming bookings",
    "Tell me what I have booked",
    "What are my upcoming trips?",
    "Do I have any planned trips?",
    "Please list my reservations",
    "Give me a summary of my bookings",
    "Do I have anything booked right now?",
    "Can you show my reservations?",
    "Show my itinerary",
    "What flights and hotels do I have booked?",
    "Tell me about my current reservations",

    # Goodbye
    "Goodbye",
    "Bye",
    "See you later",
    "I'm done",
    "Exit",
    "Quit",
    "I have to go now",
    "Talk to you soon",
    "See you next time",
    "That's all for now",
    "Catch you later",
    "Bye bye",
    "I need to leave",
    "Ending the chat",
    "I have to go",
    "Farewell",
    "Adios",
    "Signing off"
]

# Corresponding labels for each training sentence
training_labels = (
    ["flight_booking"] * 30 +
    ["hotel_booking"] * 30 +
    ["cancel_booking"] * 25 +
    ["get_name"] * 12 +
    ["name_introduction"] * 10 +
    ["small_talk"] * 36 +
    ["current_bookings"] * 15 +
    ["goodbye"] * 18
)

# Train the intent model
def train_intent_model():
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    model_pipeline.fit(training_sentences, training_labels)
    joblib.dump(model_pipeline, 'intent_model.pkl')
    return model_pipeline

# Load or train the model
def load_or_train_model():
    try:
        return joblib.load('intent_model.pkl')
    except FileNotFoundError:
        return train_intent_model()

# Match intent using the model
def match_intent(user_input, model):
    return model.predict([user_input])[0]

assert len(training_sentences) == len(training_labels), (
    f"Mismatch: {len(training_sentences)} sentences and {len(training_labels)} labels"
)

def train_intent_model():
    model_pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    model_pipeline.fit(training_sentences, training_labels)
    joblib.dump(model_pipeline, 'intent_model.pkl')
    return model_pipeline

def load_or_train_model():
    try:
        return joblib.load('intent_model.pkl')
    except FileNotFoundError:
        return train_intent_model()

# Match intent using the model
def match_intent(user_input, model):
    return model.predict([user_input])[0]

if __name__ == "__main__":
    model = load_or_train_model()
    user_input = "My name is Ziad"
    intent = match_intent(user_input, model)
    print("Detected intent:", intent)
