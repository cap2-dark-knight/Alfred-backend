from django.urls import path
from django.contrib.auth import views as auth_views
from .decorators import signin_required
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('crawl/', views.startCrawl, name='crawl'),
    path('crawldata', signin_required(views.CrawledDataView.as_view()), name='data'),
    path('accounts/signin', views.SigninView.as_view(), name='signin'),
    path('accounts/signup',views.SignupView.as_view(), name='signup'),
    path('accounts/signout', views.SignoutView.as_view(), name='signout'),
    path('accounts/user', signin_required(views.UserView.as_view()), name='user'),
    path('alert_time', signin_required(views.AlertTimeView.as_view()), name = 'alert_time'), 
    path('keyword',signin_required(views.KeywordView.as_view()), name='keyword'),
    path('keyword/smart',signin_required(views.SmartKeywordView.as_view()), name='smartkeyword'),
    path('keyword/<str:keyword>/update', signin_required(views.KeywordUpdateView.as_view()), name='keyword_update'),
    path('keyword/<str:keyword>/delete', signin_required(views.KeywordDeleteView.as_view()), name='keyword_delete'),
]
