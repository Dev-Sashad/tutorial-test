
from django.contrib import admin
from django.urls import path,include

from posts.controller.post_view_viewset import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("", PostViewSet, basename= "posts")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('posts/', include(router.urls))
    path('posts/', include('posts.urls')),
    path('auth/', include('accounts.urls'))
]
