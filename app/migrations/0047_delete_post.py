# Generated by Django 4.2.7 on 2023-11-21 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_remove_post_author_remove_post_category_and_more'),
        ('review', '0003_alter_postreview_post'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]