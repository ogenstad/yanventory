"""setup.py file."""
import uuid

from setuptools import setup, find_packages
from pip.req import parse_requirements

requirements_data = parse_requirements('requirements.txt', session=uuid.uuid1())
requirements = [str(package.req) for package in requirements_data]

version = '0.0.1alpha1'
long_description = "Yaml Inventory"

config = {
    'name': 'yanventory',
    'package_dir': {'': 'lib'},
    'packages': find_packages('lib'),
    'version': version,
    'description': 'Yanventory',
    'long_description': long_description,
    'author': 'Patrick Ogenstad',
    'author_email': 'patrick@ogenstad.com',
    'license': 'Apache',
    'url': 'https://networklore.com/yanventory/',
    'install_requires': requirements,
    'classifiers': ['Development Status :: 2 - Pre-Alpha',
                    'Intended Audience :: Developers',
                    'Intended Audience :: System Administrators',
                    'License :: OSI Approved :: Apache Software License',
                    'Operating System :: MacOS',
                    'Operating System :: POSIX',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6',
                    ]
}

setup(**config)
