# Generated by Django 2.0.6 on 2018-06-15 10:26

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='data',
            field=django_mysql.models.JSONField(default=dict, null=True),
        ),
    ]