# Generated by Django 2.0.6 on 2018-07-18 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0006_auto_20180718_1157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messageuserinfo',
            old_name='is_start',
            new_name='is_star',
        ),
    ]