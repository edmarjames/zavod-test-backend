from rest_framework import serializers

from .models import News, NewsView, Tag


class NewsSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    views_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = News
        fields = "__all__"

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def get_created_by(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image"] = instance.image.url if instance.image else None
        return data


class NewsStatisticsSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()


class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsView
        fields = "__all__"
