import os
import textwrap
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

@receiver(pre_save, sender=BlogPostPage)
def create_search_image(sender, instance, *args, **kwargs):
    if not instance.search_image:
        MAX_W, MAX_H = 500, 500
        img = PillowImage.new('RGB', (MAX_W, MAX_H), color = (0, 0, 0))
        draw = PillowImageDraw.Draw(img)
        font_big = PillowImageFont.truetype('OpenSans-Regular.ttf', 40)
        font_small = PillowImageFont.truetype('OpenSans-Regular.ttf', 20)
        # border
        shape = [(30, 30), (MAX_W - 30, MAX_H - 30)]
        draw.rectangle(shape, outline="white")
        paragraph = textwrap.wrap(instance.title, width=20)
        current_h, pad = 100, 10
        for line in paragraph:
            w, h = draw.textsize(line, font=font_big)
            draw.text(((MAX_W - w) / 2, current_h), line, font=font_big, fill=(255, 255, 255))
            current_h += h + pad
        img_bytes = BytesIO()
        img.save(img_bytes, 'JPEG')
        instance.search_image = WagtailImage.objects.create(title=instance.title,
                    file=ImageFile(img_bytes, name=f'METADATA-{instance.slug}.jpg'))
