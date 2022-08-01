
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