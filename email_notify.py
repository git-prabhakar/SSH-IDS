import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from location import get_ip_details

def notification(ip_address):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465  # SSL port
    EMAIL_ADDRESS = 'your_email'
    EMAIL_PASSWORD = 'your_password'
    RECIPIENT_EMAIL = 'recv_email'

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
