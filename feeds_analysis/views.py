# coding=utf-8
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import generics
from feeds_analysis.analysiser import analysis_tags, send_notification
from feeds_analysis.models import Rss, Info, SubList, Tags
from feeds_analysis.serializers import RssSerializer, UserSerializer, InfoSerializer, SubListSerializer, TagsSerializer
from feeds_analysis.updater import get_ani_rss, get_epi_rss, get_ani_new, get_epi_new
from old_db_reader.reader import old_db_reader
from xunlei.lixian_control import add_task


def update_all(request):
    get_ani_rss()
    get_epi_rss()
    get_ani_new()
    get_epi_new()
    return HttpResponse("Update Done")


def ana_rss(request, rid):
    rss = Rss.objects.get(pk=rid)
    analysis_tags(rss)
    HttpResponse('Analysis ani Done')


def ana_rss_all(request):
    all_rss = Rss.objects.all().order_by('id').reverse()
    for rss in all_rss:
        analysis_tags(rss)
    return HttpResponse('Analysis Done')


def read_old_db(request):
    old_db_reader(rss=True)
    return HttpResponse("Read Old db Done")


class InfoList(generics.ListCreateAPIView):
    model = Info
    serializer_class = InfoSerializer
    paginate_by = 100

    def get_queryset(self):
        queryset = Info.objects.all()
        sort = self.request.QUERY_PARAMS.get('sort', None)
        now_playing = self.request.QUERY_PARAMS.get('now_playing', None)
        weeks = self.request.QUERY_PARAMS.get('weeks', None)
        if sort is not None:
            queryset = queryset.filter(sort=sort)
        if now_playing is not None:
            queryset = queryset.filter(now_playing=now_playing)
        #if weeks is not None:
        if True:
            queryset = queryset.filter(sublist__update_time__gt=(datetime.now() - timedelta(days=40))).distinct()
        return queryset


class InfoDetail(generics.RetrieveAPIView):
    model = Info
    serializer_class = InfoSerializer


class RssList(generics.ListAPIView):
    model = Rss
    serializer_class = RssSerializer


class RssDetail(generics.RetrieveAPIView):
    model = Rss
    serializer_class = RssSerializer


class TagsList(generics.ListAPIView):
    model = Tags
    serializer_class = TagsSerializer
    paginate_by = 300

    def get_queryset(self):
        queryset = Tags.objects.all()
        sort = self.request.QUERY_PARAMS.get('sort', None)
        if sort is not None:
            queryset = queryset.filter(sort=sort).exclude(style='TL')
        return queryset


class TagsDetail(generics.RetrieveAPIView):
    model = Tags
    serializer_class = TagsSerializer


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer


class SubListList(generics.ListAPIView):
    model = SubList
    serializer_class = SubListSerializer
    paginate_by = 100

    def get_queryset(self):
        queryset = SubList.objects.all()
        info = self.request.QUERY_PARAMS.get('info', None)
        user = self.request.QUERY_PARAMS.get('user', None)
        if info is not None:
            queryset = queryset.filter(info=info)
        elif user is not None:
            queryset = queryset.filter(user=self.request.user)
        queryset = queryset.filter(update_time__gt=(datetime.now() - timedelta(days=40)))
        return queryset


class SubListDetail(generics.RetrieveAPIView):
    model = SubList
    serializer_class = SubListSerializer

#belows are test function
def add_task_test(request):
    add_task('', Rss.objects.get(pk=5))


def test_notification(request):
    rss = Rss.objects.get(id=30710)
    sub_list = SubList.objects.get(id=2668)
    send_notification(rss, sub_list)


def init_test(request):
    read_old_db(request)
    update_all(request)
    for info in Info.objects.all():
        info.create_tag_test()
    ana_rss_all(request)
    return HttpResponse('All Done')
