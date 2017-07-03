# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0004_formidable_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formidable',
            name='conditions',
            field=jsonfield.fields.JSONField(default=list),
        ),
    ]
