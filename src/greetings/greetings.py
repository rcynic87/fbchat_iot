import os
import pytz
import boto3
import fbchat
import random
import pickle
import botocore
from datetime import datetime
from fbchat.models import *
from greeting_messages import GREETINGS


GROUP_MEMBERS = {}
PART_OF_DAY = {
    7: "MORNING",
    8: "MORNING",
    9: "MORNING",
    13: "AFTERNOON",
    14: "AFTERNOON",
    15: "AFTERNOON",
    20: "NIGHT",
    21: "NIGHT",
    22: "NIGHT",
}


def get_group_members():
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=os.getenv('S3_BUCKET'), Key='group_members.pickle')
    response_obj_contents = response.get('Body').read()
    return response_obj_contents


USERNAME = os.getenv('BOT_USER')
PASS = os.getenv('BOT_PASS')
GROUP_ID = os.getenv('GROUP_ID')
try:
    dictionary = get_group_members().strip()
    GROUP_MEMBERS = pickle.loads(dictionary)
except botocore.exceptions.ClientError as s3_error:
    # some access issue, nevermind for locals
    print(s3_error)
    pass


def generate_message(timezone):
    """
    Given a timezone string, find the time of day there and send an appropriate message
    :param timezone:
    :return:
    """
    global GROUP_MEMBERS
    greeting_message = None
    time_of_day = datetime.now(tz=pytz.timezone(timezone))
    print(GROUP_MEMBERS)
    member_name = random.choice(list(GROUP_MEMBERS[timezone]))
    if time_of_day.hour in PART_OF_DAY:
        part_of_day = PART_OF_DAY.get(time_of_day.hour)
        greeting_message = random.choice(list(GREETINGS[part_of_day]))

    if not greeting_message or not member_name:
        print("No greeting for hour {} in {}".format(time_of_day.hour, timezone))
        return None

    text = greeting_message.format(member_name)
    print(text)
    mention = Mention(GROUP_ID, offset=text.index(member_name), length=len(member_name))

    return Message(text=text, mentions=[mention])


def send_greeting(client):
    timezone = random.choice(list(GROUP_MEMBERS.keys()))
    print("Picked {} for timezone".format(timezone))
    message = generate_message(timezone)
    if message:
        client.send(message, thread_id=GROUP_ID, thread_type=ThreadType.GROUP)


def handler(event, context):
    client = fbchat.Client(USERNAME, PASS)
    send_greeting(client)


if __name__ == "__main__":
    # Import this here for local dev/testing
    import group_members
    GROUP_MEMBERS = group_members.GROUP_MEMBERS
    handler(None, None)
