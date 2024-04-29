# Word Analysis of Player Text

from collections import Counter
from analysis import player_text


# Define a set of common stopwords
stopwords = {
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "it",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "should",
    "now",
}


# Function to tokenize text into words and count their occurrences, removing stopwords
def count_words(text):
    words = text.split()  # Split the text into words
    # Filter out stopwords
    words = [word for word in words if word.lower() not in stopwords]
    return Counter(words)  # Count the occurrences of each word


# Dictionary to store word counts for each player
player_word_counts = {}

# Iterate over each player and their associated text
for player, texts in player_text.items():
    # Initialize counter for the player
    player_word_counts[player] = Counter()

    # Iterate over each text associated with the player
    for text in texts:
        # Count words in the text and update player's word count
        player_word_counts[player] += count_words(text)

# Example: Print word counts for each player
for player, word_count in player_word_counts.items():
    print(f"Word counts for {player}:")
    print(word_count)
    print()
