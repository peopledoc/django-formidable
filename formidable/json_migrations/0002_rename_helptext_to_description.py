"""
The field help_text has been renamed into description.

"""


def migrate(data):
    if 'fields' in data:
        for field in data['fields']:
            if 'help_text' in field:
                field['description'] = field.pop('help_text')

    return data
