
from django.urls import path

from . import views

from django.conf.urls.static import static

from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API Routes
    path("post", views.post, name="post"),
    path("post/<int:post_id>", views.like, name="like"),
    path("post/edit/<int:post_id>", views.edit, name="edit"),
    path("following", views.following, name="following"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("profile/<str:username>/follow", views.follow, name="follow")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)