from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

class Category(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Video(BaseModel):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    users_watched = models.ManyToManyField(User, related_name='watched_videos', blank=True)
    views_number = models.PositiveIntegerField(default=0)
    length_in_seconds = models.PositiveIntegerField(help_text="Duration of the video in seconds.")
    cover_image = models.URLField(unique=True) 
    description = models.TextField(blank=True, null=True)

    def watched(self, user):
        return user in self.users_watched.all()

    @property
    def length(self):
        hours, remainder = divmod(self.length_in_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)

    def __str__(self):
        return self.title
