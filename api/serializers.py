from rest_framework import serializers
from .models import *



class TagSerializer(serializers.ModelSerializer):
    # ,'tagprofile_profiles','tagpost_posts'
    class Meta:
        model = Tag
        fields = ('id','name','created_at','updated_at')

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('id','content','created_at','updated_at','profile','post')

class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = ('id','url','created_at','updated_at','profile')

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'content','url','created_at','updated_at','profile')

class ProfileSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True)
    # posts = PostSerializer(many=True, read_only=True)
    # ,'from_tos'
    class Meta:
        model = Profile
        fields = ('id', 'name','email','avatar','created_at','updated_at','nationality','city','age','telenumber','user','posts')
        # tab1( id,name,email,password_digest,token,json,avatar,created_at,updated_at,nationality,city,age,telenumber
        depth = 1









