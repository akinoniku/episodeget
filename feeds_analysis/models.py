# coding=utf-8
from django.db import models

# Create your models here.


class Sort(models.Model):
    title = models.CharField(max_length=200)


class FeedRss(models.Model):
    sort = models.ForeignKey(Sort)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2000)
    hash_code = models.CharField(max_length=45)
    episode_id = models.SmallIntegerField(max_length=4)
    timestamp = models.DateTimeField(auto_now=True, auto_created=True)


class FeedTags(models.Model):
    STYLE_CHOICES = (
        ('TM', '字幕组'),
        ('TL', '作品名'),
        ('CL', '清晰度'),
        ('FM', '格式'),
        ('LG', '字幕语言'),
    )
    sort = models.ForeignKey(Sort)
    title = models.CharField(max_length=200)
    style = models.CharField(max_length=2, choices=STYLE_CHOICES)
    tags = models.CharField(max_length=2000)


class Douban(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    average = models.SmallIntegerField(max_length=2)
    country = models.CharField(max_length=20)
    episodes = models.SmallIntegerField(max_length=3)
    tags = models.SmallIntegerField(max_length=500)
    full = models.CharField(max_length=6000)


class SubList(models.Model):
    sort = models.ForeignKey(Sort)
    tm = models.SmallIntegerField(default=0)
    tl = models.SmallIntegerField(default=0)
    cl = models.SmallIntegerField(default=0)
    fm = models.SmallIntegerField(default=0)
    lg = models.SmallIntegerField(default=0)


class FeedInfo(models.Model):
    sort = models.ForeignKey(Sort)
    title = models.CharField(max_length=200)
    tags = models.ForeignKey(FeedTags)
    douban = models.ForeignKey(Douban)
    sub_list = models.ForeignKey(SubList)
    now_playing = models.SmallIntegerField(default=0)


