# Generated by Django 4.2.4 on 2023-09-04 18:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videos_app', '0002_alter_video_users_watched'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='users_watched',
            field=models.ManyToManyField(blank=True, related_name='watched_videos', to=settings.AUTH_USER_MODEL),
        ),
    ]
