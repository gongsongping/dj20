from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        fields = ('id', 'content','url','created_at','updated_at','profile')

class ProfileSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True)
    # posts = PostSerializer(many=True, read_only=True)
    class Meta:
        model = Profile
        fields = ('id', 'name','email','avatar','created_at','updated_at','nationality','city','age','telenumber','user','posts')
        # tab1( id,name,email,password_digest,token,json,avatar,created_at,updated_at,nationality,city,age,telenumber
        depth = 1









