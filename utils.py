# -*- coding: utf-8 -*-
import os
from sys import exit

import yaml

DEFAULT_CONFIG = 'config.yaml'

CZ_MONTHS = {
    'března': 3,
    'dubna': 4,
    'května': 5,
    'června': 6,
}


def readable(file_name):
    if os.path.isfile(file_name) and os.access(file_name, os.R_OK):
        return
    print(file_name, ' is not readable or does not exist!')
    exit()


def load_settings(config_file):
    if not config_file:
        config_file = DEFAULT_CONFIG
    readable(config_file)
    with open(config_file, 'r') as config:
        settings = yaml.load(config)
        return settings
