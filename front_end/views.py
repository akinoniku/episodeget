# coding=utf-8
import json
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from episodeget.settings import SAE_VERSION
from feeds_analysis.models import Info, Douban, SubList, Tags, Rss
from feeds_analysis.serializers import UserSerializer


@ensure_csrf_cookie
def index(request):
    return render_to_response('front_end/index.html',
                              {'page': 'index',
                               'IS_SAE': SAE_VERSION
                               },
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



@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_reg(request):
    status = True
    msg = '没有错误'
    user_serializer = False
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if len(User.objects.filter(email=email)):
            status = False
            msg = "Email 已经被注册过了"
        elif username and password and email:
            User.objects.create_user(username, email, password)
            user = authenticate(username=username, password=password)
            login(request, user)
            user_serializer = UserSerializer(user).data
    except BaseException, e:
        status = False
        msg = '未知错误'
        if e.args[0] == 1062:
            msg = '跟别人重名了！'
    return Response({'msg': msg,
                     'user': user_serializer,
                     'status': status})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_current_user(request):
    if request.user.id:
        user_serializer = UserSerializer(request.user)
        return Response(data=user_serializer.data)
    else:
        return Response(data=False)
        #return HttpResponseForbidden()


@ensure_csrf_cookie
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def add_sub_list(request):
    try:
        list_id = request.POST['list_id']
        sub_list = SubList.objects.get(pk=list_id)
        sub_list.user.add(request.user)
        sub_list.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    except Exception, e:
        return HttpResponseForbidden(e)


@permission_classes((IsAuthenticated, ))
def remove_sub_list(request):
    try:
        list_id = request.POST['list_id']
        sub_list = SubList.objects.get(pk=list_id)
        sub_list.user.remove(request.user)
        sub_list.save()
        return HttpResponse(json.dumps({'status': 'success'}))
    except Exception, e:
        return HttpResponseForbidden(e)


def index_manifest(request):
    return HttpResponse("nothing")
    # return render_to_response('front_end/index.manifest', content_type='text/cache-manifest')


def rss_feed(userId):
    try:
        user = User.objects.get(username=userId)
    except:
        return []
    sub_lists = SubList.objects.filter(user=user).select_related()
    all_rss = []
    for sub_list in sub_lists:
        all_rss = all_rss + list(sub_list.rss.all())
        if len(all_rss) > 50:
            break
    all_rss.sort(key=lambda x: x.timestamp, reverse=True)
    return all_rss
