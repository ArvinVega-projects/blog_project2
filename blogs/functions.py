# Functions associated with views.
from django.http import Http404

def check_admin(user):
    """Check if user is a superuser."""
    return user.is_superuser

def check_blog_owner(blog, user):
    """
    Check if blog owner matches request user. If not, raise 404
    exception.
    """
    if blog.owner != user:
        raise Http404

def check_if_live(blog_or_blogpost):
    """
    Check if a blog is live. If not, raise 404 error. This will be used for
    blog so that getting URLs for unpublished blogs will raise exception.
    """
    if blog_or_blogpost.public == False:
        raise Http404