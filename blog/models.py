from django import forms
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.conf import settings

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtailcodeblock.blocks import CodeBlock

from .blocks import ImageBlock, BlogPostSectionBlock, AlertBlock




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

# ADD THIS! TABLE OF CONTENTS
# https://stackoverflow.com/questions/58120483/wagtail-blog-post-table-of-contents

class BlogPostPage(Page):
    """Parental post blog page. """
    localize_default_translation_mode = "simple"
    subpage_types = []
    parent_subpage_types = ['blog.BlogListingPage']
    # ajax_template = 'blog/other_template_fragment.html'

    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    view_count = models.PositiveBigIntegerField(default=0, blank=True)

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
        MultiFieldPanel([FieldPanel('categories', widget=forms.CheckboxSelectMultiple)], heading='Categories'),
        FieldPanel('tags'),
        StreamFieldPanel('content'),
        ]

    settings_panels = Page.settings_panels + [
        FieldPanel('view_count', widget=forms.NumberInput(attrs={'disabled': 'disabled', 'readonly': 'readonly'}))
        ]

    def serve(self, request):
        self.view_count += 1
        self.save()
        return super().serve(request)

    def update(self, *args, **kwargs):
        key = make_template_fragment_key("blog_post_preview", [self.id])
        cache.delete(key)
        return super().update(*args, **kwargs)




class BlogListingPage(Page):
    """ Listing page lists all the Blog Detail Pages. """
    max_count = 1
    subpage_types = ['blog.BlogPostPage']
    template_name = 'blog/blog_listing_page.html'

    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text='Overwrites the default title')
    content_panels = Page.content_panels + [
            FieldPanel('custom_title'),
    ]

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
