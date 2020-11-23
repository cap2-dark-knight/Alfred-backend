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
from .models import Keyword



def index(request):
    return HttpResponse("TEST!")


class SigninView(APIView):
    def get(self, request):
        return Response("ok", status=200)

    @csrf_exempt
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

    @csrf_exempt
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name = request.data['last_name']

        if User.objects.filter(email=email).exists():
            return Response("fail",401)
        else:
            user = User.objects.create_user(username = username, email=email, password=password, first_name=first_name, last_name=last_name)
            auth.login(request, user)
            return Response("ok", status=200)


class KeywordView(APIView):

    def get(self, request):

        obj_keyword = Keyword.objects.filter(follower=request.user)
        qs_keyword = serializers.serialize('json', keyword)
        print(qs_keyword)
        return Response(qs_keyword, status=200)

    def post(self, request):
        keyword = request.data['keyword']
        try:
            obj_keyword = Keyword.objects.filter(keyword=keyword)
            try:
                obj_obj_keyword.Keyword.objects.filter(keyword=keyword, follower=request.user)
            except ObjectDoesNotExist:
                obj_keyword.follower.add(request.user)
        except ObjectDoesNotExist:
            Keyword.objects.create(keyword = keyword, follwers = request.user, check_smartkeyword=False)
