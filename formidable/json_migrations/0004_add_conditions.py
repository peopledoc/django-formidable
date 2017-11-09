"""
Add conditions as an empty list if it doesn't exist in the form.

This JSON migration is related to:
  * 0004_formidable_conditions
  * 0005_conditions_default

"""


def migrate(data):
    if 'conditions' not in data:
        data.setdefault('conditions', [])

    return data
