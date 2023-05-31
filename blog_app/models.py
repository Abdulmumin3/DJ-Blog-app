from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFill

# Create your models here.
# class User(AbstractUser):
#     pass

class User(AbstractUser):
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    
    profile_picture = ProcessedImageField(default='default.jpeg', blank=True, upload_to='images', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    #avatar =
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, default='')
    tags = models.ManyToManyField('Tag')
    # image = models.ImageField(default='', blank=True, upload_to='images')
    image_thumbnail = ProcessedImageField(default='', blank=True, upload_to='images', processors=[ResizeToFill(350, 200)], format='JPEG', options={'quality': 60})
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save()
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={"slug": self.slug})

    class Meta: 
        ordering = ['-created_at']    
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=256)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comment by "{self.name}" on {self.post}'
    
class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, default='')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save()
          
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     profile_picture = ProcessedImageField(default='default.jpeg', blank=True, upload_to='images', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
#     bio = models.TextField()
#     def __str__(self):
#         return f'{self.user.username} Profile'