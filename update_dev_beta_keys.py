# This Python script is designed to update specific configuration settings within multiple JSON files.
# It allows users to switch between different configurations (e.g., Dev, Beta, Default) 
# to facilitate testing of plugins for new patches.
# The script searches each JSON file for the specified keys, updates their values based on the chosen configuration, 
# and then saves the changes. Additionally, it logs the changes made to a log.txt file located in the same directory 
# as the script.

import json
import os
import requests

# Select the configuration you want to apply by setting the value below.
# Options: "Dev", "Beta", "Default"
selected_config = "Default"  # Modify this to "Dev", "Beta", or "Default" as needed

# Define the URL for fetching the latest configuration data
config_url = "https://kamori.goats.dev/Dalamud/Release/Meta"

# Define the file paths
file_paths = [
    r"C:\Users\username\AppData\Roaming\XIVLauncher\dalamudConfig.json",
    r"C:\Users\username\AltData\launcher1\dalamudConfig.json",
    r"C:\Users\username\AltData\launcher2\dalamudConfig.json"
]

# Function to fetch and parse the latest configurations from the URL
def fetch_configurations(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch configuration from {url}")

# Fetch the latest configuration data
latest_configs = fetch_configurations(config_url)

# Map the selected configuration to the appropriate section in the JSON data
config_map = {
    "Dev": {
        "DalamudBetaKey": latest_configs.get("api11", {}).get("key"),
        "DalamudBetaKind": latest_configs.get("api11", {}).get("track")
    },
    "Beta": {
        "DalamudBetaKey": latest_configs.get("stg", {}).get("key"),
        "DalamudBetaKind": latest_configs.get("stg", {}).get("track")
    },
    "Default": {
        "DalamudBetaKey": None,
        "DalamudBetaKind": None
    }
}

# Select the appropriate configuration based on user selection
selected_data = config_map.get(selected_config, config_map["Default"])

# Function to log errors
def log_error(file_path, error_message):
    log_path = os.path.join(os.path.dirname(__file__), 'log.txt')
    with open(log_path, 'a') as log_file:
        log_file.write(f"Error updating {file_path}: {error_message}\n")

# Function to update a JSON file with the selected configuration.
def update_json_file(file_path, config):
    try:
        # Open and read the JSON file.
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load the JSON content

        # Store a copy of the original data for comparison.
        original_data = data.copy()

        # Update the JSON data with the selected configuration.
        data.update(config)

        # Save the updated data back to the file.
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        # Log the changes made to the file.
        log_changes(file_path, original_data, data)
    
    except json.JSONDecodeError as e:
        error_message = f"JSONDecodeError: {str(e)}"
        log_error(file_path, error_message)
        print(f"Error decoding JSON in {file_path}: {e}")
    except Exception as e:
        error_message = str(e)
        log_error(file_path, error_message)
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
    update_json_file(path, selected_data)

# Print a message confirming that the configurations have been updated.
updated_config = ', '.join([f'{key}: {value}' for key, value in selected_data.items()])
print(f"Configurations updated to {selected_config} keys: {updated_config}.")
input("Press Enter to exit...")
