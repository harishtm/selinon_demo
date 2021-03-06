# Generated by Django 2.0.6 on 2018-08-08 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0007_auto_20180616_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='NodeRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('python_class', models.CharField(max_length=100, verbose_name='Class Implementation')),
                ('python_package', models.CharField(max_length=100, verbose_name='Package holds Class')),
                ('node_type', models.CharField(choices=[('TRANSFORM', 'Transformation Node'), ('ACTION', 'Validation Action Execution Node'), ('CONDITION', 'Condition Node To Execute Validation'), ('SINK', 'Storage Node To Sink Data')], default='ACTION', max_length=20, verbose_name='Node Type')),
                ('registered', models.DateTimeField(auto_now_add=True, help_text='Date on which node registered', null=True, verbose_name='Registration Date')),
                ('version', models.FloatField(default=1.0, verbose_name='Node version')),
            ],
        ),
    ]
