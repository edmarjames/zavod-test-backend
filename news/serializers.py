from rest_framework import serializers
from .models import (
  News,
  NewsView,
  Tag
)

class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )

    class Meta:
        model = News
        fields = "__all__"

class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsView
        fields = "__all__"