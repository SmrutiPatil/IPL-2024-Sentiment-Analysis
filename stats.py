from collections import Counter
import matplotlib.pyplot as plt
from analysis import tweet_text
import nltk
from nltk import ngrams
from wordcloud import WordCloud


def count_ngrams(text, n):
    words = nltk.word_tokenize(text)  # Tokenize text into words
    ngrams_list = list(ngrams(words, n))  # Generate ngrams of words
    return Counter(ngrams_list)


# Function to plot Rank vs Frequency distribution
def plot_rank_vs_frequency(ngrams, ngram_type):
    sorted_ngrams = sorted(ngrams.items(), key=lambda x: x[1], reverse=True)
    frequencies = [freq for _, freq in sorted_ngrams]
    ranks = range(1, len(frequencies) + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(ranks, frequencies, marker="o", linestyle="-")
    plt.title(f"Rank vs Frequency Distribution for {ngram_type}")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True)
    plt.savefig(f"rank_vs_frequency_{ngram_type}.png")
    plt.show()


# Assuming 'text' contains your data
text = " ".join(
    tweet for tweet in tweet_text
)  # Assuming 'tweet_text' is a list of tweets


# Count unigrams, bigrams, and trigrams
unigrams = count_ngrams(text, 1)
bigrams = count_ngrams(text, 2)
trigrams = count_ngrams(text, 3)


# print("Unigrams:", unigrams)
# Plot Rank vs Frequency distributions
plot_rank_vs_frequency(unigrams, "Unigrams")
plot_rank_vs_frequency(bigrams, "Bigrams")
plot_rank_vs_frequency(trigrams, "Trigrams")
