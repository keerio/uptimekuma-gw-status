def display_menu(options):
    print("\nPlease choose an option:")
    for i, option in enumerate(options, start=1):
        print("{:2}. {:<20} {:<20} {:<10}".format(i, *option))

def select_option(options):
    while True:
        display_menu(options)
        selected = input("\nEnter the number of your choice or 'q' to quit: ")
        if selected.lower() == 'q':
            break
        elif not selected.isdigit() or int(selected) > len(options):
            print("Invalid input. Please try again.")
            continue
        else:
            return options[int(selected) - 1]

if __name__ == "__main__":
    with open('options.txt', 'r') as file:
        options = [line.strip().split(',') for line in file]
    selected_option = select_option(options)
    print(f"\nYou have selected: {' '.join(map(str, selected_option))}")
