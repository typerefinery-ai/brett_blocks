#!/usr/bin/env python3
"""
Convert icon_registry.json to CSV format
"""

import json
import csv
import os

def convert_json_to_csv():
    # Define file paths
    json_file = r"c:\projects\brett_blocks\Block_Families\General\_library\icon_registry.json"
    csv_file = r"c:\projects\brett_blocks\Block_Families\General\_library\icon_registry.csv"
    
    try:
        # Read JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Write CSV file
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['icon', 'type', 'protocol'])
            
            # Write data rows
            for item in data:
                writer.writerow([item['icon'], item['type'], item['protocol']])
        
        print(f"Successfully converted {len(data)} records from JSON to CSV")
        print(f"Output file: {csv_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find file {json_file}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    convert_json_to_csv()
