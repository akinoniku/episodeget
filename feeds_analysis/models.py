# coding=utf-8
import json
import re
import urllib2
from django.db import models

STYLE_CHOICES = (
    ('TM', '字幕组'),
    ('TL', '作品名'),
    ('CL', '清晰度'),
    ('FM', '格式'),
    ('LG', '字幕语言'),
)

SORT_CHOICES = (
    ('AN', '动画'),
    ('EP', '番剧'),
)


class FeedInfo(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    title = models.CharField(max_length=200)
    feed_tags = models.ForeignKey('FeedTags', blank=True, null=True)
    douban = models.ForeignKey('Douban', blank=True, null=True)
    weekday = models.SmallIntegerField()
    bgm_count = models.IntegerField()
    now_playing = models.SmallIntegerField(default=0)

    def __unicode__(self):
        return self.title


class FeedRss(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2000)
    hash_code = models.CharField(max_length=45)
    episode_id = models.SmallIntegerField(max_length=4)
    timestamp = models.DateTimeField(auto_now=True, auto_created=True)
    sub_list = models.ForeignKey('SubList', null=True, blank=True)

    def __unicode__(self):
        return self.title


class FeedTags(models.Model):
    title = models.CharField(max_length=200)
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    style = models.CharField(max_length=2, choices=STYLE_CHOICES)
    tags = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.title


class Douban(models.Model):
    title = models.CharField(max_length=200)
    aka = models.CharField(max_length=300)
    original_title = models.CharField(max_length=200)
    alt = models.URLField()
    countries = models.CharField(max_length=20)
    current_season = models.SmallIntegerField()
    directors = models.CharField(max_length=40)
    genres = models.CharField(max_length=100)
    images = models.URLField()
    douban_id = models.BigIntegerField()
    average = models.FloatField()
    episodes_count = models.SmallIntegerField(max_length=3)
    summary = models.CharField(max_length=6000)
    year = models.SmallIntegerField()

    def __unicode__(self):
        return self.title



class SubList(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    feed_info = models.ForeignKey('FeedInfo', blank=True, null=True)
    feed_tags = models.ManyToManyField('FeedTags', blank=True, null=True)
    # feed_rss = models.CharField(max_length=400)
    # tm = models.ForeignKey('FeedTags', blank=True, null=True)
    # tl = models.ForeignKey('FeedTags', blank=True, null=True)
    # cl = models.ForeignKey('FeedTags', blank=True, null=True)
    # fm = models.ForeignKey('FeedTags', blank=True, null=True)
    # lg = models.ForeignKey('FeedTags', blank=True, null=True)

    def __unicode__(self):
        return self.feed_info


