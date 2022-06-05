from django import forms
from django.db import models
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext as _

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core import blocks
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtailcodeblock.blocks import CodeBlock
from wagtailmetadata.models import MetadataPageMixin

from .blocks import ImageBlock, BlogPostSectionBlock, AlertBlock
from utils.times import one_hour_from_now


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey("BlogPostPage", related_name="tagged_items", on_delete=models.CASCADE)


@register_snippet
class BlogCategory(models.Model):
    """ Blog category for a snippet """

    name = models.CharField(max_length=255)
    slug = models.SlugField(verbose_name="slug", max_length=255, allow_unicode=True,
                            help_text="A slug to identify posts by this category")


    class Meta:
        verbose_name = 'Blog Category'
        verbose_name_plural = 'Blog Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class BlogPostPage(MetadataPageMixin, Page):
    """Parental post blog page. """
    localize_default_translation_mode = "simple"
    subpage_types = []
    parent_subpage_types = ['blog.BlogListingPage']
    # ajax_template = 'blog/other_template_fragment.html'

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    view_count = models.PositiveBigIntegerField(default=0, blank=True)
    show_in_listings = models.BooleanField(default=True)

    # promoting in social media
    promoting_time = models.DateTimeField(default=one_hour_from_now, null=True)
    share_in_webdev_accounts = models.BooleanField(default=False, null=True, blank=True)
    share_in_matlab_accounts = models.BooleanField(default=False, null=True, blank=True)
    share_in_excel_accounts = models.BooleanField(default=False, null=True, blank=True)

    promote_in_instagram = models.BooleanField(default=True, null=True, blank=True)
    promote_in_telegram = models.BooleanField(default=True, null=True, blank=True)
    promote_in_facebook = models.BooleanField(default=True, null=True, blank=True)
    promote_in_linkedin = models.BooleanField(default=True, null=True, blank=True)
    promote_in_twitter = models.BooleanField(default=True, null=True, blank=True)

    post_text_for_instagram = models.TextField(max_length=2000, null=True, blank=True)
    post_text_for_telegram = models.TextField(max_length=2000, null=True, blank=True)
    post_text_for_facebook = models.TextField(max_length=2000, null=True, blank=True)
    post_text_for_linkedin = models.TextField(max_length=1300, null=True, blank=True)
    post_text_for_twitter = models.TextField(max_length=140, null=True, blank=True)

    content = StreamField([
        # wagtail blocks
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),

        # my custom or third party blocks
        ('post_section', BlogPostSectionBlock()),
        ('code', CodeBlock(label='Code')),
        ('image', ImageBlock()),
        ('alert', AlertBlock()),
        ], null=True, blank=True)


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple)], heading='Categories'),
            FieldPanel('tags'),
            StreamFieldPanel('content'),
        ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('promoting_time', heading=_('When to post in social media')),
            FieldPanel('share_in_webdev_accounts', heading=_('Share in WEBDEV social media accounts')),
            FieldPanel('share_in_matlab_accounts', heading=_('Share in MATLAB social media accounts')),
            FieldPanel('share_in_excel_accounts', heading=_('Share in EXCEL-VBA  social media accounts')),
        ], heading="Sharing, when and where"),
        MultiFieldPanel([
            FieldPanel('promote_in_instagram'),
            FieldPanel('post_text_for_instagram'),
        ], heading="Instagram"),
        MultiFieldPanel([
            FieldPanel('promote_in_facebook'),
            FieldPanel('post_text_for_facebook'),
        ], heading="Facebook"),
        MultiFieldPanel([
            FieldPanel('promote_in_twitter'),
            FieldPanel('post_text_for_twitter'),
        ], heading="Twitter"),
        MultiFieldPanel([
            FieldPanel('promote_in_telegram'),
            FieldPanel('post_text_for_telegram'),
        ], heading="Telegram"),
        MultiFieldPanel([
            FieldPanel('promote_in_linkedin'),
            FieldPanel('post_text_for_linkedin'),
        ], heading="Linkedin"),
    ]




    settings_panels = Page.settings_panels + [
        FieldPanel('view_count', widget=forms.NumberInput(attrs={'disabled': 'disabled', 'readonly': 'readonly'})),
        FieldPanel('show_in_listings')
        ]


    def serve(self, request):
        self.view_count += 1
        self.save()
        return super().serve(request)

    def update(self, *args, **kwargs):
        key = make_template_fragment_key("blog_post_preview", [self.id])
        cache.delete(key)
        return super().update(*args, **kwargs)

    def save(self, *args, **kwargs):
        # in case I need it later
        super(self.__class__, self).save(*args, **kwargs)



class BlogListingPage(RoutablePageMixin, Page):
    """ Listing page lists all the Blog Detail Pages. """
    max_count = 1
    subpage_types = ['blog.BlogPostPage']
    template_name = 'blog/blog_listing_page.html'

    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Overwrites the default title')
    content_panels = Page.content_panels + [
            FieldPanel('custom_title'),
    ]

    def get_posts(self):
        return BlogPostPage.objects.live().filter(
            locale=Locale.get_active(), show_in_listings=True).order_by('-first_published_at')

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.posts = self.get_posts().filter(categories__blog_category__slug=category)
        return self.render(request)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return self.render(request)

    # https://www.accordbox.com/blog/wagtail-seo-guide/#sitemap
    def get_sitemap_urls(self, request):
        # Uncomment to have no sitemap for this page
        # return []
        sitemap = super().get_sitemap_urls(request)
        # sitemap.append(
        #     {
        #         "location": self.full_url + self.reverse_subpage("latest_posts"),
        #         "lastmod": (self.last_published_at or self.latest_revision_created_at),
        #         "priority": 0.9,
        #     }
        # )
        return sitemap

    def get_context(self, request, *args, **kwargs):
        """ Adding custom stuff to our context """
        context = super().get_context(request, *args, **kwargs)
        all_posts = BlogPostPage.objects.live().public().order_by('-first_published_at')

        if request.GET.get("tag", None):
            tags = request.GET.get("tag")
            all_posts = all_posts.filter(tags__slug__in=[tags])

        paginator = Paginator(all_posts, 2)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger as e:
            posts = paginator.page(1)
        except EmptyPage as e:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()
        return context
