# SSH-IDS

SSH-IDS (Intrusion Detection System) is a script designed to monitor SSH connection attempts, alert the administrator via email if the number of failed attempts exceeds a threshold, block the offending IP address, and obtain the IP address location using IP2Location.

## Features

- Monitor SSH connection attempts
- Alert admin via email for multiple failed attempts
- Block offending IP addresses
- Obtain location information of the IP address
- Log other events from the auth.log file

##Installation

To install SSH-IDS, clone the repository and the run the setup.py file, after all the installation you can run the console.py (Make sure you are root) to run the IDS.

But, before running the console.py file, there are certain requirements that has to be met:

- First, set the SSH Daemon to VERBOSE, so that we can log the other events from the auth.log file
       Just do sudo nano /etc/ssh/sshd_config and change the LogLevel to VERBOSE and restart the SSH service
- Second, we have to configure Cron to run our temp.sh regularl interval
       Enter this command in your terminal crontab -e and at the end of the script write this line: "*/30 * * * * /home/kali/Project/temp.sh" .
       This tell's cron to run our temp.sh script every 30mins to check for IP's which needs to be unblocked.
