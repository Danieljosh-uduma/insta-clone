from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from bs4 import BeautifulSoup
import requests
from django.contrib import messages


# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'a_post/home.html', context)

def post_create_view(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            # print(sourcecode.prettify())

            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image

            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title

            find_artist = sourcecode.select('a.owner-name')
            artist = find_artist[0].text.strip()
            post.artist = artist
              
            post.save() 
            messages.success(request, 'Post uploaded successfully')
            return redirect('home')
        
    context = {'form': form}
    return render(request, 'a_post/post_create.html', context)

def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    
    context = {'post': post}
    return render(request, 'a_post/post_delete.html', context)

def post_update_view(request, pk):
    post = Post.objects.get(id=pk)
    form = PostEditForm(instance=post)

    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successful')
            return redirect('home')
        
    context = {'post': post, 'form':form}
    return render(request, 'a_post/post_update.html', context)

def post_view(request, pk):
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk)
    return render(request, 'a_post/post_view.html', {'post': post})


