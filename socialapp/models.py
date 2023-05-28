from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
# to get the model of the currently authenticated user
# Create your models here.

User = get_user_model()
# this will get the model of the currently login user

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    # user might not want to put any bio
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='img3.jpg')
    # django create it manually we can as well put defualt profile
    location = models.CharField(max_length=100, blank=True)

    # media allow user to store videos image create a folder media

    def __str__(self):
        return self.user.username 
    

class Post(models.Model):
    # to use uniquik id
    id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_like = models.IntegerField(default=0)


    def __str__(self):
        return self.user
    

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

class FollowersCount(models.Model):
    follower =models.CharField(max_length=200)
    user = models.CharField(max_length=200)

    def __str_(self):
        return self.user