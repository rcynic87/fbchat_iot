import json
import random
import requests
import time
from PIL import Image, ImageDraw, ImageFont


YO_MOMMA_URL = "http://api.yomomma.info"
CHUCK_NORRIS_URL = "http://api.icndb.com/jokes/random"


def get_yo_momma():
    response = requests.get(YO_MOMMA_URL, timeout=10)
    data = json.loads(response.text)
    return data['joke']


def get_chuck_norris():
    response = requests.get(CHUCK_NORRIS_URL, timeout=10)
    data = json.loads(response.text)
    return data['value']['joke']


def get_message():
    response = requests.get(CHUCK_NORRIS_URL)
    data = json.loads(response.text)
    return data['value']['joke']


def generate_image(choice, msg):
    if choice == YO_MOMMA_URL:
        image = Image.open("yomamma.jpg")
        xy = (0, 235)  # this was found manually
    elif choice == CHUCK_NORRIS_URL:
        image = Image.open("chucknorris.jpg")
        xy = (0, 25)  # this was found manually
    fnt = ImageFont.truetype('Xpressive Bold.ttf', 20)

    draw = ImageDraw.Draw(image)
    for line in msg.split(","):
        draw.text(xy, line, (255, 255, 255), font=fnt)
        new_y = xy[1] + 20
        xy = (xy[0], new_y)
    output_filename = "/tmp/{}.jpg".format(int(time.time()))
    image.save(output_filename)
    return output_filename


def send_msg_to_group(sources):
    global YO_MOMMA_URL
    global CHUCK_NORRIS_URL
    choice = random.choice(list(sources.keys()))
    msg = sources.get(choice)()
    processed_image = generate_image(choice, msg)
    return processed_image


def handler(event, context):
    sources = {YO_MOMMA_URL: get_yo_momma,
               CHUCK_NORRIS_URL: get_chuck_norris}
    image_file = send_msg_to_group(sources)
    with open(image_file, 'rb') as fp:
        image_contents = fp.readlines()
    return image_contents


if __name__ == "__main__":
    # If we want to test it on the terminal
    handler(None, None)
