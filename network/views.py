
import json
import traceback
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Post, User, Like, Comment


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    print(f"The user is {request.user}")
    user_likes = None

    if request.user.is_authenticated :
        likes = Like.objects.filter(user=request.user)
        user_likes = [like.post.id for like in likes]

    print(f"The user likes {user_likes}")

    return render(request, "network/index.html",{
        "posts": posts,
        "user_likes": user_likes
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
def like(request, post_id):
    if request.method == "PUT":
        print("Attempting to update the user like...")
        print(f"The post id is {post_id}")
        user = request.user
        body = json.loads(request.body)
        print(f"The message body from the client is { body }")
        response = ""
        count_likes = None
        liked = False
        message = None
        stat = None

        try:

            post = Post.objects.get(id=post_id)
            like = Like.objects.get(user=user, post=post)
            like.delete()
            message = "Post was successfully unliked."
            count_likes = Like.objects.filter(post=post).count()
            stat = 201
        except Post.DoesNotExist:
            print("The post does not exist. No action will be taken.")
            message = "The post does not exist. No action will be taken."
            stat = 400
            traceback.print_exc
        except Like.DoesNotExist:
            print("The user hasn't liked this post yet. We will now create a like entry on this post for the user.")
            Like.objects.create(user=user, post=post)
            liked = True
            message = "Post was successfully liked."
            count_likes = Like.objects.filter(post=post).count()
            stat = 201
            traceback.print_exc

    return JsonResponse({"liked": liked, "count_likes": count_likes, "message": message }, status=stat)

    
