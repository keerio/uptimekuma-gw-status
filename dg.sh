#!/bin/sh

# Function to display dialog for initial choice
show_initial_dialog() {
    dialog --backtitle "Initial Choice" \
           --title "Choose Initial Action" \
           --menu "Select an option:" 12 60 2 \
           1 "Set up Uptime Kuma URL" \
           2 "Select GW to monitor" \
           2>tempfile

    # Check the exit status
    status=$?

    # Read the selected option from the temporary file
    choice=$(cat tempfile)

    # If OK button is pressed and a choice is made
    if [ $status -eq 0 ] && [ ! -z "$choice" ]; then
        case $choice in
            1)
                # Prompt the user to enter Uptime Kuma URL
                uptime_kuma_url=$(dialog --inputbox "Enter Uptime Kuma URL:" 10 40 2>&1 >/dev/tty)

                # Check if the user provided a URL
                if [ -n "$uptime_kuma_url" ]; then
                    # Save the URL to a file (e.g., uptime_kuma_url.txt)
                    echo "$uptime_kuma_url" > uptime_kuma_url.txt
                    echo "Uptime Kuma URL saved to uptime_kuma_url.txt"
                else
                    echo "No URL entered. Exiting."
                    exit 1
                fi
                ;;
            2)
                # Other actions for option 2
                ;;
        esac
    else
        echo "No option selected."
        exit 1
    fi

    # Clean up temporary file
    rm -f tempfile
}

# Initial execution
show_initial_dialog


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
        for choice in $choices; do
            # Prompt the user for additional input for each selected option
            additional_input=$(dialog --inputbox "Enter additional information for $choice:" 10 40 "$default_value" 2>&1 >/dev/tty)
            
            # Process the additional input (you can customize this part)
            echo "Option: $choice, Additional Input: $additional_input"
        done
    else
        echo "No options selected."
    fi

    # Clean up temporary file
    rm -f tempfile
}



# Read the CSV file and extract options based on the user's choice
options=()
default_value=""
while IFS=, read -r gateway ip interface kuma_link; do
    # Check if all four options are non-empty
    if [ -n "$gateway" ] && [ -n "$ip" ] && [ -n "$interface" ] && [ -n "$kuma_link" ]; then
        options+=("$gateway" "IP: $ip | Int: $interface" on)
        default_value="$kuma_link" # Set the default value
    elif [ -n "$gateway" ] && [ -n "$ip" ] && [ -n "$interface" ]; then
        options+=("$gateway" "IP: $ip | Int: $interface" off)
    fi
done < options.csv

# Show initial dialog to get the user's choice
show_initial_dialog
# Display checklist dialog
show_checklist_dialog