from django.http import JsonResponse
from django.shortcuts import redirect, reverse

def signin_required(function):
    def decorator(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'result':'false','info':'Unauthorized Error'},status="401")
        return function(request, *args, **kwargs)

    return decorator