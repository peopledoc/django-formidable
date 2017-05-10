# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0002_remove_access_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.TextField(),
        ),
    ]
