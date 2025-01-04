from . import views
from .controller import post_view, post_view_mixin
from django.urls import path

urlpatterns = [
    path('', post_view_mixin.PostListCreateView.as_view(), name= 'create_or_list_posts'),
    path('<int:pk>', post_view_mixin.PostRetriveUpdateDeleteView.as_view(), name= 'get_update_delete_post'),
    # path('', post_view.PostListCreateView.as_view(), name= 'create_or_list_posts'),
    # path('<int:post_id>', post_view.PostRetriveUpdateDeleteView.as_view(), name= 'get_update_delete_post'),
    # path('<int:post_id>/update', views.updatePost, name= 'update_single_post'),
    # path('<int:post_id>/delete', views.deletePost, name= 'delete_single_post'),
]
