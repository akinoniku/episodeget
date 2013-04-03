# coding=utf-8
import re
import urllib2
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from feeds_analysis.analysiser import analysis_tags
from feeds_analysis.models import FeedRss, Douban, FeedInfo
from old_db_reader.reader import old_db_reader


def get_ani_rss(request):
    rss_json = urllib2.urlopen(
        'http://pipes.yahoo.com/pipes/pipe.run?_id=2a1aee3dda9a657eaa4d8eece5441f8f&_render=json').read()
    rss_json = json.loads(rss_json)['value']['items']
    loopToStoreRss(rss_json, 'AN')
    return render_to_response('feeds_analysis/get_ani_rss.html', {'rss_json': rss_json})


def get_epi_rss(request):
    rss_json = urllib2.urlopen(
        'http://pipes.yahoo.com/pipes/pipe.run?_id=4059b898dc1eef8661b3eabcfc1d905a&_render=json').read()
    rss_json = json.loads(rss_json)['value']['items']
    loopToStoreRss(rss_json, 'EP')
    return render_to_response('feeds_analysis/get_ani_rss.html', {'rss_json': rss_json})


def loopToStoreRss(rss_json, sort, episode_id=0):
    counter = 0
    for rss in rss_json:
        if not FeedRss.objects.filter(hash_code=rss['hash']):
            new_rss = FeedRss(title=rss['title'], link=rss['url'], hash_code=rss['hash'], sort=sort,
                              episode_id=episode_id)
            new_rss.save()
            counter += 1
        else:
            break
    return counter


def get_ani_new(request):
    ani_json = urllib2.urlopen('http://www.bilibili.tv/index/bangumi.json').read()
    ani_json = json.loads(ani_json)
    loopToStoreAni(ani_json)
    # return render_to_response('feeds_analysis/get_ani_rss.html', {'rss_json': ''})
    return HttpResponse("Get ani done!")


def loopToStoreAni(ani_json):
    counter = 0
    added_info_array = []
    # loop to add
    for ani in ani_json:
        info = FeedInfo.objects.filter(title=ani['title'])
        if not info:
            new_ani = FeedInfo(
                sort='AN',
                title=ani['title'],
                weekday=ani['weekday'],
                bgm_count=ani['bgmcount'],
                now_playing=1,
            )
            new_ani.save()
            added_info_array.append(new_ani.id)
            counter += 1
        else:
            info.update(
                sort='AN',
                title=ani['title'],
                weekday=ani['weekday'],
                bgm_count=ani['bgmcount'],
                now_playing=1,
            )
            added_info_array.append(info[0].id)
    # check the now_playing info finished
    if len(added_info_array) > 5:
        for info in FeedInfo.objects.filter(sort='AN', now_playing=1):
            if not info.id in added_info_array:
                FeedInfo.objects.filter(pk=info.id).update(now_playing=0)
    return counter


def get_epi_new(request):
    epi_json = urllib2.urlopen(
        'http://pipes.yahoo.com/pipes/pipe.run?_id=47147fbe121a2a307f87d2de85a416be&_render=json').read()
    epi_json = json.loads(epi_json)
    loopToStoreEpi(epi_json)
    return HttpResponse("Get epi done!")


def loopToStoreEpi(epi_json):
    counter = 0
    for epi in epi_json['value']['items']:
        if epi['title'].find(u'连载') != -1:
            now_playing = 1
        elif epi['title'].find(u'完结') != -1:
            now_playing = 0
        else:
            continue
        title_cn = re.search(u'《[\w\W]+》', epi['title']).group(0)[1:-1]
        title_en = re.search(u'\([\w\W]+\)', epi['title']).group(0)[1:-1]
        title = title_cn + ',' + title_en

        info = FeedInfo.objects.filter(title=title)
        if not info:
            new_epi = FeedInfo(
                sort='EP',
                title=title,
                now_playing=now_playing,
            )
            new_epi.save()
            counter += 1
        else:
            info.update(
                sort='EP',
                title=title,
                now_playing=now_playing,
            )


def get_douban_by_douban_id(douban_id):
    douban_subject = Douban.objects.filter(douban_id=douban_id)
    if douban_subject:
        return douban_subject[0]
    douban_subject = urllib2.urlopen(
        'http://api.douban.com/v2/movie/subject/%s?apikey=020149640d8ca58a0603dc2c28a5f09e' % douban_id).read()
    douban_subject = json.loads(douban_subject)
    new_douban = Douban(
        title=douban_subject['title'],
        aka=json.dumps(douban_subject['aka']),
        original_title=douban_subject['original_title'],
        alt=douban_subject['alt'],
        countries=json.dumps(douban_subject['countries']),
        current_season=douban_subject['current_season'],
        directors=douban_subject['directors'][0]['name'] if len(douban_subject['directors']) > 0 else None,
        genres=json.dumps(douban_subject['genres']),
        images=douban_subject['images']['large'],
        douban_id=douban_subject['id'],
        average=douban_subject['rating']['average'],
        episodes_count=douban_subject['episodes_count'],
        summary=douban_subject['summary'],
        year=douban_subject['year'],
    )
    new_douban.save()
    return new_douban


def ana_rss(request, id):
    rss = FeedRss.objects.get(pk=id)
    analysis_tags(rss)
    HttpResponse('Analysis ani Done')


def read_old_db(request):
    old_db_reader()
    return HttpResponse("Read Old db Done")
