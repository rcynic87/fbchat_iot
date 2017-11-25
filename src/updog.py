import os
import json
import fbchat
import random
import requests
from fbchat.models import *


USERNAME = os.getenv('BOT_USER')
PASS = os.getenv('BOT_PASS')
GROUP_ID = '1484230981612644'
YO_MOMMA_URL = "http://api.yomomma.info"
CHUCK_NORRIS_URL = "http://api.icndb.com/jokes/random"


def get_yo_momma():
    response = requests.get(YO_MOMMA_URL)
    data = json.loads(response.text)
    return data['joke']


def get_chuck_norris():
    response = requests.get(CHUCK_NORRIS_URL)
    data = json.loads(response.text)
    return data['value']['joke']


def get_message():
    response = requests.get(CHUCK_NORRIS_URL)
    data = json.loads(response.text)
    return data['value']['joke']


def send_msg_to_group(client, sources):
    msg = sources.get(random.choice(list(sources.keys())))()
    sent = client.send(Message(text=msg), thread_id=GROUP_ID,
                       thread_type=ThreadType.GROUP)
    if sent:
        print("Message sent successfully!")


def handler(event, context):
    client = fbchat.Client(USERNAME, PASS)
    sources = {YO_MOMMA_URL: get_yo_momma,
               CHUCK_NORRIS_URL: get_chuck_norris}
    send_msg_to_group(client, sources)


if __name__ == "__main__":
    # If we want to test it on the terminal
    handler(None, None)
