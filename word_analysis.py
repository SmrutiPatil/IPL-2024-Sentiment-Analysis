import spacy
import re
from collections import Counter
import matplotlib.pyplot as plt
from analysis import player_text
import numpy as np 
import seaborn as sns

# Load spaCy English tokenizer and stop words
nlp = spacy.load("en_core_web_sm")

def count_words(text):
    # Remove all non-alphanumeric characters except spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize the text into words and filter out stopwords
    doc = nlp(text)
    words = [token.text.lower() for token in doc if not token.is_stop and token.text.isalnum()]
    
    # Count the occurrences of each word
    word_counts = Counter(words)
    
    return word_counts


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

player_name = input("Enter player's name: ")

if player_name in player_word_counts:
    # Get word count for the specified player
    word_count = player_word_counts[player_name]

    # Select top 20 words with highest frequency count
    top_words = dict(word_count.most_common(20))

    # Plot the bar plot for the specified player
    plt.figure(figsize=(10, 6))
    plt.bar(top_words.keys(), top_words.values())  # Plot the bar plot
    plt.xlabel('Word')
    plt.ylabel('Count')
    plt.title(f'Top 20 Words for {player_name}')  # Title includes player's name
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig('bar.png')
    plt.show()    # Rotate x-axis labels for readability
    # Show the plot
    
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(top_words)), list(top_words.values()))  # Plot the scatter plot
    plt.xlabel('Word Index')
    plt.ylabel('Count')
    plt.title(f'Scatter Plot of Word Frequencies for {player_name}')  # Title includes player's name

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig('scatter.png')
    plt.show() 
    # Plot heatmap for the top 20 words
    word_count_list = [word_count[word] for word in top_words]
    word_count_matrix = np.array(word_count_list).reshape(1, -1)

    plt.figure(figsize=(10, 6))
    sns.heatmap(word_count_matrix, cmap="Blues", annot=True, fmt='g', xticklabels=top_words.keys(), yticklabels=False)
    plt.title(f'Top 20 Word Frequencies for {player_name}')  # Title includes player's name
    plt.xlabel('Words')
    plt.ylabel('Player')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability
    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.savefig('heatmap.png')
    plt.show()  # Show the heatmap
else:
    print("Player not found.")
    
count_words(player_text['MS Dhoni'])
