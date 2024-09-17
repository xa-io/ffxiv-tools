import json
import os

# Get the current logged-in user's username
username = os.getlogin()

# Paths to the necessary files, using the dynamically fetched username
json_file_path = fr"C:\Users\{username}\Desktop\Projects\python\item_finder\item_names_and_codes.json"
find_items_file_path = fr"C:\Users\{username}\Desktop\Projects\python\item_finder\find_items.txt"
output_file_path = fr"C:\Users\{username}\Desktop\Projects\python\item_finder\found_item_ids.txt"

# Read the items to find from the find_items.txt file
with open(find_items_file_path, 'r', encoding='utf-8') as f:
    items_to_find = [line.strip() for line in f.readlines()]

# Load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# List to store found items (as tuples of ID and name)
found_items = []

# Loop through the JSON data (keys are IDs, values are item names)
for item_id, item_name in data.items():
    if item_name in items_to_find:
        found_items.append((item_id, item_name))

# Sort the items alphabetically by name (A-Z)
found_items_sorted = sorted(found_items, key=lambda x: x[1])

# Output the list of found IDs and names to a file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for item_id, item_name in found_items_sorted:
        output_file.write(f"{item_id}\t{item_name}\n")

print(f"Found item IDs and names have been written to {output_file_path}")
