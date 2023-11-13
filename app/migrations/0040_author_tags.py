# Generated by Django 4.2.7 on 2023-11-13 11:49

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('app', '0039_author_social_media_url_author_website_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
