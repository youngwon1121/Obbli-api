# Generated by Django 2.0.8 on 2019-03-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0004_auto_20190319_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selfie',
            field=models.ImageField(blank=True, default='me.jpg', upload_to=''),
        ),
    ]