import json
import urllib2
from django.contrib.admin import SimpleListFilter
from feeds_analysis.updater import get_douban_by_douban_id
from user_settings.models import Xunlei

__author__ = 'akino'
from django.contrib import admin
from feeds_analysis.models import Rss, Tags, Douban, SubList, Info

# admin.site.register(Rss)
# admin.site.register(Tags)
# admin.site.register(Douban)
# admin.site.register(SubList)
# admin.site.register(Info)
admin.site.register(Xunlei)


class RssAdmin(admin.ModelAdmin):
    list_display = ('sort', 'title',)
    search_fields = ('title',)
    list_display_links = ('title',)


admin.site.register(Rss, RssAdmin)


class TagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort', 'style', 'show_tags')
    list_editable = ('style',)
    list_filter = ('sort', 'style')


admin.site.register(Tags, TagsAdmin)


class DoubanAdmin(admin.ModelAdmin):
    list_display = ('title', 'original_title', 'countries_decode', 'all_tags_dump', 'average', 'year')


admin.site.register(Douban, DoubanAdmin)


class GetTagsFilter(SimpleListFilter):
    title = "Need Tags?"
    parameter_name = 'need_tags'

    def lookups(self, request, model_admin):
        return (
            ('Created', 'Created'),
            ('With douban', 'With douban'),
            ('No douban', 'No douban'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Created':
            return queryset.filter(tags__isnull=False)
        if self.value() == 'No douban':
            return queryset.filter(douban__isnull=True)
        if self.value() == 'With douban':
            return queryset.filter(douban__isnull=False, tags__isnull=True)


class FeedInfoAdmin(admin.ModelAdmin):
    list_display = ('sort', 'title', 'douban', 'now_playing',
                    'weekday', 'count_sub_list', 'show_tags', 'tag_created', )
    list_display_links = ('title',)
    list_filter = ('sort', GetTagsFilter, 'now_playing')
    list_editable = ('now_playing',)
    search_fields = ('title',)
    actions = ['get_douban', 'create_tag', 'create_short_tag']
    list_max_show_all = 600

    def create_tag(self, request, queryset):
        infos = queryset.select_related().all()
        for info in infos:
            if Tags.objects.filter(title=info.title):
                continue
            new_tag = Tags(
                sort=info.sort,
                title=info.title,
                style='TL',
                tags=info.get_tags()
            )
            new_tag.save()
            info.tags = new_tag
            info.save()

    def create_short_tag(self, request, queryset):
        infos = queryset.select_related().all()
        for info in infos:
            info.create_tag_test()

    create_tag.short_description = 'Create Tag'
    create_short_tag.short_description = 'Create short Tag(debug)'

    def get_douban(self, request, queryset):
        infos = queryset.select_related().all()
        for info in infos:
            douban_api_string = 'http://api.douban.com/v2/movie/search?q=%s?apikey=020149640d8ca58a0603dc2c28a5f09e' % info.title.replace(' ', '%20')
            first_result = urllib2.urlopen(douban_api_string.encode('utf-8')).read()
            try:
                first_result = json.loads(first_result)
            except:
                douban_api_string = 'http://api.douban.com/v2/movie/search?q=%s?apikey=020149640d8ca58a0603dc2c28a5f09e' % info.title.split(',')[0].replace(' ', '%20')
                first_result = urllib2.urlopen(douban_api_string.encode('utf-8')).read()
            if first_result['total'] > 0:
                douban_id = first_result['subjects'][0]['id']
                new_douban = get_douban_by_douban_id(douban_id)
                info.douban = new_douban
                info.save()

    get_douban.short_description = 'Get Douban'


admin.site.register(Info, FeedInfoAdmin)


class SubListAdmin(admin.ModelAdmin):
    list_display = ('sort', 'show_title', 'show_all_styles', 'show_all_tags', 'count_rss')
    list_display_links = ('show_title',)


admin.site.register(SubList, SubListAdmin)
