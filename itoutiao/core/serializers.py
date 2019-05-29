from rest_framework import serializers

from .models import Post, PostTag, Tag


class PostTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTag
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    post_tag = PostTagSerializer(many=True)

    class Meta:
        model = Tag
        fields = ("name", "post_tag")


class PostSerializer(serializers.ModelSerializer):
    abstract_content = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author_id", "title", "orig_url", "abstract_content", "tags")

    def get_abstract_content(self, obj):
        return obj.abstract_content

    def get_tags(self, obj):
        return obj.tags
