import os
import xml.etree.ElementTree as ET
import csv

def write_gateway(rows):
    with open('options.csv', 'w') as f:
        writer = csv.writer(f, delimiter=",")
        for row in rows:
            writer.writerow(row)


def compare_gateway(options, xml_reader):
    
    options_file = 'options.csv'
    if os.stat(options_file).st_size == 0:
        write_gateway(xml_reader)
        print("Filled the csv with init data")

    for option in options:
        for xreader in xml_reader:
            if option == xreader:
                print(f"Match found: {option}")
            else:
                print(f"No match found for: {option}")

def read_xml():
    tree = ET.parse('config.xml')
    root = tree.getroot()
    xml_reader = []
    for gateway_item in root.iter('gateway_item'):
        interface = gateway_item.find('interface').text
        gateway = gateway_item.find('gateway').text
        name = gateway_item.find('name').text
        # Append the row to the list
        xml_reader.append([name, gateway, interface]) 
    return (xml_reader)
    
def read_options():
    options = []
    with open("options.csv","r") as fi:
        reader = csv.reader(fi, delimiter=",")
        for row in reader:
            options.append(row[:3]) # Appends the first three elements of each row
        return(options)

def check_file():
    options_file = 'options.csv'
    if not os.path.exists(options_file) or os.stat(options_file).st_size == 0:
        open(options_file, 'w').close()

        print ('new options.csv created')


# def read_gateway():
#     tree = ET.parse('config.xml')
#     root = tree.getroot()

#     temp_file = 'temp.txt'
#     options_file = 'options.csv'

#     if not os.path.exists(options_file) or os.stat(options_file).st_size == 0:
#         open(options_file, 'w').close()

#         print ('new options.csv created')

#     options = []
#     with open("options.csv","r") as fi:
#         reader = csv.reader(fi, delimiter=",")
#         for row in reader:
#             options.append(row[:3]) # Appends the first three elements of each row
        
#     xml_reader = []
#     for gateway_item in root.iter('gateway_item'):
#         interface = gateway_item.find('interface').text
#         gateway = gateway_item.find('gateway').text
#         name = gateway_item.find('name').text
#         # Append the row to the list
#         xml_reader.append([name, gateway, interface])
    
#     return (options, xml_reader)
# def dialog_menu():
            
#     import locale
#     from dialog import Dialog

#     # This is almost always a good thing to do at the beginning of your programs.
#     locale.setlocale(locale.LC_ALL, '')

#     # You may want to use 'autowidgetsize=True' here (requires pythondialog >= 3.1)
#     d = Dialog(dialog="dialog")
#     # Dialog.set_background_title() requires pythondialog 2.13 or later
#     d.set_background_title("My little program")
#     # For older versions, you can use:
#     #   d.add_persistent_args(["--backtitle", "My little program"])

#     # In pythondialog 3.x, you can compare the return code to d.OK, Dialog.OK or
#     # "ok" (same object). In pythondialog 2.x, you have to use d.DIALOG_OK, which
#     # is deprecated since version 3.0.0.
#     if d.yesno("Are you REALLY sure you want to see this?") == d.OK:
#         d.msgbox("You have been warned...")

#         # We could put non-empty items here (not only the tag for each entry)
#         code, tags = d.checklist("What sandwich toppings do you like?",
#                                 choices=[("Catsup", "",             False),
#                                         ("Mustard", "",            False),
#                                         ("Pesto", "",              False),
#                                         ("Mayonnaise", "",         True),
#                                         ("Horse radish","",        True),
#                                         ("Sun-dried tomatoes", "", True)],
#                                 title="Do you prefer ham or spam?",
#                                 backtitle="And now, for something "
#                                 "completely different...")
#         if code == d.OK:
#             # 'tags' now contains a list of the toppings chosen by the user
#             pass
#     else:
#         code, tag = d.menu("OK, then you have two options:",
#                         choices=[("(1)", "Leave this fascinating example"),
#                                     ("(2)", "Leave this fascinating example")])
#         if code == d.OK:
#             # 'tag' is now either "(1)" or "(2)"
#             pass

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

def main():
    # Check if csv exist
    check_file()

    dialog_menu()

    # Read CSV and XML
    options = read_options()
    xml_reader = read_xml()

    print("OPTIONS------------------")
    print (options)
    print("XML----------------------")
    print (xml_reader)
    

    # Compare CSV and XML
    compare_gateway(options, xml_reader)

    while True:
        with open('options.csv', 'r') as fi:
            reader = csv.reader(fi, delimiter=",")
            menu_options = [row for row in reader]
        selected_option = select_option(menu_options)
        if selected_option is None:
            break
        print(f"\nYou have selected: {' '.join(map(str, selected_option))}")
        
        with open('options.csv', 'w') as file:
            writer = csv.writer(file, delimiter=",")
            for option in menu_options:
                writer.writerow(option)

if __name__ == "__main__":
    main()
