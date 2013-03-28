__author__ = 'akino'
from django.contrib import admin
from feeds_analysis.models import FeedRss, FeedTags, Douban, SubList, FeedInfo

admin.site.register(FeedRss)
admin.site.register(FeedTags)
# admin.site.register(Douban)
admin.site.register(SubList)
# admin.site.register(FeedInfo)


class DoubanAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_title', 'aka_decode', 'countries_decode', 'all_tags', 'average', 'year')

admin.site.register(Douban, DoubanAdmin)

class FeedInfoAdmin(admin.ModelAdmin):
    list_display = ('sort', 'title', 'douban', 'now_playing',
                    'feed_tags', 'weekday', 'bgm_count')
    list_display_links = ('title',)
    # list_editable = ('douban',)
    actions = ['create_tag']

    def create_tag(self, request, queryset):
        infos = queryset.select_related().all()
        for info in infos:
            new_tag = FeedTags(
                sort=info['sort'],
                title=info['title'],
                style='TL',

            )
    create_tag.short_description = 'Create Tag'


admin.site.register(FeedInfo, FeedInfoAdmin)
