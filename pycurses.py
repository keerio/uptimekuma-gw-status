def get_options_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]

# Get options from file
options = get_options_from_file('options.txt')

# Ask the user to select an option
print("\nPlease select an option:")
for i, option in enumerate(options, start=1):
    print(f"{i}. {option}")

selected_option = int(input()) - 1

# Check if the selected option is valid
if selected_option >= len(options) or selected_option < 0:
    print("Invalid selection. Please try again.")
else:
    # Ask the user to enter a URL for the selected option
    url = input(f"\nPlease enter a URL for {options[selected_option]}: ")
    
    # Store the URL or perform some action with it here
    print(f"\nURL for {options[selected_option]} set to {url}")
