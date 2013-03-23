__author__ = 'akino'
from django.contrib import admin
from feeds_analysis.models import FeedRss, FeedTags, Douban, SubList, FeedInfo

admin.site.register(FeedRss)
admin.site.register(FeedTags)
admin.site.register(Douban)
admin.site.register(SubList)
admin.site.register(FeedInfo)
