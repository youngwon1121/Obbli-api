# Generated by Django 2.0.8 on 2019-03-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0005_auto_20190319_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selfie',
            field=models.ImageField(blank=True, default='me.jpg', null=True, upload_to=''),
        ),
    ]
