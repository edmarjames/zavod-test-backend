from rest_framework import serializers

from .models import News, NewsView, Tag


class NewsSerializer(serializers.ModelSerializer):
    # tags = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    views_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = News
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = [tag.name for tag in instance.tags.all()]
        data["image"] = instance.image.url if instance.image else None
        return data


class NewsStatisticsSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()


class NewsViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsView
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

