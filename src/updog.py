import json
import base64
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


def resize_text(msg, number_of_lines):
    message_lines = []
    line_length = len(msg) / number_of_lines
    line = ""
    for word in msg.split(" "):
        if len(line + " " + word) > line_length:
            message_lines.append(line)
            line = word
        else:
            line += " {}".format(word)
    message_lines.append(line)
    return message_lines


def generate_image(choice, msg):
    if choice == YO_MOMMA_URL:
        image = Image.open("yomamma.jpg")
        xy = (5, 200)  # this was found manually
        max_y = 400
    elif choice == CHUCK_NORRIS_URL:
        image = Image.open("chucknorris.jpg")
        xy = (5, 5)  # this was found manually
        max_y = 500
    fnt = ImageFont.truetype('Xpressive Bold.ttf', 20)

    if fnt.getsize(msg)[0] > max_y:
        message_lines = resize_text(msg, (fnt.getsize(msg)[0]/max_y) + 1)
        msg = "\n".join(message_lines)
    draw = ImageDraw.Draw(image)
    draw.multiline_text(xy, msg, (255, 255, 255), font=fnt, align="center")
    output_filename = "/tmp/{}.jpg".format(int(time.time()))
    image.save(output_filename)
    return output_filename


def send_msg_to_group(sources):
    global YO_MOMMA_URL
    global CHUCK_NORRIS_URL
    choice = random.choice(list(sources.keys()))
    msg = sources.get(choice)()
    processed_image = generate_image(choice, msg)
    return processed_image, msg


def handler(event, context):
    sources = {YO_MOMMA_URL: get_yo_momma,
               CHUCK_NORRIS_URL: get_chuck_norris}
    image_file, msg = send_msg_to_group(sources)
    with open(image_file, 'rb') as fp:
        image_contents = fp.read()
    image_base_encoded = base64.b64encode(image_contents)
    # Get the API to respond with HTML that can display base64
    html_response = "<html><body><div><img src='data:image/png;base64, {}' /></div></body></html>".format(
        image_base_encoded)
    return html_response


if __name__ == "__main__":
    # If we want to test it on the terminal
    handler(None, None)
