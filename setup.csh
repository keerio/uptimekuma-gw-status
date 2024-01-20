#!/bin/csh -f

# Make py script executable
chmod +x dpinger-gateway-status.py

# Query
#!/bin/csh -f

# Ask for the number of gateways
echo "How many gateways do you want to monitor? Set number:"
set num = $<

# Initialize empty arrays to store gateway names, URLs, and API calls
set gateway_names = ()
set urls = ()
set api_calls = ()

# Open the file for writing
set fd = `mktemp /tmp/XXXXXX`
cat > $fd <<EOF
Gateway Name,API Call
EOF

# Run a loop as many times as the number entered by the user
@ i = 1
while ($i <= $num)
 echo "Enter gateway #$i name:"
 set gateway_name = $<
 # Append the gateway name to the array
 set gateway_names = ($gateway_names $gateway_name)
 
 echo "Paste Uptime Kuma push URL. Set heartbeat to 20:"
 set uptime_url = $<
 # Append the uptime URL to the array
 set urls = ($urls $uptime_url)
 
 # Parse the URL to get the 'url=' part and '/api/push' part
 set url = `echo $uptime_url | awk -F'/' '{print $3}'`
# Parse the URL to get the part after 'push/' and before '?'
set api_call = `echo $uptime_url | sed 's/\/$//' | awk -F'push/' '{print "push/"substr($2,1,index($2,"?")-1)}'`
 
 # Append the parsed URL and API call to the arrays
 set urls = ($urls $url)
 set api_calls = ($api_calls $api_call)
 
 # Write the gateway name and API call to the file
 echo "$gateway_name,$api_call" >> $fd
 
 @ i += 1
end

# Ask for more inputs
echo "Enter script name (default value: 'uptimekuma-pfsense-gw-status'):"
set script_name = $<
if ("$script_name" == "") then
  set script_name = "uptimekuma-pfsense-gw-status"
endif

echo "Enter script path (default value: '/root/local-scripts/uptimekuma-pfsense-gw-status'):"
set script_path = $<
if ("$script_path" == "") then
  set script_path = "/root/local-scripts/uptimekuma-pfsense-gw-status"
endif

echo "Enter log file (default value: 'uptime-kuma-gateway-status.log'):"
set log_file = $<
if ("$log_file" == "") then
  set log_file = "uptime-kuma-gateway-status.log"
endif

echo "Enter Uptime Kuma gateway dictionary file (default value: 'uptime-kuma-gateway-dictionary.txt'):"
set uptime_kuma_gateway_dictionary = $<
if ("$uptime_kuma_gateway_dictionary" == "") then
  set uptime_kuma_gateway_dictionary = "uptime-kuma-gateway-dictionary.txt"
endif

# Close the file
close $fd

# Rename the temporary file to the final file name
mv $fd $uptime-kuma-gateway-dictionary
