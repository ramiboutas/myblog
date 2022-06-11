import os
import json
import textwrap
import requests
import telegram
from telegram.utils.helpers import escape_markdown
import qrcode
from io import BytesIO
from PIL import Image as PillowImage
from PIL import ImageDraw as PillowImageDraw
from PIL import ImageFont as PillowImageFont

from django.core.files.images import ImageFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings

from wagtail.signals import page_published
from wagtail.images import get_image_model
WagtailImage = get_image_model()

from .models import BlogPostPage

def escape_html_for_telegram(text):
    text.replace("<", "&lt;")
    text.replace(">", "&gt;")
    text.replace("&", "&amp;")
    return text


def promote_post_instance_in_telegram(instance):
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
        bot.send_message(chat_id=channel, text=parsed_text,
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=False)


def promote_post_instance_in_linkedin(instance):
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

    print(response)


def promote_post_instance_in_instagram(instance):
    if instance.share_in_matlab_accounts or True:
        instagram_accounts = settings.INSTAGRAM_ACCOUNTS_FOR_MATLAB
        user_id = instagram_accounts[instance.locale.language_code]["USER_ID"]
        access_token = instagram_accounts[instance.locale.language_code]["ACCESS_TOKEN"]

        post_url = 'https://graph.facebook.com/v14.0/{}/media'.format(user_id)

        payload = {
            'image_url': instance.search_image.usage_url,
            'caption': instance.post_text_for_instagram,
            'access_token': access_token
            }
        r = requests.post(post_url, data=payload)
        print(r.text)
        result = json.loads(r.text)
        if 'id' in result:
            creation_id = result['id']
            second_url = 'https://graph.facebook.com/v14.0/{}/media_publish'.format(user_id)
            second_payload = {
                'creation_id': creation_id,
                'access_token': access_token
            }
            r = requests.post(second_url, data=second_payload)
            print('--------Just posted to instagram--------')
            print(r.text)
        else:
            print('HOUSTON we have a problem')




@receiver(page_published, sender=BlogPostPage)
def temporal_function_post_in_social_media(sender, instance, *args, **kwargs):
    # include in tasks.py later!
    if instance.promote_in_instagram:
        promote_post_instance_in_instagram(instance)

    if instance.promote_in_telegram:
        promote_post_instance_in_telegram(instance)


    if instance.promote_in_facebook:
        pass

    if instance.promote_in_linkedin:
        promote_post_instance_in_linkedin(instance)

    if instance.promote_in_twitter:
        pass




# >>> from django.conf import settings
# >>> accounts = settings.INSTAGRAM_ACCOUNTS
# >>> accounts
# {'es': {'API_PUBLIC': 'whatever ES', 'USERNAME': 'whatever ES'}, 'en': {'API_PUBLIC': 'whatever EN', 'USERNAME': 'whatever EN'}, 'de': {'API_PUBLIC': 'whatever DE', 'USERNAME': 'whatever DE'}}
# >>> accounts["en"]
# {'API_PUBLIC': 'whatever EN', 'USERNAME': 'whatever EN'}
# >>> accounts["en"]["API_PUBLIC"]
# 'whatever EN'
#
# if "page" is a Page instance, we can get its language code:
# page.locale.language_code



@receiver(pre_save, sender=BlogPostPage)
def create_search_image_and_default_social_media_text(sender, instance, *args, **kwargs):
    """
    Creates a search image if is not created and also:
    Default post text for social media is created (populated from instance.title),
    if no text is provided and if the editor wants to promote the page.
    """
    # move to tasks.py later
    if not instance.search_image:
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

    if not instance.post_text_for_instagram and instance.promote_in_instagram:
        instance.post_text_for_instagram = instance.title

    if not instance.post_text_for_telegram and instance.promote_in_telegram:
        instance.post_text_for_telegram = instance.title

    if not instance.post_text_for_facebook and instance.promote_in_facebook:
        instance.post_text_for_facebook = instance.title

    if not instance.post_text_for_linkedin and instance.promote_in_linkedin:
        instance.post_text_for_linkedin = instance.title

    if not instance.post_text_for_twitter and instance.promote_in_twitter:
        instance.post_text_for_twitter = instance.title

    instance.save()
