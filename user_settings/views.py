# Create your views here.
from datetime import timedelta, datetime
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from feeds_analysis.models import SubList, Info
from user_settings.models import SubListPrefer


@api_view(['POST'])
def save_prefer(request):
    user = request.user
    prefer_list = request.POST['list']
    try:
        prefer = SubListPrefer.objects.get(user=user)
    except:
        prefer = SubListPrefer(user=user)

    prefer.preferList = prefer_list
    prefer.save()
    return Response(data=True)


@api_view(['GET'])
def get_prefer(request):
    user = request.user
    try:
        prefer = SubListPrefer.objects.get(user=user)
        data = prefer.preferList
    except:
        data = False
    return Response(data=json.loads(data))


@api_view(['POST'])
def one_click_add(request):
    user = request.user
    try:
        prefer = SubListPrefer.objects.get(user=user)
        prefer = json.loads(prefer.preferList)
    except:
        prefer = False

    try:
        info = Info.objects.get(id=request.POST['infoId'])
    except:
        return Response(data=False)

    sub_lists = SubList.objects.filter(update_time__gt=(datetime.now() - timedelta(days=40))).filter().filter(info=info)

    #get avg time
    sum = 0
    for sub_list in sub_lists:
        sum += sub_list.rss.count()
    counter = 10
    avg = sum / sub_lists.count()
    if (avg/2) < 10:
        counter = avg/2

    weight = 0
    this_sub_list = 0
    select_sub_list = 0
    for sub_list in sub_lists:
        if sub_list.rss.count() < counter:
            continue
        else:
            tagIds = sub_list.tags_index.split(',')
            this_wight = 0
            this_sub_list = sub_list
            for pre in prefer[info.sort]:
                if pre in tagIds:
                    this_wight += 1
            if this_wight > weight:
                weight = this_wight
                select_sub_list = this_sub_list

    if not select_sub_list:
        select_sub_list = this_sub_list

    if not SubList.objects.filter(user=user).filter(id=select_sub_list.id).count():
        select_sub_list.user.add(user)
        select_sub_list.save()

    return Response(data=True)


@api_view(['POST'])
def add_xunlei_id(request):
    status = False
    if 'xunlei-id' in request.POST and 'xunlei-password' in request.POST:
        from xunlei.lixian_control import add_user

        status = add_user(request.user, request.POST['xunlei-id'], request.POST['xunlei-password'])
    return Response(data=status)
