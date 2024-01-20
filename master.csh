#!/bin/csh -f

# Add necessary directories to the system path
set path = ($path /bin /sbin /usr/bin /usr/local/bin /usr/local/sbin /usr/local/)

# Check current python version and update py scripts

# Step 1: Find Python3 executable in /usr/local/lib
#set found = `/usr/bin/find /usr/local/lib -name "python3*" -print | head -1 | xargs -n1 basename`
#set found = `/usr/bin/find /usr/local/bin -name "python3*" -print | head -1 | xargs -n1 basename`


# Step 2: Create a string "#!/usr/local/bin/" + basename
#set shebang="#!/usr/local/bin/$found\n"

# Step 3: Modify file dpinger-gateway-status.py, replace 1st string with output from step 2
#sed -i "1c$shebang" dpinger-gateway-status.py
#sed -i "1c$shebang" opnsense_gateway_status.py

chmod +x opnsense_gateway_status.py

set output = `python3 opnsense_gateway_status.py`
echo $output

# $script_path/dpinger-gateway-status.py > $script_path/dpinger-gateway-status.out
#!/bin/csh -f
set i = 1
while ($i <= `cat output.csv | wc -l`)
    set row = `sed -n "${i}p" output.csv`
    echo "${i}: $row"
    @ i++
end
echo "Please enter the number of the row you want to select:"
set selection = "$<"

# Try to subtract one from the selection
set test = `expr $selection - 1`

# Check if the subtraction resulted in a number
if ("$test" != "") then
    # Convert the selection to a number
    set selection = `expr $selection + 0`
    echo "You selected row $selection"
else
    echo "Invalid input. Please enter a digit."
endif

