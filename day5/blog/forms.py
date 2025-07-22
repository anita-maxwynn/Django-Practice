from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'image']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter an engaging title for your blog post...',
                'style': 'font-size: 1.1rem;'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Share your thoughts, stories, and ideas here...',
                'style': 'font-size: 1rem; line-height: 1.6;'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name',
                'style': 'font-size: 1rem;'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        
        labels = {
            'title': 'Blog Title',
            'content': 'Content',
            'author': 'Author Name',
            'image': 'Featured Image',
        }
        
        help_texts = {
            'title': 'Create a catchy title that grabs attention (max 200 characters)',
            'content': 'Write your blog content. You can include stories, insights, tutorials, or any thoughts you want to share.',
            'author': 'Enter your name or pen name',
            'image': 'Upload an image to make your post more engaging (optional)',
        }
        
        error_messages = {
            'title': {
                'required': 'Please provide a title for your blog post.',
                'max_length': 'Title must be less than 200 characters.',
            },
            'content': {
                'required': 'Please write some content for your blog post.',
            },
            'author': {
                'required': 'Please enter the author name.',
                'max_length': 'Author name must be less than 100 characters.',
            },
        }