from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Post

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    success_url ='/posts/'

def home(request):
    return render(request, 'home.html')

def posts_index(request):
    posts=[]
    return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, post_id):
    post = []
    return render(request, 'posts/detail.html', {'post': post})

