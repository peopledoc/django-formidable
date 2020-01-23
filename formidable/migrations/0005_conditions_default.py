from django.db import migrations
from jsonfield import JSONField


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0004_formidable_conditions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formidable',
            name='conditions',
            field=JSONField(default=list),
        ),
    ]
