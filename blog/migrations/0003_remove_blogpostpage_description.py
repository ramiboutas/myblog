# Generated by Django 4.0.4 on 2022-05-22 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpostpage_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpostpage',
            name='description',
        ),
    ]
