# Generated by Django 2.2.2 on 2019-07-02 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20190701_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(default='Unavailable', max_length=1024),
        ),
    ]
