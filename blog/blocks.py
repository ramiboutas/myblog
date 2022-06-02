""" Streamfields live in here """
from django.conf import settings

from wagtail.core import blocks
from wagtailmarkdown.blocks import MarkdownBlock as ThirdPartyMarkdownBlock
from wagtail.images.blocks import ImageChooserBlock

from django.utils.safestring import mark_safe

# from .settings import get_language_choices


class RichTextBlock(blocks.RichTextBlock):
    """ Rich text block """

    class Meta:
        template = 'blog/blocks/richt_text.html'
        icon = 'edit'
        label = 'Full RichtText'


class MarkdownBlock(blocks.StreamBlock):
    text = ThirdPartyMarkdownBlock(icon="code")

    class Meta:
        template = 'blog/blocks/markdown.html'
        icon = 'code'
        label = 'Markdown'


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'blog/blocks/image.html'



class BlogPostSectionBlock(blocks.CharBlock):
    # header = blocks.CharBlock(required=True)

    class Meta:
        icon = 'doc-full'
        template = 'blog/blocks/blog_post_section.html'
