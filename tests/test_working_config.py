"""test_working_config."""
from yanventory.yanventory import Yanventory


def test_it_just_works():
    """Basic test so see that a simple site is working."""
    y = Yanventory()
    y.load_structure('examples/basic/yanventory.yml')
    y.populate()
