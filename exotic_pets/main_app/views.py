from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def posts_index(request):
    posts=[]
    return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, post_id):
    post = []
    return render(request, 'posts/detail.html', {'post': post})