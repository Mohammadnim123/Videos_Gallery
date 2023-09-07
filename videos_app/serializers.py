from rest_framework import serializers
from .models import Category, Video

class VideoSerializer(serializers.ModelSerializer):
    length = serializers.CharField()
    watched = serializers.SerializerMethodField()

    def get_watched(self, obj):
        return obj.watched(self.context['request'].user)

    def to_representation(self, instance):
        data = super(VideoSerializer, self).to_representation(instance)
        if self.context['request'].user.is_anonymous:
            data.pop('watched')
        return data

    class Meta:
        model = Video
        fields = ['id', 'title', 'url', 'views_number', 'length',
                'cover_image', 'description', 'watched', 'created_at']


class ExtendedVideoSerializer(VideoSerializer):
    category_name = serializers.CharField(source='category.name')
    class Meta(VideoSerializer.Meta):
        fields = VideoSerializer.Meta.fields + ['category_name']


class CategorySerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True)
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'videos']
