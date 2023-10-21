import time
import requests

# Note: I made a hosted API to send emails, because it is blocked on the school network
EMAIL_API_URL = "https://iot-email-proxy-aa5866a0f983.herokuapp.com"

LIGHT_EMAIL_SUBJECT = "IntelliHouse - Light status change"
TEMP_EMAIL_SUBJECT = "IntelliHouse - Temperature is high"


class EmailClient:
    def __init__(self, my_email: str, my_password: str):
        self.my_email = my_email
        self.my_password = my_password

    # Sends an email to the receiver
    def send_email(self, receiver_email: str, subject: str, body: str):
        print("[Email]: Sending an email...")

        res = requests.post(
            EMAIL_API_URL + "/sendmail",
            json={
                "auth": {
                    "email": self.my_email,
                    "password": self.my_password,
                    "smtpServer": "smtp.office365.com",
                    "port": 587,
                },
                "message": {
                    "to": receiver_email,
                    "subject": subject,
                    "text": body,
                },
            },
        )

        try:
            res_json = res.json()
        except requests.JSONDecodeError:
            print("[Email] Send Fail: Failed parsing JSON")
            return

        if res.status_code == 200:
            print(f"[Email] Send Success: {res_json['message']}")
        else:
            print(f"[Email] Send Fail: {res_json['message']}")

    # Alerts high temperature, and asks if user wants to turn on the fan
    def send_temp_email(self, receiver_email: str, temp: float, prefered_temp: float):
        body = (
            f"The current temperature is {temp}°C, "
            f"but prefered temperature is {prefered_temp}°C"
            "\n\n"
            "Would you like to turn on the fan? Reply YES or NO"
        )

        self.send_email(receiver_email, TEMP_EMAIL_SUBJECT, body)

    # Checks for a YES response
    def check_temp_res(self, receiver_email: str):
        res = requests.post(
            EMAIL_API_URL + "/readmail",
            json={
                "auth": {
                    "email": self.my_email,
                    "password": self.my_password,
                    "imapServer": "outlook.office365.com",
                    "port": 993,
                },
                "filters": {
                    "from": receiver_email,
                    "subject": TEMP_EMAIL_SUBJECT,
                    "text": "YES",
                },
                "options": {"only_unseen": False, "delete_email": True},
            },
        )

        try:
            res_json = res.json()
        except requests.JSONDecodeError:
            print("[Email] Read Fail: Failed parsing JSON")
            return False

        if res.status_code == 200:
            emails = res_json["emails"]

            if len(emails) > 0:
                print(f"[Email] Read Found: {len(emails)} emails")

            # See if there is a YES reply
            for email in emails:
                if email["text"].startswith("YES"):
                    return True

        return False
