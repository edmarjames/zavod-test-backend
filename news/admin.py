from django.contrib import admin

from .models import News, NewsView, Tag

admin.site.register(Tag)
admin.site.register(News)
admin.site.register(NewsView)