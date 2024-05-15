#!/usr/bin/env python3
from ssh_ids import list_blocked_ips, unblock_ip, start_ids, stop_ids
from colorama import Fore, init
import time
import sys

init(autoreset=True)

def animated_welcome():
    animation_frames = [
        Fore.YELLOW + "Welcome to the SSH-IDS interactive console |",
        Fore.YELLOW + "Welcome to the SSH-IDS interactive console /",
        Fore.YELLOW + "Welcome to the SSH-IDS interactive console -",
        Fore.YELLOW + "Welcome to the SSH-IDS interactive console \\"
    ]

    for frame in animation_frames:
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        time.sleep(0.2)

    ssh_art = Fore.GREEN + '''
      _____    _____   __    __        __   _____      _____
     / ____| / _____| |  |  |  |      |  | |  __ \   / _____|
    | (___  | |_____  |  |__|  |      |  | | |  | | | |_____
     \___ \  \_____ \ |   __   | ---- |  | | |  | |  \ _____ \ 
     ____) |  _____) ||  |  |  |      |  | | |  | |   _____)  |
    |_____/  |______/ |__|  |__|      |__| |_____/   |_______/
    '''
    print(ssh_art)

def display_menu():
    print(Fore.CYAN + "Options:")
    print(Fore.MAGENTA + "[+]1. Start IDS")
    print(Fore.MAGENTA + "[+]2. Unblock IP")
    print(Fore.MAGENTA + "[+]3. List blocked IPs")
    print(Fore.MAGENTA + "[+]4. Exit")

def start_interactive_console():
    animated_welcome()
    while True:
        display_menu()
        choice = input(Fore.CYAN + "Enter your choice: ")
        if choice == "1":
            print(Fore.GREEN + "IDS Started")
            start_ids()
        elif choice == "2":
            ip_to_unblock = input(Fore.YELLOW + "Enter the IP address to unblock: ")
            unblock_ip(ip_to_unblock)
        elif choice == "3":
            print(Fore.GREEN + "Listing blocked IPs...")
            list_blocked_ips()
        elif choice == "4":
            print(Fore.GREEN + "Exiting interactive console.")
            stop_ids()
            break
        else:
            print(Fore.RED + " ")
        time.sleep(2)

if __name__ == "__main__":
    start_interactive_console()
