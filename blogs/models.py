from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    """The model for a blog."""
    text = models.CharField(max_length=43)
    date_made = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text

class BlogPost(models.Model):
    """The specific post for a blog."""
    blog_to_post_under = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    title = models.CharField(null=True, max_length=64) # Post title
    text = models.TextField(null=True) # Post entry
    date_made = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return str(self.title)


