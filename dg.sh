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
    else
        echo "No options selected."
    fi

    # Clean up temporary file
    rm -f tempfile
}

# Read the CSV file and extract options
while IFS=, read -r gateway ip interface fourth_value; do
    # Check if all four options are non-empty
    if [ -n "$gateway" ] && [ -n "$ip" ] && [ -n "$interface" ] && [ -n "$fourth_value" ]; then
        options+=("$gateway" "IP: $ip | Int: $interface" on)
    elif [ -n "$gateway" ] && [ -n "$ip" ] && [ -n "$interface" ]; then
        options+=("$gateway" "IP: $ip | Int: $interface" off)
    fi
done < options.csv

# Display checklist dialog
show_checklist_dialog
