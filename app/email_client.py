import os
import smtplib
import imaplib
import time

from email.mime.text import MIMEText
from enum import Enum


class EmailType(Enum):
    LIGHT = 1
    TEMPERATURE = 1


# Just says "Light is ON, Time: hh:mm:ss"
def send_light_email(receiver_email: str):
    my_email = os.environ.get("EMAIL_ADDRESS")
    my_password = os.environ.get("EMAIL_PASSWORD")

    cur_time = time.strftime("%H:%M:%S")
    body = f"Light is ON, Time: {cur_time}"

    msg = MIMEText(body)
    msg["Subject"] = "IntelliHouse - Light status change"
    msg["From"] = my_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(my_email, my_password)
        server.sendmail(my_email, receiver_email, msg.as_string())


# Asks if they want to turn on fans
def send_temp_email(receiver_email: str, temp: float, prefered_temp: float):
    my_email = os.environ.get("EMAIL_ADDRESS")
    my_password = os.environ.get("EMAIL_PASSWORD")

    body = (
        f"The current temperature is {temp}°C, "
        f"but prefered temperature is {prefered_temp}°C"
        "\n\n"
        "Would you like to turn on the fan? Reply YES or NO"
    )

    msg = MIMEText(body)
    msg["Subject"] = "IntelliHouse - Temperature is high"
    msg["From"] = my_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(my_email, my_password)
        server.sendmail(my_email, receiver_email, msg.as_string())


# Check if the user has replied YES
def check_temp_res(receiver_email: str):
    my_email = os.environ.get("EMAIL_ADDRESS")
    my_password = os.environ.get("EMAIL_PASSWORD")

    with imaplib.IMAP4_SSL("outlook.office365.com") as server:
        server.login(my_email, my_password)

        # Check for new emails
        server.select("INBOX")
        _, data = server.search(None, f'(FROM "{receiver_email}")')

        # Go through, all the received emails. Check if one of them contains YES
        for num in data[0].split():
            _, data = server.fetch(num, "(RFC822)")
            msg = data[0][1].decode("utf-8")

            # Delete the email
            server.store(num, "+FLAGS", "\\Deleted")
            server.expunge()

            # Check if the message contains YES
            if "YES" in msg:
                return True

    return False
