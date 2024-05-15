import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from location import get_ip_details
import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return {
        'email_address': config['email']['email_address'],
        'email_password': config['email']['email_password'],
        'recipient_email': config['email']['recipient_email'],
        'smtp_server': config['email']['smtp_server'],
        'smtp_port': config['email']['smtp_port']
    }

def notification(ip_address):
    config = load_config()

    SMTP_SERVER = config['smtp_server']
    SMTP_PORT = int(config['smtp_port'])
    EMAIL_ADDRESS = config['email_address']
    EMAIL_PASSWORD = config['email_password']
    RECIPIENT_EMAIL = config['recipient_email']

    ip_info = get_ip_details(ip_address)
    city = ip_info.get("City", "Unknown city")
    region = ip_info.get("Region", "Unknown region")

    subject = f"IP Address {ip_address} Blocked"
    body = f"The IP address {ip_address} has been blocked after exceeding the maximum number of failed login attempts.\n\nLocation: {city}, {region}"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = None
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print("Email notification sent successfully")
    except Exception as e:
        print("Failed to send email notification:", e)
    finally:
        if server:
            server.quit()

if __name__ == "__main__":
    # Example IP address for testing
    notification('1.1.1.1')
