from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Keyword,CrawledData,Profile
from .crawler import general_crawler
import threading

def index(request):
    return HttpResponse("TEST!")


def startCrawl(request):
    thr = threading.Thread(target=doCrawl)
    thr.setDaemon(True)
    thr.start()
    return HttpResponse("Crawling")

def doCrawl():
    keywords = Keyword.objects.all()
    for keyword in keywords:
        datalist = general_crawler(keyword.keyword)
        for d in datalist :
            CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])

def doCrawlByKeyword(keyword):
    datalist = general_crawler(keyword.keyword)
    for d in datalist :
        CrawledData.objects.create(keywords=keyword, url=d['url'], title=d['title'], content=d['contents'], image_url=d['img'])

class CrawledDataView(APIView):
    def get(self, request):
        keywords = Keyword.objects.filter(follower=request.user)
        data = CrawledData.objects.filter(keywords__in=keywords)
        print("data" + serializers.serialize('json', data))
        
        return Response("ok", status=200)

class SigninView(APIView):
    def get(self, request):
        return Response("ok", status=200)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return Response("ok", status=200)

        else:
            return Response("fail",401)

class SignupView(APIView):

    def post(self, request):
        username = request.data['email']
        password = request.data['password']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        if User.objects.filter(username=username).exists():
            return Response("duplicated username",401)
        elif User.objects.filter(email=email).exists():
            return Response("duplicated email",401)
        else:
            user = User.objects.create_user(username = email, email=email, password=password, first_name=first_name, last_name=last_name)
            Profile.objects.create(user=user)
            auth.login(request, user)
            return Response("ok", status=200)


class KeywordView(APIView):
    def get(self, request):
        obj_keyword = Keyword.objects.filter(follower=request.user)
        qs_keyword = serializers.serialize('json', obj_keyword)
        return Response(qs_keyword, status=200)

class KeywordUpdateView(APIView):
    def put(self, request, keyword):
        obj_keyword = Keyword.objects.filter(keyword=keyword)
        print(obj_keyword.count())
        if obj_keyword.count()==0 :
            obj_obj_keyword = Keyword(keyword = keyword,check_smartkeyword=False)
            obj_obj_keyword.save()
            obj_obj_keyword.follower.add(request.user)
            thr = threading.Thread(target=doCrawlByKeyword,args=[obj_obj_keyword])
            thr.setDaemon(True)
            thr.start()
            return Response(status=200)
        else:
            obj_obj_keyword = Keyword.objects.filter(keyword=keyword, follower=request.user)
            if obj_obj_keyword.count() == 0:
                print(serializers.serialize('json', obj_keyword))
                obj_keyword[0].follower.add(request.user)
                return Response(status=200)
            else:
                obj_obj_keyword = Keyword.objects.filter(keyword=keyword, follower=request.user)
                return Response(status=409)
            

class KeywordDeleteView(APIView):
    def delete(self, request, keyword):
        try:
            obj_keyword = Keyword.objects.filter(keyword=keyword)
            obj_keyword[0].follower.remove(request.user)
            return Response(status=200)
        except ObjectDoesNotExist:
            return Response(status=404)

