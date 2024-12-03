from django.contrib import admin
from .models import (
  Tag,
  News,
  NewsView
)

admin.site.register(Tag)
admin.site.register(News)
admin.site.register(NewsView)