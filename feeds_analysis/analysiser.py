import json
from django.core.cache import get_cache
from feeds_analysis.models import FeedTags, SubList, FeedInfo

__author__ = 'akino'


def get_tags_with_cache(type):
    key_string = 'allTags2'
    key_string += type
    cache = get_cache('default')
    allTags = cache.get(key_string)
    if not allTags:
        allTags = FeedTags.objects.filter(sort=type)
        cache.set(key_string, allTags, 3600)
    return allTags


def analysis_tags(rss):
    """

    :type rss: FeedRss
    """
    feed_tags_list = []
    info_tags = None
    for feed_tags in get_tags_with_cache(rss.sort):
        tag_list = json.loads(feed_tags.tags)
        for tag in tag_list:
            if rss.title.find(tag) != -1:
                if feed_tags.style == 'TL':
                    info_tags = FeedInfo.objects.filter(title=feed_tags.title)
                    info_tags = info_tags[0]
                feed_tags_list.append(feed_tags)
                break
    if not len(feed_tags_list):
        return False

    tag_string_list = []
    for tag in feed_tags_list:
        tag_string_list.append(tag.id)

    tag_string_list.sort()
    tag_string_list = ','.join(str(i) for i in tag_string_list)
    rows = SubList.objects.filter(tags_index=tag_string_list)

    if len(rows):
        rows.filter(feed_rss=rss)
        if len(rows):
            rows[0].feed_rss.add(rss)
            rows[0].save()
    else:
        new_list = SubList(
            feed_info=info_tags,
            sort=rss.sort,
            tags_index=tag_string_list,
        )
        new_list.save()
        new_list.feed_rss.add(rss)
        for tags in feed_tags_list:
            new_list.feed_tags.add(tags)
        new_list.save()
    return True
