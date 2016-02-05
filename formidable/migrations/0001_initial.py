# -*- coding: utf-8 -*-
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
                ('level', models.CharField(max_length=128, choices=[(b'REQUIRED', b'Required'), (b'EDITABLE', b'Editable'), (b'HIDDEN', b'Hidden'), (b'READONLY', b'Readonly')])),
                ('display', models.CharField(blank=True, max_length=128, null=True, choices=[(b'FORM', b'Form'), (b'TABLE', b'Table')])),
            ],
        ),
        migrations.CreateModel(
            name='Fieldidable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=256)),
                ('label', models.CharField(max_length=256)),
                ('type_id', models.CharField(max_length=256)),
                ('placeholder', models.CharField(max_length=256, null=True, blank=True)),
                ('helpText', models.TextField(null=True, blank=True)),
                ('default', models.TextField(null=True, blank=True)),
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
                ('key', models.CharField(max_length=256)),
                ('value', models.CharField(max_length=256)),
                ('field', models.ForeignKey(related_name='items', to='formidable.Fieldidable')),
            ],
        ),
        migrations.CreateModel(
            name='Validationidable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=256)),
                ('message', models.TextField(null=True, blank=True)),
                ('field', models.ForeignKey(related_name='validations', to='formidable.Fieldidable')),
            ],
        ),
        migrations.AddField(
            model_name='fieldidable',
            name='form',
            field=models.ForeignKey(related_name='fields', to='formidable.Formidable'),
        ),
        migrations.AddField(
            model_name='access',
            name='field',
            field=models.ForeignKey(related_name='accesses', to='formidable.Fieldidable'),
        ),
        migrations.AlterUniqueTogether(
            name='fieldidable',
            unique_together=set([('slug', 'form')]),
        ),
        migrations.AlterUniqueTogether(
            name='access',
            unique_together=set([('field', 'access_id')]),
        ),
    ]
