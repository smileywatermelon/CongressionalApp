from typing import Any
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

# redirects user to different urls
from django.shortcuts import HttpResponseRedirect

from .models import User, Profile, Post
from .forms import UserForm


class LoginRequired(LoginRequiredMixin):
    login_url = "/login/"
    redirect_field_name = "redirect_to"


class HomeView(LoginRequired, ListView):
    template_name = "user/index.html"
    paginate_by = 30
    queryset = Post.objects.filter(parent__isnull=True).all()


def profile_login(request):
    logout(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")
    return render(request, "user/login.html")


class ProfileCreate(CreateView):
    template_name = "user/create.html"
    model = Profile
    form_class = UserForm

    def get_success_url(self) -> str:
        return "/user/login/"


class ProfileDetail(LoginRequired, DetailView):
    template_name = "user/detail.html"
    queryset = Profile.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["posts"] = self.object.posts.all()

        return data

    def get_slug_field(self) -> str:
        return "user__username"


class ProfileEdit(LoginRequired, UpdateView):
    template_name = "user/settings.html"
    queryset = Profile

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

@login_required
def create_post(request):
    """creates post/tweets"""
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        tweet = request.POST.get("tweet")
        if tweet:
            post = Post.objects.create(profile=profile, text=tweet)
            post.save()
            return HttpResponseRedirect("/")
    return render(request, "post/create.html")


class PostDetail(LoginRequired, DetailView):
    template_name = "post/detail.html"
    model = Post

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data["parent"] = self.object.parent
        data["comments"] = self.object.replies.filter(parent=self.object).all()
        return data


# Base Code for Reference
@login_required
def post_reply(request, pk):
    if request.method == "POST":
        comment = request.POST.get('comment')
        post = Post.objects.filter(id=pk).first()
        reply = Post(parent = comment, Profile = request.user)
        reply.save()
        return HttpResponseRedirect('/') 
    return render(request, 'post/reply.html')


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, id=pk)

    user = request.user.profile

    if user.liked_posts.filter(id=post.id).exists():
        user.liked_posts.remove(post)
    else:
        user.liked_posts.add(post)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
