# Generated by Django 3.1.1 on 2020-11-24 16:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eventFinder', '0012_auto_20201123_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='events_attended', to=settings.AUTH_USER_MODEL),
        ),
    ]
