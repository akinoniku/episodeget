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
    prefer = SubListPrefer.objects.get(user=user)
    if prefer.id:
        prefer.preferList = prefer_list
        prefer.save()
    else:
        prefer = SubListPrefer(
            user=user,
            preferList=prefer_list
        )
        prefer.save()
    Response(data=True)


@api_view(['POST'])
def get_prefer(request):
    user = request.user
