# read_xml.py
import xml.etree.ElementTree as ET

def read_gateway():
    tree = ET.parse('/conf/config.xml')
    root = tree.getroot()

    for gateway_item in root.iter('gateway_item'):
        interface = gateway_item.find('interface').text
        gateway = gateway_item.find('gateway').text
        name = gateway_item.find('name').text
        priority = gateway_item.find('priority').text
        weight = gateway_item.find('weight').text
        ipprotocol = gateway_item.find('ipprotocol').text
        interval = gateway_item.find('interval').text
        descr = gateway_item.find('descr').text
        monitor_disable = gateway_item.find('monitor_disable').text
        monitor = gateway_item.find('monitor').text
        disabled = gateway_item.find('disabled').text
        
        print(f"Interface: {interface}, Gateway: {gateway}, Name: {name}, Priority: {priority}, Weight: {weight}, IP Protocol: {ipprotocol}, Interval: {interval}, Description: {descr}, Monitor Disable: {monitor_disable}, Monitor: {monitor}, Disabled: {disabled}")

if __name__ == "__main__":
    read_gateway()
