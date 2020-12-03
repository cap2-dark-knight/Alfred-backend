from email.policy import default

from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    last_updated = models.DateTimeField(blank = True, auto_now_add=True)
    alart_times = models.IntegerField(default=0b1000000000, blank=False, null=False)

    def get_alart_time_list(self):
        idx=0b1
        times = []
        for i in range(24):
            if idx & self.alart_times:
                times.append(i) 
            idx = idx << 1
        return times          

    def __str__(self):
        return self.user.email+' '+str(self.get_alart_time_list())

class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=30 ,blank=False, null=False)
    follower = models.ManyToManyField(User, related_name="following")

    def __str__(self):
        try:
            return self.keyword+" ["+self.smartkeywordinfo.type+"]"
        except:
            return self.keyword

    def get_smartkeywordinfo(self) :
        try:
            return self.smartkeywordinfo.__dict__
        except:
            return None

class SmartKeywordInfo(models.Model):
    keyword = models.OneToOneField(Keyword, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(default="", max_length=20, blank=True, null=True)
    url = models.TextField(default="", blank=True, null=True)
    articles = models.TextField(default="", blank=True, null=True)
    target_base = models.TextField(default="", blank=True, null=True)
    title = models.TextField(default="", blank=True, null=True)
    image = models.TextField(default="", blank=True, null=True)
    contents = models.TextField(default="", blank=True, null=True)
    def __str__(self):
        return self.keyword.keyword


class CrawledData(models.Model):
    id = models.AutoField(primary_key=True)
    updated_time = models.DateTimeField(blank=False, auto_now_add=True)
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    title = models.CharField(max_length=30 ,blank=False, null=False)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return "["+ str(self.updated_time) +"]"+ self.keywords.keyword + ' : ' +self.url

