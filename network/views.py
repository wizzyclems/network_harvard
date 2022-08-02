
import traceback
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Post, User, Like, Comment


def index(request):
    posts = Post.objects.all().order_by("-timestamp")

    return render(request, "network/index.html",{
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# @csrf_exempt
@login_required
def post(request):
    if request.method == 'POST':
        print("trying to make a post")
        post = request.POST["post"]
        user = request.user
        post = Post.objects.create(post=post, user=user)
        post.save()
        print(f"The user attempting to post is : {user}")
        print(f"The post is : {post}")
        return HttpResponseRedirect(reverse("index"))
    else: 
        print("Not a post request but Getter")


@csrf_exempt
@login_required
def like(request):
    if request.method == "UPDATE":
        print("Attempting to update the user like...")
        user = request.user
        post_id = request.UPDATE["post_id"]

        try:
            post = Post.objects.get(id=post_id)
            like = Like.objects.get(user=user, post=post)
            if like:
                like.delete()
            else:
                like = Like.objects.create(user=user, post=post_id)
                like.save()

        except IntegrityError:
            traceback.print_exc
