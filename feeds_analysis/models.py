# coding=utf-8
import json
from django.db import models
from extra_app.langcov import langconv

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

    def tag_created(self):
        return None != self.feed_tags

    tag_created.boolean = True

    def show_tags(self):
        return ','.join(json.loads(self.get_tags()))

    def get_tags(self):
        c = langconv.Converter('zh-hant')
        all_tags = self.douban.all_tags().split(',')
        all_tags.insert(0, self.title)
        new_tags = []
        for tags in all_tags:
            if tags:
            # tags can be null
                if not tags in new_tags:
                    new_tags.append(tags)
                    #convert it!
                    convert_tag = c.convert(tags)
                    if not convert_tag in new_tags:
                        new_tags.append(convert_tag)
        return json.dumps(new_tags)

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
    aka = models.CharField(max_length=300, default=0)
    original_title = models.CharField(max_length=200, default=0)
    alt = models.URLField(default=0)
    countries = models.CharField(max_length=20, default=0)
    current_season = models.SmallIntegerField(default=1)
    directors = models.CharField(max_length=40, default=0)
    genres = models.CharField(max_length=100, default=0)
    images = models.URLField(default=0)
    douban_id = models.BigIntegerField()
    average = models.FloatField(default=0)
    episodes_count = models.SmallIntegerField(max_length=3, default=0)
    summary = models.CharField(max_length=6000, default=0)
    year = models.SmallIntegerField(default=0)

    def all_tags(self):
        return ','.join([self.title, self.original_title,
                         self.aka_decode()])

    def aka_decode(self):
        return ','.join(json.loads(self.aka))

    def countries_decode(self):
        return ','.join(json.loads(self.countries))

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


