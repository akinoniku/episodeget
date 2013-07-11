# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_settings.models import SubListPrefer


def notify_user(user, rss):
    pass


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
