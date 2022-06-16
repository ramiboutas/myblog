from django.db import models

from wagtail.core.models import Page, Locale
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, ObjectList, TabbedInterface, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from blog.models import BlogCategory, BlogPostPage

class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1
    subpage_types = ['blog.BlogListingPage', 'contact.ContactPage', 'flex.FlexPage']
    parent_subpage_types = ['wagtailcore.Page']
    sub_title = models.CharField(max_length=250, blank=False, null=True)

    # banner_subtitle = RichTextField(features=['h2', 'h3', 'bold', 'italic', 'link'], blank=False, null=True)
    # banner_image = models.ForeignKey('wagtailimages.Image', null=True, blank=False, on_delete=models.SET_NULL, related_name='+')
    # banner_cta = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    #
    # banner_panels = [
    #     MultiFieldPanel([
    #     FieldPanel('banner_title'),
    #     FieldPanel('banner_subtitle'),
    #     ImageChooserPanel('banner_image'),
    #     PageChooserPanel('banner_cta')
    #     ])
    # ]

    content_panels = Page.content_panels + [
        FieldPanel('sub_title', heading="Subtitle"),
    ]
    promote_panels = Page.promote_panels
    settings_panels = Page.settings_panels
    # edit_handler = TabbedInterface([
    #     ObjectList(Page.content_panels, heading='Content'),
    #     ObjectList(Page.promote_panels, heading='Promo stuff'),
    #     ObjectList(Page.settings_panels, heading='Settings stuff'),
    #     # ObjectList(banner_panels, heading='Banners'),
    #     ])

    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff to our context """
        context = super().get_context(request, *args, **kwargs)
        recent_posts = BlogPostPage.objects.live().filter(
                    locale=Locale.get_active(), show_in_listings=True).order_by('-first_published_at')[:10]
        popular_posts = BlogPostPage.objects.live().filter(
                    locale=Locale.get_active(), show_in_listings=True).order_by('-view_count')[:5]
        context['recent_posts'] = recent_posts
        context['popular_posts'] = popular_posts
        context['categories'] = BlogCategory.objects.all()
        return context
