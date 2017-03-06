"""yanventory.yanventory."""
from .validator import YanventoryValidator


class Yanventory:
    """Yanventory."""

    def __init__(self, yml_source=None):
        """Yanventory."""
        if yml_source:
            self.load_structure(yml_source)
            self.populate()

    def load_structure(self, src):
        """Load structure from data source."""
        validator = YanventoryValidator(src)
        self._structure = validator.raw
        self._defaults = validator.defaults
        self._classes = validator.classes

    def populate(self):
        self.groups = dict()
        self.populate_nodes()
        self.populate_groups()
        self.populate_containers()

    def populate_containers(self):
        apply_nodes, apply_groups = self.parse_container_rules()
        self.populate_containers_nodes(apply_nodes)

    def populate_containers_nodes(self, rules):
        for container in rules:
            for obj in rules[container]:
                for node in rules[container][obj]:
                    properties = self._structure['containers'][container]['objects'][obj]['data']
                    for p in properties:
                        if p not in self.nodes[node]['data'].keys():
                            value = self._structure['containers'][container]['objects'][obj]['data'][p]
                            self.nodes[node]['data'][p] = value

    def parse_container_rules(self):
        src = self._structure['containers']
        for collection in src:
            mappings = src[collection]['config']['mapping']
            # map_rules = []
            apply_hosts = dict()
            for mapping in mappings:
                # m = dict()
                if mapping.get('node_name'):
                    if mapping['node_name'].get('split'):
                        for node in self.nodes:
                            index = mapping['node_name']['split']['index']
                            rule = mapping['node_name']['split']['rule']
                            for obj in src[collection]['objects']:
                                if obj == node.split(rule)[index]:
                                    if collection not in apply_hosts.keys():
                                        apply_hosts[collection] = dict()
                                    if obj not in apply_hosts[collection].keys():
                                        apply_hosts[collection][obj] = []
                                    apply_hosts[collection][obj].append(node)

        return apply_hosts, None

    def populate_groups(self):
        src = self._structure['groups']
        for collection in src:
            for group in src[collection]['objects']:
                if group not in self.groups.keys():
                    self.add_group(group)
                self.groups[group]['nodes'] += src[collection]['objects'][group]['data'].get('nodes', [])
                data = src[collection]['objects'][group]['data']
                properties = list(data.keys())
                all_parents = []
                for p in properties:
                    if p in self._classes['nodes']:
                        data.pop('nodes', None)
                    elif p in self._classes['parents']:
                        parents = data[p]
                        data.pop('parents', None)
                        if not isinstance(parents, list):
                            parents = [parents]
                        all_parents += parents

                for parent in all_parents:
                    self.add_child_to_group(group, parent)

                self.groups[group]['data'] = data
                self.groups[group]['parents'] = all_parents

    def populate_nodes(self):
        src = self._structure['nodes']
        nodes = {}
        for collection in src:
            for node in src[collection]['objects']:
                groups = []
                if node not in nodes.keys():
                    nodes[node] = dict()
                    nodes[node]['data'] = src[collection]['objects'][node]['data']
                properties = list(nodes[node]['data'].keys())
                for p in properties:
                    if p in self._classes['groups']:
                        groups = nodes[node]['data'][p]
                        if not isinstance(groups, list):
                            groups = [groups]
                        nodes[node]['data'].pop(p)
                nodes[node]['groups'] = groups
                for group in groups:
                    self.add_node_to_group(node, group)
                defaults = self._defaults['properties']
                for p in defaults:
                    if p not in nodes[node]['data'].keys():
                        nodes[node]['data'][p] = self._defaults['properties'][p]
                groups = self._defaults['groups']
                for group in groups:
                    self.add_node_to_group(node, group)
                nodes[node]['groups'] += groups
        self.nodes = nodes

    def add_group(self, group):
        self.groups[group] = dict()
        self.groups[group]['nodes'] = list()
        self.groups[group]['children'] = list()
        self.groups[group]['parents'] = list()
        self.groups[group]['data'] = dict()

    def add_node_to_group(self, node, group):
        if group not in self.groups.keys():
            self.add_group(group)
        self.groups[group]['nodes'].append(node)

    def add_child_to_group(self, child, group):
        if group not in self.groups.keys():
            self.add_group(group)
        self.groups[group]['children'].append(child)

    def ansible_inventory(self):
        inv = dict()
        inv['all'] = dict()
        inv['all']['hosts'] = self.nodes.keys()
        inv['_meta'] = dict()
        inv['_meta']['hostvars'] = dict()
        for host in self.nodes:
            inv['_meta']['hostvars'][host] = self.nodes[host]['data']
        for group in self.groups:
            inv[group] = {}
            inv[group]['hosts'] = self.groups[group]['nodes']
            inv[group]['children'] = self.groups[group]['children']
            inv[group]['vars'] = self.groups[group]['data']
        return inv
