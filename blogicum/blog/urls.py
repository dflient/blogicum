from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('posts/create', views.CreatePost.as_view(), name='create_post'),
    path('posts/<int:pk>/edit', views.EditPost.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete', views.DeletePost.as_view(), name='delete_post'),
    path('category/<slug:category_slug>/',
         views.CategoryPosts.as_view(),
         name='category_posts'),
    path('profile/<username>/', views.Profile.as_view(), name='profile'),
    path('edit_profile/<username>', views.EditProfile.as_view(), name='edit_profile'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:pk>/comment/<int:pk2>', views.EditComment.as_view(), name='edit_comment'),
    path('posts/<int:pk>/delete/<int:pk2>', views.DeleteComment.as_view(), name='delete_comment')
]
