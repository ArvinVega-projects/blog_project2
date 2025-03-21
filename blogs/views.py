from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Blog, BlogPost
from .forms import BlogForm, BlogPostForm
# Create your views here.

def index(request):
    """Home page for Blogs. Blog Posts will appear here."""
    # Set alphabetical order of the blog titles
    blog_titles = Blog.objects.order_by('text')
    context = {'blog_titles': blog_titles}
    return render(request, 'blogs/index.html', context)

def blog(request, blog_id):
    """The page to display a specific blog and its posts."""
    blog = Blog.objects.get(id=blog_id)
    blog_posts = blog.blogpost_set.order_by('-date_made')
    context = {'blog': blog, 'blog_posts': blog_posts}
    return render(request, 'blogs/blog.html', context)

@login_required
def new_blog(request):
    """Add a new blog."""
    if request.method != 'POST':
        # No data submitted; create blank form.
        form = BlogForm()
    else:
        # POST data submitted; process data.
        form = BlogForm(data=request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.owner = request.user
            new_blog.save()
            return redirect('blogs:index')
    
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogs/new_blog.html', context)

@login_required
def new_blogpost(request, blog_id):
    """Add a new blog post under specified blog_id."""
    blog = Blog.objects.get(id=blog_id)

    if request.method != 'POST':
        # No data submitted; create blank form with curent blog initially in the dropdown.
        form = BlogPostForm(initial={"blog_to_post_under": blog})
    else:
        # POST data submitted; process data.
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_blogpost = form.save(commit=False)
            new_blogpost.blog = blog
            new_blogpost.owner = request.user
            new_blogpost.save()
            return redirect('blogs:blog', blog_id=blog_id)
    
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_blogpost.html', context)

@login_required
def edit_blogname(request, blog_id):
    """Edit an existing blog name."""
    blog = Blog.objects.get(id=blog_id)
    # If request user does not match blog owner, raise 404 exception.
    check_blog_owner(blog, request.user)

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = BlogForm(instance=blog)
    else:
        # POST data submitted; process data.
        form = BlogForm(instance=blog, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')
    
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/edit_blogname.html', context)

@login_required
def edit_blogpost(request, blog_post_id):
    """Edit an existing blog post."""
    blogpost = BlogPost.objects.get(id=blog_post_id)
    blog = blogpost.blog_to_post_under
    # If request user does not match blog owner, raise 404 exception.
    check_blog_owner(blogpost, request.user)

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = BlogPostForm(instance=blogpost)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=blogpost, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:blog', blog_id=blog.id)
    
    context = {'blogpost': blogpost, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_blogpost.html', context)



# Functions associated with above views.
def check_blog_owner(blog, user):
    """
    Check if blog owner matches request user. If not, raise 404
    exception.
    """
    if blog.owner != user:
        raise Http404
