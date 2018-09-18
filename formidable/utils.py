from importlib import import_module

import six


def import_object(object_path):
    """
    Import class or function by path
    :param object_path: path to the object for import
    :return: imported object
    """
    module_path, class_name = object_path.rsplit('.', 1)
    if six.PY3:
        module = import_module(module_path)
    else:
        module = import_module(module_path, [class_name])
    return getattr(module, class_name)
