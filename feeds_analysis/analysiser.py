# coding=utf-8
from datetime import datetime
from django.utils import timezone
import json
from django.core.cache import get_cache
from feeds_analysis.models import Tags, SubList, Info, Rss
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

__author__ = 'akino'

all_tags_cache = {}


def get_tags_with_cache(sort):
    allTags = {}
    key_string = 'allTagsA'
    key_string += sort
    if not sort in all_tags_cache:
        cache = get_cache('default')
        allTags[sort] = cache.get(key_string)
        if not allTags[sort]:
            allTags[sort] = Tags.objects.filter(sort=sort).order_by('id').reverse()
            cache.set(key_string, allTags[sort], 3600)
        all_tags_cache[sort] = allTags[sort]
    return all_tags_cache[sort]


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
                    try:
                        info_tags = Info.objects.get(title=tags.title)
                    except Exception, e:
                        info_tags = None
                tags_list.append(tags)
                break
    if not len(tags_list):
        return False

    tag_string_list = []
    for tag in tags_list:
        tag_string_list.append(tag.id)

    tag_string_list.sort()
    tag_string_list = ','.join(str(i) for i in tag_string_list)
    try:
        resultList = SubList.objects.get(tags_index=tag_string_list)
    except:
        resultList = None

    if resultList:
        if not resultList.rss.filter(id=rss.id).count():
            resultList.rss.add(rss)
            if rss.timestamp > resultList.update_time:
                resultList.update_time = rss.timestamp
            resultList.save()
            send_notification(rss, resultList)
        else:
            #already added
            pass
    else:
        new_list = SubList(
            sort=rss.sort,
            tags_index=tag_string_list,
            create_time=rss.timestamp,
            update_time=rss.timestamp,
        )
        new_list.save()
        new_list.rss.add(rss)
        if info_tags:
            new_list.info.add(info_tags)
        for tags in tags_list:
            new_list.tags.add(tags)
        new_list.save()
        send_notification(rss, new_list)
    return True


def send_notification(rss, sub_list):
    qq = sub_list.user.all()
    for user in sub_list.user.all():
        info = sub_list.info.get()
        fromEmail = 'aki@foxmail.com'
        toEmail = user.email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = u"%s更新啦" % info.title
        msg['From'] = fromEmail
        msg['To'] = toEmail

        html = u"""<h3>%s,</h3><p>请点击下载</p><a href=%s>%s</a>""" % (user.username, rss.link, rss.title)
        part = MIMEText(html.encode('utf-8'), 'html')
        msg.attach(part)

        username = 'postmaster@xingqiniang.sendcloud.org'
        password = 'dBu8lCZz'
        s = smtplib.SMTP('smtpcloud.sohu.com:25')
        s.login(username, password)
        s.sendmail(fromEmail, toEmail, msg.as_string())
        s.quit()
        return True
