# This Python script is designed to update specific configuration settings within multiple JSON files.
# It allows users to switch between different configurations (e.g., Dev, Beta, Default) 
# to facilitate testing of plugins for new patches.
# The script searches each JSON file for the specified keys, updates their values based on the chosen configuration, 
# and then saves the changes. Additionally, it logs the changes made to a log.txt file located in the same directory 
# as the script.

# Select the configuration you want to apply by setting the value below.
# Options: "Dev", "Beta", "Default"
selected_config = "Default"  # Modify this to "Dev" or "Beta" as needed

import json
import os

# Define the file paths to the JSON configuration files that need to be updated.
# If you only have one account, remove the two AltData lines below the AppData line, and ensure you also remove the trailing comma.
file_paths = [
    r"C:\Users\username\AppData\Roaming\XIVLauncher\dalamudConfig.json",
    r"C:\Users\username\AltData\launcher1\dalamudConfig.json",
    r"C:\Users\username\AltData\launcher2\dalamudConfig.json"
]


# Define the possible configuration sets with their corresponding keys and values.
configurations = {
    "Dev": {
        "DalamudBetaKey": "warrior_of_light",
        "DalamudBetaKind": "crystalAPI"
    },
    "Beta": {
        "DalamudBetaKey": "moogle_mania",
        "DalamudBetaKind": "kupocloudAPI"
    },
    "Default": {
        "DalamudBetaKey": None,
        "DalamudBetaKind": None
    }
}

# Function to update a JSON file with the selected configuration.
def update_json_file(file_path, config):
    try:
        # Open and read the JSON file.
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Store a copy of the original data for comparison.
        original_data = data.copy()

        # Update the JSON data with the selected configuration.
        data.update(config)

        # Save the updated data back to the file.
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Log the changes made to the file.
        log_changes(file_path, original_data, data)
    
    except Exception as e:
        print(f"Error updating {file_path}: {e}")

# Function to log the changes made to the JSON files.
def log_changes(file_path, original_data, updated_data):
    log_path = os.path.join(os.path.dirname(__file__), 'log.txt')
    with open(log_path, 'a') as log_file:
        log_file.write(f"Changes made to {file_path}:\n")
        for key in updated_data:
            # Check if the value for the key has changed, and log the difference.
            if original_data.get(key) != updated_data.get(key):
                log_file.write(f"  {key}: {original_data.get(key)} -> {updated_data.get(key)}\n")
        log_file.write("\n")

# Iterate through each JSON file and apply the selected configuration.
for path in file_paths:
    update_json_file(path, configurations[selected_config])

# Print a message confirming that the configurations have been updated.
print(f"Configurations updated to {selected_config} keys.")
input("Press Enter to exit...")
