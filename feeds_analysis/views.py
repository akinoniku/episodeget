# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from rest_framework import generics
from feeds_analysis.analysiser import analysis_tags
from feeds_analysis.models import Rss, Info
from feeds_analysis.serializers import RssSerializer
from feeds_analysis.updater import get_ani_rss, get_epi_rss, get_ani_new, get_epi_new
from old_db_reader.reader import old_db_reader
from xunlei.lixian_control import add_task


def update_all(request):
    get_ani_rss()
    get_epi_rss()
    get_ani_new()
    get_epi_new()
    return HttpResponse("Update Done")


def ana_rss(request, id):
    rss = Rss.objects.get(pk=id)
    analysis_tags(rss)
    HttpResponse('Analysis ani Done')


def ana_rss_all(request):
    all_rss = Rss.objects.all().order_by('id').reverse()
    for rss in all_rss:
        analysis_tags(rss)
    return HttpResponse('Analysis Done')


def read_old_db(request):
    old_db_reader()
    return HttpResponse("Read Old db Done")


class RssList(generics.ListCreateAPIView):
    model = Rss
    serializer_class = RssSerializer


class RssDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Rss
    serializer_class = RssSerializer

#belows are test function


def add_task_test(request):
    add_task('', Rss.objects.get(pk=5))


def init_test(request):
    read_old_db(request)
    update_all(request)
    for info in Info.objects.all():
        info.create_tag_test()
    ana_rss_all(request)
    return HttpResponse('All Done')
