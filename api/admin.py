from django.contrib import admin
from .models import *
# Register your models here.
# from django.core.urlresolvers import reverse #before 2.0
from django.urls import reverse
from django.utils.safestring import mark_safe    

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False

class CustomUserAdmin(UserAdmin):
    # inlines = [ProfileInline]
    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)


class CustomAdmin(admin.ModelAdmin):
    # list_display = ('id','name','email','password_digest','token','json','avatar','created_at','updated_at','nationality','city','age','telenumber' )
    # list_display = ('id','name','email','token','created_at','updated_at','nationality','city','age','telenumber','user' )
    # list_display_links = ('first_name', 'last_name')
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name not in ('json','avatar','password_digest')]
        super(CustomAdmin, self).__init__(model, admin_site)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','avatar_img','name','email','token','created_at','updated_at','nationality','city','age','telenumber', 'user_link' )
    list_display_links = ('id', 'email')
    # Add it to the details view:
    search_fields = ('=id','name', '=age')
    # inlines = [ProfileUserInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            obj.user.username
        ))
    user_link.short_description = 'user'

    def avatar_img(self, obj):
        return mark_safe('<img width="50" height="50" src="{}" />'.format(obj.avatar))
    avatar_img.short_description = 'avatar'

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'url','user_link' )
    list_display_links = ('id', 'content',)
    search_fields = ('=id','content','profile__email','profile__name')
    
    # list_select_related = ('profile',)
    # Add it to the details view:
    # read_only_fields = ('user_link',)
    # inlines = [ProfileUserInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            obj.profile.name
        ))
    user_link.short_description = 'user'

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id','url','image','user_link' )
    list_display_links = ('id', 'image')
    # Add it to the details view:
    search_fields = ('=id','profile__email','profile__name')
    # inlines = [ProfileUserInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            obj.profile.name
        ))
    user_link.short_description = 'user'

    def image(self, obj):
        return mark_safe('<img width="100" height="100" src="{}" />'.format(obj.url))
    image.short_description = 'image'

class CommentAdmin(admin.ModelAdmin):
    list_display =  ('id','content','user_link','post_link')
    # list_display_links = ('first_name', 'last_name')
    # Add it to the details view:
    search_fields = ('content','post__content','profile__email','profile__name')
    # inlines = [ProfileUserInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            obj.profile.name
        ))
    user_link.short_description = 'user'

    def post_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_post_change", args=(obj.post.pk,)),
            obj.post.content
        ))
    user_link.short_description = 'post'



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)