import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse


from news.models import Video, UpInfo
from news.gen import generate_charts


def gen(request):
    context = {}
    # list = Video.objects.filter(up_name='学码匠')
    # context['list'] = list
    # generate_charts.gen('tu')
    return render(request, 'tu.html', context)


def index(request):
    res = {'ups': UpInfo.objects.all()}
    return render(request, 'index.html', res)


def list(request):
    print('enter list view')
    return render(request, 'list.html')


def single_cloud(request):
    mid = request.GET.get('mid')
    videos = Video.objects.filter(mid=mid).order_by('-bfl')
    res = []
    for video in videos:
        res.append({'title': video.title, 'mid': video.mid, 'url': video.url, 'play_cnt': video.bfl})
    return JsonResponse(json.dumps(res, ensure_ascii=False), content_type='application/json', safe=False)
