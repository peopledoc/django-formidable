# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_id', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=128, choices=[('REQUIRED', 'Required'), ('EDITABLE', 'Editable'), ('HIDDEN', 'Hidden'), ('READONLY', 'Readonly')])),
                ('display', models.CharField(blank=True, max_length=128, null=True, choices=[('FORM', 'Form'), ('TABLE', 'Table')])),
            ],
        ),
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=256)),
                ('label', models.CharField(max_length=256)),
                ('type_id', models.CharField(max_length=256)),
                ('placeholder', models.CharField(max_length=256, null=True, blank=True)),
                ('help_text', models.TextField(null=True, blank=True)),
                ('multiple', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Formidable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
                ('label', models.CharField(max_length=256)),
                ('order', models.IntegerField()),
                ('help_text', models.TextField(null=True, blank=True)),
                ('field', models.ForeignKey(related_name='items', to='formidable.Field')),
            ],
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=128)),
                ('message', models.TextField(null=True, blank=True)),
                ('form', models.ForeignKey(related_name='presets', to='formidable.Formidable')),
            ],
        ),
        migrations.CreateModel(
            name='PresetArg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=128)),
                ('value', models.CharField(max_length=128, null=True, blank=True)),
                ('field_id', models.CharField(max_length=128, null=True, blank=True)),
                ('preset', models.ForeignKey(related_name='arguments', to='formidable.Preset')),
            ],
        ),
        migrations.CreateModel(
            name='Validation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=256)),
                ('message', models.TextField(null=True, blank=True)),
                ('field', models.ForeignKey(related_name='validations', to='formidable.Field')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='form',
            field=models.ForeignKey(related_name='fields', to='formidable.Formidable'),
        ),
        migrations.AddField(
            model_name='default',
            name='field',
            field=models.ForeignKey(related_name='defaults', to='formidable.Field'),
        ),
        migrations.AddField(
            model_name='access',
            name='field',
            field=models.ForeignKey(related_name='accesses', to='formidable.Field'),
        ),
        migrations.AlterUniqueTogether(
            name='field',
            unique_together=set([('slug', 'form')]),
        ),
        migrations.AlterUniqueTogether(
            name='access',
            unique_together=set([('field', 'access_id')]),
        ),
    ]
