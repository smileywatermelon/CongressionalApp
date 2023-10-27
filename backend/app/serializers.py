from rest_framework import serializers

from .models import User, Profile, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ("user", "display_name")


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    like_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ("id", "profile", "text", "liked_users")


class PostChildSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    parent = PostSerializer(many=False)

    like_count = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ("id", "profile", "text", "parent")
