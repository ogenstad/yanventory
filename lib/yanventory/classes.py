"""yanventory.classes."""

from ipaddress import IPv4Address
from ipaddress import IPv4Network
from six import string_types
from six import text_type


def is_valid_ipv4_address(address):
    """Return True if address is a valid ipv4 address, else False."""
    try:
        IPv4Address(text_type(address))
        return True
    except:
        return False


def is_valid_ipv4_addresses(addresses):
    """Return True if addresses contains a list of ipv4 addresses."""
    if not isinstance(addresses, list):
        addresses = [addresses]
    for address in addresses:
        if not is_valid_ipv4_address(address):
            return False
    return True


def is_valid_ipv4_net(network):
    """Return True if network is a valid IPv4 network."""
    net = network.get('net')
    mask = network.get('mask')
    # prefixlen = network.get('prefixlen')
    try:
        IPv4Network(text_type('{}/{}'.format(net, mask)))
        return True
    except:
        return False


def is_valid_string_or_list_of_strings(value):
    """Return true if valid_string_or_list_of_strings."""
    if isinstance(value, list):
        for entry in value:
            if not isinstance(entry, string_types):
                return False
        return True
    elif isinstance(value, string_types):
        return True
    return False


def is_valid_string(text):
    """Return True if text is a string."""
    if isinstance(text, string_types):
        return True
    else:
        return False


CLASS_FUNCTIONS = {
    'ipv4_address': is_valid_ipv4_address,
    'ipv4_addresses': is_valid_ipv4_addresses,
    'ipv4_net': is_valid_ipv4_net,
    'string': is_valid_string,
    'nodes': is_valid_string_or_list_of_strings,
    'parents': is_valid_string_or_list_of_strings,
    'groups': is_valid_string_or_list_of_strings
}


def validate_class(class_type, data):
    """Return True if data is valid for class_type."""
    return CLASS_FUNCTIONS[class_type](data)
