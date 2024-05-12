#!/bin/bash
current_epoch=$(date +%s)
iptables -L INPUT -n --line-numbers | grep 'expire_at_' | while read line; do
    rule_number=$(echo $line | cut -d' ' -f1)
    expire_time=$(echo $line | grep -oP 'expire_at_\K\d+')
    if [ "$current_epoch" -gt "$expire_time" ]; then
        iptables -D INPUT $rule_number
    fi
done
