# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('front_end/index.html')


def index_manifest(request):
    return HttpResponse("nothing")
    # return render_to_response('front_end/index.manifest', content_type='text/cache-manifest')
