from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    """Блог пользователя."""
    title = models.CharField(
        max_length=256,
        verbose_name='Название Блога',
    )
    author = models.OneToOneField(
        User,
        related_name='blog',
        verbose_name='Блог пользователя',
        on_delete=models.CASCADE,
    )

class Post(models.Model):
    """Пост в блоге."""
    title = models.CharField(
        max_length=64,
        verbose_name='Заголовок поста',
    )
    text = models.CharField(
        max_length=140,
        blank=True,
        verbose_name='Текст поста',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания поста',
    )
    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE,
        verbose_name='Автор поста',
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        verbose_name='Блог, в котором опубликован пост',
        related_name='posts',
    )


