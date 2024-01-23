#!/bin/bash


# Define the CSV file path
csv_file="output.csv"

# Parse the CSV file and extract the first field from each line
# Append " on" if the fourth field is not empty, otherwise append " off"
options=$(awk -F',' '{if ($4 != "") printf "%s \"%s,%s,%s\" on\n", NR, $1,$2,$3; else printf "%s \"%s,%s,%s\" off\n", NR, $1,$2,$3}' "$csv_file")

#options=$(awk -F',' '{if ($4 != "") printf "%s \"%s,%s,%s\" on\n", NR, $1; else printf "%s \"%s\" off\n", NR, $1}' "$csv_file")


#options=$(awk -F',' '{printf "%s \"%s,%s,%s\" on\n", NR, $1,$2,$3}' "$csv_file")



# Create the dialog box
selected_options=$(dialog --clear --backtitle "Select Options" --separate-output --checklist "Enable monitoring:" 15 60 3 $options 2>&1 >/dev/tty)

# Iterate over the selected options
for option in $selected_options; do
    # Get the first field of the selected line
    gw_name=$(awk -v line="$option" -F',' 'NR==line {print $1}' "$csv_file")

    # Get the fourth field of the selected line
    default_value=$(awk -v line="$option" -F',' 'NR==line {print $4}' "$csv_file")

    # Prompt for input
    input=$(dialog --clear --backtitle "Uptime Kuma push URL for $option" --inputbox "Uptime Kuma push URL for $gw_name:" 15 40 "$default_value" 2>&1 >/dev/tty)

    # Store the input as the fourth field of the selected line
    awk -v line="$option" -v input="$input" -F',' 'BEGIN{OFS=FS} NR==line {$4=input} 1' "$csv_file" > temp.csv && mv temp.csv "$csv_file"
done
