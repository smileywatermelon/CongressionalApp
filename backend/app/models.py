from django.db.models import Q
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
    display_name = models.CharField(max_length=40, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )
    liked_posts = models.ManyToManyField("Post", related_name="liked_users", blank=True)

    @property
    def username(self):
        return self.user.username

    def __str__(self):
        return f"{self.username} - {self.id}"


@receiver(post_save, sender=Profile)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance.user)


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=500, blank=True)

    # Allow to be used as a comment
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent:
            return f"{self.user.username} - {self.pk}, {self.user.username} - {self.parent.pk}"
        return f"{self.user.username} - {self.pk}"

    @property
    def user(self):
        return self.profile

    @property
    def children(self):
        return Post.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    @property
    def like_count(self):
        return self.liked_users.count()
