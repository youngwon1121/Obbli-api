# Generated by Django 2.0.8 on 2019-04-18 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanager', '0015_profile_awards'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPW',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('hash_key', models.CharField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
