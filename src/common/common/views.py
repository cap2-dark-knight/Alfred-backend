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
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils import timezone

from .crawler import general_crawler, smart_crawler
from .models import CrawledData, Keyword, Profile, SmartKeywordInfo


@ensure_csrf_cookie
def index(request):
    return JsonResponse({'result':'success'}, status=200)


def startCrawl(request):
    crawl_thr = threading.Thread(target=doCrawl)
    crawl_thr.setDaemon(True)
    crawl_thr.start()
    del_thr = threading.Thread(target=deleteData)
    del_thr.setDaemon(True)
    del_thr.start()
    return JsonResponse({'result':'success'}, status=200)

def doCrawl():
    keywords = Keyword.objects.all()
    for keyword in keywords:
        datalist = []
        if keyword.get_smartkeywordinfo() == None : 
            datalist = general_crawler(keyword.keyword)
        else:
            selector = keyword.get_smartkeywordinfo()
            type = selector['type']
            datalist = smart_crawler(type, keyword.keyword, selector)
        for d in datalist :
            CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])

def doCrawlByKeyword(keyword):
    datalist = []
    if keyword.get_smartkeywordinfo() == None : 
        datalist = general_crawler(keyword.keyword)
    else:
        selector = keyword.get_smartkeywordinfo()
        type = selector['type']
        datalist = smart_crawler(type, keyword.keyword, selector)
    for d in datalist :
        CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])

def deleteData():
    CrawledData.objects.filter(updated_time__lte=timezone.now()-timedelta(days=1)-timedelta(hours=1)).delete()


class CrawledDataView(APIView):
    def get(self, request):
        keywords = Keyword.objects.filter(follower=request.user)
        data = CrawledData.objects.filter(keywords__in=keywords).values()
        return Response({"crawled_data":data}, status=200)

class SigninView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = auth.authenticate(request, username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return Response({'result':'success'}, status=200)
        else:
            return Response({'result':'fail'}, status=200)

class SignupView(APIView):

    def post(self, request):
        password = request.data['password']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        if User.objects.filter(username=email).exists():
            return Response({'result':'fail','info':'email already exists'},200)
        else:
            user = User.objects.create_user(username = email, email=email, password=password, first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user)
            auth.login(request, user)
            return Response({'result':'success'}, status=201)

class SignoutView(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response({'result':'success'},status=200)


class KeywordView(APIView):
    def get(self, request):
        obj_keyword = Keyword.objects.filter(follower=request.user).values()
        return Response({'keywords': obj_keyword}, status=200)

class KeywordUpdateView(APIView):
    def put(self, request, keyword):
        obj_keyword = Keyword.objects.filter(keyword=keyword)
        if obj_keyword.count()==0 :
            obj_obj_keyword = Keyword(keyword = keyword,check_smartkeyword=False)
            obj_obj_keyword.save()
            obj_obj_keyword.follower.add(request.user)
            thr = threading.Thread(target=doCrawlByKeyword,args=[obj_obj_keyword])
            thr.setDaemon(True)
            thr.start()
            obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
            return Response({'result':'success','keywords':obj_updated_keyword},status=200)
        else:
            obj_obj_keyword = Keyword.objects.filter(keyword=keyword, follower=request.user)
            if obj_obj_keyword.count() == 0:
                print(serializers.serialize('json', obj_keyword))
                obj_keyword[0].follower.add(request.user)
                obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
                return Response({'result':'success','keywords':obj_updated_keyword},status=200)
            else:
                obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
                return Response({'result':'fail','info':'keyword already exists','keywords':obj_updated_keyword},status=200)
            

class KeywordDeleteView(APIView):
    def delete(self, request, keyword):
        obj_keyword = Keyword.objects.filter(keyword=keyword, follower=request.user)
        if obj_keyword.count()!= 0 :
            obj_keyword[0].follower.remove(request.user)
            obj_updated_keyword = Keyword.objects.filter(follower=request.user).values()
            return Response({'result':'success','keywords':obj_updated_keyword},status=200)
        else : 
            return Response({'result':'fail','info':'object does not exist'},status=200)


class SmartKeywordView(APIView):
    def get(self, request):
        obj_smartkeyword = Keyword.objects.filter(check_smartkeyword=True).values()
        return Response({'result':'success','keywords':obj_smartkeyword},status=200)

class UserView(APIView):
    def get(self, request):
        user = {
            'email' : request.user.email,
            'first_name' : request.user.last_name,
            'last_name':request.user.first_name,
            'data_period' : Profile.objects.filter(user=request.user).values().first()['data_period']
        }
        return Response({'result':'success','user' : user},status=200)

class SmartKeywordView(APIView):
    def get(self, request):
        obj_smartkeywords = Keyword.objects.filter(~Q(smartkeywordinfo=None)).values()
        return Response({'result':'success','smartkeywords' : obj_smartkeywords },status=200)