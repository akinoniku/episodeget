# coding=utf-8
import json
from django.core import serializers
from django.core.cache import get_cache
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from feeds_analysis.models import Info, Douban, SubList, Tags


def index(request):
    return render_to_response('front_end/index.html',
                              {
                                  'info_list': Info.objects.filter(sort='AN').select_related().order_by(
                                      '-douban__average')[6:14]})


def info_list(request, sort, ):
    info_lists = get_info_list_cache(sort)
    return render_to_response('front_end/info_list.html', {'info_list': info_lists})


def info_view(request, id, ):
    info = Info.objects.filter(pk=id).prefetch_related()
    if not info:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    sub_lists = SubList.objects.filter(info_id=id).prefetch_related()
    tags = get_tags_list_cache(info.get().sort)
    tid_list = []
    sub_lists_simple = {}
    for list in sub_lists:
        tag_ids = list.tags_index.split(',')
        sub_lists_simple[list.id] = tag_ids
        for t in tag_ids:
            if t not in tid_list:
                tid_list.append(int(t))
    return render_to_response('front_end/info_view.html',
                              {'page': 'view',
                               'info': info.get(),
                               'sub_lists': sub_lists,
                               'tags': tags,
                               'sub_lists_json': json.dumps(sub_lists_simple, ensure_ascii=False),
                               'tags_json': json.dumps(tags, ensure_ascii=False),
                               'tid_list': tid_list,
                              }
    )


def index_manifest(request):
    return HttpResponse("nothing")
    # return render_to_response('front_end/index.manifest', content_type='text/cache-manifest')


def get_info_show(info_id):
    return Info.objects.select_related().get(pk=info_id)


def get_info_list_cache(sort):
    cache = get_cache('default')
    cache_key = 'get_info_list_cache_' + sort
    result_list = cache.get(cache_key)
    if not result_list:
        info_list = Info.objects.filter(sort=sort).select_related().order_by('-douban__average')
        result_list = []
        for info in info_list:
            if info.sublist_set.count():
                result_list.append(info)
        cache.set(cache_key, result_list, 3600)
    return result_list


def get_tags_list_cache(sort):
    cache = get_cache('default')
    cache_key = 'get_tags_list_cache_' + sort
    # result_list = cache.get(cache_key)
    result_list = []
    if not result_list:
        for tag in Tags.objects.filter(sort=sort).exclude(style='TL'):
            result_list.append({'style': tag.style, 'id': tag.id, 'title': tag.title})
        cache.set(cache_key, result_list, 3600)
    return result_list
