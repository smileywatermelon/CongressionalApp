from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import routers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import User, Profile, Post
from .serializers import ProfileSerializer, PostSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default objects to retrieve
    page_size_query_param = "page_size"
    max_page_size = 100  # Max objects to retrieve


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Users
    """

    pagination_class = StandardResultsSetPagination
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for Posts
    """

    pagination_class = StandardResultsSetPagination
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeView(APIView):
    def get(self, request):
        pass


router = routers.SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r"posts", PostViewSet)
