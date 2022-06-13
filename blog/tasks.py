import os
import json
import textwrap
import requests
import telegram
import tweepy
from telegram.utils.helpers import escape_markdown
import qrcode
from io import BytesIO
from PIL import Image as PillowImage
from PIL import ImageDraw as PillowImageDraw
from PIL import ImageFont as PillowImageFont

from django.core.files.images import ImageFile
from django.conf import settings

from wagtail.images import get_image_model
WagtailImage = get_image_model()

from celery import shared_task

def escape_html_for_telegram(text):
    text.replace("<", "&lt;")
    text.replace(">", "&gt;")
    text.replace("&", "&amp;")
    return text

@shared_task(bind=True)
def create_pdf(self, instance):
    """
    /// TO DO ///
    Creates pdf file
    """
    pass


@shared_task(bind=True)
def create_search_image(self, instance):
    """
    Creates a search image with a QR code and page title
    """
    # geometry definitions
    MAX_W, MAX_H = 500, 500
    margin = 30
    shape = [(margin, margin), (MAX_W - margin, MAX_H - margin)]
    img = PillowImage.new('RGB', (MAX_W, MAX_H), color = (0, 0, 0))

    # QR code creation and paste it into the image
    qr = qrcode.QRCode(box_size=3)
    qr.add_data(instance.full_url)
    qr_img = qr.make_image()
    qr_pos = (int(MAX_W/2-67), int(MAX_H-margin*6))
    img.paste(qr_img, qr_pos)

    # draw definition
    draw = PillowImageDraw.Draw(img)
    font_big = PillowImageFont.truetype('OpenSans-Regular.ttf', 40)
    font_small = PillowImageFont.truetype('OpenSans-Regular.ttf', 12)

    draw.rectangle(shape, outline="white")

    # draw on top page parent url (actual blog listing page)
    w, h = draw.textsize(instance.get_parent().full_url, font=font_small)
    draw.text(((MAX_W - w) / 2, margin*2), instance.get_parent().full_url, font=font_small, fill=(246, 146, 188))

    # draw post title
    paragraph = textwrap.wrap(instance.title, width=20)
    current_h, pad = 100, 10
    for line in paragraph:
        w, h = draw.textsize(line, font=font_big)
        draw.text(((MAX_W - w) / 2, current_h), line, font=font_big, fill=(255, 255, 255))
        current_h += h + pad

    # save image
    img_bytes = BytesIO()
    img.save(img_bytes, 'JPEG')
    instance.search_image = WagtailImage.objects.create(title=instance.title,
                file=ImageFile(img_bytes, name=f'METADATA-{instance.slug}.jpg'))



@shared_task(bind=True)
def promote_post_instance_in_telegram(self, instance):
    post_text = instance.post_text_for_telegram
    if post_text == instance.title:
        text = f'{post_text} \n\n<a href="{instance.full_url}">{instance.full_url}</a>'
    else:
        text = f'{post_text} \n\n<a href="{instance.full_url}">{instance.title}</a>'

    parsed_text = escape_html_for_telegram(text)

    if instance.share_in_matlab_accounts:
        matlab_accounts = settings.TELEGRAM_ACCOUNTS_FOR_MATLAB
        api_key = matlab_accounts[instance.locale.language_code]["BOT_API_KEY"]
        channel = matlab_accounts[instance.locale.language_code]["CHANNEL_NAME"]
        bot = telegram.Bot(token=api_key)
        bot.send_message(chat_id=channel, text=parsed_text, parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=False)

    if instance.share_in_excel_accounts:
        excel_accounts = settings.TELEGRAM_ACCOUNTS_FOR_EXCEL
        api_key = excel_accounts[instance.locale.language_code]["BOT_API_KEY"]
        channel = excel_accounts[instance.locale.language_code]["CHANNEL_NAME"]
        bot = telegram.Bot(token=api_key)
        bot.send_message(chat_id=channel, text=parsed_text, parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=False)

    if instance.share_in_webdev_accounts:
        webdev_accounts = settings.TELEGRAM_ACCOUNTS_FOR_WEBDEV
        api_key = webdev_accounts[instance.locale.language_code]["BOT_API_KEY"]
        channel = webdev_accounts[instance.locale.language_code]["CHANNEL_NAME"]
        bot = telegram.Bot(token=api_key)
        bot.send_message(chat_id=channel, text=parsed_text, parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=False)


@shared_task(bind=True)
def promote_post_instance_in_linkedin(self, instance):
    #scope: w_member_social,r_liteprofile
    profile_id = settings.LINKEDIN_PROFILE_ID
    access_token = settings.LINKEDIN_ACCESS_TOKEN

    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {'Content-Type': 'application/json',
               'X-Restli-Protocol-Version': '2.0.0',
               'Authorization': 'Bearer ' + access_token}

    post_data = {
        "author": "urn:li:person:"+profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f'{instance.post_text_for_telegram} \n {instance.full_url} '
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "LOGGED_IN"
        }
    }

    response = requests.post(url, headers=headers, json=post_data)


@shared_task(bind=True)
def promote_post_instance_in_twitter(self, instance):

    # API keys
    api_key = settings.TWITTER_API_KEY
    api_secret = settings.TWITTER_API_KEY_SECRET
    access_token = settings.TWITTER_ACCESS_TOKEN
    access_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(api_key,api_secret)
    auth.set_access_token(access_token,access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    status = f"{instance.post_text_for_twitter}\n {instance.full_url}"
    api.update_status(status=status)
