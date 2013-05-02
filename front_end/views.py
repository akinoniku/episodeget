# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context
from feeds_analysis.models import Info


def index(request):
    info_list = []
    for info_id in range(15, 23):
        info_list.append(get_info_show(info_id))
    return render_to_response('front_end/index.html', {'info_list': info_list})


def index_manifest(request):
    return HttpResponse("nothing")
    # return render_to_response('front_end/index.manifest', content_type='text/cache-manifest')

def get_info_show(info_id):
    return Info.objects.select_related().get(pk=info_id)
