#!/bin/bash

# Function to display dialog with checklist
show_checklist_dialog() {
    dialog --backtitle "Checklist Example" \
           --title "Choose options" \
           --checklist "Select one or more options:" 40 80 4 \
           "${options[@]}" \
           2>tempfile

    # Check the exit status
    status=$?

    # Read the selected options from the temporary file
    choices=$(cat tempfile)

    # If OK button is pressed and choices are made
    if [ $status -eq 0 ] && [ ! -z "$choices" ]; then
        echo "Selected options: $choices"
        prompt_for_values "$choices"
    else
        echo "No options selected."
    fi

    # Clean up temporary file
    rm -f tempfile
}

# Function to prompt for input values for selected options
prompt_for_values() {
    selected_options=($1)
    for option in "${selected_options[@]}"; do
        gateway=$(echo "$option" | cut -d" " -f1)
        ip_interface=$(echo "$option" | cut -d" " -f3-)
        default_value=$(get_default_value "$gateway") # Get the existing fourth value as default
        read -p "Enter fourth value for $gateway ($ip_interface) [Default: $default_value]: " user_input
        fourth_value=${user_input:-$default_value} # Use the default if the user enters nothing
        echo "$gateway,$ip_interface,$fourth_value" >> updated_options.csv
    done
}

# Function to get the existing fourth value for a gateway (from the original CSV)
get_default_value() {
    grep "^$1," options.csv | cut -d, -f4
}

# Read the CSV file and extract options
while IFS=, read -r gateway ip interface fourth_value; do
    # Check if all four options are non-empty
    if [ -n "$gateway" ] && [ -n "$ip" ] && [ -n "$interface" ]; then
        options+=("$gateway" "IP: $ip | Int: $interface" $(get_default_value "$gateway"))
    fi
done < options.csv

# Display checklist dialog
show_checklist_dialog
