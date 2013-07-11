# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    return Response(data=data)


@api_view(['POST'])
def add_xunlei_id(request):
    status = False
    if 'xunlei-id' in request.POST and 'xunlei-password' in request.POST:
        from xunlei.lixian_control import add_user
        status = add_user(request.user, request.POST['xunlei-id'], request.POST['xunlei-password'])
    return Response(data=status)
