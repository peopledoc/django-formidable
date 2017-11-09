"""
Uncontextualize forms.

"""

from formidable.json_migrations.utils import merge_context_forms


def migrate(data):
    return merge_context_forms(data)
