from django.db import models
from django_extensions.db.fields import AutoSlugField

from modelcluster.models import ClusterableModel, ParentalKey

from wagtail.snippets.models import register_snippet
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel,
)


class MenuItem(Orderable):
    link_title = models.CharField(max_length=50, blank=True, null=True)
    link_url = models.CharField(max_length=500, blank=True, null=True)
    link_page = models.ForeignKey("wagtailcore.Page", null=True, blank=True, related_name='+', on_delete=models.SET_NULL)
    open_in_new_tab = models.BooleanField(default=False, blank=True)

    page = ParentalKey("Menu", related_name="menu_items")

    panels = [
        FieldPanel("link_title"),
        FieldPanel("link_url"),
        FieldPanel("link_page"),
        FieldPanel("open_in_new_tab"),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_url:
            return self.link_url
        return '#'

    @property
    def title(self):
        if self.link_page and not self.link_title:
            return self.link_page.title
        elif self.link_title:
            return self.link_title
        return 'Missing Title'


@register_snippet
class Menu(ClusterableModel):
    """ The main menu clusterable model. """

    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", editable=True)

    panels = [
            MultiFieldPanel([FieldPanel("title"), FieldPanel("slug")], heading="Menu"),
            InlinePanel("menu_items", label="Menu item"),
    ]

    def __str__(self):
        return self.title
