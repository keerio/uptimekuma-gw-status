#!/usr/local/bin/python3
# read_xml.py
import xml.etree.ElementTree as ET

def read_gateway():
    tree = ET.parse('/conf/config.xml')
    root = tree.getroot()

    for gateway_item in root.iter('gateway_item'):
        interface = gateway_item.find('interface').text
        gateway = gateway_item.find('gateway').text
        name = gateway_item.find('name').text
        
        print(f"Interface: {interface}, Gateway: {gateway}, Name: {name}")

if __name__ == "__main__":
    read_gateway()
