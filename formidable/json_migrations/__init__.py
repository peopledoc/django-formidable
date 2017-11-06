import os
import sys
from glob import glob
from importlib import import_module

__all__ = ['latest_version', 'migrate']

HERE = os.path.dirname(__file__)

package = sys.modules[__name__].__name__


def _get_migrations():
    """
    Return a generator with all JSON migrations sorted.

    Each item is a tuple with:
      - the version number (int)
      - the label of the migration
      - the reference to the migrate() function

    """
    for module in sorted(glob(os.path.join(HERE, '[0-9]*.py'))):
        module_name, _ = os.path.basename(module).rsplit('.', 1)
        mod = import_module('.' + module_name, package=package)

        version, label = module_name.split('_', 1)

        yield int(version), label, mod.migrate


def migrate(data, version_src=0):
    """
    Apply all migrations from ``version_src`` to the latest found on
    ``data``.

    """
    for version, label, func in list(_get_migrations()):
        if version_src < version:
            data = func(data)
            data['version'] = version
            version_src = version

    return data


latest_version = max(migration[0] for migration in list(_get_migrations()))
