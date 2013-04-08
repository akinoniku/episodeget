# coding=utf-8
import json
import urllib2
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
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

PLAYING_CHOICES = (
    (0, '已完结'),
    (1, '连载中'),
    (2, '长篇'),
    (3, '废弃'),
)


class Info(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    title = models.CharField(max_length=200)
    tags = models.ForeignKey('Tags', blank=True, null=True)
    douban = models.ForeignKey('Douban', blank=True, null=True)
    weekday = models.SmallIntegerField(blank=True, null=True)
    bgm_count = models.IntegerField(blank=True, null=True)
    now_playing = models.SmallIntegerField(default=0, choices=PLAYING_CHOICES)
    image = models.ImageField(upload_to='info_pic', blank=True, null=True)

    def tag_created(self):
        return None != self.tags

    tag_created.boolean = True

    def show_tags(self):
        return ','.join(json.loads(self.get_tags()))

    def get_simple_tags(self):
        c = langconv.Converter('zh-hant')
        all_tags = self.title.split(',')
        new_tags = []
        for tags in all_tags:
            if tags:
            # tags would be null
                if not tags in new_tags:
                    new_tags.append(tags)
                    #convert it!
                    convert_tag = c.convert(tags)
                    if not convert_tag in new_tags:
                        new_tags.append(convert_tag)
        return json.dumps(new_tags)

    def get_tags(self):
        if self.douban:
            c = langconv.Converter('zh-hant')
            all_tags = self.title.split(',')
            all_tags.extend(self.douban.all_tags())
            new_tags = []
            for tags in all_tags:
                if tags:
                # tags would be null
                    if not tags in new_tags:
                        new_tags.append(tags)
                        #convert it!
                        convert_tag = c.convert(tags)
                        if not convert_tag in new_tags:
                            new_tags.append(convert_tag)
            return json.dumps(new_tags)
        else:
            return json.dumps([])

    def count_sub_list(self):
        return len(SubList.objects.filter(info=self))

    def get_sub_list(self):
        return SubList.objects.filter(info=self)

    def __unicode__(self):
        return self.title


class Rss(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2000)
    hash_code = models.CharField(max_length=45, unique=True, db_index=True)
    episode_id = models.SmallIntegerField(max_length=4, null=True, blank=True)
    timestamp = models.DateTimeField(auto_created=True)
    # sub_list = models.ForeignKey('SubList', null=True, blank=True, db_index=True)

    def __unicode__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=200)
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    style = models.CharField(max_length=2, choices=STYLE_CHOICES)
    tags = models.CharField(max_length=2000)

    def show_tags(self):
        return ','.join(json.loads(self.tags))

    def __unicode__(self):
        return self.title


class Douban(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    aka = models.CharField(max_length=300, blank=True, null=True)
    original_title = models.CharField(max_length=200, blank=True, null=True)
    alt = models.URLField(blank=True, null=True)
    countries = models.CharField(max_length=100, blank=True, null=True)
    current_season = models.SmallIntegerField(blank=True, null=True)
    directors = models.CharField(max_length=40, blank=True, null=True)
    genres = models.CharField(max_length=400, blank=True, null=True)
    images = models.URLField(blank=True, null=True)
    douban_id = models.BigIntegerField()
    average = models.FloatField(blank=True, null=True)
    episodes_count = models.SmallIntegerField(max_length=3, blank=True, null=True)
    summary = models.CharField(max_length=6000, blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)

    def all_tags(self):
        tags = [self.title, self.original_title]
        tags.extend(self.aka_decode())
        return tags

    def aka_decode(self):
        return json.loads(self.aka)

    def countries_decode(self):
        return ','.join(json.loads(self.countries))

    def all_tags_dump(self):
        return ','.join(self.all_tags())

    def __unicode__(self):
        return self.title


class SubList(models.Model):
    sort = models.CharField(max_length=2, choices=SORT_CHOICES)
    tags_index = models.CharField(max_length=300, blank=True, null=True)
    info = models.ForeignKey(Info, blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True, null=True)
    rss = models.ManyToManyField(Rss, blank=True, null=True)
    user = models.ManyToManyField(User, blank=True, null=True)
    create_time = models.DateTimeField(auto_created=True)
    update_time = models.DateTimeField(auto_now=True)

    def count_rss(self):
        return self.rss.all().count()

    def show_all_tags(self):
        tags_title = []
        for tags in self.tags.all():
            tags_title.append(tags.title)
        return ','.join(tags_title)

    def show_all_styles(self):
        tags_style = []
        for tags in self.tags.all():
            tags_style.append(tags.style)
        return ','.join(tags_style)

    def show_title(self):
        return self.__unicode__()

    def __unicode__(self):
        if None != self.info:
            return self.info.title
        else:
            return self.tags_index


def update_with_id(instance, **kwargs):
    if not instance.title:
        douban_subject = urllib2.urlopen(
            'http://api.douban.com/v2/movie/subject/%s?apikey=020149640d8ca58a0603dc2c28a5f09e'
            % instance.douban_id).read()
        douban_subject = json.loads(douban_subject)
        Douban.objects.filter(id=instance.id).update(
            title=douban_subject['title'],
            aka=json.dumps(douban_subject['aka']),
            original_title=douban_subject['original_title'],
            alt=douban_subject['alt'],
            countries=json.dumps(douban_subject['countries']),
            current_season=douban_subject['current_season'],
            directors=douban_subject['directors'][0]['name'] if len(douban_subject['directors']) > 0 else None,
            genres=json.dumps(douban_subject['genres']),
            images=douban_subject['images']['large'],
            douban_id=douban_subject['id'],
            average=douban_subject['rating']['average'],
            episodes_count=douban_subject['episodes_count'],
            summary=douban_subject['summary'],
            year=douban_subject['year'],
        )


post_save.connect(update_with_id, sender=Douban)


