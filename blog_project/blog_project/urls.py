from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.urls import path
from blog.views import BlogViewSet, PostViewSet
from rest_framework.authtoken import views


router = SimpleRouter()
router.register('blogs', BlogViewSet, basename='blog')
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token)
]
urlpatterns += router.urls
