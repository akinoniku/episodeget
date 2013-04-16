from django.contrib.auth.models import User
from django.db import models


class Xunlei(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    xunlei_id = models.CharField(max_length=300, blank=True, null=True)
    xunlei_pass = models.CharField(max_length=300, blank=True, null=True)
    cookies = models.CharField(max_length=6000, blank=True, null=True)


class SubListPrefer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    preferList = models.CharField(max_length=6000, blank=True, null=True)
