# Generated by Django 2.0.8 on 2019-03-28 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0011_auto_20190320_0819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='graduated_school',
        ),
        migrations.AddField(
            model_name='myuser',
            name='graduated_school',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]