# coding=utf-8
import re
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
    feed_tags = models.IntegerField()
    douban = models.IntegerField()
    sub_list = models.IntegerField()
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
    average = models.SmallIntegerField(max_length=2)
    episodes_count = models.SmallIntegerField(max_length=3)
    summary = models.CharField(max_length=6000)
    year = models.SmallIntegerField()

    def __unicode__(self):
        return self.title


class SubList(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    feed_rss = models.CharField(max_length=400)
    feed_info = models.IntegerField()
    tm = models.IntegerField()
    tl = models.IntegerField()
    cl = models.IntegerField()
    fm = models.IntegerField()
    lg = models.IntegerField()

    def __unicode__(self):
        return self.feed_info


