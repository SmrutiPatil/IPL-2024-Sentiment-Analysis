# Collecting all data for analysis
# Can find the player names, sentiments, emotions, and text data for each player in the data.

import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from mappings import name_mappings
import spacy
import re
import pandas as pd
import networkx as nx
import seaborn as sns


nlp = spacy.load("en_core_web_sm")


ipl_teams = ["CSK", "DC", "GT", "KKR", "KXIP", "LSG", "MI", "PBKS", "RCB", "RR"]


# Read the JSON data
with open("formatted_data.json", "r") as file:
    data = json.load(file)


def map_name(name):
    if name in name_mappings.keys():
        return name_mappings[name]
    return name


# Fan Loyalty Analysis
tweet = []
team_tweets = {team: [] for team in ipl_teams}
player_sentiments = {}
player_emotions = {}
player_text = {}
unique_player_names = set()
for entry_id, entry_data in data.items():
    # print(entry_id)
    if entry_data is None:
        continue
    tweet.append(entry_data["tweet"])
    tweet_text = entry_data["text"]
    mentioned_teams = [team for team in ipl_teams if team in tweet_text]
    if mentioned_teams:
        for team in mentioned_teams:
            team_tweets[team].append([entry_data["tweet"],tweet_text])
    if "players" not in entry_data:
        continue
    players = entry_data["players"]
    for player in players:
        if "player_name" in player:
            # print(player["player_name"])
            common_name = map_name(player["player_name"])
            unique_player_names.add(common_name)
            player_sentiments[common_name] = player_sentiments.get(common_name, []) + [player["sentiment"]]
            player_emotions[common_name] = player_emotions.get(common_name, []) + [player["emotion"]]
            player_text[common_name] = player_text.get(common_name, []) + [entry_data["text"]]

# Define the sentiments and emotions
sentiments = np.arange(-5, 6)
emotions = [
    "happiness",
    "sadness",
    "joy",
    "hope",
    "anger",
    "neutral",
    "spam",
    "love",
]

# Dictionary to store sentiments and emotions for each team
team_sentiments = {team: [] for team in ipl_teams}
team_emotions = {team: {emotion: 0 for emotion in emotions} for team in ipl_teams}

# Iterate through team tweets and accumulate sentiments and emotions
for team, tweets in team_tweets.items():
    for tweet_data in tweets:
        tweet_text = tweet_data[1]
        sentiments = tweet_data[0].get("sentiment", 0)
        if sentiments in range(-5, 6):
            team_sentiments[team].append(sentiments)
        emotion = tweet_data[0].get("emotion", "")
        if emotion in emotions:
            team_emotions[team][emotion] += 1

def all_emotion():
    # Extract emotions and count their occurrences
    emotion_counts = {}
    for entry in tweet:
        emotion = entry.get("emotion") 
        if emotion is not None and emotion != "spam":
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

    # Plotting the pie chart
    labels = emotion_counts.keys()
    sizes = emotion_counts.values()

    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Emotions Distribution')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('emotion_distribution_all_teams.png')
    plt.show()


def player_vs_sentiment():
    for player, scores in player_sentiments.items():
        player_sentiments[player] = [int(score) for score in scores if score is not None]

    # Calculate the average sentiment score for each player
    average_sentiments = {}
    for player, sentiments in player_sentiments.items():
        print(player, sentiments)
        average_sentiments[player] = sum(sentiments)/ len(sentiments)

    # Sort players by their average sentiment score
    sorted_players = sorted(average_sentiments.items(), key=lambda x: x[1], reverse=True)

    # Extract player names and their corresponding average sentiment scores
    players = [
        player[0]
        for player in sorted_players
        if player[1] > 0 and len(player_sentiments[player[0]]) > 5
    ]
    sentiments = [player[1] for player in sorted_players if player[1] > 0 and len(player_sentiments[player[0]]) > 5]
    
    #Plotting
    plt.figure(figsize=(12, 8))  # Enlarging the figure size
    plt.bar(
        players, sentiments, color="lightblue", edgecolor="grey"
    )  # Adjusting color and edgecolor
    plt.title(
        "Fan Loyalty Analysis", fontsize=16, fontweight="bold"
    )  # Increasing title font size and making it bold
    plt.xlabel("Players", fontsize=12)  # Adjusting label font size
    plt.ylabel("Average Sentiment Score", fontsize=12)  # Adjusting label font size
    plt.xticks(
        rotation=60, ha="right", fontsize=10
    )  # Rotating and adjusting tick labels font size
    plt.yticks(fontsize=10)  # Adjusting y-axis tick labels font size
    plt.grid(
        axis="y", linestyle="--", alpha=0.7
    )  # Adding horizontal grid lines with transparency
    plt.tight_layout()
    plt.savefig('fan_loyalty_analysis.png')
    plt.show()

