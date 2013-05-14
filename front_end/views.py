# coding=utf-8
import json
from django.contrib.auth.models import User
from django.core.cache import get_cache
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from feeds_analysis.models import Info, Douban, SubList, Tags


@ensure_csrf_cookie
def index(request):
    return render_to_response('front_end/index.html',
                              {'page': 'index', },
                              RequestContext(request))


def login_success(request):
    return HttpResponse(json.dumps({'url': '/accounts/',
                                    'status': True}))


def user_prefer_list(request):
    list_an = Tags.objects.filter(sort='AN').exclude(style='TL')
    list_ep = Tags.objects.filter(sort='EP').exclude(style='TL')
    titles = {'TM': '字幕组', 'CL': '清晰度', 'FM': '格式', 'TL': '字幕语言'}
    return render_to_response('front_end/list_prefer.html',
                              {'page': 'list_prefer',
                               'titles': titles,
                               'an': list_an,
                               'ep': list_ep},
                              RequestContext(request))


def user_account(request):
    var = 1
    return render_to_response('front_end/user_account.html',
                              {'page': 'user_account'},
                              RequestContext(request))


def user_reg(request):
    status = True
    msg = '没有错误'
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if len(User.objects.filter(email=email)):
            status = False
            msg = "Email 已经被注册过了"
        if username and password and email:
            user = User.objects.create_user(username, email, password)
    except BaseException, e:
        status = False
        msg = '未知错误'
        if e.args[0] == 1062:
            msg = '跟别人重名了！'
    return HttpResponse(json.dumps({'msg': msg,
                                    'url': 'account',
                                    'status': status}))


@ensure_csrf_cookie
def info_list(request, sort, ):
    info_lists = get_info_list_cache(sort)
    return render_to_response('front_end/info_list.html', {'info_list': info_lists}, RequestContext(request))


@ensure_csrf_cookie
def info_view(request, info_id, ):
    info = Info.objects.filter(pk=info_id).prefetch_related()
    if not info:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    sub_lists = SubList.objects.filter(info_id=info_id).prefetch_related()
    tags = get_tags_list_cache(info.get().sort)
    tid_list = []
    sub_lists_simple = {}
    for sub_list in sub_lists:
        tag_ids = sub_list.tags_index.split(',')
        sub_lists_simple[sub_list.id] = tag_ids
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
                              },
                              RequestContext(request))


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
    result_list = cache.get(cache_key)
    if not result_list:
        result_list = []
        for tag in Tags.objects.filter(sort=sort).exclude(style='TL'):
            result_list.append({'style': tag.style, 'id': tag.id, 'title': tag.title})
        cache.set(cache_key, result_list, 3600)
    return result_list
