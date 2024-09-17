# Item Finder Script

This Python script reads a list of item names from a file (`find_items.txt`) and searches for their corresponding IDs in a JSON file (`item_names_and_codes.json`). It then writes the found IDs and names to an output file (`found_item_ids.txt`), sorted alphabetically by the item name.

## Features
- Dynamically adjusts file paths to match the current user's home directory.
- Reads a list of items from a plain text file (`find_items.txt`).
- Searches a JSON file for matching item names and retrieves their corresponding IDs.
- Outputs the matching IDs and names to a new file, organized by name in alphabetical order.

## File Structure
- `item_names_and_codes.json`: The JSON file that contains all items and their corresponding IDs.
- `find_items.txt`: The list of item names to search for, one item per line.
- `found_item_ids.txt`: The output file containing the IDs and names of the found items.

### Generating `item_names_and_codes.json`
The `item_names_and_codes.json` file can be generated using the tool available [here](https://github.com/xa-io/ffxiv-tools/blob/main/item_name_id_fetcher.py). This tool fetches item names and their corresponding IDs for Final Fantasy XIV.

## How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/item-finder.git
cd item-finder
