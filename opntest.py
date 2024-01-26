#!/usr/local/bin/python3
# read_xml.py
import os
import xml.etree.ElementTree as ET

def read_gateway():
    tree = ET.parse('/conf/config.xml')
    root = tree.getroot()

    temp_file = 'temp.txt'
    with open(temp_file, 'w') as f:
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text
            
            # Write each item in the row followed by a comma
            # Write a newline character at the end of each row
            f.write(f"{name},{gateway},{interface}\n")

    # If the existing file is empty, simply rename the temporary file
    if not os.path.exists('output.txt') or os.stat('output.txt').st_size == 0:
        os.rename(temp_file, 'output.txt')
    else:
        # Read the new lines from the temporary file
        with open(temp_file, 'r') as f:
            new_rows = [line.strip() for line in f]

        # Read the existing rows from the output file
        with open('output.txt', 'r') as f:
            existing_rows = {row.split(',')[0]: row for row in f} # Use the 'name' column as the key

        # Merge the new and existing rows, keeping only the rows that exist in both
        merged_rows = [new_row for new_row in new_rows if new_row.split(',')[0] in existing_rows]

        # Write the merged rows back to the output file
        with open('output.txt', 'w') as f:
            for row in merged_rows:
                f.write(row + '\n')

if __name__ == "__main__":
    read_gateway()
