# coding=utf-8
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core import serializers
from django.core.cache import get_cache
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from feeds_analysis.models import Info, Douban, SubList, Tags
from feeds_analysis.serializers import UserSerializer
from user_settings.models import SubListPrefer, Xunlei


@ensure_csrf_cookie
def index(request):
    return render_to_response('front_end/index.html',
                              {'page': 'index', },
                              RequestContext(request))


@ensure_csrf_cookie
def index_old(request):
    return render_to_response('front_end/home_page.html',
                              {'page': 'index', },
                              RequestContext(request))


@api_view(['POST'])
@permission_classes((AllowAny, ))
def login_ajax(request):
    if request.POST and request.is_ajax:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            user_serializer = UserSerializer(user)
            return Response(data=user_serializer.data)
        else:
            return HttpResponse(json.dumps({'id': 0}), content_type='application/json')


def user_prefer_list(request):
    if request.is_ajax():
        if len(SubListPrefer.objects.filter(user=request.user)):
            SubListPrefer.objects.filter(user=request.user).update(preferList=request.POST['list'])
        else:
            prefer = SubListPrefer(
                user=request.user,
                preferList=request.POST['list'],
            )
            prefer.save()
        return HttpResponse(json.dumps({'status': True}))
    list_an = Tags.objects.filter(sort='AN').exclude(style='TL')
    list_ep = Tags.objects.filter(sort='EP').exclude(style='TL')
    titles = {'TM': '字幕组', 'CL': '清晰度', 'FM': '格式', 'TL': '字幕语言'}
    return Response('front_end/list_prefer.html',
                              {'page': 'list_prefer',
                               'titles': titles,
                               'an': list_an,
                               'ep': list_ep},
                              RequestContext(request))


def user_account(request):
    has_xunlei = True if len(Xunlei.objects.filter(user=request.user)) else False
    added = request.GET['sub_list'] if 'sub_list' in request.GET else False
    sub_list = SubList.objects.select_related().filter(user=request.user)
    return render_to_response('front_end/accounts.html',
                              {'page': 'user_account',
                               'sub_list': sub_list,
                               'added': added,
                               'has_xunlei': has_xunlei,
                              },
                              RequestContext(request))


def user_xunlei(request):
    status = False
    if 'xunlei-id' in request.POST and 'xunlei-password' in request.POST:
        from xunlei.lixian_control import add_user

        status = add_user(request.user, request.POST['xunlei-id'], request.POST['xunlei-password'])
    return HttpResponse(json.dumps({'status': status}))


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
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
    except BaseException, e:
        status = False
        msg = '未知错误'
        if e.args[0] == 1062:
            msg = '跟别人重名了！'
    return HttpResponse(json.dumps({'msg': msg,
                                    'url': '/accounts/prefer/',
                                    'status': status}))


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_current_user(request):
    user_serializer = UserSerializer(request.user)
    return Response(data=user_serializer.data)


@ensure_csrf_cookie
def info_list(request, sort, ):
    info_lists = get_info_list_cache(sort)
    return render_to_response('front_end/info_list.html', {'info_list': info_lists}, RequestContext(request))


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes((AllowAny, ))
def info_view(request, info_id):
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


def get_sub_list_rss(request):
    try:
        list_id = request.POST['list_id']
        sub_list = SubList.objects.prefetch_related().get(pk=list_id)
        rss = sub_list.rss.all()
        return HttpResponse(serializers.serialize('json', rss))
    except:
        return HttpResponseNotFound('List not found')


def add_sub_list(request):
# try:
    list_id = request.POST['list_id']
    sub_list = SubList.objects.get(pk=list_id)
    sub_list.user.add(request.user)
    sub_list.save()
    return HttpResponse(json.dumps({'status': 'success'}))
    #except:
    #    return HttpResponseNotFound('List not found')


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
