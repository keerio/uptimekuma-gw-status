import os

def get_options_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip().split(',') for line in f]

# Get options from file
options = get_options_from_file('options.txt')

# Ask the user to select an option
print("\n\033[1mAvailable Options:\033[0m")
for i, option in enumerate(options, start=1):
    if len(option) > 3 and option[3]:
        print(f"\033[92m{i}. {option[0].capitalize()}\033[0m") # Green
    else:
        print(f"\033[93m{i}. {option[0].capitalize()}\033[0m") # Yellow

print("\nEnter the number associated with your choice:")
selected_option = int(input()) - 1

# Check if the selected option is valid
if selected_option >= len(options) or selected_option < 0:
    print("\n\033[91mInvalid selection. Please try again.\033[0m")
else:
    # Ask the user to enter a URL for the selected option
    print("\n\033[1mPlease enter a URL for \033[93m{}:\033[0m".format(options[selected_option][0].capitalize()))
    url = input()
    
    # Store the URL or perform some action with it here
    print("\n\033[1mURL for {} set to {}\033[0m".format(options[selected_option][0].capitalize(), url))
