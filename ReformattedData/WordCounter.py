import re
from collections import Counter

def get_top_words(filename):
    with open(filename, 'r') as file:
        # Read the entire file and convert it to lowercase
        text = file.read().lower()

        # Remove punctuation and special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)

        # Split the text into individual words
        words = text.split()

        # Count the occurrences of each word
        word_counts = Counter(words)

        # Get the top 100 most common words
        top_words = word_counts.most_common(1500)

        return top_words

# Specify the path to your text file
filename = 'aaaaaacd.xml'

# Get the top 100 most common words
top_words = get_top_words(filename)

# Print the top words
for word, count in top_words:
    print(word, count)