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
            
            f.write(f"Interface: {interface}, Gateway: {gateway}, Name: {name}\n")

    # Compare the temporary file with the existing file
    existing_names = set()
    if os.path.exists('gateway_status.txt'):
        with open('gateway_status.txt', 'r') as f:
            for line in f:
                existing_names.add(line.strip())

    with open(temp_file, 'r') as f:
        new_lines = [line for line in f]

    with open('gateway_status.txt', 'w') as f:
        for line in new_lines:
            if line.strip() in existing_names:
                f.write(line)

if __name__ == "__main__":
    read_gateway()
