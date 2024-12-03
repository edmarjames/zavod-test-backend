from rest_framework import serializers
from .models import (
  News,
  NewsView,
  Tag
)

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = "__all__"

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = instance.image.url
        return data

class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsView
        fields = "__all__"