from django.urls import path
from .views import homePage, detailPage, createPage, updatePage, deletePage

app_name = 'blog_app'

urlpatterns = [
    path('', homePage, name="home"),
    path('post/<slug:slug>/', detailPage, name="detail"),
    path('create-post', createPage, name="create"),
    path('update-post/<slug:slug>/', updatePage, name="update"),
    path('delete-post/<slug:slug>/', deletePage, name="delete"),

    # path('profile/<int:pk>', profile, name='user-profile'),

    # path('profile/<username>', profile, name="profile"),
    # path('profile/<str:pk>', profile, name='user-profile'),
]
