import smtplib
import imaplib
import email

from email.mime.text import MIMEText

LIGHT_EMAIL_SUBJECT = "IntelliHouse - Light status change"
TEMP_EMAIL_SUBJECT = "IntelliHouse - Temperature is high"


class EmailClient:
    def __init__(self, my_email: str, my_password: str):
        self.my_email = my_email
        self.my_password = my_password

    # Sends an email to the receiver
    def send_email(self, receiver_email: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.my_email
        msg["To"] = receiver_email

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(self.my_email, self.my_password)
            server.sendmail(self.my_email, receiver_email, msg.as_string())

    # Alerts high temperature, and asks if user wants to turn on the fan
    def send_temp_email(self, receiver_email: str, temp: float, prefered_temp: float):
        body = (
            f"The current temperature is {temp}°C, "
            f"but prefered temperature is {prefered_temp}°C"
            "\n\n"
            "Would you like to turn on the fan? Reply with YES"
        )

        self.send_email(receiver_email, TEMP_EMAIL_SUBJECT, body)

    def check_temp_res(self, receiver_email: str):
        with imaplib.IMAP4_SSL("outlook.office365.com") as server:
            server.login(self.my_email, self.my_password)
            server.select("INBOX")

            # Search that it's from the receiver
            _, data = server.search(
                None, f'(FROM "{receiver_email}" SUBJECT "{TEMP_EMAIL_SUBJECT}")'
            )

            # Go through, all the received emails. Check if one of them contains YES
            for num in data[0].split():
                _, data = server.fetch(num, "(RFC822)")
                msg = data[0][1]

                body = str(EmailClient.get_email_body(msg))

                # Delete the email
                server.store(num, "+FLAGS", "\\Deleted")

                # Check if the message contains YES
                if body.startswith("YES"):
                    server.expunge()
                    server.logout()

                    return True

            server.expunge()
            server.logout()

        return False

    def get_email_body(mail):
        body = ""
        msg = email.message_from_bytes(mail, policy=email.policy.default)
        body = msg.get_body(("plain",))
        if body:
            body = body.get_content()
        return body
