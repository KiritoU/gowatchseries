import json
import requests


class Notification:
    def __init__(self, msg: str):
        self.msg = msg

    def send(self):
        token = "5519686374:AAHuIXSH4luPNkxKX9x3XPwXNqSnyDAMYaU"
        chat_id = "-1001845209436"

        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={self.msg}"

        response = requests.get(url)

        return json.loads(response.text)
