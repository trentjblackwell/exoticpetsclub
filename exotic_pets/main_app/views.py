from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Photo
import uuid
import boto3
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector5'

class PostCreate(CreateView):
    model = Post
    fields = '__all__'
    success_url ='/posts/'

class PostUpdate(UpdateView):
    model = Post
    fields = '__all__'

class PostDelete(DeleteView):
    model = Post
    success_url = '/posts/'

def home(request):
    return render(request, 'home.html')

def posts_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/detail.html', {'post': post})

def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)