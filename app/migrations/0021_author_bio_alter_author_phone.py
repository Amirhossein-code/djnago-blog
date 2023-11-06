# Generated by Django 4.2.7 on 2023-11-05 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_author_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.CharField(blank=True, max_length=550, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]