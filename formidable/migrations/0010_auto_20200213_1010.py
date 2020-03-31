from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0009_field_parameters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='default',
            name='value',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
