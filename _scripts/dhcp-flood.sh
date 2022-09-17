#!/bin/bash

if [ -z "$1" ]; then
     echo "Usage: $0 <interface>"
     exit 1
fi

# fuzz DHCP server
dhcpig -c -v3  -l -a -i -o $interface
