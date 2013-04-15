from django.contrib.auth.models import User
from django.db import models
from xunlei.lixian import XunleiClient


class Xunlei(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    xunlei_id = models.CharField(max_length=300, blank=True, null=True)
    xunlei_pass = models.CharField(max_length=300, blank=True, null=True)
    cookies = models.CharField(max_length=6000, blank=True, null=True)

    def add_task(self, rss):
        xunlei = XunleiClient(username=self.xunlei_id, password=self.xunlei_pass, cookie_path=self.xunlei_id)
        xunlei.add_torrent_task_by_link(rss.link)


class SubListPrefer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    preferList = models.CharField(max_length=6000, blank=True, null=True)
