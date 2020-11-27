from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('index/', views.index, name='index'),
    path('crawl/', views.startCrawl, name='crawl'),
    path('accounts/signin', views.SigninView.as_view(), name='signin'),
    path('accounts/signup',views.SignupView.as_view(), name='signup'),
    path('keyword',views.KeywordView.as_view(), name='keyword'),
    path('keyword/<str:keyword>/update', views.KeywordUpdateView.as_view(), name='keyword_update'),
    path('keyword/<str:keyword>/delete', views.KeywordDeleteView.as_view(), name='keyword_delete'),
]
