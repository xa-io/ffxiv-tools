r"""
Script: FFXIV Character Folder Template Importer

Purpose:
This script scans the 'FINAL FANTASY XIV - A Realm Reborn' directory for folders named 
'FFXIV_CHRxxxxxx' and checks their creation dates. If any folders are found with a creation 
date newer than a specified date, the script lists those folders and prompts the user to 
import a 'character template' into them.

Usage:
1. **Configuration**:
   - Set the `set_date` variable to the desired date. Any folders created after this date 
     will be listed.
   - The script dynamically pulls the current logged-in username to ensure it works on 
     any machine. Make sure the directory structure is correct.

2. **Running the Script**:
   - Execute the script. It will scan the directory for matching FFXIV_CHR folders.
   - If matching folders are found, the script will display the number of matches and 
     their folder names.
   - The script will then prompt you to decide whether to import the 'character template' 
     into these folders.

3. **User Interaction**:
   - **y** (yes): The contents of the 'character template' folder will be copied into each 
     matching FFXIV_CHRxxxxxx folder, overwriting any existing files.
   - **n** (no): The script will exit without making any changes.

4. **Notes**:
   - The script will only copy the contents of the 'character template' folder, not the folder 
     itself, into the matching FFXIV_CHRxxxxxx folders.
   - The script will stop if there are no matching folders or if the user chooses not to 
     import the template.

5. **Directory Structure**:
   - Ensure the following structure:
     C:\Users\YourUsername\Documents\My Games\FINAL FANTASY XIV - A Realm Reborn
     ├── FFXIV_CHRxxxxxx (Character folders)
     └── character template (Folder containing the template files to be imported)

"""

import os
import shutil
from datetime import datetime

# Configuration
username = os.getlogin()  # Get the current logged-in username
base_dir = fr"C:\Users\{username}\Documents\My Games\FINAL FANTASY XIV - A Realm Reborn"
character_template_dir = os.path.join(base_dir, "character template")
set_date = datetime(2024, 9, 1)  # Set your desired date here

# Function to check the creation date of the folders
def check_folder_dates(base_dir, set_date):
    matching_folders = []
    for folder_name in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder_name)
        if os.path.isdir(folder_path) and folder_name.startswith("FFXIV_CHR"):
            creation_time = os.path.getctime(folder_path)
            creation_date = datetime.fromtimestamp(creation_time)
            if creation_date > set_date:
                matching_folders.append(folder_name)
    return matching_folders

# Function to copy character template files to the matching folders
def copy_character_template(matching_folders):
    for folder_name in matching_folders:
        target_folder = os.path.join(base_dir, folder_name)
        for item in os.listdir(character_template_dir):
            s = os.path.join(character_template_dir, item)
            d = os.path.join(target_folder, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

# Main script
matching_folders = check_folder_dates(base_dir, set_date)

if matching_folders:
    print(f"{len(matching_folders)} folders match your preferences")
    for folder_name in matching_folders:
        print(folder_name)

    response = input("Do you want to import the character template? (y/n): ").strip().lower()
    if response == 'y':
        copy_character_template(matching_folders)
        print("character template has been successfully imported.")
    else:
        print("Operation canceled.")
else:
    print("No folders match your preferences.")
