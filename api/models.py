# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Create your models here.
from django.utils import timezone
# from datetime import datetime, timedelta
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# INSERT INTO tab1( id,name,email,password_digest,token,json,avatar,created_at,updated_at,nationality,city,age,telenumber ) SELECT field1,field2,field3,field4,field5,field6,field7,field8,field9,field10,field11,field12,field13,field14,field15,field16  FROM  users

class Profile(models.Model):
    name = models.CharField(max_length=30, blank=True)
    email = models.CharField(max_length=30, blank=True)
    password_digest = models.CharField(max_length=300, blank=True)
    token = models.CharField(max_length=30, blank=True)
    json = models.CharField(max_length=30, blank=True)
    avatar = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    nationality = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    age = models.CharField(max_length=30, blank=True)
    telenumber = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=30, blank=True)
    cafeshop = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profiles'
        indexes = [
            models.Index(fields=['email', 'token']),
        ]
    #when use created
    @receiver(post_save, sender=User)
    def create_user_then_create_profile(sender, instance, created, **kwargs):
        if created:
            # Profile.objects.create(user=instance)
            Profile.objects.create(user=instance,name=instance.username,password_digest=instance.password,email=instance.email)
    #when use updated
    @receiver(post_save, sender=User)
    def update_user_then_update_profile(sender, instance, **kwargs):
        instance.profile.email = instance.email
        instance.profile.save() #insert and update both use save() insert 和 update 共用save()
    #when profile created
    # @receiver(post_save, sender=Profile)
    # def create_profile_then_create_user(sender, instance, created, **kwargs):
    #     if created:
    #         # Profile.objects.create(user=instance)
    #         User.objects.create(username=instance.username,password=instance.password_digest,email=instance.email)
    #when profile updated
    # @receiver(post_save, sender=Profile)
    # def update_profile_then_update_user(sender, instance, **kwargs):
    #     instance.user.email = instance.email
    #     instance.user.save() #insert and update both use save() insert 和 update 共用save()
    # @receiver(post_delete, sender=self)
    # def delete_profile_then_delete_user(sender, instance, **kwargs):
    #     instance.user.delete()

    def delete(self):
        super(Profile, self).delete()
        self.user.delete()

    def get_dict(self):
        return {'id': self.id,
                'is_superuser': self.user.is_superuser,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'is_active': self.user.is_active,
                'is_staff': self.user.is_staff,
                'username': self.user.username,
                'date_joined': self.user.date_joined,
                'last_login': self.user.last_login,
                'token': self.token}


class Post(models.Model):
    content = models.TextField(max_length=500)
    hidden = models.BooleanField(default=False)
    json = models.CharField(max_length=30, blank=True)    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    url = models.CharField(max_length=200,null=True, blank=True)  # new1

    class Meta:
        db_table = 'posts'


class Photo(models.Model):
    url = models.CharField(max_length=200, null=True, blank=True)  # new1
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='photos', blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    class Meta:
        db_table = 'photos'


class Comment(models.Model):
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', blank=True, null=False)    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments', blank=True, null=False)    
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    class Meta:
        db_table = 'comments'

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)       

    class Meta:
        db_table = 'tags'


class Relation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)       
    #user friendship
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="from_tos",  default=1)#以from_profile_id 为外键
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="froms_to",  default=1)#以to_profile_id 为外键
    #tag-post relation
    tagpost_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="tagpost_tags", default=1)
    tagpost_tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagpost_posts", default=1)
    #tag-profile relation
    tagprofile_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="tagprofile_tags", default=1)
    tagprofile_tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagprofile_profiles", default=1)


    class Meta:
        db_table = 'relations'






# class PermissionsMixin(models.Model):
#     """
#     A mixin class that adds the fields and methods necessary to support
#     Django's Group and Permission model using the ModelBackend.
#     """
#     is_superuser = models.BooleanField(
#         _('superuser status'),
#         default=False,
#         help_text=_(
#             'Designates that this user has all permissions without '
#             'explicitly assigning them.'
#         ),
#     )
#     groups = models.ManyToManyField(
#         Group,
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_(
#             'The groups this user belongs to. A user will get all permissions '
#             'granted to each of their groups.'
#         ),
#         related_name="user_set",
#         related_query_name="user",
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name="user_set",
#         related_query_name="user",
#     )

#     class Meta:
#         abstract = True

#     def get_group_permissions(self, obj=None):
#         """
#         Returns a list of permission strings that this user has through their
#         groups. This method queries all available auth backends. If an object
#         is passed in, only permissions matching this object are returned.
#         """
#         permissions = set()
#         for backend in auth.get_backends():
#             if hasattr(backend, "get_group_permissions"):
#                 permissions.update(backend.get_group_permissions(self, obj))
#         return permissions

#     def get_all_permissions(self, obj=None):
#         return _user_get_all_permissions(self, obj)

#     def has_perm(self, perm, obj=None):
#         """
#         Returns True if the user has the specified permission. This method
#         queries all available auth backends, but returns immediately if any
#         backend returns True. Thus, a user who has permission from a single
#         auth backend is assumed to have permission in general. If an object is
#         provided, permissions for this specific object are checked.
#         """

#         # Active superusers have all permissions.
#         if self.is_active and self.is_superuser:
#             return True

#         # Otherwise we need to check the backends.
#         return _user_has_perm(self, perm, obj)

#     def has_perms(self, perm_list, obj=None):
#         """
#         Returns True if the user has each of the specified permissions. If
#         object is passed, it checks if the user has all required perms for this
#         object.
#         """
#         return all(self.has_perm(perm, obj) for perm in perm_list)

#     def has_module_perms(self, app_label):
#         """
#         Returns True if the user has any permissions in the given app label.
#         Uses pretty much the same logic as has_perm, above.
#         """
#         # Active superusers have all permissions.
#         if self.is_active and self.is_superuser:
#             return True

#         return _user_has_module_perms(self, app_label)


# class AbstractUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.

#     Username and password are required. Other fields are optional.
#     """
#     username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=30, blank=True)
#     email = models.EmailField(_('email address'), blank=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

#     objects = UserManager()

#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')
#         abstract = True

#     def clean(self):
#         super(AbstractUser, self).clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def get_full_name(self):
#         """
#         Returns the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         "Returns the short name for the user."
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """
#         Sends an email to this User.
#         """
#         send_mail(subject, message, from_email, [self.email], **kwargs)


# class User(AbstractUser):
#     """
#     Users within the Django authentication system are represented by this
#     model.

#     Username, password and email are required. Other fields are optional.
#     """
#     class Meta(AbstractUser.Meta):
#         swappable = 'AUTH_USER_MODEL'