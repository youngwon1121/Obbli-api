# Generated by Django 2.0.8 on 2019-04-02 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announce', '0003_auto_20190328_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='announce',
            name='instrumental_type',
            field=models.CharField(choices=[('Wind', '관악기'), ('String', '현악기'), ('Percussion', '타악기'), ('Keyboard', '건반악기'), ('Vocal', '성악')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
