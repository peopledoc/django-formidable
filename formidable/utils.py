from importlib import import_module


def import_object(object_path):
    """
    Import class or function by path
    :param object_path: path to the object for import
    :return: imported object
    """
    module_path, class_name = object_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, class_name)
