import os
import sys
from glob import glob
from importlib import import_module

__all__ = ['migrate', 'get_migrations']

HERE = os.path.dirname(__file__)

package = sys.modules[__name__].__name__


def get_migrations():
    for module in sorted(glob(os.path.join(HERE, '[0-9]*.py'))):
        module_name, _ = os.path.basename(module).rsplit('.', 1)
        mod = import_module('.' + module_name, package=package)

        version, label = module_name.split('_', 1)

        yield int(version), label, mod.migrate


def migrate(data, version_src=0):
    for version, label, func in list(get_migrations()):
        if version_src < version:
            data = func(data)
            version_src = version
    return data
