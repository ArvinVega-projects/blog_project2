from django import forms

from .models import Blog, BlogPost

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['text']
        labels = {'text': ''}


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['blog_to_post_under', 'title', 'text',]
        labels = {'blog_to_post_under': 'Post Under:', 'title': 'Title', 'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 40}),
            }