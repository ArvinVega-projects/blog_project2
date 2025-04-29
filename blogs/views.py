from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
import functions as f

from .models import Blog, BlogPost
from .forms import BlogForm, BlogPostForm
# Create your views here.

def index(request):
    """Home page for Blogs. Public Blog Topics will appear here."""
    # Set alphabetical order of the blog titles
    blog_titles = Blog.objects.order_by('text')
    context = {'blog_titles': blog_titles}
    return render(request, 'blogs/index.html', context)

# Send non-superusers to home page if trying to access review_blog.
# login_url="/" is the syntax to redirect to homepage instead of login page.
@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def review_blog(request):
    """Admin only page. This shows all blogs that aren't
    published yet."""
    blogs = Blog.objects.filter(public=False)
    context = {'blogs': blogs}
    return render(request, 'blogs/review_blog.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def review_blogposts(request):
    """Admin only page. This shows all blogposts that aren't published yet."""
    blog_posts = BlogPost.objects.filter(public=False)
    context = {'blog_posts': blog_posts}
    return render(request, 'blogs/review_blogposts.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def publish_blog(request, blog_id):
    """Admin only page. This page confirms the publishing of a blog."""
    blog = Blog.objects.get(id=blog_id)
    blog.public = True
    blog.save()
    context = {'blog': blog}
    return render(request, 'blogs/publish_blog.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def publish_blog_post(request, blog_post_id):
    """Admin only page. This page confirms the publishing of a blog post."""
    bp = BlogPost.objects.get(id=blog_post_id)
    blog = bp.blog_to_post_under # Retrieve associated blog for redirect.
    bp.public = True
    bp.save()
    context = {'bp': bp, 'blog': blog}
    return render(request, 'blogs/publish_blog_post.html', context)

def blog(request, blog_id):
    """The page to display a specific blog and its posts."""
    blog = Blog.objects.get(id=blog_id)
    f.check_if_live(blog) # Raise 404 if blog isn't live.
    blog_posts = blog.blogpost_set.order_by('-date_made')
    context = {'blog': blog, 'blog_posts': blog_posts}
    return render(request, 'blogs/blog.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def new_blog(request):
    """Admin only page. Add a new blog topic."""
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
            return redirect('blogs:review_blog')
    
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
            return redirect('blogs:my_blogs')
    
    context = {'blog': blog, 'form': form}
    return render(request, 'blogs/new_blogpost.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def edit_blogname(request, blog_id):
    """Admin only. Edit an existing blog name."""
    blog = Blog.objects.get(id=blog_id)

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
    f.check_blog_owner(blogpost, request.user)

    if request.method != 'POST':
        # Initial request; pre-fill form with current entry.
        form = BlogPostForm(instance=blogpost)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=blogpost, data=request.POST)
        if form.is_valid():
            edited_bp = form.save(commit=False)
            edited_bp.public = False
            edited_bp.save()
            return redirect('blogs:my_blogs')
        
    context = {'blogpost': blogpost, 'blog': blog, 'form': form}
    return render(request, 'blogs/edit_blogpost.html', context)

@login_required
def my_blogs(request):
    """
    Page to show current user's blogs and blog posts, whether they are published
    or not.
    """
    blogs = Blog.objects.order_by("text")
    blog_posts = BlogPost.objects.order_by("blog_to_post_under")
    user = request.user
    context = {'blogs': blogs, 'blog_posts': blog_posts, 'user': user}
    return render(request, 'blogs/my_blogs.html', context)

@user_passes_test(f.check_admin, login_url="/", redirect_field_name=None)
def delete_blog(request, blog_id):
    """Page to delete a specific blog and all associated posts."""
    blog = Blog.objects.get(id=blog_id)

    if request.method == 'POST':
        blog.delete()
        return redirect('/') # Go back to home page once blog deleted.
    
    context = {'blog': blog}
    
    return render(request, 'blogs/delete_blog.html', context)


def delete_post(request, blog_post_id):
    """Page for current user to delete their specific blog post."""
    post = BlogPost.objects.get(id=blog_post_id)
    blog = post.blog_to_post_under # Retrieve associated blog for redirect.
    f.check_blog_owner(post, request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('blogs:blog', blog_id=blog.id)
    
    context = {'post': post}

    return render(request, 'blogs/delete_post.html', context)