from .models import Blog, Post
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
        )

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'text',
            'created_at',
            'author',
            'blog',
        )
        read_only_fields = (
            'blog',
            'author',
        )
