#!/bin/csh

# Add necessary directories to the system path
set path = ($path /bin /sbin /usr/bin /usr/local/bin /usr/local/sbin)

# Check current python version and update dpinger-gateway-status.py

# Step 1: Find Python3 executable in /usr/local/lib
set found = `/usr/bin/find /usr/local/lib -name "python3*" -print | head -1 | xargs -n1 basename`

# Step 2: Create a string "#!/usr/local/bin/" + basename
set shebang="#!/usr/local/bin/$found\n"

# Step 3: Modify file dpinger-gateway-status.py, replace 1st string with output from step 2
sed -i "1c$shebang" dpinger-gateway-status.py

# Set the path of the script and log file path (monitor with: tail -f uptime-kuma-gateway-status.log)
set script_name = 'uptimekuma-pfsense-gw-status'
set script_path = '/root/local-scripts/uptimekuma-pfsense-gw-status'
set log_file = 'uptime-kuma-gateway-status.log'
set is_running = `pgrep -f $script_name`

# Uptime Kuma settings
set uptime_kuma_url = 'http://uptime-kuma.example.com:3001'
set uptime_kuma_gateway_dictionary = 'uptime-kuma-gateway-dictionary.txt'
@ uptime_kuma_heartbeat_interval = 15

# WAN gateway names
set gateway_names = 'WAN_1_DHCP WAN_2_DHCP'

# Gateway health thresholds
@ latency_threshold_warn = 50
@ latency_threshold_error = 100
@ loss_threshold_warn = 5
@ loss_threshold_error = 10

if (! $?is_running) then
        echo "is_running is undefined"
else
        if ("$is_running" == "") then
                echo "is_running is empty"
        else
                echo "Another instance of $script_name is already running"
                exit 1
        endif
endif

# Loop indefinitely
while ( 1 == 1 )
    # Execute dpinger-gateway-status.py and redirect output to a file
    $script_path/dpinger-gateway-status.py > $script_path/dpinger-gateway-status.out

    # Process each WAN interface
    foreach wan ( $gateway_names )
        @ wan_error = 0
        @ wan_warn = 0

        # Initialize variable for message
        set msg = ()

        # Get the Uptime Kuma monitor push ID for the current WAN interface
        set uptime_kuma_monitor_push_id = `grep $wan $script_path/$uptime_kuma_gateway_dictionary | awk '{print $2}'`
        
        # Get the status of the current WAN interface from dpinger-gateway-status.out
        set dpinger_status = `grep $wan $script_path/dpinger-gateway-status.out`
        
        # Extract latency and loss values from dpinger status
        @ latency = `echo $dpinger_status | awk '{print $2}'`
        @ loss = `echo $dpinger_status | awk '{print $3}'`
        
        # Check if latency is above warning threshold
        if ( $latency >= $latency_threshold_warn ) then
            # Check if latency is above error threshold
            if ( $latency >= $latency_threshold_error ) then
                @ wan_error = ${wan_error} + 1
            else
                # Add 'LATENCY' to the message
                set msg = ( $msg 'LATENCY' )
                @ wan_warn = ${wan_warn} + 1
            endif
        endif
        
        # Check if loss is above warning threshold
        if ( $loss >= $loss_threshold_warn ) then
            # Check if loss is above error threshold
            if ( $loss >= $loss_threshold_error ) then
                @ wan_error = ${wan_error} + 1
            else
                # Add 'PACKETLOSS' to the message
                set msg = ( $msg 'PACKETLOSS' )
                @ wan_warn = ${wan_warn} + 1
            endif
        endif
        
        # If there are no warnings, set message to 'OK'
        if ( $wan_warn == 0 ) then
            set msg = ( 'OK' )
        endif

        # If there are no errors, set status to 'up', otherwise set it to 'down'
        if ( $wan_error == 0 ) then
            set gw_status = 'up'
        else
            set gw_status = 'down'
        endif
        
        # Push to Uptime Kuma monitor URL
        set uptime_kuma_monitor_push_result = `curl --insecure --silent "${uptime_kuma_url}/api/push/${uptime_kuma_monitor_push_id}?status=${gw_status}&msg=${msg}&ping=${latency}"`
        
        # Print the gw_status, message, and latency
        set current_datetime = `date +%Y-%m-%d\ %H:%M:%S`
        echo    "Time:    $current_datetime"
        echo    "Gateway: ${wan}"
        echo    "Status:  ${gw_status}"
        echo    "Message: ${msg}"
        echo    "Latency: ${latency}"
        echo    "ApiPush: ${uptime_kuma_monitor_push_result}"
        echo ""
        echo ""

        # Logging
        echo    "Time:    $current_datetime" >> $script_path/$log_file
        echo    "Gateway: ${wan}" >> $script_path/$log_file
        echo    "Status:  ${gw_status}" >> $script_path/$log_file
        echo    "Message: ${msg}" >> $script_path/$log_file
        echo    "Latency: ${latency}" >> $script_path/$log_file
        echo    "ApiPush: ${uptime_kuma_monitor_push_result}" >> $script_path/$log_file
        echo "" >> $script_path/$log_file
        echo "" >> $script_path/$log_file
    end
    echo "------------------------"
    echo "------------------------" >> $script_path/$log_file
    sleep $uptime_kuma_heartbeat_interval
    echo ""
    echo "" > $script_path/$log_file
end
