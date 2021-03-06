# Generated by Django 2.0.6 on 2018-06-15 10:01

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('store', '0021_auto_20180523_0655'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('purpose', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ActionClassRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrption', models.TextField()),
                ('app_name', models.CharField(max_length=100, verbose_name='Action App Name')),
                ('class_name', models.CharField(max_length=30, verbose_name='Action Implementation Class')),
                ('action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='action_class', to='automation.Action', verbose_name='ActionClass')),
            ],
        ),
        migrations.CreateModel(
            name='ActionModelRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrption', models.TextField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='Content Type')),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('condition', models.CharField(blank=True, max_length=100, verbose_name='Condition')),
                ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='destination_action', to='automation.Action', verbose_name='Destination')),
            ],
        ),
        migrations.CreateModel(
            name='WorkFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('purpose', models.TextField()),
                ('data', django_mysql.models.JSONField(default=dict, null=True, verbose_name='flow data')),
                ('current_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workflow_current_action', to='automation.Action', verbose_name='Initial state')),
                ('initial_action', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workflow_initial_action', to='automation.Action', verbose_name='Initial state')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='Store')),
            ],
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='automation.WorkFlow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='actionmodelregister',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_model', to='automation.WorkFlow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='action',
            name='transitions',
            field=models.ManyToManyField(blank=True, related_name='actions', to='automation.Transition', verbose_name='Transitions'),
        ),
        migrations.AddField(
            model_name='action',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='automation.WorkFlow', verbose_name='Workflow'),
        ),
    ]
