
from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models


class User(AbstractUser):
    pass



def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Post(models.Model):
    
    post = models.CharField(max_length=255, blank=False, editable=True)
    user = models.ForeignKey(User, related_name="posted_by", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=False)




class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comment_on", on_delete=models.CASCADE)
    comment = models.CharField(max_length=255, blank=False, editable=False)
    user = models.ForeignKey(User, related_name="comment_by", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=False)



class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="liked_by", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, null=False)




class Following(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=False)
    """This field identifies the user that is doing the following"""
    user_following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    """This field identifies the user that is being followed"""
    user_followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)

    
