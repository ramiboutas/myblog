""" Flexible page. """

from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.fields import StreamField

from wagtail.core import blocks


class FlexPage(Page):
    template = 'flex/flex_page.html'
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    subpage_types = ['flex.FlexPage', 'contact.ContactPage']
    parent_subpage_types = ['flex.FlexPage', 'home.HomePage']
    content = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ],
    null=True,
    blank=True)

    content_panels = Page.content_panels + [
            FieldPanel('subtitle'),
            StreamFieldPanel('content'),
    ]

    class Meta:
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
