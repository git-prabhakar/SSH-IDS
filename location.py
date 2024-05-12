#!/usr/bin/env python3
import IP2Location

database_file = 'IP2LOCATION-LITE-DB3.BIN'
log_file = 'blocked_ips.log'
def get_ip_details(ip):
    """Fetch details for a given IP using the specified database."""
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
    """Read IP addresses from the predefined log file and return them as a list."""
    with open(log_file, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips if ip.strip()]

def lookup_ips_from_file():
    """Perform geolocation lookups for each IP read from the predefined log file."""
    ips = read_ips_from_file()
    ip_details = {}
    for ip in ips:
        ip_details[ip] = get_ip_details(ip)
    return ip_details