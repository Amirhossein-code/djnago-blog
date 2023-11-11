# Generated by Django 4.2.7 on 2023-11-09 15:57

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_author_profile_image_delete_authorprofileimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False, populate_from='title', unique=True),
            preserve_default=False,
        ),
    ]