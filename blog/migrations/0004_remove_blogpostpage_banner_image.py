# Generated by Django 4.0.4 on 2022-05-22 20:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_blogpostpage_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpostpage',
            name='banner_image',
        ),
    ]
