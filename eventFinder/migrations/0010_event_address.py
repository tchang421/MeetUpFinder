# Generated by Django 3.1.1 on 2020-11-10 20:42

import address.models
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
        ('eventFinder', '0009_auto_20201110_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='address',
            field=address.models.AddressField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='address.address'),
        ),
    ]
