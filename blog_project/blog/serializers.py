from .models import Blog, Post
from rest_framework import serializers


class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blog
        fields = (
            'id',
            'title',
        )
