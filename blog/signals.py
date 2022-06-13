from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from wagtail.signals import page_published

from .models import BlogPostPage
from .tasks import (create_search_image, create_pdf, promote_post_instance_in_telegram,
                promote_post_instance_in_linkedin, promote_post_instance_in_twitter)


@receiver(page_published, sender=BlogPostPage)
def post_in_social_media(sender, instance, *args, **kwargs):

    # Save check - post text
    if not instance.post_text_for_telegram and instance.promote_in_telegram:
        instance.post_text_for_telegram = instance.title

    if not instance.post_text_for_linkedin and instance.promote_in_linkedin:
        instance.post_text_for_linkedin = instance.title

    if not instance.post_text_for_twitter and instance.promote_in_twitter:
        instance.post_text_for_twitter = instance.title

    # promote the blog post
    if instance.promote_in_telegram:
        promote_post_instance_in_telegram(instance)

    if instance.promote_in_linkedin:
        promote_post_instance_in_linkedin(instance)

    if instance.promote_in_twitter:
        promote_post_instance_in_twitter(instance)


@receiver(pre_save, sender=BlogPostPage)
def check_search_image(sender, instance, *args, **kwargs):
    """
    Checks if the search image exists or not.
    """
    if not instance.search_image:
        create_search_image(instance)

@receiver(pre_save, sender=BlogPostPage)
def check_pdf_creation(sender, instance, *args, **kwargs):
    """
    Checks if the pdf needs to be created or not.
    """
    if instance.create_pdf:
        create_pdf(instance)
