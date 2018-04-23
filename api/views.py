# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core import serializers

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    p=Profile.objects.prefetch_related('posts').select_related().filter(pk=2).values()[0]
    # ps=Profile.objects.raw('select profiles.id, profiles.name, (select posts.content, posts.profile_id from posts where posts.profile_id=profiles.id) posts  from profiles')
    # ps1=serializers.serialize('json',ps,fields=('id', 'name'))
    return JsonResponse(p, safe=False)