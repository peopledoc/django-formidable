from django.core.management.base import BaseCommand, CommandError
from formidable.serializers.forms import FormidableSerializer
import json


class Command(BaseCommand):
    help = 'Populate'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in options['filename']:
            with open(filename) as f:
                data = json.load(f)
                serializer = FormidableSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write('Successfully populate "%s"' % filename)
                else:
                    self.stdout.write('Broken "%s" %s' % (filename, serializer.errors))
