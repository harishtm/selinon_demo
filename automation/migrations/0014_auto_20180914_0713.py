# Generated by Django 2.0.6 on 2018-09-14 07:13

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0013_auto_20180914_0654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='automationworkflow',
            name='workflowFile',
        ),
        migrations.AddField(
            model_name='automationworkflow',
            name='workflowSpec',
            field=django_mysql.models.JSONField(default=dict),
        ),
    ]
