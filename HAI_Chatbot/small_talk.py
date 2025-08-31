import csv
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load small talk data from multiple sources
def load_small_talk(existing_filename='small_talk.csv', additional_filename='COMP3074-CW1-Dataset.csv'):
    small_talk_dict = {}

    # Load existing small_talk.csv data
    with open(existing_filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            small_talk_dict[row['prompt'].lower()] = row['response']

    # Load additional data from new CSV file
    additional_df = pd.read_csv(additional_filename)
    additional_data = dict(zip(additional_df['Question'].str.lower(), additional_df['Answer']))

    # Merge the new small talk data with the existing data
    small_talk_dict.update(additional_data)

    return small_talk_dict

# Handle small talk using fuzzy matching
def handle_small_talk(user_input, small_talk_data, user_name):
    user_input = user_input.lower()
    prompts = list(small_talk_data.keys())
    responses = list(small_talk_data.values())

    tfidf_vectorizer = TfidfVectorizer()
    all_texts = prompts + [user_input]
    vectors = tfidf_vectorizer.fit_transform(all_texts)

    similarity_scores = cosine_similarity(vectors[-1], vectors[:-1])
    most_similar_index = similarity_scores.argmax()
    max_similarity_score = similarity_scores[0, most_similar_index]

    SIMILARITY_THRESHOLD = 0.5  # Adjusted for more inclusiveness
    if max_similarity_score >= SIMILARITY_THRESHOLD:
        return responses[most_similar_index]
    else:
        return "I'm not sure about that, but I can help you with your travel plans!"

# Load the existing small talk and additional data from CSVs
small_talk_data = load_small_talk()

# Example usage
if __name__ == "__main__":
    user_input = "Can you tell me how glacier caves are formed?"
    response = handle_small_talk(user_input, small_talk_data, "John")
    print("Response:", response)
