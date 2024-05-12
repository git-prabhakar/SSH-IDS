#!/usr/bin/env python3

import subprocess
import re
import time
from email_notify import notification
import threading
from datetime import datetime
import pytz
import os
import logging

attempts_allowed = 2
ssh_log = "/var/log/auth.log"
blocked_ips_file = "blocked_ips.log"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_root():
    if subprocess.check_output(["id", "-u"]).strip() != b"0":
        print("Must be root user")
        exit(1)


def save_last_position(position):
    try:
        with open('last_position.txt', 'w') as f:
            f.write(str(position))
    except IOError as e:
        logging.error(f"Failed to save last position: {e}")


def get_last_position():
    try:
        with open('last_position.txt', 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0


def parse_ssh_log():
    last_position = get_last_position()
    file_size = os.path.getsize(ssh_log)
    if last_position > file_size:
        last_position = 0
    with open(ssh_log, "r") as file:
        file.seek(last_position)
        for line in file:
            if re.search(r'Failed password', line, re.IGNORECASE):
                output = re.findall(r'Failed password.*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line, flags=re.IGNORECASE)
                for ip in output:
                    blacklist(ip, time.time())
            elif "COMMAND=" in line:
                parse_command_entry(line)
        save_last_position(file.tell())


def parse_command_entry(entry):
    # Updated regex pattern to dynamically capture the user before 'sudo:'
    pattern = r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+-\d{2}:\d{2}) (?P<user>\S+) sudo:.+?TTY=(?P<tty>\S+) ; PWD=(?P<pwd>\S+) ; USER=(?P<run_as_user>\w+) ; COMMAND=(?P<command>.*)'
    match = re.search(pattern, entry)
    if match:
        time_stamp = match.group('timestamp')
        user = match.group('user')  # Captures the user dynamically
        pwd = match.group('pwd')
        run_as_user = match.group('run_as_user')
        command = match.group('command')
        command = os.path.basename(command)
        formatted_time_stamp = format_timestamp(time_stamp)
        log_detailed_command(formatted_time_stamp, user, pwd, run_as_user ,command)


def format_timestamp(time_stamp):
    # Parse the timestamp and convert it to a more readable format
    est = pytz.timezone('America/New_York')
    dt = datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%S.%f%z")
    # Convert the timestamp to Eastern Standard Time (EST)
    est_dt = dt.astimezone(est)
    return est_dt.strftime('%Y-%m-%d %H:%M:%S EST')


def log_detailed_command(time_stamp, user, pwd,run_as_user, command):
    log_entry = f"{time_stamp} - User: {user}, PWD: {pwd},Privilege:{run_as_user} , COMMAND: {command}\n"
    with open('detailed_ssh_commands.log', 'a') as log_file:
        log_file.write(log_entry)


def blacklist(ip, current_time):
    count = 0
    with open(ssh_log, "r") as file:
        for line in file:
            if re.search(r'Failed password', line, re.IGNORECASE) and ip in line:
                timestamp_str = re.search(r'^(\S+)', line).group(1)  # Extract timestamp string
                timestamp = time.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%f%z")
                timestamp_epoch = time.mktime(timestamp)
                if current_time - timestamp_epoch <= 60:  # Check if the entry occurred within the last 1 minute
                    count += 1
    if count >= attempts_allowed:
        if ip not in subprocess.check_output(["iptables", "-L", "INPUT", "-n"]).decode():
            expire_time = current_time + 3600  # Expires after 3600 seconds (1 hour)
            print(f"Banning {ip} for 1 hour after {count} failed login attempts")
            subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP", "-m", "comment", "--comment", f"expire_at_{expire_time}"])
            notification(ip)
            log_blocked_ip(ip)


def log_blocked_ip(ip):
    """Log the blocked IP address to a file."""
    with open(blocked_ips_file, "a") as file:
        file.write(f"{ip}\n")


def list_blocked_ips():
    try:
        with open(blocked_ips_file, "r") as file:
            blocked_ips = file.readlines()
            if blocked_ips:
                print("Blocked IP addresses:")
                for ip in blocked_ips:
                    print(ip.strip())
            else:
                print("No IP addresses are currently blocked.")
    except FileNotFoundError:
        print("Blocked IPs file not found.")


def unblock_ip(ip_to_unblock):
    try:
        with open(blocked_ips_file, "r") as file:
            blocked_ips = file.readlines()
        with open(blocked_ips_file, "w") as file:
            for ip in blocked_ips:
                if ip.strip() != ip_to_unblock:
                    file.write(ip)
        # Remove IP from iptables if it exists
        subprocess.run(["iptables", "-D", "INPUT", "-s", ip_to_unblock, "-j", "DROP"])
        print(f"IP address {ip_to_unblock} unblocked successfully.")
    except FileNotFoundError:
        print("Blocked IPs file not found.")


def run_ids():
    global ids_running
    while ids_running:
        parse_ssh_log()
        time.sleep(10)


def start_ids():
    global ids_running
    check_root()
    ids_running = True
    ids_thread = threading.Thread(target=run_ids)
    ids_thread.start()


def stop_ids():
    global ids_running
    ids_running = False