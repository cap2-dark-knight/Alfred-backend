from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


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



