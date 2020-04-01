# Generated by Django 2.2 on 2020-04-01 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('announce', '0002_auto_20200331_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announce',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='announces', to=settings.AUTH_USER_MODEL),
        ),
    ]
