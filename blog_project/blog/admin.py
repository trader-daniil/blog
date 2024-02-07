from django.contrib import admin
from .models import Post, Blog, PostUserRelation


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'blog',
        'created_at',
    )
    raw_id_fields = (
        'author',
        'blog',
    )


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
    )
    raw_id_fields = ('author',)


@admin.register(PostUserRelation)
class UserPostRelationAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'user',
        'is_read',
    )

