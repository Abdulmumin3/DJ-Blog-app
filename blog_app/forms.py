from django import forms
from django.forms import ModelForm
from .models import Post, Comment, User 
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Tag
from imagekit.forms import ProcessedImageField 
from imagekit.processors import ResizeToFill



class PostCreateForm(ModelForm):
    title = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Task title', 'class': 'w-full py-4 px-6 rounded-xl'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Task body', 'class': 'w-full py-4 px-6 rounded-xl'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)
    image_thumbnail = ProcessedImageField(spec_id='blog_app:Post:image_thumbnail', processors=[ResizeToFill(350, 200)], format='JPEG', options={'quality':60})
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'image_thumbnail']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'w-full py-4 px-6 rounded-xl'}))
    password = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Your password', 'class': 'w-full py-4 px-6 rounded-xl'}))

class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'w-full py-4 px-6 rounded-xl'}))
    password1 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Your password', 'class': 'w-full py-4 px-6 rounded-xl'}))
    password2 = forms.CharField(max_length=256, widget=forms.PasswordInput(attrs={'placeholder': 'Your password', 'class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(max_length=256, widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'w-full py-4 px-6 rounded-xl'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        
class CommentForm(ModelForm):
    name = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'w-full py-4 px-6 rounded-xl'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment', 'class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.CharField(max_length=256, widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'w-full py-4 px-6 rounded-xl'}))
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body',]
        
class UpdateUserForm(ModelForm):
    username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'w-full py-4 px-6 rounded-xl'}))
    email = forms.EmailField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your email', 'class': 'w-full py-4 px-6 rounded-xl'}))
    profile_picture = ProcessedImageField(spec_id='blog_app:Profile:profile_picture', processors=[ResizeToFill(350, 200)], format='JPEG', options={'quality':60})
    bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class': 'w-full py-4 px-6 rounded-xl'}))
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_picture']
        
# class UpdateProfileForm(ModelForm):
#     profile_picture = ProcessedImageField(spec_id='blog_app:Profile:profile_picture', processors=[ResizeToFill(350, 200)], format='JPEG', options={'quality':60})
#     bio = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class': 'w-full py-4 px-6 rounded-xl'}))
#     username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your username', 'class': 'w-full py-4 px-6 rounded-xl'}))
#     email = forms.EmailField(max_length=256, widget=forms.TextInput(attrs={'placeholder': 'Your email', 'class': 'w-full py-4 px-6 rounded-xl'}))
#     class Meta:
#         model = Profile
#         fields = ['profile_picture', 'bio']
        

