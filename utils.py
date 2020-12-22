import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(id, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TextSendMessage(text=text))

    return "OK"



def send_image_url(id, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, ImageSendMessage(original_content_url=img_url, \
                                preview_image_url=img_url))
"""
def send_button_message(id, text, buttons):
    pass

"""
