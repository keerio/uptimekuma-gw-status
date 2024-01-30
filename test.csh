#!/bin/csh
set gateway_names = `(awk -v FS="," '$4 ~ /./ {print $1}' options.txt | paste -sd ";" -)`
echo $gateway_names
