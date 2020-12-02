from django.contrib import admin
from .models import Profile, Keyword, CrawledData, SmartKeywordInfo
from django.contrib.auth.models import User

admin.site.register(Profile)
admin.site.register(Keyword)
admin.site.register(CrawledData)
admin.site.register(SmartKeywordInfo)


# Register your models here.
