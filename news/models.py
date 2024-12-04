from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date_created}"

class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField("Tag")
    image = CloudinaryField("image")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class NewsView(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="views")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View on {self.news.title} at {self.timestamp}"

