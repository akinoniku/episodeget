import urllib2
import json
from django.shortcuts import render_to_response
from feeds_analysis.models import FeedRss, Douban


def get_ani_rss(request):
    # rss_json = urllib2.urlopen(
    #     'http://pipes.yahoo.com/pipes/pipe.run?_id=1e8c89ba88de4df8def7cecb3ff7201c&_render=json').read()
    rss_json = urllib2.urlopen(
        'http://pipes.yahoo.com/pipes/pipe.run?_id=2a1aee3dda9a657eaa4d8eece5441f8f&_render=json').read()
    loopToStoreRss(json.loads(rss_json)['value']['items'], 'AN')
    return render_to_response('feeds_analysis/get_ani_rss.html', {'rss_json': rss_json})


def get_epi_rss(request):
    rss_json = urllib2.urlopen(
        'http://pipes.yahoo.com/pipes/pipe.run?_id=4059b898dc1eef8661b3eabcfc1d905a&_render=json').read()
    loopToStoreRss(json.loads(rss_json)['value']['items'], 'EP')
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


def get_douban_info(search_title):
    first_result = urllib2.urlopen('http://api.douban.com/v2/movie/search?q=%s' % search_title).read()
    douban_id = json.loads(first_result)['subject'][0]['id']
    if douban_id:
        douban_subject = urllib2.urlopen('http://api.douban.com/v2/movie/subject/%s' % douban_id).read()
        douban_subject = json.loads(douban_subject)
        new_douban = Douban(
            title=douban_subject.title,
            aka=json.dumps(douban_subject.aka),
            original_title=douban_subject.original_title,
            alt=douban_subject.alt,
            countries=json.dumps(douban_subject.countries),
            current_season=douban_subject.current_season,
            direction=douban_subject.directors,
            genres=json.dumps(douban_subject.genres),
            images=douban_subject.images.large,
            douban_id=douban_subject.id,
            average=int(douban_subject.rating.average),
            episodes_count=douban_subject.episodes_count,
            summary=douban_subject.summary,
            year=douban_subject.year,
        )
        return new_douban.save()
    else:
        return False