# player_vs_sentiment()

# word count model
def word_count_per_team(team_name, plot=True, correlation=False):
    def count_words(text):
        # Remove all non-alphanumeric characters except spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

        # Tokenize the text into words and filter out stopwords
        doc = nlp(text)
        words = [token.text.lower() for token in doc if not token.is_stop and token.text.isalnum()]

        # Count the occurrences of each word
        word_counts = Counter(words)

        return word_counts

    team_word_counts = {team: Counter() for team in ipl_teams}

    # Iterate over each team and their associated tweets
    for team, tweets in team_tweets.items():
        # Iterate over each tweet and its text
        for tweet_info in tweets:
            tweet_text = tweet_info[1]  # Extract tweet text from the second index of the tweet_info list

            # Tokenize the text into words and count the occurrences of each word
            word_count = count_words(tweet_text)

            # Update the team's word count
            team_word_counts[team] += word_count
      
    if correlation:
        return team_word_counts      
        

    # Get user input for team name
    # team_name = input("Enter team name: ")
    if team_name in team_word_counts and plot:
        # Get word count for the specified team
        word_count = team_word_counts[team_name]

        # Select top 20 words with highest frequency count
        top_words = dict(word_count.most_common(20))

        # Plot the bar plot for the specified team
        plt.figure(figsize=(10, 6))
        plt.bar(top_words.keys(), top_words.values())  # Plot the bar plot
        plt.xlabel('Word')
        plt.ylabel('Count')
        plt.title(f'Top 20 Words for {team_name}')  # Title includes team's name
        plt.xticks(rotation=45)  # Rotate x-axis labels for readability
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.savefig(f'word_frequency_{team_name}.png')

        # Create heatmap for word frequency
        top_word_count_matrix = np.array(list(top_words.values())).reshape(1, -1)
        plt.figure(figsize=(10, 6))
        sns.heatmap(top_word_count_matrix, cmap="Blues", annot=True, fmt='g', xticklabels=list(top_words.keys()), yticklabels=False)
        plt.title(f'Word Frequency Heatmap for Top 20 Words in {team_name}')
        plt.xlabel('Words')
        plt.ylabel('Team')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.show()  # Show the plots
        
    elif not plot:
        return word_count
    else:
        print("Team not found.")

    # Plot word frequency for the specified team

# word_count_per_team("CSK", plot=False)
# Assuming top_words_team1 and top_words_team2 are dictionaries containing the word frequencies for each team


def plot_word_frequency_heatmap(
    team1_name, team2_name):
    top_words_team1 = word_count_per_team(team1_name, plot=False)
    top_words_team2 = word_count_per_team(team2_name, plot=False)
    # Create matrices for word frequencies of both teams
    team1_word_count_matrix = np.array(list(top_words_team1.values())).reshape(1, -1)
    team2_word_count_matrix = np.array(list(top_words_team2.values())).reshape(1, -1)

    # Create a combined matrix for both teams
    combined_matrix = np.vstack((team1_word_count_matrix, team2_word_count_matrix))

    # Plot the heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        combined_matrix,
        cmap="Blues",
        annot=True,
        fmt="g",
        xticklabels=list(top_words_team1.keys()),
        yticklabels=[team1_name, team2_name],
    )
    plt.title(f"Word Frequency Heatmap for {team1_name} vs {team2_name}")
    plt.xlabel("Words")
    plt.ylabel("Team")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


# Example usage:
# Assuming top_words_csk and top_words_mi are dictionaries containing word frequencies for CSK and MI teams respectively
# plot_word_frequency_heatmap("CSK", "LSG")


# Assuming top_words_dict is a dictionary containing the word frequencies for all teams
def compute_correlation_matrix_all_teams():
    top_words_dict = word_count_per_team("CSK", correlation=True)
    # Convert word frequencies dictionary to DataFrame
    df = pd.DataFrame(top_words_dict)

    # Compute the correlation matrix
    correlation_matrix = df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
    )
    plt.title("Correlation Matrix of Word Frequencies between All Teams")
    plt.xlabel("Teams")
    plt.ylabel("Teams")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('correlation_matrix_all_teams.png')
    plt.show()


