# Generated by Django 2.0.6 on 2023-05-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_terminal', '0005_auto_20230513_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoterminalinfo',
            name='add_time',
            field=models.DateTimeField(verbose_name='添加时间'),
        ),
    ]
