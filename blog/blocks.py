""" Streamfields live in here """
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe

from wagtail.core import blocks
from wagtailmarkdown.blocks import MarkdownBlock as ThirdPartyMarkdownBlock
from wagtail.images.blocks import ImageChooserBlock


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


class AlertBlock(blocks.StructBlock):
    ALERT_TYPE_CHOICES = (
        ('info', _('Informative')),
        ('warning', _('Warning')),
        ('danger', _('Danger')),
    )
    alert_type = blocks.ChoiceBlock(
        label=_('Choose the type of alert'),
        required=True,
        choices=ALERT_TYPE_CHOICES,
    )
    title = blocks.CharBlock(required=False)
    text = blocks.RichTextBlock(required=True,
            features=['code', 'bold', 'italic', 'link'])

    class Meta:
        icon = 'doc-full'
        template = 'blog/blocks/alert_box.html'
