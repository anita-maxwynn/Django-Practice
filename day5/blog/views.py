from django.shortcuts import render, redirect
from .models import Blog
from .forms import BlogForm
from django.contrib import messages
# Create your views here.
def blog_list(request):
    blogs = Blog.objects.all()
    messages.success(request, 'Welcome to the Blog List!')
    return render(request, 'blog/blog_list.html', {'blogs': blogs})

def create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog_list')
        else:
            messages.error(request, 'There was an error in your form. Please correct it.')
            return render(request, 'blog/create_blog.html', {'form': form})
    else:
        messages.info(request, 'Please fill out the form to create a new blog post.')
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

def update(request,pk):
    blog =Blog.objects.get(id=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog_list')
    else:
        messages.info(request, 'You are editing the blog post.')
        form = BlogForm(instance=blog)
    return render(request, 'blog/update_blog.html', {'form': form, 'blog': blog})

def delete(request, pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect('blog_list')