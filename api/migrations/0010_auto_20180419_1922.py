# Generated by Django 2.0.4 on 2018-04-19 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180419_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendship',
            name='from_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_tos', to='api.Profile'),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='froms_to', to='api.Profile'),
        ),
    ]
