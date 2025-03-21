"""Define URL patterns for blogs."""
from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows a specific blog.
    path('blog/blog_id=<int:blog_id>/', views.blog, name='blog'),
    # Page to add a new blog.
    path('new_blog', views.new_blog, name='new_blog'),
    # Page to add a new blog post.
    path('new_blogpost/blog_id=<int:blog_id>/', views.new_blogpost, name='new_blogpost'),
    # Page to edit existing blog name.
    path('edit_blogname/blog_id=<int:blog_id>/', views.edit_blogname, name='edit_blogname'),
    # Page to edit existing blogpost.
    path('edit_blogpost/blog_post_id=<int:blog_post_id>/', views.edit_blogpost, name='edit_blogpost'),
    ]