# Example usage:
# Assuming top_words_dict is a dictionary where keys are team names and values are dictionaries containing word frequencies for each team
compute_correlation_matrix_all_teams()


def team_vs_emotion_sentiment():

    # Calculate average sentiment score for each team
    team_average_sentiments = {
        team: np.mean(sentiments) for team, sentiments in team_sentiments.items()
    }

    # Average Sentiments
    plt.bar(
        team_average_sentiments.keys(),
        team_average_sentiments.values(),
        color="skyblue",
    )
    plt.title("Average Sentiment Score for IPL Teams")
    plt.xlabel("Teams")
    plt.ylabel("Average Sentiment Score")
    plt.savefig('average_sentiment_score.png')
    plt.show()


def team_vs_emotions(team):
    # Extract emotion counts for the specified team
    team_emotion_counts = [team_emotions[team][emotion] for emotion in emotions]

    # Plotting Pie Chart for Emotions Distribution
    plt.figure(figsize=(8, 8))
    plt.pie(team_emotion_counts, labels=emotions, autopct="%1.1f%%", startangle=140)
    plt.title(f"Emotions Distribution for Team {team}")
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(f"emotions_distribution_{team}.png")
    plt.show()


def team_vs_emotion_sentiment():

    # Calculate average sentiment score for each team
    team_average_sentiments = {
        team: np.mean(sentiments) for team, sentiments in team_sentiments.items()
    }

    # Average Sentiments
    plt.bar(
        team_average_sentiments.keys(),
        team_average_sentiments.values(),
        color="skyblue",
    )
    plt.title("Average Sentiment Score for IPL Teams")
    plt.xlabel("Teams")
    plt.ylabel("Average Sentiment Score")
    plt.show()

def team_network_graph():
    # Create a directed graph
    G = nx.DiGraph()

    # Filter out None values from unique_player_names
    valid_player_names = {name for name in unique_player_names if name}

    # Iterate over each team's tweets
    for team, tweets in team_tweets.items():
        # Count occurrences of each player in the team's tweets
        player_counts = Counter()
        for tweet_data in tweets:
            tweet_text = tweet_data[1]
            # Extract player names from tweet text and count occurrences
            for player in valid_player_names:
                if player in tweet_text:
                    player_counts[player] += 1
        
        # Find the top 5 players with the highest counts for this team
        top_players = [player for player, _ in player_counts.most_common(4)]
        
        # Add nodes for the top 5 players for this team
        G.add_nodes_from(top_players, type='player')

        # Add edges between the team and the top 5 players
        for player in top_players:
            G.add_edge(player, team)

    # Plot the network graph
    plt.figure(figsize=(12, 8))
    pos = nx.fruchterman_reingold_layout(G)

    # Set node colors
    node_colors = ['lightblue' if node in ipl_teams else 'lightgreen' for node in G.nodes()]

    nx.draw(G, pos, with_labels=True, node_size=1000, font_size=12, font_weight='bold', arrowsize=20, node_color=node_colors)
    plt.title('Network Graph Between Top Players and Teams')
    plt.show()


def player_vs_team_heatmap(team_name):
    # Initialize dictionary to store data
    player_counts = Counter()
    unique_player_names = set()
    # team_name = input("Enter the team name: ")
    # Extract player names and count occurrences for the specified team
    for entry_id, entry_data in data.items():
        if entry_data is None:
            continue
        tweet_text = entry_data.get("text", "")
        if team_name in tweet_text:
            if "players" in entry_data:
                players = entry_data["players"]
                for player in players:
                    if "player_name" in player:
                        common_name = map_name(player["player_name"])
                        unique_player_names.add(common_name)
                        player_counts[common_name] += 1

    # Select top 20 players with the highest counts
    top_players = [player for player, count in player_counts.most_common(20)]
    top_player_counts = [player_counts[player] for player in top_players]
    player_counts_matrix = np.array(top_player_counts).reshape(1, -1)
    
    # Plot heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(player_counts_matrix, cmap="Blues", annot=True, fmt='g', xticklabels=top_players, yticklabels=False)
    plt.title(f'Top 20 Player-Team Relationships Heatmap for {team_name}')
    plt.xlabel('Players')
    plt.ylabel('Team')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
