from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('posts/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<int:post_pk>/comment/create/', views.add_post_comment, name='post_comment_create'),
    path('post/create/', views.add_post, name='add_post'),
    path('post/from/', views.from_post, name='from_post'),
    path('post/search/', views.PostSearchView.as_view(), name='search_posts'),
    path('post/toggle_edit/<slug:slug>', views.edit_post, name='toggle_edit_post'),
    path('post/edit/<slug:slug>/', views.form_edit_post, name='edit_post'),
    path('post/post_like/<int:pk>/', views.toggle_post_like, name='post_like_toggle'),
    path('post/post_dislike/<int:pk>/', views.toggle_post_dislike, name='post_dislike_toggle'),
    path('post/<int:pk>/comment_like/<int:comment_pk>/', views.toggle_comment_like, name='comment_like_toggle'),
    path('post/<int:pk>/comment_dislike/<int:comment_pk>/', views.toggle_comment_dislike, name='comment_dislike_toggle')
]
