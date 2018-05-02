from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    # ,'tagprofile_profiles','tagpost_posts'
    class Meta:
        model = User
        exclude = ('password',)        
        # fields = ('id','name','created_at','updated_at')

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

    comment_count = serializers.SerializerMethodField()
    def get_comment_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Post
        fields = ('id', 'content','url','created_at','updated_at','profile','comments','comment_count')

class ProfileSerializer(serializers.ModelSerializer):
    # posts = serializers.StringRelatedField(many=True)
    # posts = PostSerializer(many=True, read_only=True)
    user = UserSerializer() #要去除password,所以用此

    # from_tos = serializers.SerializerMethodField()
    # def get_from_tos(self, obj):
    #     # return obj.from_tos #Object of type 'Profile' is not JSON serializable
    #     return  ProfileSerializer(obj.from_tos)  # ProfileSerializer(profiles, many=True)
    
    class Meta:
        model = Profile
        # exclude = ('password_digest','token','json')
        fields = ('id', 'name','email','avatar','created_at','updated_at','nationality','city','age','telenumber','user','posts')
        # tab1( id,name,email,password_digest,token,json,avatar,created_at,updated_at,nationality,city,age,telenumber
        depth = 1









