from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0007_drop_preset_tables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='value',
            field=models.TextField(),
        ),
    ]
