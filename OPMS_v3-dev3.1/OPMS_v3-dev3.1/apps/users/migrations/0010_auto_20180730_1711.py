# Generated by Django 2.0.6 on 2018-07-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_useraskhelp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogininfo',
            name='agent',
            field=models.CharField(max_length=200, verbose_name='客户端'),
        ),
    ]
