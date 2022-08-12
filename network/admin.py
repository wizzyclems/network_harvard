from django.contrib import admin

# Register your models here.
from .models import Following, Post, Comment, Like, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("id","username","first_name","last_name", "email" )


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Following)
