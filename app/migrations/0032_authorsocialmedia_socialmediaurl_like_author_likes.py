# Generated by Django 4.2.7 on 2023-11-12 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_author_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorSocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website_url', models.URLField()),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.author')),
            ],
        ),
        migrations.CreateModel(
            name='SocialMediaURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('author_social_media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_media_urls', to='app.authorsocialmedia')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.author')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='authors_likes', to='app.like'),
        ),
    ]
