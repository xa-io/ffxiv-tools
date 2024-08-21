import aiohttp
import asyncio
import json
import os

# This script fetches all item names and their corresponding IDs from the XIVAPI.
# The process can take several minutes as there are over 40,000 items to retrieve.
# Progress is printed to the console as each page of items is fetched.

# Base URL for the XIVAPI
XIVAPI_BASE_URL = 'https://xivapi.com'
# Endpoint for fetching item data
XIVAPI_ITEMS_URL = f'{XIVAPI_BASE_URL}/Item'

async def fetch_items(page):
    """
    Fetches a page of items from the XIVAPI.

    Args:
        page (int): The page number to fetch.

    Returns:
        dict or None: The JSON response containing item data if successful, None if failed.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{XIVAPI_ITEMS_URL}?page={page}') as response:
            if response.status == 200:
                # Return the JSON response if the request is successful
                return await response.json()
            else:
                # Print an error message if the request fails
                print(f"Failed to fetch items on page {page}. Status code: {response.status}")
                return None

async def main():
    """
    Main function that orchestrates the fetching of all items and saves them to a JSON file.
    """
    all_items = {}  # Dictionary to store all item IDs and names
    page = 1  # Start fetching from the first page

    while True:
        # Fetch the current page of items
        data = await fetch_items(page)
        if not data or 'Results' not in data:
            # Exit the loop if no data is returned or the 'Results' key is missing
            break

        # Store each item ID and name in the all_items dictionary
        for item in data['Results']:
            all_items[item['ID']] = item['Name']

        # Print the progress after each page is fetched
        print(f"Fetched page {page} with {len(data['Results'])} items.")
        page += 1  # Move to the next page

        # Exit the loop if there are no more pages to fetch
        if not data['Pagination']['PageNext']:
            break

    if all_items:
        # Define the path to save the item data
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'item_names_and_codes.json')

        # Save the collected item data to a JSON file
        with open(file_path, 'w') as file:
            json.dump(all_items, file, indent=4)
        print(f"Saved {len(all_items)} items to {file_path}.")
    else:
        # Inform the user if no items were found
        print("No items found.")

# Run the script
asyncio.run(main())
