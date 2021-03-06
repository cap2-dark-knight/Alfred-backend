import json
import threading

from django.contrib import auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import OneToOneField
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db.models import Q
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils import timezone
from django.middleware.csrf import get_token
from .crawler import general_crawler, smart_crawler
from .models import CrawledData, Keyword, Profile, SmartKeywordInfo


class ExemptCSRFSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def startCrawl(request):
    crawl_thr = threading.Thread(target=doCrawl)
    crawl_thr.setDaemon(True)
    crawl_thr.start()
    del_thr = threading.Thread(target=deleteData)
    del_thr.setDaemon(True)
    del_thr.start()
    return JsonResponse({'result': 'success'}, status=200)


def doCrawl():
    keywords = Keyword.objects.all()
    for keyword in keywords:
        datalist = []
        if keyword.get_smartkeywordinfo() == None:
            datalist = general_crawler(keyword.keyword)
        else:
            selector = keyword.get_smartkeywordinfo()
            type = selector['type']
            datalist = smart_crawler(type, keyword.keyword, selector)
        for d in datalist:
            CrawledData.objects.create(
                keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])


def doCrawlByKeyword(keyword):
    now = timezone.now()
    now_h = now-timedelta(minutes=now.minute)-timedelta(seconds=now.second)
    print("keyword:"+str(keyword))
    datalist = []
    if keyword.get_smartkeywordinfo() == None:
        datalist = general_crawler(keyword.keyword)
    else:
        selector = keyword.get_smartkeywordinfo()
        type = selector['type']
        datalist = smart_crawler(type, keyword.keyword, selector)
    for d in datalist:
        for i in range(24):
            creates = CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])
            CrawledData.objects.filter(pk=creates.pk).update(updated_time=now_h-timedelta(hours=i))
    print("keyword:"+str(keyword))



def deleteData():
    CrawledData.objects.filter(updated_time__lte=timezone.now()-timedelta(days=1)-timedelta(hours=1)).delete()


class CrawledDataView(APIView):
    def get(self, request):
        keywords = Keyword.objects.filter(follower=request.user)

        alert_times = Profile.objects.filter(user=request.user)[
            0].get_alert_time_list()
        target_time = None
        now = timezone.now()
        now_h = timezone.now().hour
        now_date = now - timedelta(hours=now_h)-timedelta(minutes=now.minute) - timedelta(seconds=now.second)

        for t in alert_times:
            if t - now_h <= 0:
                target_time = now_date+timedelta(hours=t)

        if target_time == None:
            target_time = now_date - timedelta(days=1)+timedelta(hours=alert_times[-1])

        data = {}
        data = CrawledData.objects.filter(
            keywords__in=keywords,
            updated_time__range=[target_time-timedelta(minutes=29), target_time+timedelta(minutes=30)]
        ).values()

        return Response({"crawled_data": data}, status=200)


class SigninView(APIView):
    authentication_classes = (
        ExemptCSRFSessionAuthentication, BasicAuthentication)

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return Response({'result': 'success'}, status=200)
        else:
            return Response({'result': 'fail'}, status=200)


class SignupView(APIView):
    authentication_classes = (
        ExemptCSRFSessionAuthentication, BasicAuthentication)

    def post(self, request):
        password = request.data['password']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        if User.objects.filter(username=email).exists():
            return Response({'result': 'fail', 'info': 'email already exists'}, 200)
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user)
            auth.login(request, user)
            return Response({'result': 'success'}, status=201)


class SignoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response({'result': 'success'}, status=200)


class KeywordView(APIView):
    def get(self, request):
        obj_keyword = Keyword.objects.filter(follower=request.user).values()
        return Response({'keywords': obj_keyword}, status=200)


class KeywordUpdateView(APIView):
    authentication_classes = (ExemptCSRFSessionAuthentication, BasicAuthentication)

    def put(self, request, keyword):
        obj_keyword = Keyword.objects.filter(keyword=keyword)
        if obj_keyword.count() == 0:
            obj_obj_keyword = Keyword(keyword=keyword)
            obj_obj_keyword.save()
            obj_obj_keyword.follower.add(request.user)
            #thr = threading.Thread(target=doCrawlByKeyword, args=[obj_obj_keyword])
          #  thr.setDaemon(True)
           # thr.start()
            doCrawlByKeyword(obj_obj_keyword)
            obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
            return Response({'result': 'success', 'keywords': obj_updated_keyword}, status=200)
        else:
            obj_obj_keyword = Keyword.objects.filter(
                keyword=keyword, follower=request.user)
            if obj_obj_keyword.count() == 0:
                print(serializers.serialize('json', obj_keyword))
                obj_keyword[0].follower.add(request.user)
                obj_updated_keyword = Keyword.objects.filter(
                    follower=request.user).values()
                return Response({'result': 'success', 'keywords': obj_updated_keyword}, status=200)
            else:
                obj_updated_keyword = Keyword.objects.filter(
                    follower=request.user).values()
                return Response({'result': 'fail', 'info': 'keyword already exists', 'keywords': obj_updated_keyword}, status=200)


class KeywordDeleteView(APIView):
    authentication_classes = (
        ExemptCSRFSessionAuthentication, BasicAuthentication)

    def delete(self, request, keyword):
        obj_keyword = Keyword.objects.filter(
            keyword=keyword, follower=request.user)
        if obj_keyword.count() != 0:
            obj_keyword[0].follower.remove(request.user)
            obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
            return Response({'result': 'success', 'keywords': obj_updated_keyword}, status=200)
        else:
            return Response({'result': 'fail', 'info': 'object does not exist'}, status=200)


class UserView(APIView):
    def get(self, request):
        print(request)
        try:
            alert_times = request.user.profile.get_alert_time_list()
            user = {
                'email': request.user.email,
                'last_name': request.user.last_name,
                'first_name': request.user.first_name,
                'alert_times': alert_times
            }
            return Response({'result': 'success', 'user': user}, status=200)
        except:
            return Response({'result': 'fail', 'info': 'Profile no exist'}, status=200)


class AlertTimeView(APIView):
    authentication_classes = (
        ExemptCSRFSessionAuthentication, BasicAuthentication)

    def post(self, request):
        try:
            alert_times = request.data['alert_times']
            alert_time_int = 0
            for alert_time in alert_times:
                alert_time_int += (0b1 << alert_time)
            if alert_time_int == 0:
                return Response({'result': 'fail', 'info': 'Please select at least one option'}, status=200)
            else:
                obj_profile = request.user.profile
                obj_profile.alert_times = alert_time_int
                obj_profile.save()
                return Response({'result': 'success', 'alert_times': obj_profile.get_alert_time_list()}, status=200)
        except:
            return Response({'result': 'fail', 'info': 'Please check the data format.'}, status=200)

    def get(self, request):
        alert_times = Profile.objects.filter(user=request.user)[
            0].get_alert_time_list()
        return Response({'result': 'success', 'alert_times': alert_times}, status=200)


class SmartKeywordView(APIView):
    def get(self, request):
        obj_smartkeywords = Keyword.objects.filter(
            ~Q(smartkeywordinfo=None)).values()
        return Response({'result': 'success', 'smartkeywords': obj_smartkeywords}, status=200)
