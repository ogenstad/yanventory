"""yanventory.loader."""
import os
import yaml


def load_yaml(yml_file):
    """Return data from yaml file."""
    yml = {}
    yml['path'] = os.path.dirname(yml_file)
    yml['source'] = yml_file
    with open(yml_file, 'r') as fs:
        data = yaml.load(fs.read())
    if data:
        yml['data'] = data
    else:
        yml['data'] = {}
    return yml
