# Generated by Django 2.0.6 on 2018-09-14 06:54

import automation.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_storecountry'),
        ('automation', '0012_catalogueworkflow'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutomationWorkflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.ImageField(max_length=255, upload_to=automation.models.validator_image_directory_path, verbose_name='Thumbnail')),
                ('name', models.CharField(max_length=30, verbose_name='Automation Workflow Name')),
                ('description', models.CharField(max_length=30, verbose_name='Automation Workflow Description')),
                ('totalRunCount', models.IntegerField(default=0, verbose_name='Total Run Count')),
                ('totalFailureCount', models.IntegerField(default=0, verbose_name='Total Failure Count')),
                ('workflowFile', models.FileField(upload_to=automation.models.workflow_file_path)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date on workflow created', null=True, verbose_name='Registration Date')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='Store')),
            ],
        ),
        migrations.RemoveField(
            model_name='catalogueworkflow',
            name='store',
        ),
        migrations.DeleteModel(
            name='CatalogueWorkflow',
        ),
    ]
