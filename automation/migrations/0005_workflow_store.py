# Generated by Django 2.0.6 on 2018-06-15 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20180523_0655'),
        ('automation', '0004_auto_20180615_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='store',
            field=models.ForeignKey(default='a3a802fcc7604a46a49d5c57150d8d99', on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='Store'),
            preserve_default=False,
        ),
    ]