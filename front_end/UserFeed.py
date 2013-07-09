# coding=utf-8
from django.contrib.syndication.views import Feed
from front_end.views import rss_feed


class UserFeed(Feed):
    title = "星祈娘"
    link = "/feed/"
    domain = 'xingqiniang.com'
    description = "这是星祈娘生成的RSS订阅"

    def get_object(self, request, userId):
        result = rss_feed(userId)
        return result

    def items(self, obj):
        return obj

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.title

    def item_link(self, item):
        return item.link
