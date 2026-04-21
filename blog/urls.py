from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('create/', views.post_create, name='post_create'),
    path('tag/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
]
