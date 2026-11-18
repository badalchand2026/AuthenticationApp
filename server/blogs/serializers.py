
from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):

    author_name = serializers.CharField(
        source='author.email',
        read_only=True
    )

    class Meta:
        model = Blog

        fields = [
            'id',
            'title',
            'slug',
            'content',
            'author',
            'author_name',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'slug',
            'author',
            'author_name',
            'created_at',
            'updated_at',
        ]
