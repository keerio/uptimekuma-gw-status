#!/usr/local/bin/python3
## read_xml.py
import os
import xml.etree.ElementTree as ET
import csv

def read_gateway():
    tree = ET.parse('/conf/config.xml')
    root = tree.getroot()

    temp_file = 'temp.csv'
    with open(temp_file, 'w', newline='') as f:
        writer = csv.writer(f)
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text
            
            writer.writerow([name, gateway, interface])

    # If the existing file is empty, simply rename the temporary file
    if not os.path.exists('output.csv') or os.stat('output.csv').st_size == 0:
        os.rename(temp_file, 'output.csv')
    else:
        # Read the new lines from the temporary file
        with open(temp_file, 'r') as f:
            reader = csv.reader(f)
            new_rows = [row for row in reader]

        # Read the existing rows from the output file
        with open('output.csv', 'r') as f:
            reader = csv.reader(f)
            existing_rows = {row[0]: row for row in reader} # Use the 'name' column as the key

        # Merge the new and existing rows, keeping only the rows that exist in both
        merged_rows = [new_row for new_row in new_rows if new_row[0] in existing_rows]

        # Write the merged rows back to the output file
        with open('output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(merged_rows)

if __name__ == "__main__":
    read_gateway()
