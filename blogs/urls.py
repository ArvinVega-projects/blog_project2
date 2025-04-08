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
    # Page to show user's blogs and blog posts.
    path('my_blogs', views.my_blogs, name='my_blogs'),
    # Admin page that shows all unpublished blogs.
    path('review_blog', views.review_blog, name='review_blog'),
    # # Admin page to confirm publishing of a blog.
    path('publish_blog/blog_id=<int:blog_id>', views.publish_blog, name='publish_blog'),
    # Admin page that shows all unpublished blog posts.
    path('review_blogposts', views.review_blogposts, name='review_blogposts'),
    # Admin page to confirm publishing of a blog post.
    path('publish_blogpost/blog_post_id=<int:blog_post_id>/', views.publish_blog_post, name='publish_blog_post'),
    # Admin page to delete a blog topic and all associated posts.
    path('delete_blog/blog_id=<int:blog_id>', views.delete_blog, name='delete_blog'),
    # Page to delete specified blog post.
    path('delete_post/blog_post_id=<int:blog_post_id>', views.delete_post, name='delete_post'),
    ]