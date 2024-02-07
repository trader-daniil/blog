from rest_framework import viewsets
from .models import Blog, Post, PostUserRelation
from .serializers import BlogSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.decorators import action
from django.db.models import Prefetch
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


POSTS_PER_PAGE = 10

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

    @action(detail=True, methods=['post'], url_path='follow_blog',
            permission_classes=[IsAuthenticated])
    def follow_blog(self, request, pk=None):
        """Пользователь подписывается на блог."""
        blog = self.get_object()
        blog.followers.add(request.user)
        return Response(
            {'status': 'Вы подписались на блог'},
            status=HTTP_201_CREATED,
        )

    @action(detail=True, methods=['delete'], url_path='unfollow_blog',
            permission_classes=[IsAuthenticated])
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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """Получим все посты из блогов, на которые подписан пользователь."""
        posts = Post.objects.select_related('blog').\
                            select_related('author').\
                            filter(blog__followers=request.user).\
                            order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = POSTS_PER_PAGE
        result_page = paginator.paginate_queryset(posts, request)
        serialized_posts = PostSerializer(
            result_page,
            many=True,
        )
        return paginator.get_paginated_response(serialized_posts.data)
  
    
    def perform_create(self, serializer):
        """Пост автоматически создается пользователем в его персональном блоге."""
        serializer.save(
            author=self.request.user,
            blog=self.request.user.blog,
        )
    
    @action(detail=True, methods=['post'], url_path='mark_as_read')
    def mark_as_read(self, request, pk=None):
        """Пользователь помечает пост прочитанным."""
        PostUserRelation.objects.create(
            user=request.user,
            post=self.get_object(),
            is_read=True,
        )
        return Response(
            {'status': 'Вы прочитали пост'},
            status=HTTP_201_CREATED,
        )

    @action(detail=False, methods=['get'], url_path='read_posts')
    def mark_as_read(self, request, pk=None):
        """Показываем прочитанные посты пользователя."""
        posts = Post.objects.prefetch_related(
            Prefetch(
                'read_users',
                queryset=PostUserRelation.objects.filter(
                    user=request.user,
                    is_read=True,
                )
            )
        ).\
            filter(read_users__is_read=True).\
            filter(read_users__user=request.user).\
            all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(
            serialized_posts.data,
            status=HTTP_200_OK,
        )

        
    
    

