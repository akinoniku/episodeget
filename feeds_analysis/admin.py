__author__ = 'akino'
from django.contrib import admin
from feeds_analysis.models import FeedRss, FeedTags, Douban, SubList, FeedInfo

admin.site.register(FeedRss)
admin.site.register(FeedTags)
admin.site.register(Douban)
admin.site.register(SubList)
# admin.site.register(FeedInfo)


class FeedInfoAdmin(admin.ModelAdmin):
    list_display = ('sort', 'title', 'douban', 'now_playing',
                    'feed_tags', 'weekday', 'bgm_count')
    list_display_links = ('title',)
    # list_editable = ('douban',)

admin.site.register(FeedInfo, FeedInfoAdmin)
