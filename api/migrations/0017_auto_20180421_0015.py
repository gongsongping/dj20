# Generated by Django 2.0.4 on 2018-04-21 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20180420_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='to_profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='to_froms_rs', to='api.Profile'),
        ),
    ]
