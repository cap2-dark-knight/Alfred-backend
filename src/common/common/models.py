from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_period = models.IntegerField(blank = True, default=12)
    last_updated = models.DateTimeField(blank = True, auto_now_add=True)

class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    keyword = models.CharField(max_length=30 ,blank=False, null=False)
    follower = models.ManyToManyField(User, related_name="following")
    check_smartkeyword = models.BooleanField(default=False, blank=True, null=False)

class CrawledData(models.Model):
    id = models.AutoField(primary_key=True)
    updated_time = models.DateTimeField(blank=False, auto_now_add=True)
    keywords = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    url = models.URLField(blank=True)
    title = models.CharField(max_length=30 ,blank=False, null=False)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)




