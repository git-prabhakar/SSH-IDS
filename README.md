# SSH-IDS

SSH-IDS (Intrusion Detection System) is a script designed to monitor SSH connection attempts, alert the administrator via email if the number of failed attempts exceeds a threshold, block the offending IP address, and obtain the IP address location using IP2Location.

## Features

- Monitor SSH connection attempts
- Alert admin via email for multiple failed attempts
- Block offending IP addresses
- Obtain location information of the IP address
- Log other events from the `auth.log` file

## Installation

To install SSH-IDS, follow these steps:

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/git-prabhakar/SSH-IDS
    cd SSH-IDS
    ```

2. **Install the Dependencies**:

    ```bash
    sudo python setup.py install
    ```

## Pre-Configuration

Before running the IDS, you need to perform some pre-configuration steps:

1. **Set SSH Daemon to VERBOSE**:

    - Open the SSH daemon configuration file:

      ```bash
      sudo nano /etc/ssh/sshd_config
      ```

    - Change the `LogLevel` to `VERBOSE`:

      ```text
      LogLevel VERBOSE
      ```

    - Restart the SSH service:

      ```bash
      sudo systemctl restart ssh
      ```

2. **Configure Cron Job**:

    - Open the crontab editor:

      ```bash
      crontab -e
      ```

    - Add the following line at the end of the file to run `temp.sh` every 30 minutes:

      ```text
      */30 * * * * /path/to/temp.sh
      ```

    This tells Cron to run `temp.sh` every 30 minutes to check for IP addresses that need to be unblocked.

3. **Add Your Email Configuration**:

    - Populate the file with your email and SMTP server details. You can modify the SMTP server and port as needed. Below is an example configuration (Demo file is there):

    ```ini
    [email]
    sender_email = your_email@example.com
    receiver_email = admin@example.com
    smtp_server = smtp.example.com
    smtp_port = 465
    smtp_user = your_email@example.com
    smtp_password = your_password
    ```

## Running the IDS

To run the interactive console for SSH-IDS, use the following command (make sure you are running as root):

```bash
sudo python3 console.py
```
Or run these two commands:
```bash
sudo su
python3 console.py
```
