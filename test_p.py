import os
import xml.etree.ElementTree as ET
import csv
import sys


def read_gateway():
    tree = ET.parse('config.xml')
    root = tree.getroot()

    temp_file = 'temp.txt'
    options_file = 'options.csv'

    if not os.path.exists(options_file) or os.stat(options_file).st_size == 0:
        open(options_file, 'w').close()
        print ('new options.csv created')

    options = []
        with open("options.csv","rb") as fi:
        reader = csv.reader(fi, delimiter=",")
        for row in reader:
            options.append(row[:3])
    
    xml_reader = []
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text
            # Append the row to the list
            xml_reader.append([name, gateway, interface])
    
    for o in options:
          
    

    with open(options_file, 'w') as f:
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text

            if 
        




    with open(temp_file, 'w') as f:
        for gateway_item in root.iter('gateway_item'):
            interface = gateway_item.find('interface').text
            gateway = gateway_item.find('gateway').text
            name = gateway_item.find('name').text
            
            f.write(f"{name},{gateway},{interface}\n")

    if not os.path.exists('options.txt') or os.stat('options.txt').st_size == 0:
        os.rename(temp_file, 'options.txt')
    else:
        with open(temp_file, 'r') as f:
            new_rows = [line.strip() for line in f]

        with open('options.txt', 'r') as f:
            existing_rows = [tuple(line.strip().split(',')) for line in f]

        rows_to_be_written = []
        for new_row in new_rows:
            if tuple(new_row.split(',')) not in [x[:3] for x in existing_rows]:
                rows_to_be_written.append(new_row)

        with open('options.txt', 'w') as f:
            for row in rows_to_be_written:
                f.write(row + '\n')

def display_menu(options):
    print("\nPlease choose an option:")
    print("No. Name                 Gateway             Interface   Uptime Kuma URL")
    print("------------------------------------------------------------------------")
    for i, option in enumerate(options, start=1):
        values = option[:4] + ['']*(4-len(option))
        print("{:2}. {:<20} {:<20} {:<10} {:<10}".format(i, *values))

def select_option(options):
    while True:
        display_menu(options)
        selected = input("\nEnter the number of your choice or 'q' to quit: ")
        if selected.lower() == 'q':
            print("Exiting... Goodbye!")
            return None
        elif not selected.isdigit() or int(selected) > len(options):
            print("Invalid input. Please try again.")
            continue
        else:
            selected_index = int(selected) - 1
            extra_value = input("Paste Uptime Kuma push URL. Set heartbeat to 20: ")
            if len(options[selected_index]) >= 4:
                options[selected_index][3] = extra_value
            else:
                options[selected_index].append(extra_value)
            return options[selected_index]

if __name__ == "__main__":
    read_gateway()

    while True:
        with open('options.txt', 'r') as file:
            options = [line.strip().split(',') for line in file]
        selected_option = select_option(options)
        if selected_option is None:
            break
        print(f"\nYou have selected: {' '.join(map(str, selected_option))}")
        
        with open('options.txt', 'w') as file:
            for option in options:
                file.write(','.join(option) + '\n')
