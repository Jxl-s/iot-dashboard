import os
import smtplib
import imaplib
import time

from email.mime.text import MIMEText

LIGHT_EMAIL_SUBJECT = "IntelliHouse - Light status change"
TEMP_EMAIL_SUBJECT = "IntelliHouse - Temperature is high"


# Just says "Light is ON, Time: hh:mm:ss"
def send_light_email(receiver_email: str):
    my_email = os.environ.get("EMAIL_ADDRESS")
    my_password = os.environ.get("EMAIL_PASSWORD")

    cur_time = time.strftime("%H:%M:%S")
    body = f"Light is ON, Time: {cur_time}"

    msg = MIMEText(body)
    msg["Subject"] = LIGHT_EMAIL_SUBJECT
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
    msg["Subject"] = TEMP_EMAIL_SUBJECT
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
        server.select("INBOX")

        # Search that it's from the receiver
        _, data = server.search(
            None, f'(FROM "{receiver_email}" SUBJECT "{TEMP_EMAIL_SUBJECT}")'
        )

        # Go through, all the received emails. Check if one of them contains YES
        for num in data[0].split():
            _, data = server.fetch(num, "(RFC822)")
            msg = data[0][1].decode("utf-8")

            # Delete the email
            server.store(num, "+FLAGS", "\\Deleted")
            server.expunge()

            # Check if the message contains YES
            if "YES" in msg.upper():
                return True

    return False
