from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.urls import path
from blog.views import BlogViewSet


router = SimpleRouter()
router.register('blogs', BlogViewSet, basename='blog')
urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += router.urls
