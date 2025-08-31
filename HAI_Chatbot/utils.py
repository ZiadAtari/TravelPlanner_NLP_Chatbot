from datetime import datetime
import re

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def extract_name_from_input(user_input):
    """Extracts and cleans the name from user input using regular expressions."""
    # Patterns to match common name introduction phrases
    patterns = [
        r"\bmy name is ([a-zA-Z]+)",
        r"\bcall me ([a-zA-Z]+)",
        r"\bi am ([a-zA-Z]+)",
        r"\bi'm ([a-zA-Z]+)",
        r"\bthey call me ([a-zA-Z]+)",
        r"\bknown as ([a-zA-Z]+)",
        r"\bplease call me ([a-zA-Z]+)",
        r"\byou should call me ([a-zA-Z]+)",
        r"\bthis is ([a-zA-Z]+)"
    ]

    user_input_lower = user_input.lower()

    for pattern in patterns:
        match = re.search(pattern, user_input_lower)
        if match:
            # Extract the name from the match
            name = match.group(1).strip()
            return name.capitalize()

    # Fallback: If no keyword matches, try to return the first word
    words = user_input.strip().split()
    if words:
        return words[0].capitalize()

    return None

def validate_positive_integer(input_str):
    try:
        value = int(input_str)
        return value > 0
    except ValueError:
        return False

def is_cancel_request(user_input):
    cancel_keywords = ["cancel my booking", "cancel booking", "cancel reservation", "I want to cancel"]
    return any(keyword in user_input.lower() for keyword in cancel_keywords)
