# Generated by Django 4.0.5 on 2022-06-19 20:51

import blog.blocks
from django.db import migrations, models
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_blogpostpage_create_pdf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloglistingpage',
            name='custom_title',
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='content',
            field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='full title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('post_section', blog.blocks.BlogPostSectionBlock()), ('code', wagtail.blocks.StructBlock([('language', wagtail.blocks.ChoiceBlock(choices=[('bash', 'Bash + Shell'), ('css', 'CSS'), ('django', 'Django/Jinja2'), ('javascript', 'JavaScript'), ('json', 'JSON'), ('latex', 'LaTeX'), ('lua', 'Lua'), ('makefile', 'Makefile'), ('markdown', 'Markdown'), ('matlab', 'MATLAB'), ('nginx', 'nginx'), ('powershell', 'PowerShell'), ('python', 'Python'), ('regex', 'Regex'), ('sql', 'SQL'), ('textile', 'Textile'), ('typescript', 'TypeScript'), ('vbnet', 'VB.Net'), ('visual-basic', 'Visual Basic'), ('wiki', 'Wiki markup'), ('wolfram', 'Wolfram Mathematica')], help_text='Coding language', identifier='language', label='Language')), ('code', wagtail.blocks.TextBlock(identifier='code', label='Code'))], label='Code')), ('image', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False))])), ('alert', wagtail.blocks.StructBlock([('alert_type', wagtail.blocks.ChoiceBlock(choices=[('info', 'Informative'), ('warning', 'Warning'), ('danger', 'Danger')], label='Choose the type of alert')), ('title', wagtail.blocks.CharBlock(required=False)), ('text', wagtail.blocks.RichTextBlock(features=['code', 'bold', 'italic', 'link'], required=True))]))], blank=True, null=True, use_json_field=None),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='promote_in_linkedin',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='promote_in_telegram',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='blogpostpage',
            name='promote_in_twitter',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
