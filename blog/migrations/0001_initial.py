# Generated by Django 4.0.5 on 2022-06-04 18:57

import blog.blocks
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmetadata.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0069_log_entry_jsonfield'),
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('wagtailimages', '0024_index_image_file_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, help_text='A slug to identify posts by this category', max_length=255, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Blog Category',
                'verbose_name_plural': 'Blog Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='BlogListingPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('custom_title', models.CharField(help_text='Overwrites the default title', max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPostPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('view_count', models.PositiveBigIntegerField(blank=True, default=0)),
                ('content', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('post_section', blog.blocks.BlogPostSectionBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('arduino', 'Arduino'), ('autoit', 'AutoIt'), ('bash', 'Bash + Shell'), ('batch', 'Batch'), ('css', 'CSS'), ('css-extras', 'CSS Extras'), ('django', 'Django/Jinja2'), ('git', 'Git'), ('javascript', 'JavaScript'), ('js-extras', 'JS Extras'), ('js-templates', 'JS Templates'), ('json', 'JSON'), ('latex', 'LaTeX'), ('lua', 'Lua'), ('makefile', 'Makefile'), ('markdown', 'Markdown'), ('markup', 'Markup + HTML + XML + SVG + MathML'), ('markup-templating', 'Markup templating'), ('matlab', 'MATLAB'), ('nginx', 'nginx'), ('powershell', 'PowerShell'), ('python', 'Python'), ('regex', 'Regex'), ('sql', 'SQL'), ('textile', 'Textile'), ('typescript', 'TypeScript'), ('vbnet', 'VB.Net'), ('visual-basic', 'Visual Basic'), ('wiki', 'Wiki markup'), ('wolfram', 'Wolfram Mathematica')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))], label='Code')), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('alert', wagtail.blocks.StructBlock([('alert_type', wagtail.blocks.ChoiceBlock(choices=[('info', 'Informative'), ('warning', 'Warning'), ('danger', 'Danger')], label='Choose the type of alert')), ('title', wagtail.blocks.CharBlock(required=False)), ('text', wagtail.blocks.RichTextBlock(features=['code', 'bold', 'italic', 'link'], required=True))]))], blank=True, null=True, use_json_field=None)),
                ('categories', modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.blogcategory')),
                ('search_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image', verbose_name='Search image')),
                ('tags', modelcluster.contrib.taggit.ClusterTaggableManager(blank=True, help_text='A comma-separated list of tags.', through='blog.BlogPageTag', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.AddField(
            model_name='blogpagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.blogpostpage'),
        ),
        migrations.AddField(
            model_name='blogpagetag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag'),
        ),
    ]
