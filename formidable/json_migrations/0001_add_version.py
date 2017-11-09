"""
The field help_text has been renamed into description.

"""


def migrate(data):
    if 'version' not in data:
        data['version'] = 0

    return data
