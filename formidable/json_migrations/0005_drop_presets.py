"""
The presets attribute must be removed.

This JSON migration is related to:
  * 0006_drop_preset_fields
  * 0007_drop_preset_tables

"""


def migrate(data):
    if 'presets' in data:
        data.pop('presets')

    return data
