#!/bin/csh -f

# Add necessary directories to the system path
set path = ($path /bin /sbin /usr/bin /usr/local/bin /usr/local/sbin /usr/local/)

chmod +x opnsense_gateway_status.py

set output = `python3 opnsense_gateway_status.py`

#echo $output

set i = 1
while ($i <= `cat output.csv | wc -l`)
    set row = `sed -n "${i}p" output.csv`
    echo "${i}: $row"
    @ i++
end
