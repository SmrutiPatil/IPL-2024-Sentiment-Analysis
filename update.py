# Modifying formulated_data.json

import json
from mappings import name_mappings


# Read the original JSON data
with open("formatted_data.json", "r") as file:
    data = json.load(file)


# Function to map player names
def map_name(name):
    return name_mappings.get(
        name, name
    )  # Return the mapped name, or original name if not found


# Update player names in the data
for entry_id, entry_data in data.items():
    if entry_data is None:
        continue
    if "players" in entry_data:
        players = entry_data["players"]
        for player in players:
            if "player_name" in player:
                entry_data["players"] = [
                    {"player_name": map_name(player["player_name"]),
                     "sentiment": player["sentiment"],
                     "emotion": player["emotion"]}
                    for player in entry_data["players"]
                ]

# Write the updated data back to the JSON file
with open("formatted_data_updated.json", "w") as file:
    json.dump(data, file, indent=4)
