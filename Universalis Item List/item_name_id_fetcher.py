import aiohttp
import asyncio
import json
import os

API_URL_BASE = "https://v2.xivapi.com/api/sheet/Item?fields=Name&after="

async def fetch_items(session, after):
    """
    Fetch a batch of items from XIVAPI v2 using the 'after' parameter.
    Returns parsed JSON data, or None if the request fails.
    """
    url = f"{API_URL_BASE}{after}"
    async with session.get(url) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Failed to fetch items for after={after}. Status code: {response.status}")
            return None

async def main():
    all_items = {}
    after = 0
    step = 100  # We'll fetch 100 items per request

    async with aiohttp.ClientSession() as session:
        while True:
            data = await fetch_items(session, after)

            # If no data or no rows, we're done
            if not data or 'rows' not in data or len(data['rows']) == 0:
                break

            # Each entry in "rows" looks like:
            # {
            #   "row_id": 1,
            #   "fields": {
            #       "Name": "Gil"
            #   }
            # }
            for row in data['rows']:
                row_id = row['row_id']
                name = row['fields'].get('Name', '')
                all_items[row_id] = name

            print(f"Fetched {len(data['rows'])} items (after={after}).")

            # Move to the next batch
            after += step

    # Write the results to a JSON file if we found any items
    if all_items:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'item_names_and_codes.json')

        # Note the ensure_ascii=True for escaped Unicode characters
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(all_items, file, indent=4, ensure_ascii=True)

        print(f"Saved {len(all_items)} items to {file_path}.")
    else:
        print("No items found.")

# Run the script if called directly
if __name__ == "__main__":
    asyncio.run(main())
