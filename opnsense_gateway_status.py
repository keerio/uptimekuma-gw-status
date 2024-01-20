#!/usr/local/bin/python3
# read_xml.py
import os
import xml.etree.ElementTree as ET

def read_gateway():
    tree = ET.parse('/path/to/your/config.xml')
    root = tree.getroot()

    temp_file = 'temp.txt'
    with open(temp_file, 'w') as f:
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text
            
            f.write(f"Interface: {interface}, Gateway: {gateway}, Name: {name}\n")

    # If the existing file is empty, simply rename the temporary file
    if not os.path.exists('gateway_status.txt') or os.stat('gateway_status.txt').st_size == 0:
        os.rename(temp_file, 'gateway_status.txt')
    else:
        # Read the new lines from the temporary file
        with open(temp_file, 'r') as f:
            new_lines = [line for line in f]

        # Add the new lines to the existing file
        with open('gateway_status.txt', 'a') as f:
            for line in new_lines:
                f.write(line)

if __name__ == "__main__":
    read_gateway()
