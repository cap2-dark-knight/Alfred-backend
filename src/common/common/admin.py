from django.contrib import admin
from .models import Profile, Keyword, CrawledData
from django.contrib.auth.models import User

admin.site.register(Profile)
admin.site.register(Keyword)
admin.site.register(CrawledData)


# Register your models here.
