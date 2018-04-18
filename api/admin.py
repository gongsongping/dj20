from django.contrib import admin
from .models import *
# Register your models here.
# from django.core.urlresolvers import reverse #before 2.0
from django.urls import reverse
from django.utils.safestring import mark_safe    


class CustomAdmin(admin.ModelAdmin):
    # list_display = ('id','name','email','password_digest','token','json','avatar','created_at','updated_at','nationality','city','age','telenumber' )
    # list_display = ('id','name','email','token','created_at','updated_at','nationality','city','age','telenumber','user' )
    # list_display_links = ('first_name', 'last_name')
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name not in ('json','avatar','password_digest')]
        super(CustomAdmin, self).__init__(model, admin_site)
    
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','token','created_at','updated_at','nationality','city','age','telenumber', 'user_link' )
    # list_display_links = ('first_name', 'last_name')
    # Add it to the details view:
    read_only_fields = ('user_link',)

    def user_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:auth_user_change", args=(obj.user.pk,)),
            obj.user.username
        ))
    user_link.short_description = 'user'

# class PersonAdmin(admin.ModelAdmin):
# # class PersonAdmin(admin.UserAdmin):
#     list_filter = ('username', 'email')
#     # search_fields = ('email',)
#     list_display_links = ('first_name', 'last_name')    
#     def __init__(self, model, admin_site):
#             self.list_display = [
#                 field.name for field in model._meta.fields if field.name not in ["id","password"]]
#             super(PersonAdmin, self).__init__(model, admin_site)

class UserAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name not in ["id","password"]]
        super(UserAdmin, self).__init__(model, admin_site)


class PostAdmin(CustomAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)