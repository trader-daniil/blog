from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.decorators import action


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        """Получим блог и все посты в нем."""
        blog = Blog.objects.prefetch_related('posts').get(id=kwargs['pk'])
        serialized_blog = self.get_serializer(blog)
        serialized_posts = PostSerializer(
            blog.posts.all(),
            many=True,
        )
        return Response(
            {
                'blog': serialized_blog.data,
                'posts': serialized_posts.data,
            },
            status=HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], url_path='follow_blog')
    def follow_blog(self, request, pk=None):
        """Пользователь подписывается на блог."""
        blog = self.get_object()
        blog.followers.add(request.user)
        return Response(
            {'status': 'Вы подписались на блог'},
            status=HTTP_201_CREATED,
        )

    @action(detail=True, methods=['delete'], url_path='unfollow_blog')
    def unfollow_blog(self, request, pk=None):
        """Пользователь отписывается от блога."""
        blog = Blog.objects.prefetch_related('followers').get(id=pk)
        if request.user not in blog.followers.all():
            return Response(
                {'status': 'Вы не подписаны на блог'},
                status=HTTP_200_OK,
            )
        blog.followers.remove(request.user)
        return Response(
                {'status': 'Вы отписались от блога'},
                status=HTTP_204_NO_CONTENT,
            )

