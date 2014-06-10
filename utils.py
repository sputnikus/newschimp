# -*- coding: utf-8 -*-
import os
import sys

import click
import yaml

# TODO: Logging

# TODO: The fuck
CZ_MONTHS = {
    'března': 3,
    'dubna': 4,
    'května': 5,
    'června': 6,
}

UTIL_FILES = ('__init__.py', 'utils.py', 'cli.py', 'newschimp.py')


def readable(file_name):
    if os.path.isfile(file_name) and os.access(file_name, os.R_OK):
        return True
    print(file_name, ' is not readable or does not exist!')
    return False


def load_settings(config_file):
    if not readable(config_file):
        exit()
    with open(config_file, 'r') as config:
        settings = yaml.load(config)
        return settings

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          'social'))
root_folder = os.path.abspath(os.path.dirname(__file__))

class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename not in UTIL_FILES:
                rv.append(filename[:-3])
        for filename in os.listdir(root_folder):
            if filename.endswith('.py') and filename not in UTIL_FILES:
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__('social.' + name, None, None, ['cli'])
            return mod.cli
        except ImportError:
            pass
        try:
            mod = __import__(name, None, None, ['cli'])
        except ImportError:
            return
        return mod.cli
