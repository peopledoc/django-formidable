from django.core.management.base import BaseCommand
from formidable.serializers.forms import FormidableSerializer
from formidable.models import Formidable
import json


class Command(BaseCommand):
    help = 'Populate'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)
        parser.add_argument('--append', action="store_true", default=False)

    def handle(self, *args, **options):
        for filename in options['filename']:
            with open(filename) as f:
                data = json.load(f)

                # By default, the serializer is for updating
                serializer = FormidableSerializer(data=data)
                if not options['append'] and 'id' in data:
                    try:
                        instance = Formidable.objects.get(id=data['id'])
                        # If the instance is found
                        # passing it will trigger an "update"
                        serializer = FormidableSerializer(
                            instance,
                            data=data
                        )
                    except Formidable.DoesNotExist:
                        self.stdout.write(
                            'Unknown Formidable form with pk: `%s`; creating'
                            % data['id'])

                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(
                        'Successfully populate "%s (%d)"'
                        % (serializer.instance, serializer.instance.pk))
                else:
                    self.stdout.write('Broken "%s" %s' % (
                        filename, serializer.errors))
