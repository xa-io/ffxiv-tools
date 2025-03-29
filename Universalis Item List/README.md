# FFXIV Item Name ID Fetcher

A Python utility script that fetches all item names and their corresponding IDs from XIVAPI for Final Fantasy XIV, and saves them to a JSON file for easy reference.

## Description

This script connects to the XIVAPI service, retrieves all available items in Final Fantasy XIV, and creates a JSON file mapping item IDs to their names. This can be useful for:

- Creating tools that need to reference FFXIV items by ID
- Data analysis of FFXIV items
- Building integrations with other FFXIV tools and services
- Looking up item IDs without manual searching

## Features

- Asynchronous HTTP requests for efficient data retrieval
- Automatic pagination handling to fetch all available items
- Progress reporting during the fetch process
- Saves results to a JSON file in the same directory as the script

## Requirements

- Tested on Python 3.12.4
- aiohttp
- asyncio

## Installation
1. Install the required dependencies:
   ```
   pip install aiohttp
   ```

## Usage

Simply run the script:

```
python item_name_id_fetcher.py
```

The script will:
1. Connect to XIVAPI
2. Fetch all item data page by page
3. Extract item IDs and names
4. Save the results to `item_names_and_codes.json` in the same directory

## Output

The script generates a JSON file with the following structure:

```json
{
    "1": "Item Name 1",
    "2": "Item Name 2",
    "3": "Item Name 3",
    ...
}
```

Where the keys are item IDs and the values are the corresponding item names.

## Notes

- This script relies on XIVAPI, which may have rate limits or change its API structure over time
- The full dataset may take time to fetch, as FFXIV has thousands of items
