# Generated by Django 1.11.6 on 2017-10-09 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0006_drop_preset_fields'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PresetArg',
        ),
        migrations.DeleteModel(
            name='Preset',
        ),
    ]
