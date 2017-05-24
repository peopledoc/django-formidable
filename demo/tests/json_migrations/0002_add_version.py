"""
We add the version number of migrations.

"""


def migrate(data):
    data['version'] = 2

    return data
