"""yanventory.validator."""
import os
from glob import glob
from .exceptions import YanventoryParsingError
from .loader import load_yaml
from .classes import validate_class


class YanventoryValidator:
    """Validate configuration."""

    def __init__(self, src):
        """Validate configuration."""
        self.classes = dict()
        self.config = load_yaml(src)
        self.raw = dict()
        self._load_configuration()
        self._validate_collections()

    def _load_configuration(self):
        self.raw['nodes'] = dict()
        self.raw['containers'] = dict()
        self.raw['groups'] = dict()
        self.raw['properties'] = dict()
        self.defaults = dict()
        self.defaults['properties'] = {}
        self.defaults['groups'] = []

        for entry in self.config['data']:
            if entry == 'nodes':
                for group in self.config['data']['nodes']:
                    self._load_collection('nodes', group)
            elif entry == 'containers':
                for group in self.config['data']['containers']:
                    self._load_collection('containers', group)
            elif entry == 'groups':
                for group in self.config['data']['groups']:
                    self._load_collection('groups', group)
            elif entry == 'properties':
                for properties in self.config['data']['properties']:
                    self._load_collection('properties', properties)

    def _load_collection(self, collection_type, collection):
        c = dict()
        c['config'] = self.config['data'][collection_type][collection]
        c['objects'] = dict()
        collection_path = self.config['path'] + os.sep + collection_type + os.sep + collection
        collection_files = glob('{}/*.yml'.format(collection_path))
        for c_file in collection_files:
            c_name = c_file.split(os.sep)[-1][:-4]
            c['objects'][c_name] = load_yaml(c_file)
        self.raw[collection_type][collection] = c

    def _validate_collections(self):
        self._define_properties()
        self._validate_defaults()
        self._validate_collection_required_properties()
        self._validate_collection_valid_properties()

    def _validate_defaults(self):

        if self.config['data'].get('defaults'):
            # ########################################
            #  Raise error if defaults is not a dictionary
            # ########################################
            if self.config['data']['defaults'].get('groups'):
                # ########################################
                # ###Raise error if groups isn't string or list!
                # ########################################
                self.defaults['groups'] = self.config['data']['defaults']['groups']

            if self.config['data']['defaults'].get('properties'):
                for p in list(self.config['data']['defaults']['properties'].keys()):

                    if p in self.properties:
                        if not validate_class(
                            self.properties[p]['class'],
                            p
                        ):
                            raise YanventoryParsingError(
                                'Invalid value for property {} for defaults in {} expected {}'.format(p,
                                    self.config['source'],
                                    self.properties[p]['class'])
                            )
                    else:
                        error = '{} is not a valid property for defaults in : {}'.format(
                            p,
                            self.config['source'])
                        raise YanventoryParsingError(error)

                    if p in self.classes['groups']:
                        groups = self.config['data']['defaults']['properties'].pop(p)
                        if not isinstance(groups, list):
                            groups = [groups]
                        self.defaults['groups'] += groups
                self.defaults['properties'] = self.config['data']['defaults']['properties']
        else:
            self.config['data']['defaults'] = dict()
            self.config['data']['defaults']['properties'] = dict()
            self.config['data']['defaults']['groups'] = []

    def _define_properties(self):
        collections = self.raw['properties']
        properties = dict()
        for collection in collections:
            for obj in collections[collection]['objects']:
                for p in collections[collection]['objects'][obj]['data']:
                    if p in properties.keys():
                        error = 'Property {} defined twice (in {} and {})'.format(p,
                            collections[collection]['objects'][obj]['source'],
                            properties[p]['source']
                        )
                        raise YanventoryParsingError(error)
                    else:
                        properties[p] = dict()
                        p_class = collections[collection]['objects'][obj]['data'][p]['class']
                        properties[p]['source'] = collections[collection]['objects'][obj]['source']
                        properties[p]['class'] = p_class
                        if p_class not in self.classes:
                            self.classes[p_class] = list()
                        self.classes[p_class].append(p)
        self.properties = properties

    def _validate_collection_required_properties(self):
        collections = self.raw
        config = self.config
        for collection in ['nodes', 'groups', 'containers']:
            for c in collections[collection]:
                required = config['data'][collection][c].get('required_properties', [])
                if not isinstance(required, list):
                    raise YanventoryParsingError(
                        'required_properties in {}/{} has to be a list'.format(collection, c)
                    )

                required_exceptions = []
                for obj in collections[collection][c]['objects']:
                    for r in required:
                        if r not in collections[collection][c]['objects'][obj]['data'].keys():
                            required_exceptions.append("Required property {} not found in {}".format(
                                    r,
                                    collections[collection][c]['objects'][obj]['source']))

                if len(required_exceptions) > 0:
                    raise YanventoryParsingError(required_exceptions)

    def _validate_collection_valid_properties(self):
        collections = self.raw
        # config = self.config
        for collection in ['nodes', 'groups', 'containers']:
            for c in collections[collection]:

                for obj in collections[collection][c]['objects']:
                    for p in collections[collection][c]['objects'][obj]['data']:
                        if p in self.properties:
                            if not validate_class(
                                self.properties[p]['class'],
                                collections[collection][c]['objects'][obj]['data'][p]
                            ):
                                raise YanventoryParsingError(
                                    'Invalid value for property {} in {} expected {}'.format(p,
                                        collections[collection][c]['objects'][obj]['source'],
                                        self.properties[p]['class'])
                                )
                        else:
                            error = '{} is not a valid property in: {}'.format(
                                p,
                                collections[collection][c]['objects'][obj]['source'])
                            raise YanventoryParsingError(error)
