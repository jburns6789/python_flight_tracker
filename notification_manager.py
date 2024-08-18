import os
import vonage
from dotenv import load_dotenv

load_dotenv()


class NotificationManager:

    def __init__(self):
        self.client = vonage.Client(key=os.getenv("VONAGE_KEY"), secret=os.getenv("VONAGE_SECRET"))
        self.sms = vonage.Sms(self.client)

    def send_sms(self, message_body):
        message = self.client.messages.create(
            from_=os.environ["VONAGE_FROM_NUMBER"],
            body=message_body,
            to=os.environ["VONAGE_RECEIVE_NUMBER"]
        )
        # Prints if successfully sent
        print(message.sid)
