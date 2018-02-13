from os.path import abspath, join, dirname
import json
import collections

from jsonschema import Draft4Validator
import yaml

ROOT_PATH = dirname(abspath(__file__))


def yaml2json():
    """
    Builds a dictionary of the BuilderForm definition out of the Swagger YAML.
    """
    # Setup support for ordered dicts so we do not lose ordering
    # when importing from YAML
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

    def dict_representer(dumper, data):
        return dumper.represent_mapping(_mapping_tag, data.iteritems())

    def dict_constructor(loader, node):
        return collections.OrderedDict(loader.construct_pairs(node))

    yaml.add_representer(collections.OrderedDict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)

    # Building raw data out of the Swagger Formidable definition
    swagger_file = join(ROOT_PATH, '..', 'swagger', 'formidable.yml')
    with open(swagger_file) as fd:
        data = yaml.load(fd)

    to_exclude = (
        'BuilderForm', 'InputError', 'BuilderError', 'InputForm', 'InputField'
    )
    definitions = (item for item in data['definitions'].items())
    definitions = filter(lambda item: item[0] not in to_exclude, definitions)

    new_data = {}
    new_data.update(data['definitions']['BuilderForm'])
    new_data.update({"definitions": dict(definitions)})
    return new_data


def _load_fixture(path):
    if not path.startswith('fixtures/'):
        path = 'fixtures/{}'.format(path)
    return json.load(open(join(ROOT_PATH, path)))


schema = yaml2json()
validator = Draft4Validator(schema)
