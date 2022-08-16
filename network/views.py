
import json
import traceback
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Following, Post, User, Like, Comment



def index(request):

    posts = Post.objects.all().order_by("-timestamp")
    

    meta = { 
            "components_to_show" : ("make_post","posts")
        }

    return load_posts(request=request, posts=posts, meta_data=meta)



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
        print("Inside the login view. Now time to redirect to login page.")
        return render(request, "network/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        bio = request.POST["bio"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password.strip() != confirmation.strip() or len(password.strip()) <= 2 :
            return render(request, "network/register.html", {
                "message": "Passwords must match and contain more than 2 characters."
            })

        if len(username.strip()) <= 2 :
            return render(request, "network/register.html", {
                    "message": "Username must contain more than 2 characters."
            })

        #Ensure the username does not already exist.
        if get_user(username.lower()) :
            return render(request, "network/register.html", {
                "message": "Username already in use."
            })

        if request.FILES and request.FILES.get("photo") :
            filename = request.FILES.get("photo").name
            filename_parts = filename.split(".")
            extension = filename_parts[ len(filename_parts)-1 ]
            request.FILES.get("photo").name = request.POST["username"].lower() + "." + extension.lower()
            photo = request.FILES.get("photo")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
               first_name=firstname, last_name=lastname, bio=bio, photo=photo)

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



@csrf_exempt
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
def edit(request, post_id):
    
    if request.method == 'PUT':
        user = request.user
        try:
            post = Post.objects.get(id=post_id)

            if user != post.user:
                print("You cannot edit another user's post.")
                return JsonResponse({"post_id": post.id, "message": "You cannot edit another user's post.", "status":401 }, status=401) 

            request_body = json.loads(request.body)
            print(f"the edit post request body is {request_body}")
            post_content = request_body.get("post_content")
            print("trying to make a post")
            
            post.post = post_content
            post.save()
        except Post.DoesNotExist:
            traceback.print_exc
            return JsonResponse({"post_id": post_id, "message": "The requested post does not exist.", "status":400 }, status=400) 

        return JsonResponse({"post_id": post.id, "message": "Your post was successfully edited.", "status":201 }, status=201) 
    else: 
        print("Not a post request but Getter")



@csrf_exempt
def like(request, post_id):
    if request.user.is_authenticated :
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
    else:
        print("The user is not authenticated. Trigger login operation")
        liked = False
        message = "The user is not authenticated. Request login."
        count_likes = 0
        stat = 403


    return JsonResponse({"liked": liked, "count_likes": count_likes, "message": message, "status":stat }, status=stat)



def authenticate_user(request):
    pass



""""
This method loads the posts from the users the currently logged in user follows.
These posts are ordered by the timestamp in descendingly.
"""
@login_required
def following(request):
    
    #This is a bit complicated access to multiple objects using the related name relationship.
    posts = Post.objects.filter(user__followed__user_following=request.user).order_by("-timestamp")
    

    meta = { 
            "components_to_show": ("posts")
        }

    return load_posts(request=request, posts=posts, meta_data=meta)



def profile(request, username):

    posts = Post.objects.filter(user__username=username).order_by("-timestamp")
    
    user_following = request.user
    follows_user = False
   
    if request.user.is_authenticated :
        try:
            following = Following.objects.get(user_following=user_following, user_followed__username=username)
            follows_user = True
        except Following.DoesNotExist:
            follows_user = False

    count_user_follows = Following.objects.filter(user_following__username=username).count()
    count_followers = Following.objects.filter(user_followed__username=username).count()

    profile_user = get_user(username=username)
    print(f"The profile user is : {profile_user}")


    meta = { 
            "components_to_show": ("profile", "posts"),
            "profile_user": profile_user,
            "follows_user": follows_user,
            "followers_count": count_followers,
            "count_user_follows": count_user_follows
        }

    return load_posts(request=request, posts=posts, meta_data=meta)



"""
This re-usable method loads related posts and likes of the current user to be rendered in the index.html
template page.

It is called by the following methods
    a. profile
    b. index 
    c. following

"""
def load_posts(request, posts, user_likes=None, 
    meta_data={
        "components_to_show" : None, 
        "profile_user" : None, 
        "follows_user" : None,
        "followers_count": 0,
        "count_user_follows": 0
    }):

    if request.user.is_authenticated :
        likes = Like.objects.filter(user=request.user)
        user_likes = [like.post.id for like in likes]
    else:
        print("The user is not authenticated.")

    paginator = Paginator(posts, 10)
    page_number = 1

    try:
        page_number = request.GET.get('page')
    except Exception:
        print("The paginator page number threw and exception.")
        traceback.print_exc

    new_posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts" : new_posts,
        "user_likes" : user_likes,
        "meta" : meta_data
    })



@login_required
def follow(request, username):
    print(f"The user to follow is { username }")
    print(f"The user following is {request.user}")

    user_following = request.user
    user_followed = User.objects.get(username=username)

    try:

        following = Following.objects.get(user_following=user_following, user_followed=user_followed)
        following.delete()

    except Following.DoesNotExist:
        print("The user hasn't liked this post yet. We will now create a like entry on this post for the user.")
        Following.objects.create(user_following=user_following, user_followed=user_followed)
        traceback.print_exc

    return HttpResponseRedirect(reverse("profile",kwargs={"username": username}))

    
def get_user(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        traceback.print_exc

    return user


