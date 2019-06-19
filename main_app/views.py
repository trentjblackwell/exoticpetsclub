from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Photo, Comment
from .forms import CommentForm
import uuid
import boto3
from django.db.models import Q


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector5'

class SearchResult(ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
      query = self.request.GET.get('q')
      object_list = Post.objects.filter(
      Q(title__istartswith=query)
      )
      print(query)
      print (object_list)
      return object_list

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'price', 'contact']
    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form)
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/posts/'

def home(request):
    return render(request, 'home.html')

def posts_index(request):
    posts = Post.objects.all()
    return render(request, 'posts/index.html', {'posts': posts})

def posts_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    comment_form = CommentForm()
    print(user)
    return render(request, 'posts/detail.html', {
        'post': post, 
        'user': user,
        'comment_form': comment_form,
        })

@login_required
def user_index(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'main_app/user_index.html', {'posts': posts})


def add_comment(request, post_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_id = post_id
        new_comment.save()
    return redirect('detail', post_id=post_id)

@login_required
def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        print(photo_file)
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, post_id=post_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', post_id=post_id)

def delete_photo(request, post_id, photo_id):
    # start_pos captures index of item right after last slash 
    # key slices url using start_pos, capturing the photo name
    photo = Photo.objects.get(id=photo_id)
    s3 = boto3.client('s3')
    start_pos = photo.url.rfind('/') + 1
    key = photo.url[start_pos:]
    s3.delete_object(Bucket= 'catcollector5', Key=key)
    Photo.objects.get(id=photo_id).delete()
    return redirect('detail', post_id=post_id)

def delete_comment(request, post_id, comment_id):
    Comment.objects.get(id=comment_id).delete()
    return redirect('detail', post_id=post_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)