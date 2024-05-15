#!/bin/bash

current_epoch=$(date +%s)

iptables -L INPUT -n --line-numbers | grep 'expire_at_' | while read -r line; do
    line_number=$(echo "$line" | awk '{print $1}')
    ip_address=$(echo "$line" | awk '{print $4}')
    expire_time=$(echo "$line" | grep -oP 'expire_at_\K\d+')

    if [ "$current_epoch" -gt "$expire_time" ]; then
        iptables -D INPUT $line_number
        echo "Removed expired rule for IP $ip_address on line $line_number with expiration at $expire_time"
    fi
done
