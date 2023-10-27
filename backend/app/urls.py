
from django.urls import path, include
from django.views.generic import RedirectView

from .views import (
    HomeView,
    PostDetail,
    ProfileCreate, ProfileDetail, logout_view,
    post_like, post_reply, profile_login, create_post
)
from . import views

from .views_api import (
    router
)

urlpatterns = [
    path("", HomeView.as_view(), name = ""),

    # User 
	path('user/', RedirectView.as_view(url='/'), name='user-redirect'),
    path('user/login/', views.profile_login, name = 'user-login'),
    path('user/signup/', ProfileCreate.as_view(), name='user-signup'),
	path('user/@<str:slug>/', ProfileDetail.as_view(), name='user-detail'),
    path('post/create/', views.create_post, name = 'post-create'),
    path('post/<pk>/', PostDetail.as_view(), name='post-detail'),
    path('post/<int:pk>/like/', post_like, name='post-like'),
    path('post/<str:pk>/reply/', views.post_reply, name = 'reply'),
    
    # Redirects
    path('signup/', RedirectView.as_view(url='/user/signup/')),
    path('login/', RedirectView.as_view(url='/user/login/')),
    path("user/logout/", logout_view, name="logout"),

    path('api/', include(router.urls))
]