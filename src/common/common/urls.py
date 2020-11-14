from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('index/', views.index, name='index'),
    path('accounts/signin', views.SigninView.as_view(), name='signin'),
    path('accounts/signup',views.SignupView.as_view(), name='signup'),
]
