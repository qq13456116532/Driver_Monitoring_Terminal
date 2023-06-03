# Generated by Django 2.0.6 on 2018-07-27 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_management', '0002_auto_20180727_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='troubletag',
            options={'verbose_name': '故障标签表', 'verbose_name_plural': '故障标签表'},
        ),
        migrations.AlterField(
            model_name='troublerecord',
            name='event_time',
            field=models.DateTimeField(verbose_name='故障时间'),
        ),
        migrations.AlterField(
            model_name='troublerecord',
            name='handle_time',
            field=models.DateTimeField(verbose_name='处理时间'),
        ),
    ]
