[![Build Status](https://travis-ci.org/ogenstad/yanventory.svg?branch=develop)](https://travis-ci.org/ogenstad/yanventory)
[![Build status](https://ci.appveyor.com/api/projects/status/onkpc3a0gxh09ftr/branch/develop?svg=true)](https://ci.appveyor.com/project/ogenstad/yanventory)
[![Coverage Status](https://coveralls.io/repos/ogenstad/yanventory/badge.svg?branch=develop&service=github)](https://coveralls.io/github/ogenstad/yanventory?branch=develop)
[![Saythanks](https://img.shields.io/badge/Say%20Thanks!-%F0%9F%A6%89-1EAEDB.svg)](https://saythanks.io/to/ogenstad)


Yanventory
==========

[Yanventory (YAML Inventory)](https://networklore.com/yanventory/) is a data source tool which lets you define an inventory along with configuration data using YAML files. These YAML files will be read by Yanventory which will be able to output all the data in a format which tools such as Ansible understands.

Warning
=======

Yanventory is in pre-release mode and there's a big chance that the structure of the project as well as the structure of the source Yaml files will change. Feedback is more than welcome!

The vision
==========

The goal of this is that Yanventory is a building block of that which will create the inventory. Once the structure is more set I will write a frontend in Flask which exposes the inventory through a rest-api.

When working with Yanventory I see a workflow which will look something like this.

1) The Yanventory Yaml files exists in a central Git repo

This could be in an instance of GitHub, GitLab, Bitbucket etc.

2) A user sends in a pull request / merge request to the repo

3) A CI pipeline is triggered and validates the Yaml configuration files according to the defined rules

4) Along with the built in validations you have scripts which perform your own business logic before the pull request is considered valid

5) The pull / merge request is accepted

6) The CI pipeline is triggered once again, when completed it notifies the Yanventory flask frontend which pulls the updated repo.

7) Yanventory assembles the inventory and saves down the end result in json format to enable the ability to quickly load the inventory.

7) You use Ansible and have an inventory script which polls the Flask app with the git branch as an argument, letting you run against different branches.

Yanventory will be able to support other automation frameworks like Salt. Ansible is the one I know best though so it's easiest for me to test with.

A simpler way
=============

If the above steps looks too complicated, don't worry. It will be possible to run Yanventory without involving Git or any rest-api, the above is just what I want to be able to do.

The structure of Yanventory
===========================

There's an example of the structure in the examples/basic folder. I will write more about how it works.

An example: Running Yanventory from Python
==========================================

```python
import json
from yanventory.yanventory import Yanventory
y = Yanventory(yml_source='examples/basic/yanventory.yml')
inv = y.ansible_inventory()
print(json.dumps(inv, indent=4, sort_keys=True))

{
    "_meta": {
        "hostvars": {
            "lon-sw-01": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "latitude": "51.507189",
                "longitude": "-0.135012",
                "operating_system": "ios",
                "site_id": "1260",
                "snmp_contact": "NOC",
                "vendor": "cisco"
            },
            "lon-sw-02": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "latitude": "51.507189",
                "longitude": "-0.135012",
                "operating_system": "ios",
                "site_id": "1260",
                "snmp_contact": "NOC",
                "vendor": "cisco"
            },
            "lon-sw-03": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "latitude": "51.507189",
                "longitude": "-0.135012",
                "operating_system": "ios",
                "site_id": "1260",
                "snmp_contact": "NOC",
                "vendor": "cisco"
            },
            "srv-file-1": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "ipv4": "10.10.30.158",
                "operating_system": "windows",
                "snmp_contact": "NOC"
            },
            "srv-web-1": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "ipv4": "10.10.30.16",
                "operating_system": "windows",
                "snmp_contact": "NOC"
            },
            "sth-sw-01": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "latitude": "59.331482",
                "longitude": "18.071491",
                "operating_system": "ios",
                "site_id": "1452",
                "snmp_contact": "NOC",
                "vendor": "cisco"
            },
            "sth-sw-02": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "production",
                "latitude": "59.331482",
                "longitude": "18.071491",
                "operating_system": "ios",
                "site_id": "1452",
                "snmp_contact": "NOC",
                "vendor": "cisco"
            },
            "tsrv-file-1": {
                "ansible_python_interpreter": "/usr/bin/env python",
                "env": "testing",
                "ipv4": "10.10.30.152",
                "operating_system": "windows",
                "snmp_contact": "NOC"
            }
        }
    },
    "access_switches": {
        "children": [
            "sth_sw"
        ],
        "hosts": [],
        "vars": {
            "type": "network"
        }
    },
    "all": {
        "hosts": [
            "tsrv-file-1",
            "sth-sw-01",
            "srv-web-1",
            "srv-file-1",
            "lon-sw-02",
            "lon-sw-03",
            "lon-sw-01",
            "sth-sw-02"
        ]
    },
    "all_the_things": {
        "children": [],
        "hosts": [
            "sth-sw-02",
            "sth-sw-01",
            "lon-sw-02",
            "lon-sw-03",
            "lon-sw-01",
            "srv-web-1",
            "srv-file-1",
            "tsrv-file-1"
        ],
        "vars": {}
    },
    "everything": {
        "children": [],
        "hosts": [
            "sth-sw-02",
            "sth-sw-01",
            "lon-sw-02",
            "lon-sw-03",
            "lon-sw-01",
            "srv-web-1",
            "srv-file-1",
            "tsrv-file-1"
        ],
        "vars": {}
    },
    "lon_sw": {
        "children": [],
        "hosts": [],
        "vars": {
            "location": "london"
        }
    },
    "network_devices": {
        "children": [
            "access_switches"
        ],
        "hosts": [],
        "vars": {}
    },
    "servers": {
        "children": [],
        "hosts": [
            "srv-file-1",
            "tsrv-file-1"
        ],
        "vars": {}
    },
    "sth_sw": {
        "children": [],
        "hosts": [
            "sth-sw-01",
            "sth-sw-02"
        ],
        "vars": {
            "location": "stockholm"
        }
    }
}

```
