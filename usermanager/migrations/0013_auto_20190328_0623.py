# Generated by Django 2.0.8 on 2019-03-28 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0012_auto_20190328_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selfie',
            field=models.ImageField(blank=True, default='me.jpg', upload_to=''),
        ),
    ]
