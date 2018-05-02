# from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import *
# from django.core import serializers

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import *

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    p=Profile.objects.prefetch_related('posts').select_related().filter(pk=2).values()[0]
    # ps=Profile.objects.raw('select profiles.id, profiles.name, (select posts.content, posts.profile_id from posts where posts.profile_id=profiles.id) posts  from profiles')
    # ps1=serializers.serialize('json',ps,fields=('id', 'name'))
    return JsonResponse(p, safe=False)

def profile_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)    