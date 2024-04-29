# Collecting all data for analysis
# Can find the player names, sentiments, emotions, and text data for each player in the data.

import json
import matplotlib.pyplot as plt

from mappings import name_mappings

# Read the JSON data
with open("formatted_data.json", "r") as file:
    data = json.load(file)


def map_name(name):
    if name in name_mappings.keys():
        return name_mappings[name]
    return name

def save_output(my_set, filename):
    with open(filename, "w", encoding="utf-8") as file:
        for item in my_set:
            file.write(str(item) + "\n")
    print(f"Set saved to {filename}")


# Fan Loyalty Analysis
tweet = []
player_sentiments = {}
player_emotions = {}
player_text = {}
unique_player_names = set()
for entry_id, entry_data in data.items():
    # print(entry_id)
    if entry_data is None:
        continue
    tweet = entry_data["tweet"]
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
            # print(player["player_name"], common_name)
            # unique_player_names.add(player["player_name"])
            # print(player["player_name"])

# for player in unique_player_names:
#     print(player)
# print(player_sentiments)
# print(player_emotions)

# print(player_emotions)



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

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(players, sentiments, color="skyblue")
    plt.title("Fan Loyalty Analysis")
    plt.xlabel("Players")
    plt.ylabel("Average Sentiment Score")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    
# player_vs_sentiment()