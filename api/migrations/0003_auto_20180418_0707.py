# Generated by Django 2.0.4 on 2018-04-18 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20180418_0630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='profile',
        ),
    ]
