import datetime

from django.utils import timezone
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
import random

class ProfileModelTest(TestCase):
    # fixtures = ['all.json','api.relation']

#     # def setUp(self):
#     #     # Test definitions as before.
#     #     # call_setup_methods()

#     # @classmethod
#     # def setUpTestData(cls):
#     #     # Set up non-modified objects used by all test methods
#     #     User.objects.create(username='user1',password='gsp191954')
#     #     #Comment.objects.create() 返回 <Comment: Comment object (33)>, ct = c1.save() 不返回任何值, c=Comment()
#     #     # user=User.objects.get(pk=1)
#     #     # Profile.objects.create(user=user, name='big', email='big@gmail.com')
#     #     # self.assertIs(future_question.was_published_recently(), False)
#     #     #  self.assertFalse(form.is_valid())
#     #     #  self.assertTrue(form.is_valid())

    def test_db(self):
        p = Profile.objects.get(pk=3)
        self.assertEqual(p.id, 3)

    def test_user_post_save_profile(self):
        user = User.objects.get(pk=1)
        profile = Profile.objects.get(pk=1)
        self.assertEquals(profile.user_id, user.id)
    
    def test_from_to(self):
        n1 = str(random.random())
        n2 = str(random.random())
        u1=User.objects.create(username=n1,password='gsp123456')
        u2=User.objects.create(username=n2,password='gsp123456')
        p1=u1.profile
        p2=u2.profile
        r=Relation.objects.create(from_profile=p1, to_profile=p2)
        b1=p2 in p1.from_tos
        b2=p1 in p2.to_froms
        self.assertTrue(b1&b2)




