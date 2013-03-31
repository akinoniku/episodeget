import urllib2
import json
from django.shortcuts import render_to_response
from extra_app.langcov import langconv
from feeds_analysis.models import FeedRss, Douban, FeedInfo, FeedTags


# TODO I should make a old database reader for my old data. For tags, rss, and info
from old_db_reader.reader import ani_rss_sql, epi_rss_sql, ani_tags_sql, epi_tags_sql, ani_info_sql, epi_info_sql


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
    added_info_array = []
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
    FeedInfo.objects.filter(sort='AN')
    return counter


def get_douban_by_id(request, douban_id):
    new_douban = get_douban_by_douban_id(douban_id)
    return render_to_response('feeds_analysis/douban_view.html', {'douban': new_douban})


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


def read_old_db(request):
    old_db = ani_rss_sql()
    for row in old_db:
        if not FeedRss.objects.filter(hash_code=row[2][20:52]):
            new_ani_rss = FeedRss(
                sort='AN',
                title=row[1],
                link=row[2],
                hash_code=row[2][20:52],
                episode_id=0,
                timestamp=row[3]
            )
            new_ani_rss.save()

    old_db = epi_rss_sql()
    for row in old_db:
        if not FeedRss.objects.filter(hash_code=row[2][20:52]):
            new_epi_rss = FeedRss(
                sort='EP',
                title=row[1],
                link=row[2],
                hash_code=row[2][20:52],
                episode_id=0,
                timestamp=row[3]
            )
            new_epi_rss.save()

    mapper = {1: 'TM', 2: 'Tl', 3: 'CL', 4: 'FM', 5: 'LG'}

    old_db = ani_tags_sql()
    for row in old_db:
        if row[2] != 2 and not FeedTags.objects.filter(sort='AN', title=row[1]):
            new_tag = FeedTags(
                sort='AN',
                title=row[1],
                style=mapper[row[2]],
                tags=json.dumps(row[3].split(','))
            )
            new_tag.save()

    old_db = epi_tags_sql()
    for row in old_db:
        if row[2] != 2 and not FeedTags.objects.filter(sort='EP', title=row[1]):
            new_tag = FeedTags(
                sort='EP',
                title=row[1],
                style=mapper[row[2]],
                tags=json.dumps(row[3].split(','))
            )
            new_tag.save()

    c = langconv.Converter('zh-hans')
    old_db = ani_info_sql()
    for row in old_db:
        title = c.convert(row[2])
        if not FeedInfo.objects.filter(title=title):
            new_info = FeedInfo(
                sort='AN',
                title=title,
                now_playing=row[6],
            )
            new_info.save()

    old_db = epi_info_sql()
    for row in old_db:
        if not FeedInfo.objects.filter(title=row[2]):
            new_info = FeedInfo(
                sort='EP',
                title=row[2],
                now_playing=row[6],
            )
            new_info.save()
