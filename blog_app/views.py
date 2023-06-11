from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Tag, User
from .forms import PostCreateForm, LoginForm, SignupForm, CommentForm, UpdateUserForm
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth import get_user_model
# Create your views here.

def landPage(request):
    return render(request, 'blog_app/land-page.html',)

@login_required
def homePage(request):
    tags = Tag.objects.all()
    q = request.GET.get('q', None)
    if q is None or q is "":
        posts = Post.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 4)
        try:
            postss = paginator.page(page)
        except PageNotAnInteger:
            postss = paginator.page(1)
        except EmptyPage:
            postss = paginator.page(paginator.num_pages)
    elif q is not None:
        posts = Post.objects.filter(title__contains=q)
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 4)
        try:
            postss = paginator.page(page)
        except PageNotAnInteger:
            postss = paginator.page(1)
        except EmptyPage:
            postss = paginator.page(paginator.num_pages)
    return render(request, 'blog_app/home-page.html', {'postss': postss, 'tags':tags})

@login_required
def tags(request, slug):
    postss = Post.objects.filter(tags__slug=slug)
    return render(request, 'blog_app/home-page.html', {'postss': postss})

@login_required
def detailPage(request, slug):
    comment_form = CommentForm()
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    #tags = post.tags.all()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment was created successfully!')
    return render(request, 'blog_app/detail-page.html', {'post': post, 'comments':comments, 'new_comment':new_comment, 'comment_form':comment_form,})

@login_required
def createPage(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # tags = form.cleaned_data.get("tags")
            # for tag in tags:
            #     instance.tags.add(tag)
            # tags = form.cleaned_data.get("tags")
            # instance.tags.add(*tags)
            instance.author = request.user
            instance.image_thumbnail = form.cleaned_data.get('image_thumbnail')
            instance.save()
            tags = form.cleaned_data.get("tags")
            for tag in tags:
                instance.tags.add(tag)
            instance.save()
            return redirect('blog_app:home')
    return render(request, 'blog_app/create-page.html', {'form':form})

@login_required
def updatePage(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise Http404
    form = PostCreateForm(instance=post)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image_thumbnail = form.cleaned_data.get('image_thumbnail')
            instance.author = request.user
            tags = form.cleaned_data.get("tags")
            for tag in tags:
                instance.tags.add(tag)
            instance.save()
            
            return redirect('blog_app:home')
    return render(request, 'blog_app/update-page.html', {'form':form, 'post':post})

@login_required
def deletePage(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise Http404
    if request.method == 'POST':
        post.delete()
        return redirect('blog_app:home')
    return render(request, 'blog_app/delete-page.html', {'post':post})

def loginPage(request):
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('blog_app:home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'],)
            if user is not None:
                login(request, user)
                return redirect('blog_app:home')
            else:
                messages.error(request, 'User credentials not correct')
    return render(request, 'blog_app/login-page.html', {'form':form,})

def logoutPage(request):
    logout(request)
    return redirect('login')

def signupPage(request):
    form = SignupForm()
    if request.user.is_authenticated:
        return redirect('blog_app:home')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            messages.success(request, 'You can login successfully now!')
            return redirect('login')
    return render(request, 'blog_app/signup-page.html', {'form':form,})


# @login_required
# def profile(request, pk):
#     user_form = None
#     profile_form = None
#     user = get_object_or_404(User, pk=pk)
#     profile = get_object_or_404(Profile, pk=pk)
#     if request.method == 'POST':
#         user_form = UpdateUserForm(request.POST, instance=user)
#         profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile)

#         if user_form.is_valid() and profile_form.is_valid(): 
#             user = user_form.save(commit=False)
#             user_form.save()
#             profile_form.save()
#             messages.success(request, 'Your profile is updated successfully')
#             return redirect('users-profile', pk)
#     else:
#         user_form = UpdateUserForm(instance=request.user)
#         profile_form = UpdateProfileForm(instance=profile)

#     return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def profile(request, pk):
    user = User.objects.get(id=pk)
    posts = Post.objects.filter(author=user)
    return render(request, 'users/profile.html', {'user':user, 'posts':posts})

@login_required
def account(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    user_form = UpdateUserForm(instance=user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            instance = user_form.save(commit=False)
            instance.profile_picture = user_form.cleaned_data.get('profile_picture')
            instance.email = user.email
            instance.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user-acccount')
    return render(request, 'users/account.html', {'user':user, 'posts':posts, 'user_form':user_form})