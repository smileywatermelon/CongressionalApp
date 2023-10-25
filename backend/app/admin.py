from django.contrib import admin
from .models import User, Profile, Post


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ("user", "display_name", "following")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fields = ("profile", "text", "parent")
