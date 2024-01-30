#!/usr/local/bin/python3
# read_xml.py
import os
import xml.etree.ElementTree as ET
def read_gateway():
    tree = ET.parse('config.xml')
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
    if not os.path.exists('options.txt') or os.stat('options.txt').st_size == 0:
        os.rename(temp_file, 'options.txt')
    else:
        # Read the new lines from the temporary file
        with open(temp_file, 'r') as f:
            new_rows = [line.strip() for line in f]

        # Read the existing rows from the output file
        with open('options.txt', 'r') as f:
            existing_rows = {tuple(line.strip().split(',')) for line in f} # Strip the newline characters before splitting

        # Check if each new row is in the set of existing rows
        # If it's not, add it to the list of rows to be written
        rows_to_be_written = []
        for new_row in new_rows:
            if tuple(new_row.split(',')) not in existing_rows:
                rows_to_be_written.append(new_row)

        # Write the rows to be written back to the output file
        with open('options.txt', 'a') as f:
            for row in rows_to_be_written:
                f.write(row + '\n')

def display_menu(options):
    print("\nPlease choose an option:")
    print("No. Name                 Gateway             Interface   Uptime Kuma URL")
    print("------------------------------------------------------------------------")
    for i, option in enumerate(options, start=1):
        # Get the four values. If there's no fourth value, replace it with an empty string
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
        
        # Write the updated options back to the file
        with open('options.txt', 'w') as file:
            for option in options:
                file.write(','.join(option) + '\n')