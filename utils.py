import os

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, PostbackEvent, PostbackTemplateAction, ImageSendMessage
import random

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(id, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TextSendMessage(text=text))

    return "OK"



def send_image_url(id, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, ImageSendMessage(original_content_url=img_url, \
                                preview_image_url=img_url))

def send_button_message(id, starburst_img):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(id, TemplateSendMessage(
                            alt_text='星爆!',
                            template=ButtonsTemplate(
                                thumbnailImageUrl=starburst_img[random.randomrange(0, 193)],
                                title='桐人星爆爆，魔眼閃耀耀',
                                text='想要更多星爆圖嗎?',
                                defaultAction=PostbackTemplateAction(
                                        label='I want more!',
                                        text='I want more!',
                                        data='YES'
                                    ),
                                actions=[
                                    PostbackTemplateAction(
                                        label='I want more!',
                                        text='I want more!',
                                        data='YES'
                                    ),
                                    PostbackTemplateAction(
                                        label='NO, PLEASE NO!',
                                        text='NO, PLEASE NO!',
                                        data='NO'
                                    )
                                ]
                            )
                        )
    )

