#!/usr/bin/env python3
import IP2Location

database_file = 'IP2LOCATION-LITE-DB3.BIN'
log_file = 'blocked_ips.log'
def get_ip_details(ip):
    database = IP2Location.IP2Location(database_file)
    try:
        record = database.get_all(ip)
        if record is not None:
            return {
                "Country Code": record.country_short,
                "Country Name": record.country_long,
                "Region": record.region,
                "City": record.city,
            }
        else:
            return "IP address not found in database."
    finally:
        database.close()

def read_ips_from_file():
    with open(log_file, 'r') as file:
        ips = [line.split()[0] for line in file if line.strip()]
    return ips

def lookup_ips_from_file():
    ips = read_ips_from_file()
    ip_details = {}
    for ip in ips:
        ip_details[ip] = get_ip_details(ip)
    return ip_details
