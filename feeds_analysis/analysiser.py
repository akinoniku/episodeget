# coding=utf-8
from datetime import datetime
import json
from django.core.cache import get_cache
from feeds_analysis.models import Tags, SubList, Info, Rss
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        try:
            resultList.rss.get(id=rss.id)
        except:
            return True
        resultList.rss.add(rss)
        resultList.rss.update_time = datetime.now()
        resultList.save()
        # send_notification(rss, rows[0])
    else:
        new_list = SubList(
            sort=rss.sort,
            tags_index=tag_string_list,
            create_time=datetime.now(),
            update_time=datetime.now(),
        )
        new_list.save()
        new_list.rss.add(rss)
        if info_tags:
            new_list.info.add(info_tags)
        for tags in tags_list:
            new_list.tags.add(tags)
        new_list.save()
        # send_notification(rss, new_list)
    return True


def send_notification(rss, sub_list):
    for user in sub_list.user.all():
        info = sub_list.info.get()
        fromEmail = 'aki@foxmail.com'
        toEmail = user.email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = u"%s更新啦" % info.title
        msg['From'] = fromEmail
        msg['To'] = toEmail

        html = """<h3>%s,</h3><p>请点击下载</p><a href=%s>%s</a>""" % (user.username, rss.link, rss.title)
        part = MIMEText(html.encode('utf-8'), 'html')
        msg.attach(part)

        username = 'postmaster@xingqiniang.sendcloud.org'
        password = 'dBu8lCZz'
        s = smtplib.SMTP('smtpcloud.sohu.com:25')
        s.set_debuglevel(1)
        s.login(username, password)
        s.sendmail(fromEmail, toEmail, msg.as_string())
        s.quit()
        return True
