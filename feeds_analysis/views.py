import urllib2
import json
from django.shortcuts import render_to_response
from feeds_analysis.models import FeedRss, Douban, FeedInfo


def get_ani_rss(request):
    # rss_json = urllib2.urlopen(
    #     'http://pipes.yahoo.com/pipes/pipe.run?_id=1e8c89ba88de4df8def7cecb3ff7201c&_render=json').read()
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
    return render_to_response('feeds_analysis/get_ani_rss.html', {'rss_json': ''})


def loopToStoreAni(ani_json):
    counter = 0
    for ani in ani_json:
        if not FeedInfo.objects.filter(title=ani['title']):
            new_ani = FeedInfo(
                sort='AN',
                title=ani['title'],
                weekday=ani['weekday'],
                bgm_count=ani['bgmcount'],
                now_playing=1,
            )
            new_ani.save()
            counter += 1
        else:
            break
    return counter


def get_douban_by_title(request):
    get_douban_result = False
    no_douban_feeds = FeedInfo.objects.filter(douban=None)[:5]
    for feeds in no_douban_feeds:
        get_douban_result = get_douban_info(feeds.title)
        if get_douban_result:
            feeds.douban = get_douban_result
            feeds.save()
        else:
            pass
    return render_to_response('feeds_analysis/douban_view.html', {'douban': get_douban_result})


def get_douban_by_id(request, douban_id):
    new_douban = get_douban_by_douban_id(douban_id)
    return render_to_response('feeds_analysis/douban_view.html', {'douban': new_douban})


def get_douban_info(search_title):
    douban_api_string = 'http://api.douban.com/v2/movie/search?q=%s' % search_title
    first_result = urllib2.urlopen(douban_api_string.encode('utf-8')).read()
    first_result = json.loads(first_result)
    if first_result['total'] > 0:
        douban_id = first_result['subjects'][0]['id']
        new_douban = get_douban_by_douban_id(douban_id)
        return new_douban
    else:
        return False


def get_douban_by_douban_id(douban_id):
    douban_subject = Douban.objects.filter(douban_id=douban_id)
    if douban_subject:
        return douban_subject[0]
    douban_subject = urllib2.urlopen('http://api.douban.com/v2/movie/subject/%s' % douban_id).read()
    douban_subject = json.loads(douban_subject)
    new_douban = Douban(
        title=douban_subject['title'] if douban_subject['title'] else 0,
        aka=json.dumps(douban_subject['aka']),
        original_title=douban_subject['original_title'] if douban_subject['original_title'] else 0,
        alt=douban_subject['alt'] if douban_subject['alt'] else 0,
        countries=json.dumps(douban_subject['countries']),
        current_season=douban_subject['current_season'] if douban_subject['current_season'] else 1,
        directors=douban_subject['directors'] if douban_subject else 0,
        genres=json.dumps(douban_subject['genres']),
        images=douban_subject['images']['large'] if douban_subject['images']['large'] else 0,
        douban_id=douban_subject['id'],
        average=douban_subject['rating']['average'],
        episodes_count=douban_subject['episodes_count'] if douban_subject['episodes_count'] else 0,
        summary=douban_subject['summary'] if douban_subject['summary'] else 0,
        year=douban_subject['year'] if douban_subject['year'] else 0,
        )
    new_douban.save()
    return new_douban