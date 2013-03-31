import json
from django.core.cache import get_cache
from feeds_analysis.models import FeedTags

__author__ = 'akino'


def get_tags_with_cache():
    cache = get_cache('alternate')
    allTags = cache.get('allTags')
    if not allTags:
        allTags = FeedTags.objects.all()
        cache.set('allTags', allTags, 3600)
    return allTags


def analysis_tags(rss):
    """

    :type rss: FeedRss
    """
    feed_tags_list = []
    for feed_tags in get_tags_with_cache():
        tag_list = json.loads(feed_tags.tags)
        for tag in tag_list:
            if rss.title.find(tag) != -1:
                feed_tags_list.append(feed_tags)
                break