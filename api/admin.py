from django.contrib import admin
from .models import *
# Register your models here.
# from django.core.urlresolvers import reverse #before 2.0
from django.urls import reverse
from django.utils.safestring import mark_safe    

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CommentInline(admin.TabularInline):
    model = Comment

class PostInline(admin.TabularInline):
    model = Post

class PhotoInline(admin.StackedInline):
    model = Photo

class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False

#等同于给用户加关注着
class From_tos(admin.TabularInline):
    model = Relation
    fk_name = "from_profile"

#等同于给用户加粉丝
# class Froms_to(admin.TabularInline):
#     model = Friendship
#     fk_name = "to_profile"

class CustomUserAdmin(UserAdmin):
    # UserAdmin.inlines = [ProfileInline]
    UserAdmin.list_display+=('id','profile_link')
    def profile_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            str(obj.profile.pk)+', '+obj.profile.name+', '+ obj.profile.email
        ))
    profile_link.short_description = 'profile'

    def add_view(self, *args, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.inlines = [ProfileInline]
        return super(UserAdmin, self).change_view(*args, **kwargs)


# class CustomAdmin(admin.ModelAdmin):
#     # list_display = ('id','name','email','password_digest','token','json','avatar','created_at','updated_at','nationality','city','age','telenumber' )
#     # list_display = ('id','name','email','token','created_at','updated_at','nationality','city','age','telenumber','user' )
#     # list_display_links = ('first_name', 'last_name')
#     def __init__(self, model, admin_site):
#         self.list_display = [
#             field.name for field in model._meta.fields if field.name not in ('json','avatar','password_digest')]
#         super(CustomAdmin, self).__init__(model, admin_site)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','avatar_img','name','email','token','created_at','updated_at','nationality','city','age','telenumber', 'user_link' )
    list_display_links = ('id', 'email')
    search_fields = ('=id','name', '=age')
    # Add it to the details view:
    exclude = ('password_digest',)
    readonly_fields = ('json','token',)  #user  
    inlines = [PostInline,  From_tos]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            str(obj.user.pk)+', '+obj.user.username+', '+ obj.user.email
        ))
    user_link.short_description = 'user'

    def avatar_img(self, obj):
        return mark_safe('<img width="50" height="50" src="{}" />'.format(obj.avatar))
    avatar_img.short_description = 'avatar'


class PostAdmin(admin.ModelAdmin):
    list_display = ('id','content', 'url','user_link', 'comments')
    list_display_links = ('id', 'content',)
    search_fields = ('=id','content','profile__email','profile__name')
    
    # list_select_related = ('profile',)
    # Add it to the details view:
    # readonly_fields = ('user_link',)
    inlines = [CommentInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            obj.profile.name
        ))
    user_link.short_description = 'user'

    def comments(self, obj):
        import json
        cmts = [c.content for c in obj.comments.all()]
        return json.dumps(cmts)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id','url','image','user_link' )
    list_display_links = ('id', 'image')
    # Add it to the details view:
    search_fields = ('=id','profile__email','profile__name')
    # inlines = [CommentInline]

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.profile.pk,)),
            obj.profile.name
        ))
    user_link.short_description = 'user'

    def image(self, obj):
        return mark_safe('<img width="100" height="100" src="{}" />'.format(obj.url))+ mark_safe('<img width="100" height="100" src="{}" />'.format(obj.url))
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
    post_link.short_description = 'post'

class RelationAdmin(admin.ModelAdmin):
    list_display =  ('id','from_link' ,'to_link')
    # list_display_links = ('first_name', 'last_name')
    # Add it to the details view:
    search_fields = ('from_profile__id','from_profile__name','from_profile__email','to_profile__id','to_profile__name','to_profile__email')
    # inlines = [ProfileUserInline]

    def from_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.from_profile.pk,)),
            str(obj.from_profile.id)+',  '+obj.from_profile.name+',  '+obj.from_profile.email
        ))
    from_link.short_description = 'from_profile'

    def to_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_profile_change", args=(obj.to_profile.pk,)),
            str(obj.to_profile.id)+',  '+obj.to_profile.name+',  '+obj.to_profile.email
        ))
    to_link.short_description = 'to_profile'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Relation, RelationAdmin)