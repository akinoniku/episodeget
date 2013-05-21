# coding=utf-8
from datetime import datetime
import json
from django.core.cache import get_cache
from feeds_analysis.models import Tags, SubList, Info, Rss

__author__ = 'akino'

all_tags_cache = {}


def get_tags_with_cache(type):
    allTags = {}
    key_string = 'allTagsA'
    key_string += type
    if not type in all_tags_cache:
        cache = get_cache('default')
        allTags[type] = cache.get(key_string)
        if not allTags[type]:
            allTags[type] = Tags.objects.filter(sort=type).order_by('id').reverse()
            cache.set(key_string, allTags[type], 3600)
        all_tags_cache[type] = allTags[type]
    return all_tags_cache[type]


def analysis_tags(rss):
    """

    :type rss: Rss
    """
    tags_list = []
    info_tags = None
    all_tags = get_tags_with_cache(rss.sort)
    for tags in all_tags:
        if info_tags and tags.style == 'TL':
            continue
        tag_list = json.loads(tags.tags)
        for tag in tag_list:
            if rss.title.find(tag) != -1:
                if tags.style == 'TL':
                    info_tags = Info.objects.filter(title=tags.title)
                    info_tags = info_tags[0]
                tags_list.append(tags)
                break
    if not len(tags_list):
        return False

    tag_string_list = []
    for tag in tags_list:
        tag_string_list.append(tag.id)

    tag_string_list.sort()
    tag_string_list = ','.join(str(i) for i in tag_string_list)
    rows = SubList.objects.filter(tags_index=tag_string_list)

    if len(rows):
        rows.filter(rss=rss)
        if not len(rows):
            rows[0].rss.add(rss)
            rows[0].save()
            send_notification(rss, rows[0])
    else:
        new_list = SubList(
            info=info_tags,
            sort=rss.sort,
            tags_index=tag_string_list,
            create_time=datetime.now(),
            update_time=datetime.now(),
        )
        new_list.save()
        new_list.rss.add(rss)
        for tags in tags_list:
            new_list.tags.add(tags)
        new_list.save()
        send_notification(rss, new_list)
    return True


def send_notification(rss, sub_list):
    for user in sub_list.user:
        notify_user(user, rss)