# FFXIV AutoRetainer JSON to Excel Converter

A Python utility that extracts character data from FFXIV's AutoRetainer plugin configuration files and exports it to a well-formatted Excel spreadsheet.

## Overview

This tool parses the `DefaultConfig.json` files created by the AutoRetainer plugin for FFXIV and compiles character information across multiple accounts into a single Excel file. It extracts and organizes:

- Character names, worlds, and gil amounts
- Retainer information (names, gil, market board items, ventures)
- Free Company data (name, points)
- Submarine information (parts configuration, levels)
- Summary statistics across all characters

## Features

- **Multi-account support**: Process data from multiple FFXIV accounts simultaneously
- **Automatic path resolution**: Works regardless of where you run the script from
- **Error handling**: Gracefully handles missing files or parsing errors
- **Timestamp filenames**: Output files include date and time for easy tracking
- **Enhanced Excel formatting**:
  - Multiple sheets for different data views
  - Conditional formatting for easy visual scanning
  - Proper column sizing and header formatting
  - Summary statistics

## Requirements

- Tested on Python 3.12.4
- Required packages:
  - xlsxwriter
  - argparse
  - json

## Installation

1. Install required packages:
   ```
   pip install xlsxwriter
   ```

## Usage

1. Edit the `account_locations` list in the script to match your FFXIV account configuration paths:
   ```python
   account_locations = [
       ("Main", f"C:\\Users\\{user}\\AppData\\Roaming\\XIVLauncher\\pluginConfigs\\AutoRetainer\\DefaultConfig.json"),
       # Add additional accounts as needed
   ]
   ```

2. Run the script:
   ```
   python json_to_excel.py
   ```

3. The output Excel file will be created in the same directory with a timestamp prefix:
   ```
   YYYY-MM-DD-HH-MM - ffxiv_gil_summary.xlsx
   ```

### Summary Sheet

| Metric | Value |
|--------|-------|
| Total Characters | {total_characters} |
| Total Retainers | {total_retainers} |
| Total Gil (All Characters) | {total_gil} |
| Average Gil per Character | {avg_gil_per_char} |
| Richest Character | {richest_character} |
| Richest Character Gil | {richest_character_gil} |
| Total FC's | {total_fcs} |
| Total FC's Farming Subs | {total_farming_subs} |
| Total FC Points | {total_fc_points} |
| Lowest Sub Level | {lowest_sub_level} |
| Highest Sub Level | {highest_sub_level} |
| Unique Submersible Parts | {unique_parts} |
| Submarine Builds | {sub_builds} |
| Build #1 | {build_1} |
| Build #2 | {build_2} |
| Gil Farmed Annually | {annual_gil} |
| Gil Farmed Every 30 Days | {monthly_gil} |
| Gil Farmed Each Day | {daily_gil} |
| Report Generated | {timestamp} |

## Customization

- Modify the `account_locations` list to include your specific account paths
- Adjust Excel formatting in the `write_excel()` function
- Add or modify submarine part definitions in the `SUB_PARTS_LOOKUP` dictionary

## How It Works

1. The script locates and loads the AutoRetainer configuration files for each account
2. It extracts character data, retainer information, and FC data
3. The data is processed and compiled into a standardized format
4. An Excel workbook is created with multiple sheets for different views of the data
5. The final file is saved with a timestamp in the filename

## To-Dos

1. Input other build gil rates into calculations. 

## Acknowledgments

- FFXIV AutoRetainer Puni.sh developers and community
