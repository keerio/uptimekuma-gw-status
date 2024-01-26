#!/usr/bin/env bash

# Add necessary directories to the system path
set path = ($path /bin /sbin /usr/bin /usr/local/bin /usr/local/sbin /usr/local/)

chmod +x opnsense_gateway_status.py
chmod +x dpinger-gateway-status.py

set output = `python3 opnsense_gateway_status.py`

echo $output